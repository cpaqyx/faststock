__author__ = 'FL'
# @Time : 2022/12/10 20:08
# @Author : FL 363642626@qq.com

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

BaseEntity = declarative_base()


class StockBasicInfo(BaseEntity):
    __tablename__ = 'stock_basic_info'

    index = Column(Integer(), primary_key=True)
    ts_code = Column(String(20))
    code = Column(String(20))
    name = Column(String(20))
    area = Column(String(20))
    industry = Column(String(20))
    market = Column(String(20))
    list_date = Column(String(20))
    update_date = Column(DateTime())
