from sqlalchemy.orm import sessionmaker
from dao.dao_base_service import dao_base_service


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

    def get_list_by_name(self, strategy_name):
        db_session = sessionmaker(self.engine)
        session = db_session()
        sql = "select * from stock_strategy_cond where strategy_name='{}' order by degree".format(strategy_name)
        stock_list = session.execute(sql).fetchall()
        return stock_list
