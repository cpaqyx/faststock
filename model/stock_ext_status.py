from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base


class stock_ext_status(declarative_base()):

    __tablename__ = 'stock_ext_status'

    id = Column(Integer(), primary_key=True)
    ts_code = Column(String(20))
    total_type = Column(String(15))
    flags = Column(String(15))
    sync_status = Column(Integer())
    last_value = Column(String(50))
    last_success_date = Column(DATETIME())

