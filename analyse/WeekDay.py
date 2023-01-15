import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common.BaseService import BaseService
from common.CommonUtil import get_stock_cond


class WeekDay(BaseService):
    def show_week_up_percent(self, code_or_name, start_date, end_date):

        sql = """
        select
            T2.*,
            T2.up_cnt/T2.cnt as up_percent_rate
        from
        (
            select
                T1.week_index,
                count(*) as cnt,
                sum(case when  T1.change_percent > 0 then 1 else 0 end) as up_cnt,
                sum(case when  T1.change_percent < 0 then 1 else 0 end) as down_cnt,
                sum(T1.change_percent) as percent,
                sum(case when  T1.change_percent > 0 then T1.change_percent else 0 end) as up_percent,
                sum(case when  T1.change_percent < 0 then T1.change_percent else 0 end) as down_percent
            from
            (
                select
                     (`change`/pre_close)*100 as change_percent,
                     weekday(str_to_date(trade_date,'%%Y%%m%%d')) as week_index
                from
                    stock_line_day
                where 1=1 {}
            )T1
            group by week_index
        )T2
        order by week_index asc;
        """

        where_cond = get_stock_cond(self, code_or_name, start_date, end_date)

        sql = sql.format(where_cond)
        stock_list = pd.read_sql(sql, self.engine)
        print(stock_list[2:4])

        plt.rcParams["font.sans-serif"] = ["SimHei"]
        x = np.array(["星期一", "星期二", "星期三", "星期四", "星期五"])
        y = stock_list["up_percent_rate"].values
        plt.bar(x, y, width=0.5, align="center", label="星期涨跌")
        plt.title("星期涨跌统计", loc="center")
        plt.show()


def main():
    WeekDay().show_week_up_percent("600036.SH", "20220001", "20221230")
    # WeekDay().show_week_up_percent("all", "", "")
    # ChartTools().show_k_line("中国铝业1", "20220001", "20221230", (5, 10, 30))


if __name__ == '__main__':
    main()




