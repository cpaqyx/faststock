from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base


class stock_basic_status(declarative_base()):

    __tablename__ = 'stock_basic_status'

    id = Column(Integer(), primary_key=True)
    ts_code = Column(String(20))
    line_type = Column(Integer)
    sync_status = Column(Integer())
    last_value = Column(String(50))

    last_success_date = Column(DATETIME())
    order_index = Column(String(50))
    app_mode = Column(Integer)
    degree = Column(Integer)
    allow_delay_second = Column(String(50))
    label = Column(String(50))
    record_status = Column(Integer)
    remark = Column(String(50))
    created_on = Column(DATETIME())
    updated_on = Column(DATETIME())
