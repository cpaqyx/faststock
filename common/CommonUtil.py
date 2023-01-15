from datetime import datetime
import datetime as dt
import pandas as pd


def get_last_work_day(cur_date):
    # 周日、周一仍同步上一周的，把时间退回到前面的周六
    if cur_date.weekday().__eq__(5):
        cur_date = cur_date - dt.timedelta(days=1)
    elif cur_date.weekday().__eq__(6):
        cur_date = cur_date - dt.timedelta(days=2)
    elif cur_date.hour > 18:
        cur_date = cur_date - dt.timedelta(days=1)
    return cur_date


def get_next_work_day(cur_date):
    next_day = cur_date + dt.timedelta(days=1)
    # 周日、周一仍同步上一周的，把时间前进到后面的周一
    if next_day.weekday().__eq__(5):
        next_day = next_day + dt.timedelta(days=2)
    elif next_day.weekday().__eq__(6):
        next_day = next_day + dt.timedelta(days=1)
    return next_day


def get_stock_cond(self, code_or_name, start_date, end_date, prefix):
    where_cond = ""
    if not code_or_name.__eq__("all"):
        basic_info = self.get_stock_info(code_or_name)
        if basic_info is None:
            self.logger.info("{}找不到".format(code_or_name))
            return
        where_cond = where_cond + " and {}ts_code ='{}'".format(prefix, basic_info.ts_code)

    if start_date:
        where_cond = where_cond + " and {}trade_date >='{}'".format(prefix, start_date)
    if end_date:
        where_cond = where_cond + " and {}trade_date <='{}'".format(prefix, end_date)
    return where_cond


def get_up_down_grade(row, col_name):
    if row[col_name] >= 2:
        return 2
    elif row[col_name] > 0:
        return 1
    elif row[col_name] <= -2:
        return -2
    elif row[col_name] < 0:
        return -1
    else:
        return 0


# '#90000', '#ff3366', '#cccccc', '#99ff00', '#336600'
# Colors = ('#90000', '#ff3366', '#cccccc', '#99ff00', '#336600')
def get_up_down_grade_color(row, col_name):
    if row[col_name] >= 2:
        return "darkred"
    elif row[col_name] > 0:
        return "red"
    elif row[col_name] <= -2:
        return "darkgreen"
    elif row[col_name] < 0:
        return "lightgreen"
    else:
        return "gray"


def export_to_excel(table, excel_name):
    writer = pd.ExcelWriter("D:\\git\\faststock\\analyse\\data\\" + excel_name + ".xlsx")  # 初始化一个writer
    table.to_excel(writer, float_format='%.5f')  # table输出为excel, 传入writer
    writer.close()


def get_my_follow_sql(degree):
    return "select * from stock_basic_status where degree <= {}".format(degree)


def get_my_all_sql():
    return "select * from stock_basic_status order by degree asc"


def get_default_end_date():
    return datetime.strftime(datetime.now(), '%Y%m%d')


