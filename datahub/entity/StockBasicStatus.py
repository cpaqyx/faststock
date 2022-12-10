__author__ = 'fastwave'
# @Time : 2022/12/10 20:08
# @Author : fastwave 363642626@qq.com

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

BaseEntity = declarative_base()


class StockBasicStatus(BaseEntity):
    __tablename__ = 'stock_basic_status'

    id = Column(Integer, primary_key=True)
    index = Column(Integer())
    code = Column(String(20))

    line_type = Column(String(20))
    sync_status = Column(Integer())
    order_index = Column(Integer())
    app_mode = Column(Integer())
    degree = Column(Integer())
    allow_delay_second = Column(Integer())
    record_status = Column(Integer())

    last_value = Column(String(20))
    label = Column(String(20))
    remark = Column(String(20))

    last_success_date = Column(DateTime())
    created_on = Column(DateTime())
    updated_on = Column(DateTime())
