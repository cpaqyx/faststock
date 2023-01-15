__author__ = 'fastwave'
# @Time : 2023/1/15 22:45
# @Author : fastwave 363642626@qq.com

# from sqlalchemy import null
from analyse.entity.StockLineDayMa import StockLineDayMa
import talib as ta
import pandas as pd


def up_total(stock_day_list, method_params):

    stock_day_list.index = pd.to_datetime(stock_day_list['trade_date'])
    stock_list = stock_day_list.sort_index()
    df_ma = pd.DataFrame(stock_list.ts_code)
    df_ma["trade_date"] = stock_list.trade_date
    df_ma["close"] = stock_list.close
    # , stock_list.trade_date, stock_list.close
    for i in range(1, 361):
        if i <= 30 or i % 10 == 0:
            col = "up" + str(i)
            # 当天的价格与前i天的对比，计算出相对前i天的涨跌幅度
            df_ma[col] = (stock_day_list.close/stock_day_list.close.shift(i) - 1) * 100

    return df_ma


def ma_total(stock_day_list, method_params):

    stock_day_list.index = pd.to_datetime(stock_day_list['trade_date'])
    stock_list = stock_day_list.sort_index()
    df_ma = pd.DataFrame(stock_list.ts_code)
    df_ma["trade_date"] = stock_list.trade_date
    df_ma["close"] = stock_list.close
    # , stock_list.trade_date, stock_list.close
    for i in range(2, 361):
        if i <= 30 or i % 10 == 0:
            col = "ma" + str(i)
            df_ma[col] = ta.MA(stock_day_list.close, timeperiod=i, matype=0)

    return df_ma


# 统计指定天数ma
def ma_calc(row_index, stock_day_list, ma_days):
    ma_days_index = ma_days - 1
    if row_index < ma_days_index:
        return 0

    # 前N-1天和当天
    pre_list = stock_day_list[(row_index - ma_days_index): row_index + 1]
    sum_price = 0.0
    for pre_index, pre_row in pre_list.iterrows():
        sum_price = sum_price + pre_row["close"]

    if sum_price > 0:
        return sum_price/ma_days

    return 0


# 统计所有Ma
def ma_total_my_code(stock_day_list, method_params):
    analyse_list = []
    for row_index, row in stock_day_list.iterrows():
        analyse = StockLineDayMa(ts_code=row["ts_code"], trade_date=row["trade_date"], close=row["close"])
        analyse.ma2 = ma_calc(row_index, stock_day_list, 2)
        analyse.ma3 = ma_calc(row_index, stock_day_list, 3)
        analyse.ma4 = ma_calc(row_index, stock_day_list, 4)
        analyse.ma5 = ma_calc(row_index, stock_day_list, 5)
        analyse.ma6 = ma_calc(row_index, stock_day_list, 6)
        analyse.ma7 = ma_calc(row_index, stock_day_list, 7)
        analyse.ma8 = ma_calc(row_index, stock_day_list, 8)
        analyse.ma10 = ma_calc(row_index, stock_day_list, 10)
        analyse.ma11 = ma_calc(row_index, stock_day_list, 11)
        analyse.ma12 = ma_calc(row_index, stock_day_list, 12)
        analyse.ma13 = ma_calc(row_index, stock_day_list, 13)
        analyse.ma14 = ma_calc(row_index, stock_day_list, 14)
        analyse.ma15 = ma_calc(row_index, stock_day_list, 15)
        analyse.ma16 = ma_calc(row_index, stock_day_list, 16)
        analyse.ma17 = ma_calc(row_index, stock_day_list, 17)
        analyse.ma18 = ma_calc(row_index, stock_day_list, 18)
        analyse.ma19 = ma_calc(row_index, stock_day_list, 19)
        analyse.ma20 = ma_calc(row_index, stock_day_list, 20)
        analyse.ma24 = ma_calc(row_index, stock_day_list, 24)
        analyse.ma25 = ma_calc(row_index, stock_day_list, 25)
        analyse.ma26 = ma_calc(row_index, stock_day_list, 26)
        analyse.ma28 = ma_calc(row_index, stock_day_list, 28)
        analyse.ma30 = ma_calc(row_index, stock_day_list, 30)
        analyse.ma35 = ma_calc(row_index, stock_day_list, 35)
        analyse.ma36 = ma_calc(row_index, stock_day_list, 36)
        analyse.ma37 = ma_calc(row_index, stock_day_list, 37)
        analyse.ma40 = ma_calc(row_index, stock_day_list, 40)
        analyse.ma50 = ma_calc(row_index, stock_day_list, 50)
        analyse.ma60 = ma_calc(row_index, stock_day_list, 60)
        analyse.ma70 = ma_calc(row_index, stock_day_list, 70)
        analyse.ma80 = ma_calc(row_index, stock_day_list, 80)
        analyse.ma90 = ma_calc(row_index, stock_day_list, 90)
        analyse.ma100 = ma_calc(row_index, stock_day_list, 100)
        analyse.ma110 = ma_calc(row_index, stock_day_list, 110)
        analyse.ma120 = ma_calc(row_index, stock_day_list, 120)
        analyse.ma150 = ma_calc(row_index, stock_day_list, 150)
        analyse.ma160 = ma_calc(row_index, stock_day_list, 160)
        analyse.ma180 = ma_calc(row_index, stock_day_list, 180)
        analyse.ma200 = ma_calc(row_index, stock_day_list, 200)
        analyse.ma240 = ma_calc(row_index, stock_day_list, 240)
        analyse.ma250 = ma_calc(row_index, stock_day_list, 250)
        analyse.ma300 = ma_calc(row_index, stock_day_list, 300)
        analyse.ma360 = ma_calc(row_index, stock_day_list, 360)

        # print(analyse)
        analyse_list.append(analyse)

    return analyse_list
