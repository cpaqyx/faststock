__author__ = 'fastwave'
# @Time : 2022/12/10 20:08
# @Author : fastwave 363642626@qq.com

import datetime as dt
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from common.BaseService import BaseService
from datahub.entity.StockBasicStatus import StockBasicStatus

from concurrent.futures import ThreadPoolExecutor
import threading
import time

LINE_TYPE = 'day'


class StockSyncDayThread(BaseService):

    def async_stock_line_day(self):
        db_session = sessionmaker(self.engine)
        session = db_session()
        cur_date = datetime.now()

        # 周日、周一仍同步上一周的，把时间退回到前面的周六
        if cur_date.weekday().__eq__(6) or cur_date.hour < 18:
            cur_date = cur_date - dt.timedelta(days=1)
        elif cur_date.weekday().__eq__(0):
            cur_date = cur_date - dt.timedelta(days=2)

        # 本次要同步到的日期
        cur_date_str = datetime.strftime(cur_date, '%Y%m%d')
        # 下次开始同步的时间点
        next_date_str = datetime.strftime(cur_date + dt.timedelta(days=1), '%Y%m%d')

        # 查询出未同步到当天的股票基本信息，已同步的忽略
        sql = """
        select 
            I.* 
        from 
            stock_basic_info I left join stock_basic_status S on S.ts_code = I.ts_code 
        where 
            S.id is null or S.`last_value` < :last_value;
        """
        basic_list = session.execute(text(sql), {"last_value": cur_date_str}).fetchall()

        # 创建一个包含2条线程的线程池
        pool = ThreadPoolExecutor(max_workers=10)

        for item in basic_list:
            # 向线程池提交一个task
            pool.submit(sync_single_stock, self, item, cur_date_str, next_date_str)

def sync_single_stock(self, item, cur_date_str, next_date_str):
    DBSession = sessionmaker(self.engine)
    session = DBSession()

    # 查询该code的状态信息，如果不存在则添加到表中
    basic_status = session.query(StockBasicStatus).filter(StockBasicStatus.index == item.index
                                                          and StockBasicStatus.line_type == LINE_TYPE).first()
    if basic_status is None:
        basic_status_new = StockBasicStatus(index=item.index, ts_code=item.ts_code, sync_status=0, app_mode=1,
                                            last_success_date=datetime.strptime('1900-01-01', '%Y-%m-%d'),
                                            degree=10000, allow_delay_second=1440 * 60, record_status=1,
                                            created_on=datetime.now(), updated_on=datetime.now(),
                                            line_type=LINE_TYPE, last_value='19000101', order_index=10000,
                                            label='', remark='')
        session.add(basic_status_new)
        session.commit()
        basic_status = session.query(StockBasicStatus).filter(StockBasicStatus.index == item.index
                                                              and StockBasicStatus.line_type == LINE_TYPE
                                                              and StockBasicStatus.code == item.code).first()

    # 如果上次状态标记未成功更新为2，仍在进行中，则先删除上次未确认部分
    if basic_status.sync_status == 1:
        session.execute("delete from stock_line_day where ts_code='{}' and trade_date >= '{}'"
                        .format(item.ts_code, cur_date_str))
        session.commit()

    # 置为进行中
    basic_status.updated_on = datetime.now()
    basic_status.sync_status = 1
    session.commit()

    # 下载单个股票日线数据（会自动commit）
    df = self.pro.daily(ts_code=item.ts_code, start_date=basic_status.last_value, end_date=cur_date_str)
    # if_exists: 当数据库中已经存在数据表时对数据表的操作，有replace替换、append追加，fail则当表存在时提⽰
    df.to_sql('stock_line_day', self.engine, if_exists='append')

    # 置为完成状态
    basic_status.last_success_date = datetime.now()
    basic_status.updated_on = datetime.now()
    basic_status.sync_status = 2
    basic_status.last_value = next_date_str
    session.commit()

    self.logger.info("同步股票{}({})到最新日期{},线程名{}".format(item.name, item.ts_code, cur_date_str, threading.current_thread().name))
    session.close()


def main():
    StockSyncDayThread().async_stock_line_day()


if __name__ == '__main__':
    main()
