from sqlalchemy.orm import sessionmaker

from analyse.entity.stock_ext_status import stock_ext_status
from common.BaseService import BaseService
from common.CommonUtil import get_stock_cond
import pandas as pd
from datetime import datetime

from common.dao_base_service import dao_base_service
from common.CommonUtil import get_stock_cond, get_my_follow_sql, get_default_end_date, get_my_all_sql


# 扩展状态类
class stock_strategy_cond_dao(dao_base_service):
    # 获取
    def get_list(self, cond_type, degree):
        db_session = sessionmaker(self.engine)
        session = db_session()
        sql = "select * from stock_strategy_cond where cond_type={} and degree < {} order by degree".format(cond_type,
                                                                                                            degree)
        stock_list = session.execute(sql).fetchall()
        return stock_list


