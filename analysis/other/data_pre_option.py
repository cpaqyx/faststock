

import numpy as np
import pandas as pd
from sklearn.preprocessing import Binarizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

from analysis.strategy.trend_line.v0102 import get_trend_list_v0102
from analysis.strategy.trend_line.v0106 import get_trend_list_v0106
from analysis.strategy.trend_line.v0107 import get_trend_list_v0107
from common.common_util import get_default_end_date
from common.constant_common import DEFAULT_START_DATE
from dao.coin_line_dao import coin_line_dao
from dao.stock_line_day_dao import stock_line_day_dao

# （1）二值化处理
# array1 = np.arange(1, 10)
# array2 = array1.reshape(-1, 1)
# print(array1)

# # Binarizer 二值化处理，大于5为1，小于为0
# transformer = Binarizer(threshold=5).fit_transform(array2)
# print(transformer)

# numpy直接处理，顺序很重要，后面的处理是基于前面的结果
# array2[array2 < 5] = -1
# array2[array2 == 5] = 0
# array2[array2 > 5] = 1
# print(array2)


# 2.归一化，再按极差（最大值 - 最小值）缩放，数据移动了最小值个单位，并且会被收敛到 [0,1]之间
# scaler_2 = MinMaxScaler(feature_range=(0, 1))  # 默认为0到1之间，也可以是0到2
# scaled = scaler_2.fit_transform(array2)
# print('a-transformed:', scaled)


# 3.z-score
# scaler = StandardScaler()
# x_train = scaler.fit_transform(array2)
# print('标准差标准化的矩阵为：{}'.format(x_train))

# 标准差(σ)计算方法：sqrt((4*4+3*3+2*2+1+0+1+2*2+3*3+4*4)/9); = 2.581988897471611
# select sqrt((4*4+3*3+2*2+1+0+1+2*2+3*3+4*4)/9);
# select 4 / 2.581988897471611;
# X = (x - u)/σ
# 按上描计算 当x为1时， （1-5）/ 2.581988897471611 = 1.5491933384829668

# 3.2 手工计逄z-score， 计算公式：（x-u) / σ
# 有一列数据分别是：6、3、8、9、1
# （1）求平均值
# select (6+3+8+9+1)/5
# -- 5.4

# （2）样本标准差计算（简称σ)
# select sqrt(((6-5.4)*(6-5.4)+(3-5.4)*(3-5.4)+(8-5.4)*(8-5.4)+(9-5.4)*(9-5.4)+(1-5.4)*(1-5.4))/5);
# -- 3.0066592756745814

# (3) 计算第一个数值的z-score值
# select (6-5.4)/3.0066592756745814
# 0.19956

# start_date = DEFAULT_START_DATE
# end_date = get_default_end_date()
# # day_list = stock_line_day_dao().get_stock_line_day("002125.SZ", start_date, end_date)
# day_list = stock_line_day_dao().get_stock_line_day("605108.SH", start_date, end_date)
# index_no = day_list.shape[0]
# max_index = day_list.index.max()
# # print(max_index)
# list1 = get_trend_list_v0102(max_index, day_list,
#                              {"trend_line_analyse_days": 50,
#                               "first_ignore_days": 1.0, "twice_ignore_days": 3, "third_ignore_days": 5,
#                               "first_ignore_percent": 0, "twice_ignore_percent": 1.0, "third_ignore_percent": 3.0,
#                               "ignore_percent": 1.0})


coin_code = "GFT"
start_date = "2023-10-26 15:30:00"
end_date = "2023-10-27 15:00:00"
table_name = "coin_line_5m"
line_list = coin_line_dao().get_coin_line_by_time(coin_code, start_date, end_date, table_name)
# list1 = get_trend_list_v0107(line_list.index.max(), line_list,
#                              {"trend_line_analyse_days": 150,
#                                  "first_ignore_days": 1, "twice_ignore_days": 3, "third_ignore_days": 5,
#                               "first_ignore_percent": 0, "twice_ignore_percent": 1.0, "third_ignore_percent": 2.0})

list1 = get_trend_list_v0107(line_list.index.max(), line_list,
                             {"rec_cnt": 150, "ignore_days": 5, "merge_percent": 0.08})
for item in list1:
    print(item.start_date, item.end_date, item.change_type, item.continue_day, item.opposite_day, item.total_percent)

