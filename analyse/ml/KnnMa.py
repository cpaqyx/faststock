__author__ = 'fastwave'
# @Time : 2023/1/15 20:08
# @Author : fastwave 363642626@qq.com

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Binarizer

from analyse.entity.StockLineDayCoef import StockLineDayCoef


# 相关性测试
def knn_ref(stock_day_ma_list, method_params):
    # y_list = ['after_3day_change_grade', 'after_5day_change_grade', 'after_10day_change_grade',
    #           'after_30day_change_grade']

    y_list = ['after_3day_change_percent', 'after_5day_change_percent', 'after_10day_change_percent',
              'after_30day_change_percent']

    ts_code = method_params[0]
    date = method_params[1]
    analyse_list = []

    knn = KNeighborsClassifier(n_neighbors=5)

    for after in y_list:
        columns = stock_day_ma_list.columns
        # y = np.expand_dims(stock_day_ma_list[after].values, 1)
        # Binarizer 二值化处理，大于0为1，否则为0
        y = Binarizer(threshold=0).fit_transform(np.expand_dims(stock_day_ma_list[after].values, 1))

        for col in columns:
            if col.find("ma") >= 0:
                x = np.expand_dims(stock_day_ma_list[col].values, 1)
                x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

                knn.fit(x_train, y_train.ravel())
                score = knn.score(x_test, y_test)
                # ref_list[col] = score

                analyse = StockLineDayCoef(ts_code=ts_code, trade_date=date, predict_output=after, predict_input=col,
                                           input_flag='knn', score=score)
                analyse_list.append(analyse)

        # ref_list_sort = Series(ref_list).sort_values(ascending=False)
        # print(ref_list_sort)

    return analyse_list

# def grade(percent):
#     if percent >= 2:
#         return 2
#     elif percent >0:
#         return 1
#     elif percent <= -2:
#         return -2
#     elif percent < 0:
#         return -1
#     return 0
