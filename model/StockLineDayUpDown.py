__author__ = 'FL'
# @Time : 2023/1/2 20:08
# @Author : FL 363642626@qq.com

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DECIMAL

BaseEntity = declarative_base()


class StockLineDayUpDown(BaseEntity):
    __tablename__ = 'stock_line_day_up_down'

    id = Column(Integer(), primary_key=True)
    ts_code = Column(String(20))
    trade_date = Column(String(15))
    pre_days = Column(Integer())
    cur_change_percent = Column(DECIMAL(10, 4))
    up_days = Column(Integer())
    down_days = Column(Integer())

    max_continue_up_days = Column(Integer())
    max_continue_down_days = Column(Integer())
    last_continue_days = Column(Integer())
    change_percent = Column(DECIMAL(10, 4))

    last_change_percent = Column(DECIMAL(10, 4))
    big_up_days = Column(Integer())
    big_down_days = Column(Integer())
    big_max_continue_up_days = Column(Integer())
    big_max_continue_down_days = Column(Integer())
    big_last_change_percent = Column(DECIMAL(10, 4))
    big_last_continue_days = Column(Integer())

    after_1day_change_percent = Column(DECIMAL(10, 4))
    after_2day_change_percent = Column(DECIMAL(10, 4))
    after_3day_change_percent = Column(DECIMAL(10, 4))
    after_5day_change_percent = Column(DECIMAL(10, 4))
    after_7day_change_percent = Column(DECIMAL(10, 4))
    after_10day_change_percent = Column(DECIMAL(10, 4))
    after_15day_change_percent = Column(DECIMAL(10, 4))
    after_30day_change_percent = Column(DECIMAL(10, 4))

