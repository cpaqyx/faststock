from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy.ext.declarative import declarative_base


class stock_strategy_detail(declarative_base()):

    __tablename__ = 'stock_strategy_detail'

    id = Column(Integer(), primary_key=True)
    ts_code = Column(String(20))
    strategy_name = Column(String(50))
    option_date = Column(DATETIME())
    option_type = Column(String(20))
    option_flag = Column(String(20))
    option_price = Column(DECIMAL(10, 4))
    sell_profit_percent = Column(DECIMAL(10, 4))
    sell_order_cnt = Column(Integer())
