__author__ = 'fastwave'

from datetime import datetime

from analyse.entity.stock_strategy_detial import stock_strategy_detail
from common.BaseService import BaseService
from common.constant_common import COND_FIELD_NAME,  OPTION_TYPE_BUY, OPTION_TYPE_SELL


# @Time : 2023/1/15 20:08
# @Author : fastwave 363642626@qq.com

# 策略验证
def run_strategy(stock_list, buy_cond, sell_cond, params):

    # 获取设置的参数
    ts_code = params[0]
    # date = params[1]

    # stock_strategy_detail 全部集合
    strategy_list_all = []
    strategy_list_temp = []

    # 读取buy_cond
    buy_strategy_name = buy_cond.strategy_name
    buy_compare_type = buy_cond.compare_type
    buy_start_value = buy_cond.start_value
    buy_end_value = buy_cond.end_value
    # buy_step_value = buy_cond.step_value

    buy_start_value_list = []
    buy_end_value_list = []
    # buy_step_value_list = []

    if buy_compare_type == "5":
        buy_start_value_list = buy_start_value.split(',')
        buy_end_value_list = buy_end_value.split(',')
        # buy_step_value_list = buy_step_value.split(',')

    # 读取sell_cond
    sell_strategy_name = sell_cond.strategy_name
    sell_compare_type = sell_cond.compare_type
    sell_start_value = sell_cond.start_value
    sell_end_value = sell_cond.end_value
    sell_step_value = sell_cond.step_value

    sell_start_value_list = []
    sell_end_value_list = []
    # sell_step_value_list = []

    detail_buy = stock_strategy_detail(ts_code=ts_code, strategy_name=buy_strategy_name,
                                       option_type=OPTION_TYPE_BUY)
    detail_sell = stock_strategy_detail(ts_code=ts_code, option_type=OPTION_TYPE_SELL,
                                        strategy_name=sell_strategy_name)

    if sell_compare_type == "5":
        sell_start_value_list = sell_start_value.split(',')
        sell_end_value_list = sell_end_value.split(',')
        # sell_step_value_list = sell_step_value.split(',')

    for row_index, row in stock_list.iterrows():
        # 该值是select cond_expression 语句列的值，可以是单个，也可以是多个值用逗号隔开
        cond_result = row[COND_FIELD_NAME]

        # ############################ 买入 ###################################################
        buy_flag = False

        # 1 真假比较，2固定值比较
        if (buy_compare_type == "1" or buy_compare_type == "2") and cond_result == buy_start_value:
            buy_flag = True

        # 3 范围比较，起始值和终目值做比较， 起始和终止为1~10，则结果值在1~10时被认为策略可以执行
        elif buy_compare_type == "3" and buy_start_value <= cond_result < buy_end_value:
            buy_flag = True

        # 5 一组范围值比较， 有结果值，每个结果值都会有一个相同下标对应的起始值
        elif buy_compare_type == "5":
            cond_result_array = cond_result.split(",")
            result_len = len(cond_result_array)
            buy_flag = True
            for i in range(result_len):
                cur_result_value = cond_result_array[i]
                # 所有条件是与的关系，如果有一个不成立，则直接返回False
                if not buy_start_value_list[i] <= cur_result_value < buy_end_value_list[i]:
                    buy_flag = False
                    break

        # 判断是否买入
        if buy_flag:
            detail_buy.option_price = row["close"]
            detail_buy.option_date = row["trade_date"]
            detail_buy.option_type = "buy"
            detail_buy.option_flag = buy_compare_type
            strategy_list_all.append(detail_buy)
            strategy_list_temp.append(detail_buy)

        # ############################ 卖出 ###################################################
        sell_flag = False

        # 1 真假比较，2固定值比较
        if (sell_compare_type == "1" or sell_compare_type == "2") and cond_result == sell_start_value:
            sell_flag = True

        # 3 范围比较，起始值和终目值做比较， 起始和终止为1~10，则结果值在1~10时被认为策略可以执行
        elif sell_compare_type == "3" and sell_start_value <= cond_result < sell_end_value:
            sell_flag = True

        # 5 一组范围值比较， 有结果值，每个结果值都会有一个相同下标对应的起始值
        elif sell_compare_type == "5":
            cond_result_array = cond_result.split(",")
            result_len = len(cond_result_array)
            sell_flag = True
            for i in range(result_len):
                cur_result_value = cond_result_array[i]
                # 所有条件是与的关系，如果有一个不成立，则直接返回False
                if not sell_start_value_list[i] <= cur_result_value < sell_end_value_list[i]:
                    sell_flag = False
                    break

        # 判断是否卖出
        if sell_flag:
            option_price = row["close"]
            detail_sell.option_price = option_price
            detail_sell.option_date = row["trade_date"]
            detail_sell.option_type = "sell"
            detail_sell.option_flag = sell_compare_type
            detail_sell.sell_order_cnt = 0
            detail_sell.sell_profit_percent = 0

            if strategy_list_temp.__sizeof__() > 0:
                # 卖出的笔数
                detail_sell.sell_order_cnt = strategy_list_temp.__sizeof__()

                # 计算卖出的利润
                sum_percent = 0
                for buy_item in strategy_list_temp:
                    sum_percent = sum_percent + \
                                  (option_price - strategy_list_temp.option_price)/strategy_list_temp.option_price
                detail_sell.sell_profit_percent = sum_percent
                strategy_list_temp.clear()

            strategy_list_all.append(detail_sell)

        return strategy_list_all

# class StrategyCheck(BaseService):
#     pass
