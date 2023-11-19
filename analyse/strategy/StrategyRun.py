__author__ = 'FL'

from sqlalchemy.orm import sessionmaker

from dao.stock_basic_status_dao import stock_basic_status_dao
from dao.stock_line_day_dao import stock_line_day_dao
from dao.stock_strategy_cond_dao import stock_strategy_cond_dao
from analyse.strategy.ConfigCheck import run_strategy
from analyse.strategy.ShapeCheckV4 import run_shape_v4
from analyse.strategy.ShapeCheckV5 import run_shape_v5
from common.base_service import BaseService
from common.common_util import get_default_end_date
from common.constant_common import BUY_TIP, SELL_TIP, DEFAULT_START_DATE


# @Time : 2023/1/15 20:08
# @Author : FL 363642626@qq.com

# 策略验证
class StrategyRun(BaseService):

    def run_batch(self, degree, params):
        # 分析的股票列表
        stock_list = stock_basic_status_dao().get(degree)

        start_date = DEFAULT_START_DATE
        end_date = get_default_end_date()

        db_session = sessionmaker(self.engine)
        session = db_session()

        # 运行模式，
        run_type = params["run_type"]
        if run_type == "shape" or run_type == "all":
            # big_continue_percent: 多天连续累计跌幅超过多少时也可作为大涨或大跌
            # big_percent: 某一天涨跌幅度超过多少时也可作为大涨或大跌
            # is_continue_ignore: 计算连续涨跌时，是否忽略小涨跌
            # max_down_percent_not_buy: 在统计的天数内跌幅超过多少时，不考虑买入
            # down_total_days: 向前统计的天数
            # max_up_percent_sell: 如果统计天数内，涨幅超过50%则卖出
            # max_up_days:  涨幅统计天数
            shape_params = {"ts_code": "", "min_up_percent": 0.5, "ignore_percent": 1.0, "big_percent": 1.5,
                            "big_continue_percent": 2.0, "is_continue_ignore": True, "max_down_percent_not_buy": 30,
                            "down_total_days": 50, "max_up_days": 30, "max_up_percent_sell": 50, "option_flag_suffix": "p_50_d_30"}
            # 遍历所有股票，用所有买卖策略模
            for item in stock_list:
                # 获取到股票日数据、相关指标数据
                day_list = stock_line_day_dao().get_stock_line_day(item.ts_code, start_date, end_date)

                # 所形状策略
                shape_params["ts_code"] = item.ts_code
                # analyse_list_v1 = run_shape_v1(day_list, shape_params)
                # session.bulk_save_objects(analyse_list_v1)
                # analyse_list_v2 = run_shape_v2(day_list, shape_params)
                # session.bulk_save_objects(analyse_list_v2)

                # analyse_list_v3 = run_shape_v3(day_list, shape_params)
                # session.bulk_save_objects(analyse_list_v3)

                # 独立V4测试
                for max_up_days in (10, 15, 20, 30, 40, 50, 60):
                    for max_up_percent_sell in (30, 40, 50, 80):
                        shape_params = {"ts_code": "", "min_up_percent": 0.5, "ignore_percent": 1.0, "big_percent": 1.5,
                                        "big_continue_percent": 2.0, "is_continue_ignore": True, "max_down_percent_not_buy": 30,
                                        "down_total_days": 50, "max_up_days": max_up_days, "max_up_percent_sell": max_up_percent_sell,
                                        "option_flag_suffix": "_p_{}_d_{}".format(max_up_percent_sell, max_up_days)}
                        analyse_list_v4 = run_shape_v4(day_list, shape_params)
                        session.bulk_save_objects(analyse_list_v4)
                analyse_list_v5 = run_shape_v5(day_list, shape_params)
                # session.bulk_save_objects(analyse_list_v5)

                # analyse_list_v6 = run_shape_v6(day_list, shape_params)
                # session.bulk_save_objects(analyse_list_v6)

                session.commit()
                self.logger.info("shape类型V3~V5方法分析股票{}到最新日期{}".format(item.ts_code, end_date))

        if run_type == "config" or run_type == "all":
            # 买策略列表
            buy_list = stock_strategy_cond_dao().get_list(BUY_TIP)

            # 卖策略
            sell_list = stock_strategy_cond_dao().get_list(SELL_TIP)

            # 遍历所有股票，用所有买卖策略模拟
            for item in stock_list:
                # 获取到股票日数据、相关指标数据
                day_list = stock_line_day_dao().get_stock_line_day(item.ts_code, start_date, end_date)

                # 所有买策略
                for buy_cond in buy_list:
                    for sell_cond in sell_list:
                        result = run_strategy(day_list, buy_cond, sell_cond, params)
                        # session.bulk_save_objects(analyse_list)
                        # result.to_sql("stock_strategy_detail", self.engine, index=False, if_exists='append')

def main():
    # 运行模式：shape|config|all
    # StrategyRun().run_batch(10, {"run_type": "shape"})
    StrategyRun().run_batch(-1, {"run_type": "shape"})


if __name__ == '__main__':
    main()


