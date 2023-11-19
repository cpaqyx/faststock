__author__ = 'FL'

from datetime import datetime

# @Time : 2023/1/15 20:08
# @Author : FL 363642626@qq.com

from dao.stock_line_day_dao import stock_line_day_dao
from analysis.discover.ml.KnnMa import knn_ref
from common.base_service import BaseService


# 按天统计各类指标
class DayAnalyse(BaseService):
    def day_total(self, code_or_name, start_date, end_date, table_name, method_name, method_params):

        # 删除已分析的结果
        self.delete_table_data(table_name, code_or_name, start_date, end_date)

        # 读取股票数据
        stock_day_list = stock_line_day_dao().get_stock_line_day_list(code_or_name, start_date, end_date)

        # 分析数据
        analyse_list = method_name(stock_day_list, method_params)

        # 保存分析结果
        self.save_table_data(analyse_list)


def main():
    cur_date_str = datetime.strftime(datetime.now(), '%Y%m%d')

    # 涨跌幅度统计
    # DayAnalyse().day_total("600036.SH", "20220601", "20221230", "stock_line_day_up_down", down_up_total, (15, 2.0))

    # 均线（ma）统计
    # DayAnalyse().day_total("600036.SH", "19000101", "20221230", "stock_line_day_ma",  line_total, (15, 2.0))

    # linear
    # DayAnalyse().day_total("600036.SH", "19000101", "20221230", "stock_line_day_coef_analyse", line_ref, ('600036.SH', cur_date_str))

    # knn ma
    DayAnalyse().day_total("600036.SH", "19000101", "20221230", "stock_line_day_coef_analyse", knn_ref, ('600036.SH', cur_date_str))


if __name__ == '__main__':
    main()

