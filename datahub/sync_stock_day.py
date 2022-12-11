__author__ = 'fastwave'
# @Time : 2022/12/10 20:08
# @Author : fastwave 363642626@qq.com

import datetime as dt
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from common.BaseService import BaseService
from datahub.entity.StockBasicStatus import StockBasicStatus
LINE_TYPE = 'day'


class StockSyncDay(BaseService):

    def async_stock_line_day(self):
        DBSession = sessionmaker(self.engine)
        session = DBSession()
        curDate = datetime.now()

        # 周日、周一仍同步上一周的，把时间退回到前面的周六
        if curDate.weekday().__eq__(6):
            curDate = curDate - dt.timedelta(days=1)
        if curDate.weekday().__eq__(0):
            curDate = curDate - dt.timedelta(days=2)

        curDateStr = datetime.strftime(curDate, '%Y%m%d')

        # 查询出未同步到当天的股票基本信息，已同步的忽略
        sql = """
        select 
            I.* 
        from 
            stock_basic_info I left join stock_basic_status S on S.`index` = I.`index` 
        where 
            S.id is null or S.`last_value` < :last_value;
        """
        basicList = session.execute(text(sql), {"last_value": curDateStr}).fetchall()
        for item in basicList:
            # 查询该code的状态信息，如果不存在则添加到表中
            basicStatus = session.query(StockBasicStatus).filter(StockBasicStatus.index == item.index
                                                                 and StockBasicStatus.line_type == LINE_TYPE).first()
            if basicStatus is None:
                basicStatusNew = StockBasicStatus(index=item.index, code=item.code, sync_status=0, app_mode=1,
                                                  last_success_date=datetime.strptime('1900-01-01', '%Y-%m-%d'),
                                                  degree=10000, allow_delay_second=1440*60, record_status=1,
                                                  created_on=datetime.now(), updated_on=datetime.now(),
                                                  line_type=LINE_TYPE, last_value='19000101', order_index=10000,
                                                  label='', remark='')
                session.add(basicStatusNew)
                session.commit()
                basicStatus = session.query(StockBasicStatus).filter(StockBasicStatus.index == item.index
                                                                     and StockBasicStatus.line_type == LINE_TYPE
                                                                     and StockBasicStatus.code == item.code).first()

            # 如果上次状态标记未成功更新为2，仍在进行中，则先删除上次未确认部分
            if basicStatus.sync_status == 1:
                session.execute("delete from stock_line_day where ts_code='{}' and trade_date >= '{}'"
                                .format(item.ts_code, curDateStr))
                session.commit()

            # 置为进行中
            basicStatus.updated_on = datetime.now()
            basicStatus.sync_status = 1
            session.commit()

            # 下载单个股票日线数据（会自动commit）
            df = self.pro.daily(ts_code=item.ts_code, start_date=basicStatus.last_value, end_date=curDateStr)
            # if_exists: 当数据库中已经存在数据表时对数据表的操作，有replace替换、append追加，fail则当表存在时提⽰
            df.to_sql('stock_line_day', self.engine, if_exists='append')

            # 置为完成状态
            basicStatus.last_success_date = datetime.now()
            basicStatus.updated_on = datetime.now()
            basicStatus.sync_status = 2
            basicStatus.last_value = curDateStr
            session.commit()

            self.logger.info("同步股票{}({})到最新日期{}".format(item.name, item.ts_code, curDateStr))

        session.close()


def main():
    StockSyncDay().async_stock_line_day()


if __name__ == '__main__':
    main()
