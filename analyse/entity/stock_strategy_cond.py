from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base


class stock_strategy_cond(declarative_base()):

    __tablename__ = 'stock_strategy_cond'

    id = Column(Integer(), primary_key=True)
    strategy_name = Column(String(50))
    option_date = Column(DATETIME())
    cond_expression = Column(String(500))
    compare_type = Column(String(50))
    start_value = Column(String(500))
    end_value = Column(String(500))
    step_value = Column(String(500))
