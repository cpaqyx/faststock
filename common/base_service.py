__author__ = 'FL'

from datetime import datetime

# @Time : 2022/12/10 20:08
# @Author : FL 363642626@qq.com

import tushare as ts

from common.common_util import get_stock_cond
from common.config_tool import DBSelector, config_dict
from loguru import logger
from sqlalchemy.orm import sessionmaker

from common.log_util import log_util
from model.StockBasicInfo import StockBasicInfo


class BaseService(object):

    def __init__(self):
        # tushare
        ts_token = config_dict('ts_token')
        ts.set_token(ts_token)
        self.pro = ts.pro_api()
        self.ts = ts

        # logger
        self.logger = log_util("base_service").get_log()
        # self.logger = logger
        # logfile = "../log/{}.log".format(datetime.strftime(datetime.now(), '%Y%m%d'))
        # self.logger.add(sink=logfile, encoding='utf-8', level='WARNING')

        # db
        self.engine = DBSelector().get_engine()

    def get_stock_info(self, code_or_name):
        db_session = sessionmaker(self.engine)
        session = db_session()
        basic_info = session.query(StockBasicInfo).filter(
            (StockBasicInfo.ts_code == code_or_name) | (StockBasicInfo.name.like('%{}%'.format(code_or_name)))).first()
        return basic_info

    def delete_table_data(self, table_name, code_or_name, start_date, end_date):
        db_session = sessionmaker(self.engine)
        session = db_session()
        del_sql = "delete from {} where 1=1 {};"
        where_cond_del = get_stock_cond(self, code_or_name, start_date, end_date, "")
        del_sql = del_sql.format(table_name, where_cond_del)
        session.execute(del_sql)
        session.commit()

    def save_table_data(self, data_list):
        db_session = sessionmaker(self.engine)
        session = db_session()
        session.bulk_save_objects(data_list)
        session.commit()
        session.close()


if __name__ == '__main__':
    pass
