

import numpy as np
import pandas as pd
from sklearn.preprocessing import Binarizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

# 二值化处理
array1 = np.arange(1, 10)
array2 = array1.reshape(-1, 1)
print(array1)

# # Binarizer 二值化处理，大于5为1，小于为0
# transformer = Binarizer(threshold=5).fit_transform(array2)
# print(transformer)

# numpy直接处理，顺序很重要，后面的处理是基于前面的结果
# array2[array2 < 5] = -1
# array2[array2 == 5] = 0
# array2[array2 > 5] = 1
# print(array2)

# 归一化，再按极差（最大值 - 最小值）缩放，数据移动了最小值个单位，并且会被收敛到 [0,1]之间
# scaler_2 = MinMaxScaler(feature_range=(0, 1))  # 默认为0到1之间，也可以是0到2
# scaled = scaler_2.fit_transform(array2)
# print('a-transformed:', scaled)


scaler = StandardScaler()
x_train = scaler.fit_transform(array2)
print('标准差标准化的矩阵为：{}'.format(x_train))

# 标准差(σ)计算方法：sqrt((4*4+3*3+2*2+1+0+1+2*2+3*3+4*4)/9); = 2.581988897471611
# select sqrt((4*4+3*3+2*2+1+0+1+2*2+3*3+4*4)/9);
# select 4 / 2.581988897471611;
# X = (x - u)/σ
# 按上描计算 当x为1时， （1-5）/ 2.581988897471611 = 1.5491933384829668



