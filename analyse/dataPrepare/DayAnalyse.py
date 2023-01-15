__author__ = 'fastwave'
# @Time : 2023/1/15 20:08
# @Author : fastwave 363642626@qq.com



# python 有哪些金融相关的库.
# https://blog.csdn.net/u011960727/article/details/128881331

# TA-lib 指标详解与实践
# https://zhuanlan.zhihu.com/p/447716939

# pyalgotrade量化回测框架简单试用
# https://zhuanlan.zhihu.com/p/562830162


# 几款回测工具对比
# https://zhuanlan.zhihu.com/p/151897607


import pandas as pd
from sqlalchemy import false
from sqlalchemy.orm import sessionmaker

from analyse.dao.stock_basic_status_dao import stock_basic_status_dao
from analyse.dao.stock_ext_status_dao import stock_ext_status_dao
from analyse.dataPrepare.DayDownUp import down_up_total
from analyse.dataPrepare.DayMa import ma_total, up_total
from analyse.entity.stock_ext_status import stock_ext_status
from common.BaseService import BaseService
from common.CommonUtil import get_stock_cond, get_my_follow_sql, get_default_end_date, get_my_all_sql
from common.constant_common import DEFAULT_START_DATE
from datetime import datetime

import talib as ta

from common.dao_base_service import dao_base_service


# 按天统计各类指标
class DayAnalyse(dao_base_service):
    def total_single(self, code_or_name, start_date, end_date, table_name, method_name, method_params):
        # 获取状态信息
        ext_status_cond = stock_ext_status(ts_code=code_or_name, total_type=method_name.__name__)
        ext_status = stock_ext_status_dao().get(ext_status_cond)
        is_delete = False
        if ext_status and ext_status.last_value >= end_date:
            return
        elif ext_status:
            start_date = ext_status.last_value
            is_delete = ext_status.sync_status != 2

        where_cond = get_stock_cond(self, code_or_name, start_date, end_date, "")
        sql = "select * from stock_line_day_view where 1=1 {} order by trade_date asc;"
        sql = sql.format(where_cond)
        stock_day_list = pd.read_sql(sql, self.engine)
        if len(stock_day_list) == 0:
            return

        # ii = len(stock_day_list)
        # print(ii)
        #
        # stock_day_list.index = pd.to_datetime(stock_day_list['trade_date'])
        # stock_list = stock_day_list.sort_index()
        #
        # types = ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 'MAMA', 'T3']
        # df_ma = pd.DataFrame(stock_list.close)
        # for i in range(len(types)):
        #     df_ma[types[i]] = ta.MA(stock_day_list.close, timeperiod=5, matype=i)
        #
        # df_ma.to_sql('test1', self.engine, index=false, if_exists='append')
        #
        # print(df_ma)
        # exit()

        db_session = sessionmaker(self.engine)
        session = db_session()

        # 删除已分析的结果
        if is_delete:
            del_sql = "delete from {} where 1=1 {};"
            del_sql = del_sql.format(table_name, where_cond)
            session.execute(del_sql)
            session.commit()

        # 执行统计
        analyse_list = method_name(stock_day_list, method_params)

        # 保存统计结果
        # session.bulk_save_objects(analyse_list)
        # session.commit()
        analyse_list.to_sql(table_name, self.engine, index=false, if_exists='append')

        # 更新状态
        ext_status_cond.sync_status = 2
        ext_status_cond.last_success_date = datetime.now()
        ext_status_cond.last_value = end_date
        stock_ext_status_dao().save(ext_status_cond)

    def total_batch(self, degree):

        stock_list = stock_basic_status_dao().get(degree)

        start_date = DEFAULT_START_DATE
        end_date = get_default_end_date()

        for item in stock_list:
            # MA
            # print("统计股票{}，类型{} ，时间范围：{}-{}".format(item.ts_code, "MA", start_date, end_date))
            # self.total_single(item.ts_code, start_date, end_date, "stock_line_day_point_ma", ma_total, (15, 2.0))

            # UP
            print("统计股票{}，类型{} ，时间范围：{}-{}".format(item.ts_code, "UP", start_date, end_date))
            self.total_single(item.ts_code, start_date, end_date, "stock_line_day_point_up360", up_total, (15, 2.0))


            # 涨跌
            # self.total_single(item.ts_code, start_date, end_date, "stock_line_day_up_down", down_up_total, (15, 2.0))


def main():
    DayAnalyse().total_batch(-1)

    # 涨跌幅度统计
    # DayAnalyse().day_total("600036.SH", "20200601", "20221230", "stock_line_day_up_down", down_up_total, (15, 2.0))

    # 统计所有关注
    # DayAnalyse().my_follow(10)

    # 均线（ma）统计
    # DayAnalyse().day_total("600036.SH", "19000101", "20221230", "stock_line_day_ma",  ma_total, (15, 2.0))

    # 把各种图形的定义，也按天进行统计，也作为一个指标项
    # 各项指标定义


if __name__ == '__main__':
    main()

