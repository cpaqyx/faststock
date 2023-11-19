from common.common_util import get_stock_cond
import pandas as pd

from dao.dao_base_service import dao_base_service


# 数据
class stock_line_day_dao(dao_base_service):
    def get_stock_line_day_list(self, code_or_name, start_date, end_date):
        sql = '''
        SELECT 
            MA.id,
            MA.ts_code,
            MA.trade_date,
            MA.`close`,
            MA.ma2   -  `close` AS   ma2  ,
            MA.ma3   -  `close` AS   ma3  ,
            MA.ma4   -  `close` AS   ma4  ,
            MA.ma5   -  `close` AS   ma5  ,
            MA.ma6   -  `close` AS   ma6  ,
            MA.ma7   -  `close` AS   ma7  ,
            MA.ma8   -  `close` AS   ma8  ,
            MA.ma10   -  `close` AS  ma10 ,
            MA.ma11   -  `close` AS  ma11 ,
            MA.ma12   -  `close` AS  ma12 ,
            MA.ma13   -  `close` AS  ma13 ,
            MA.ma14   -  `close` AS  ma14 ,
            MA.ma15   -  `close` AS  ma15 ,
            MA.ma16   -  `close` AS  ma16 ,
            MA.ma17   -  `close` AS  ma17 ,
            MA.ma18   -  `close` AS  ma18 ,
            MA.ma19   -  `close` AS  ma19 ,
            MA.ma20   -  `close` AS  ma20 ,
            MA.ma24   -  `close` AS  ma24 ,
            MA.ma25   -  `close` AS  ma25 ,
            MA.ma26   -  `close` AS  ma26 ,
            MA.ma28   -  `close` AS  ma28 ,
            MA.ma30   -  `close` AS  ma30 ,
            MA.ma35   -  `close` AS  ma35 ,
            MA.ma36   -  `close` AS  ma36 ,
            MA.ma37   -  `close` AS  ma37 ,
            MA.ma40   -  `close` AS  ma40 ,
            MA.ma50   -  `close` AS  ma50 ,
            MA.ma60   -  `close` AS  ma60 ,
            MA.ma70   -  `close` AS  ma70 ,
            MA.ma80   -  `close` AS  ma80 ,
            MA.ma90   -  `close` AS  ma90 ,
            MA.ma100   -  `close` AS ma100 ,
            MA.ma110   -  `close` AS ma110 ,
            MA.ma120   -  `close` AS ma120 ,
            MA.ma150   -  `close` AS ma150 ,
            MA.ma160   -  `close` AS ma160 ,
            MA.ma180   -  `close` AS ma180 ,
            MA.ma200   -  `close` AS ma200 ,
            MA.ma240   -  `close` AS ma240 ,
            MA.ma250   -  `close` AS ma250 ,
            MA.ma300   -  `close` AS ma300 ,
            MA.ma360   -  `close` AS ma360 ,
            DW.pre_days,
            DW.cur_change_percent,
            DW.up_days,
            DW.down_days,
            DW.max_continue_up_days,
            DW.max_continue_down_days,
            DW.last_continue_days,
            DW.change_percent,
            DW.last_change_percent,
            DW.big_up_days,
            DW.big_down_days,
            DW.big_max_continue_up_days,
            DW.big_max_continue_down_days,
            DW.big_last_continue_days,
            DW.big_last_change_percent,
            DW.after_3day_change_percent,
            DW.after_5day_change_percent,
            DW.after_10day_change_percent,
            DW.after_30day_change_percent 
        FROM stock_line_day_ma MA
        JOIN stock_line_day_up_down DW on MA.ts_code = DW.ts_code and MA.trade_date = DW.trade_date 
        where 1=1 {};
        '''

        where_cond = get_stock_cond(self, code_or_name, start_date, end_date, "MA.")
        sql = sql.format(where_cond)
        stock_day_list = pd.read_sql(sql, self.engine)
        return stock_day_list

    def get_stock_line_day(self, code_or_name, start_date, end_date):
        where_cond = get_stock_cond(self, code_or_name, start_date, end_date, "")
        # sql = "select * from stock_line_day_view where 1=1 {} order by trade_date asc;"
        sql = "select * from stock_line_day_qfq_view where 1=1 {} order by trade_date asc;"
        sql = sql.format(where_cond)
        stock_day_list = pd.read_sql(sql, self.engine)
        return stock_day_list
