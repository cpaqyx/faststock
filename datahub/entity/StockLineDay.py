__author__ = 'fastwave'
# @Time : 2022/12/10 20:08
# @Author : fastwave 363642626@qq.com

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.ext.declarative import declarative_base

BaseEntity = declarative_base()


class StockLineDay(BaseEntity):
    __tablename__ = 'stock_line_day'

    id = Column(Integer(), primary_key=True)
    index = Column(Integer())
    ts_code = Column(String(12))
    trade_date = Column(String(12))
    open = Column(FLOAT(10, 2))
    high = Column(FLOAT(10, 2))
    low = Column(FLOAT(10, 2))
    close = Column(FLOAT(10, 2))
    pre_close = Column(FLOAT(10, 2))
    change = Column(FLOAT(10, 2))
    pct_chg = Column(FLOAT(10, 2))
    vol = Column(FLOAT(10, 2))
    amount = Column(FLOAT(10, 2))
