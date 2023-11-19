from sqlalchemy.orm import sessionmaker

from model.stock_ext_status import stock_ext_status

from dao.dao_base_service import dao_base_service


# 扩展状态类
class stock_ext_status_dao(dao_base_service):
    # 获取
    def get(self, item):
        db_session = sessionmaker(self.engine)
        session = db_session()
        result = session.query(stock_ext_status).filter(stock_ext_status.ts_code == item.ts_code
                                                        , stock_ext_status.total_type == item.total_type).first()
        return result

    # 更新或添加
    def save(self, item):
        db_session = sessionmaker(self.engine)
        session = db_session()
        result = session.query(stock_ext_status).filter(stock_ext_status.ts_code == item.ts_code
                                                        , stock_ext_status.total_type == item.total_type).first()
        if result:
            result.update({stock_ext_status.last_value: item.last_value,
                           stock_ext_status.last_success_date: item.last_success_date})
        else:
            session.add(item)
        session.commit()
