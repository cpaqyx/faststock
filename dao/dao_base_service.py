__author__ = 'FL'
# @Time : 2022/12/10 20:08
# @Author : FL 363642626@qq.com

from common.common_util import get_stock_cond
from common.config_tool import DBSelector
from sqlalchemy.orm import sessionmaker

from model.StockBasicInfo import StockBasicInfo


class dao_base_service(object):

    def __init__(self, logfile='../log/default.log'):
        # db
        self.engine = DBSelector().get_engine()

    def execute_sql(self, sql):
        session = sessionmaker(self.engine)()
        session.execute(sql)
        session.commit()

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
