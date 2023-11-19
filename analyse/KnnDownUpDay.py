import pandas as pd
import matplotlib.pyplot as plt
from common.base_service import BaseService
from common.common_util import get_stock_cond, get_up_down_grade_color


# 统计N天内涨跌
class KnnDownUpDay(BaseService):
    # 打点图
    def down_up_port(self, code_or_name, start_date, end_date, col_x, col_y):
        where_cond = get_stock_cond(self, code_or_name, start_date, end_date)
        sql = "select * from stock_line_day_up_dwon where 1=1 {} order by trade_date asc;"
        sql = sql.format(where_cond)
        stock_list = pd.read_sql(sql, self.engine)

        # 提取出当前上涨下跌有关的列
        # X = stock_list[["last_continue_days", "change_percent"]]
        grade = stock_list.apply(lambda row: get_up_down_grade_color(row, col_y), axis=1)
        # plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.scatter(stock_list[col_x], stock_list[col_y], c=grade.values)
        plt.show()

    # 统计输出
    def down_up_ref(self, code_or_name, start_date, end_date, col_x, col_y):
        where_cond = get_stock_cond(self, code_or_name, start_date, end_date)
        sql = "select * from stock_line_day_up_dwon where 1=1 {} order by trade_date asc;"
        sql = sql.format(where_cond)
        stock_list = pd.read_sql(sql, self.engine)
        # print(stock_list.cov())
        # export_to_excel(stock_list.cov(), "test")
        # export_to_excel(stock_list.corr(), "corr")

        print(stock_list["after_30day_change_percent"].corr(stock_list["big_down_days"]))
        # -0.12625945755920115
        print(stock_list["after_30day_change_percent"].corr(stock_list["big_up_days"]))
        # -0.12555880974784153


def main():
    # KnnDownUpDay().down_up_total("600036.SH", "20201201", "20221230", "down_days", "cur_change_percent")
    KnnDownUpDay().down_up_ref("600036.SH", "19001201", "20221230", "down_days", "cur_change_percent")


if __name__ == '__main__':
    main()
