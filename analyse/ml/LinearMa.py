__author__ = 'fastwave'
# @Time : 2023/1/15 20:08
# @Author : fastwave 363642626@qq.com

import numpy as np
import pandas as pd
import sklearn
from pandas import Series
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
from sqlalchemy.orm import sessionmaker
from sklearn import linear_model

from analyse.dataPrepare.DayMa import ma_total
from analyse.entity.StockLineDayCoef import StockLineDayCoef
from common.BaseService import BaseService
from common.CommonUtil import get_stock_cond


# 线性回归
def line_total(stock_day_ma_list, method_params):
    x = np.expand_dims(stock_day_ma_list["ma10"].values, 1)
    y = np.expand_dims(stock_day_ma_list["after_3day_change_percent"].values, 1)
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2, random_state=0)

    reg = linear_model.LinearRegression()  # 创建线性回归

    reg.fit(x_train, y_train)
    print(reg.coef_, reg.intercept_)  # w,b

    y_pred = reg.predict(x_test)  # 预测

    print('############')
    # # 回归评估指标
    print(mean_squared_error(y_test, y_pred))  # 均方误差
    print(mean_absolute_error(y_test, y_pred))  # 平均绝对误差
    print(r2_score(y_test, y_pred))  # R2评分
    print(explained_variance_score(y_test, y_pred))  # 可解释方差


# 相关性测试
def line_ref(stock_day_ma_list, method_params):
    y_list = ['after_3day_change_percent', 'after_5day_change_percent', 'after_10day_change_percent',
              'after_30day_change_percent']

    ts_code = method_params[0]
    date = method_params[1]
    analyse_list = []

    linear_reg = linear_model.LinearRegression()  # 创建线性回归

    for after in y_list:
        columns = stock_day_ma_list.columns
        y = np.expand_dims(stock_day_ma_list[after].values, 1)
        ref_list = {}
        value_list = []

        for col in columns:
            if col.find("ma") >= 0:
                x = np.expand_dims(stock_day_ma_list[col].values, 1)
                linear_reg.fit(x, y)
                ref_list[col] = linear_reg.coef_[0][0]

                value_list.append(linear_reg.coef_[0][0])
                value_list.append(linear_reg.intercept_[0])

                analyse = StockLineDayCoef(ts_code=ts_code, trade_date=date, predict_output=after, predict_input=col,
                                           input_flag='up', coef=linear_reg.coef_[0][0], intercept=linear_reg.intercept_[0])
                analyse_list.append(analyse)

        ref_list_sort = Series(ref_list).sort_values(ascending=False)
        print(ref_list_sort)

        Series(value_list).sort_values(ascending=False).plot(kind='bar')
        # value_list.plot(kind='bar')

    return analyse_list
