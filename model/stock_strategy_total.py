from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy.ext.declarative import declarative_base


class stock_strategy_total(declarative_base()):

    __tablename__ = 'stock_strategy_total'

    id = Column(Integer(), primary_key=True)
    ts_code = Column(String(20))
    buy_cnt = Column(Integer())
    max_buy_cnt = Column(Integer())
    sell_cnt = Column(Integer())
    buy_and_sell_cnt = Column(Integer())
    profit_percent = Column(DECIMAL(10, 4))
    profit_avg_percent = Column(DECIMAL(10, 4))
    max_loss_percent = Column(DECIMAL(10, 4))
    total_date = Column(DATETIME())
