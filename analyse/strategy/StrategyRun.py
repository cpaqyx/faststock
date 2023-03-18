__author__ = 'fastwave'

from sqlalchemy.orm import sessionmaker

from analyse.dao.stock_basic_status_dao import stock_basic_status_dao
from analyse.dao.stock_line_day_dao import stock_line_day_dao
from analyse.dao.stock_strategy_cond_dao import stock_strategy_cond_dao
from analyse.strategy.StrategyCheck import run_strategy
from common.BaseService import BaseService
from common.CommonUtil import get_default_end_date
from common.constant_common import BUY_TIP, SELL_TIP, \
    DEFAULT_START_DATE


# @Time : 2023/1/15 20:08
# @Author : fastwave 363642626@qq.com

# 策略验证
class StrategyRun(BaseService):

    def run_batch(self, degree, params):
        # 分析的股票列表
        stock_list = stock_basic_status_dao().get(degree)

        # 买策略列表
        buy_list = stock_strategy_cond_dao().get_list(BUY_TIP)

        # 卖策略
        sell_list = stock_strategy_cond_dao().get_list(SELL_TIP)

        start_date = DEFAULT_START_DATE
        end_date = get_default_end_date()

        # 遍历所有股票，用所有买卖策略模拟
        for item in stock_list:
            # 获取到股票日数据、相关指标数据
            day_list = stock_line_day_dao().get_stock_line_day(item.ts_code, start_date, end_date)

            # 所有买策略
            for buy_cond in buy_list:
                for sell_cond in sell_list:
                    result = run_strategy(day_list, buy_cond, sell_cond, params)
                    result.to_sql("stock_strategy_detail", self.engine, index=False, if_exists='append')


def main():
    StrategyRun().run_batch(-1, (1, 2))


if __name__ == '__main__':
    main()


