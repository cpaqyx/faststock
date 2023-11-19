__author__ = 'FL'
# @Time : 2023/1/2 20:08
# @Author : FL 363642626@qq.com

from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

BaseEntity = declarative_base()


class StockLineDayCoef(BaseEntity):
    __tablename__ = 'stock_line_day_coef_analyse'

    id = Column(Integer(), primary_key=True)
    ts_code = Column(String(20))
    trade_date = Column(String(15))
    predict_output = Column(String(25))
    predict_input = Column(String(25))
    input_flag = Column(String(10))
    coef = Column(DECIMAL(10, 4))
    intercept = Column(DECIMAL(10, 4))
    score = Column(DECIMAL(10, 4))

