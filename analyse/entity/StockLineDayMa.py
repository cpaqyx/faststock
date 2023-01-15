__author__ = 'fastwave'
# @Time : 2023/1/2 20:08
# @Author : fastwave 363642626@qq.com

from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

BaseEntity = declarative_base()


class StockLineDayMa(BaseEntity):
    __tablename__ = 'stock_line_day_ma'

    id = Column(Integer(), primary_key=True)
    ts_code = Column(String(20))
    trade_date = Column(String(15))
    close = Column(DECIMAL(10, 2))
    ma2 = Column(DECIMAL(10, 2))
    ma3 = Column(DECIMAL(10, 2))
    ma4 = Column(DECIMAL(10, 2))
    ma5 = Column(DECIMAL(10, 2))
    ma6 = Column(DECIMAL(10, 2))
    ma7 = Column(DECIMAL(10, 2))
    ma8 = Column(DECIMAL(10, 2))
    ma10 = Column(DECIMAL(10, 2))
    ma11 = Column(DECIMAL(10, 2))
    ma12 = Column(DECIMAL(10, 2))
    ma13 = Column(DECIMAL(10, 2))
    ma14 = Column(DECIMAL(10, 2))
    ma15 = Column(DECIMAL(10, 2))
    ma16 = Column(DECIMAL(10, 2))
    ma17 = Column(DECIMAL(10, 2))
    ma18 = Column(DECIMAL(10, 2))
    ma19 = Column(DECIMAL(10, 2))
    ma20 = Column(DECIMAL(10, 2))
    ma24 = Column(DECIMAL(10, 2))
    ma25 = Column(DECIMAL(10, 2))
    ma26 = Column(DECIMAL(10, 2))
    ma28 = Column(DECIMAL(10, 2))
    ma30 = Column(DECIMAL(10, 2))
    ma35 = Column(DECIMAL(10, 2))
    ma36 = Column(DECIMAL(10, 2))
    ma37 = Column(DECIMAL(10, 2))
    ma40 = Column(DECIMAL(10, 2))
    ma50 = Column(DECIMAL(10, 2))
    ma60 = Column(DECIMAL(10, 2))
    ma70 = Column(DECIMAL(10, 2))
    ma80 = Column(DECIMAL(10, 2))
    ma90 = Column(DECIMAL(10, 2))
    ma100 = Column(DECIMAL(10, 2))
    ma110 = Column(DECIMAL(10, 2))
    ma120 = Column(DECIMAL(10, 2))
    ma150 = Column(DECIMAL(10, 2))
    ma160 = Column(DECIMAL(10, 2))
    ma180 = Column(DECIMAL(10, 2))
    ma200 = Column(DECIMAL(10, 2))
    ma240 = Column(DECIMAL(10, 2))
    ma250 = Column(DECIMAL(10, 2))
    ma300 = Column(DECIMAL(10, 2))
    ma360 = Column(DECIMAL(10, 2))

