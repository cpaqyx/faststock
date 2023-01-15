import numpy as np
from sklearn import preprocessing


# x = np.array([1, 5.5, 10])
# # 标准化：将数据转换为均值为0，方差为1的数据，即标注正态分布的数据
# x_scale = preprocessing.scale(x)

# 将数据缩放至给定范围（0-1）
x = np.array([[1,-1,2],[2,0,0],[0,10,-1]])
mm_scale = preprocessing.MinMaxScaler()
x_mm = mm_scale.fit_transform(x)


print(x_mm)
#
# records = [[111, 'aaa', True],                 #此处可以是List。
#           [222, 'bbb', False],
#           [333, 'ccc', True],
#           [444, '中文', False]]
#
# records.append([666, 'bbb', False])
# row = []
# row.append(777)
# row.append('cccc')
# row.append(True)
#
# records.append(row)
#
# records.append([])
#
# print(records)