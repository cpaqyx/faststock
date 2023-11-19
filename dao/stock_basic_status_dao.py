from sqlalchemy.orm import sessionmaker

from common.common_util import get_my_all_qfq_sql
from datetime import datetime
from dao.dao_base_service import dao_base_service
from common.common_util import get_my_follow_sql, get_my_all_sql


# 扩展状态类
class stock_basic_status_dao(dao_base_service):
    # 获取
    def get(self, degree):
        db_session = sessionmaker(self.engine)
        session = db_session()
        sql = get_my_follow_sql(degree)
        if degree == -1:
            sql = get_my_all_sql()
        stock_list = session.execute(sql).fetchall()
        return stock_list

    def get_not_run(self, degree, strategy_name):
        db_session = sessionmaker(self.engine)
        session = db_session()
        sql = get_my_follow_sql(degree)
        if degree == -1:
            sql = "select  I.*  from  stock_basic_info I left join stock_basic_status_qfq S on S.ts_code = I.ts_code " \
                  " where I.market = '主板' and I.name not like '%ST%' " \
                  " and I.industry not in('全国地产','汽车服务','汽车配件','汽车整车','通信设备') " \
                  " and I.ts_code not in(select distinct(ts_code) from " \
                  "stock_strategy_result_part where strategy_name = '{}') order by S.degree asc;".format(strategy_name)

        stock_list = session.execute(sql).fetchall()
        return stock_list

    def get_check_stock_list(self, degree):
        db_session = sessionmaker(self.engine)
        session = db_session()

        # 2023-06-20 2862 items
        sql = "select  I.*  from  stock_basic_info I left join stock_basic_status_qfq S on S.ts_code = I.ts_code " \
              " where I.market = '主板' and I.name not like '%ST%' " \
              " and I.industry not in('全国地产','汽车服务','汽车配件','汽车整车') " \
              "and S.degree <= {}" \
              " order by S.degree asc;".format(degree)

        stock_list = session.execute(sql).fetchall()
        return stock_list

    def get_check_stock_list_test(self, degree):
        db_session = sessionmaker(self.engine)
        session = db_session()

        # 2023-06-20 2862 items
        sql = "select  I.*  from  stock_basic_info I left join stock_basic_status_qfq S on S.ts_code = I.ts_code " \
              " where I.ts_code='600036.SH'".format(degree)

        stock_list = session.execute(sql).fetchall()
        return stock_list

    def get_trade_stock_list(self, degree):
        db_session = sessionmaker(self.engine)
        session = db_session()

        # sql = "select  I.*  from  stock_basic_info I left join stock_basic_status_qfq S on S.ts_code = I.ts_code " \
        #       " where I.market = '主板' and I.name not like '%ST%' " \
        #       " and I.industry not in('全国地产','汽车服务','汽车配件','汽车整车','通信设备', '石油加工', '石油贸易', " \
        #       "'白酒', '中成药', '生物制药', '区域地产') " \
        #       "and S.degree <= {}" \
        #       " order by S.degree asc;".format(degree)
        sql = "select  I.*  from  stock_basic_info I left join stock_basic_status_qfq S on S.ts_code = I.ts_code " \
              " where I.market = '主板' and I.name not like '%ST%' " \
              " and I.industry not in('全国地产','汽车服务','汽车配件','汽车整车','通信设备', '石油加工', '石油贸易', " \
              "'白酒', '区域地产') " \
              "and S.degree <= {}" \
              " order by S.degree asc;".format(degree)

        stock_list = session.execute(sql).fetchall()
        return stock_list

    def get_trade_stock_sell_list(self, before_sync_time):
        # 获取当天的时间，忽略时分秒
        # cur_date_str = datetime.strftime(datetime.now(), '%Y-%m-%d')
        session = sessionmaker(self.engine)()
        sql = "select  I.*,P.cost_price from  stock_basic_info I  join trade_position P on I.code = P.ts_code " \
              " where P.create_date > '{}';".format(before_sync_time)

        stock_list = session.execute(sql).fetchall()
        return stock_list

    def temp(self, degree):
        db_session = sessionmaker(self.engine)
        session = db_session()
        sql = "select * from stock_basic_status_qfq where ts_code not in(select distinct(ts_code) " \
              "from stock_strategy_detail where option_flag in('shape_v3','shape_v4','shape_v5'));"
        stock_list = session.execute(sql).fetchall()
        return stock_list

    def get_qfq(self, degree):
        db_session = sessionmaker(self.engine)
        session = db_session()
        sql = get_my_all_qfq_sql(degree)
        if degree == -1:
            sql = get_my_all_qfq_sql()
        stock_list = session.execute(sql).fetchall()
        return stock_list
