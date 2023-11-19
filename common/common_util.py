import json
import time
from datetime import datetime
import datetime as dt
from decimal import Decimal
import pandas as pd
from common.constant_common import DEFAULT_COIN_START_DATE, DEFAULT_COIN_START_DATE_M
from model.coin_line_1m import coin_line_1m
from model.coin_line_60m import coin_line_60m
from model.coin_line_15m import coin_line_15m
from model.coin_line_5m import coin_line_5m
from model.coin_line_day import coin_line_day


def get_last_work_day(cur_date):
    # 周日、周一仍同步上一周的，把时间退回到前面的周六
    if cur_date.weekday().__eq__(5):
        cur_date = cur_date - dt.timedelta(days=1)
    elif cur_date.weekday().__eq__(6):
        cur_date = cur_date - dt.timedelta(days=2)
    elif cur_date.hour < 22:
        cur_date = cur_date - dt.timedelta(days=1)
    elif cur_date.hour >= 22:
        cur_date = cur_date
    return cur_date


def get_last_unit_time(time_type, time_cnt):
    cur_time = datetime.now()
    cur_hour = cur_time.hour
    cur_minute = cur_time.minute
    cur_seconds = cur_hour * 3600 + cur_minute * 60 + cur_time.second
    if time_type == 'd' and cur_hour < 8:
        return cur_time - dt.timedelta(days=1) - dt.timedelta(seconds=cur_seconds) + dt.timedelta(seconds=8 * 3600)
    elif time_type == 'd':
        return cur_time - dt.timedelta(seconds=cur_seconds) + dt.timedelta(seconds=8 * 3600)
    elif time_type == 'h':
        return cur_time - dt.timedelta(seconds=cur_minute * 60 + cur_time.second) \
            - dt.timedelta(seconds=(cur_hour % time_cnt) * 3600)
    elif time_type == 'm':
        return cur_time - dt.timedelta(seconds=cur_time.second) - dt.timedelta(seconds=(cur_minute % time_cnt) * 60)
    else:
        return cur_time


def get_last_unit_time_str(cur_time, ine_type_cnt, line_type):
    if line_type == "d":
        return datetime.strftime(cur_time, '%Y-%m-%d')
    elif line_type == "h":
        return datetime.strftime(cur_time - dt.timedelta(hours=ine_type_cnt), '%Y-%m-%d %H')
    elif line_type == "m":
        # 向前推ine_type_cnt分钟,保证mexc平台可以获取到最后一个时刻的数据
        return datetime.strftime(cur_time - dt.timedelta(minutes=ine_type_cnt), '%Y-%m-%d %H:%M:%S')
    else:
        return datetime.strftime(cur_time, '%Y-%m-%d %H:%M:%S')


def get_cur_time_str():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def split_time_scope(start_time_str, end_time_str, line_type, line_type_cnt, max_rows_limit):
    start_time_stamp = time.mktime(time.strptime(start_time_str, '%Y-%m-%d %H:%M:%S'))
    end_time_stamp = time.mktime(time.strptime(end_time_str, '%Y-%m-%d %H:%M:%S'))
    # 步长（秒数）
    step_second = line_type_cnt
    if line_type == 'd':
        step_second = 3600*24*line_type_cnt
    elif line_type == 'h':
        step_second = 3600*line_type_cnt
    elif line_type == 'm':
        step_second = 60 * line_type_cnt
    step_second = step_second * max_rows_limit
    scope_list = []
    while start_time_stamp < end_time_stamp:
        start_step = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time_stamp))
        start_time_stamp = start_time_stamp + step_second
        if start_time_stamp > end_time_stamp:
            start_time_stamp = end_time_stamp
        end_step = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time_stamp))
        scope_list.append([start_step, end_step])

    return scope_list


def str_to_date(date_str):
    return datetime.strptime(date_str, '%Y%m%d')


def cat_date(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y%m%d')
    end_date = datetime.strptime(end_date_str, '%Y%m%d')

    cat_list = []
    start_year = int(start_date.strftime("%Y"))
    end_year = int(end_date.strftime("%Y"))

    while start_year < end_year:
        cat_list.append([datetime.strftime(datetime(start_year, 1, 1), '%Y%m%d'),
                         datetime.strftime(datetime(start_year, 6, 30), '%Y%m%d')])
        cat_list.append([datetime.strftime(datetime(start_year, 7, 1), '%Y%m%d'),
                         datetime.strftime(datetime(start_year, 12, 31), '%Y%m%d')])
        start_year += 1

    cat_list.append([datetime.strftime(datetime(start_year, 1, 1), '%Y%m%d'),
                     datetime.strftime(end_date, '%Y%m%d')])

    return cat_list


def get_next_work_day(cur_date):
    next_day = cur_date + dt.timedelta(days=1)
    # 周日、周一仍同步上一周的，把时间前进到后面的周一
    if next_day.weekday().__eq__(5):
        next_day = next_day + dt.timedelta(days=2)
    elif next_day.weekday().__eq__(6):
        next_day = next_day + dt.timedelta(days=1)
    return next_day


# def get_next_trade_day(cur_date):
#     next_day = cur_date
#     if cur_date.hour > 21:
#         next_day = cur_date + dt.timedelta(days=1)
#     # 周日、周一仍同步上一周的，把时间前进到后面的周一
#     if next_day.weekday().__eq__(5):
#         next_day = next_day + dt.timedelta(days=2)
#     elif next_day.weekday().__eq__(6):
#         next_day = next_day + dt.timedelta(days=1)
#     return next_day

def get_next_sync_day(cur_date):
    next_day = cur_date
    if cur_date.hour > 21:
        next_day = cur_date + dt.timedelta(days=1)
    # 周日、周一仍同步上一周的，把时间前进到后面的周一
    if next_day.weekday().__eq__(5):
        next_day = next_day + dt.timedelta(days=2)
    elif next_day.weekday().__eq__(6):
        next_day = next_day + dt.timedelta(days=1)
    return next_day


def get_cur_sync_day(cur_date):
    # sync_day = cur_date
    if cur_date.hour <= 21:
        return cur_date - dt.timedelta(days=1)
    return cur_date


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


def get_coin_stock_cond(self, coin_code, start_date, end_date, prefix):
    where_cond = " and {}coin_code ='{}'".format(prefix, coin_code)
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
    return "select * from stock_basic_status where degree <= {} order by ts_code".format(degree)


def get_my_all_sql():
    return "select * from stock_basic_status order by degree asc"


def get_my_all_qfq_sql():
    return "select * from stock_basic_status_qfq order by degree asc"


def get_default_end_date():
    return datetime.strftime(datetime.now(), '%Y%m%d')


def get_coin_default_end_date():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


def get_before_n_day(days):
    return datetime.strftime((datetime.now() - dt.timedelta(days=days)), '%Y%m%d')


def get_coin_time_flag(method_type, time_type):
    cur_time = datetime.now()
    cur_minute = cur_time.minute
    cur_seconds = cur_time.second
    skip_second = 60
    option = "height_none"

    if time_type == "5m":
        skip_second = 300 - (cur_minute % 5) * 60 - cur_seconds
        option = "run_per_5m"
    elif time_type == "1m":
        skip_second = 60 - cur_seconds
        option = "run_per_1m"

    if method_type == "skip":
        return skip_second

    if method_type == "method":
        return option


def get_coin_low_frequency_time_flag(method_type):
    cur_time = datetime.now()
    cur_hour = cur_time.hour
    cur_minute = cur_time.minute
    # cur_seconds = cur_hour * 3600 + cur_minute * 60 + cur_time.second
    skip_second = 1800
    # option = "low_none"

    # 只有为整点被4整除，则返回一个方法，这里可以扩展
    if cur_minute == 58 or cur_minute == 28:
        option = "run_per_30m"
    else:
        option = "run_per_30m"

    # 每个半小时为单位，即等待时间不超过1800秒
    if 0 <= cur_minute < 28:
        skip_second = 1800 - 120 - cur_minute * 60 - cur_time.second
    elif 28 <= cur_minute < 58:
        skip_second = 3800 - 120 - cur_minute * 60 - cur_time.second
    elif cur_minute >= 58:
        skip_second = 3600 + 1800 - 120 - cur_minute * 60 - cur_time.second

    if method_type == "skip":
        return skip_second

    if method_type == "method":
        return option


# stock_a
def get_time_flag(time_type):
    cur_time = datetime.now()
    cur_hour = cur_time.hour
    cur_minute = cur_time.minute
    cur_seconds = cur_hour * 3600 + cur_minute * 60 + cur_time.second
    skip_second = 60
    option = "none"

    # 周六日
    if cur_time.weekday().__eq__(5):
        option = "none"
        skip_second = (24+22) * 3600 - cur_seconds
    elif cur_time.weekday().__eq__(6) and cur_hour < 22:
        option = "none"
        skip_second = 22 * 3600 - cur_seconds
    # 其他时间
    else:
        # 9:00 前
        if cur_seconds < 9 * 3600:
            skip_second = 9 * 3600 - cur_seconds
            option = "before_9"

        # 9：00 ~ 9：30
        if 9 * 3600 <= cur_seconds < (9 * 3600 + 30 * 60):
            skip_second = (9 * 3600 + 30 * 60) - cur_seconds
            option = "before_open"

        # 开市期间每5分钟跑一次
        elif ((9 * 3600 + 30 * 60) <= cur_seconds < (11 * 3600 + 30 * 60)) \
                or ((13 * 3600) <= cur_seconds < (14 * 3600 + 50 * 60)):
            skip_second = 300
            option = "open"

        # 中午休息 11:30 ~ 13:00
        elif (11 * 3600 + 30 * 60) <= cur_seconds < (13 * 3600):
            skip_second = (13 * 3600) - cur_seconds
            option = "am_close"

        # 收盘前执行14：50 ~ 15:00
        elif (14 * 3600 + 50 * 60) <= cur_seconds < (15 * 3600):
            skip_second = (15 * 3600) - cur_seconds
            option = "before_close"

        # 收盘后，15:00 ~ 22:00
        elif 15 * 3600 <= cur_seconds < 22 * 3600:
            skip_second = 22 * 3600 - cur_seconds
            option = "pm_close"

        # 收盘后，22点以后，等到明天上午9：00
        elif cur_seconds >= 22 * 3600:
            skip_second = 24 * 3600 - cur_seconds + 9 * 3600
            option = "next_trust"
    if skip_second <= 0:
        skip_second = 60

    # 默认为1分钟
    if time_type == "skip":
        return skip_second

    if time_type == "method":
        return option


def ts_code_2_code(ts_code):
    return ts_code.replace(".SZ", "").replace(".SH", "")


def get_today_zero():
    now = datetime.now()
    today_zero = now - dt.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                    microseconds=now.microsecond)
    return today_zero


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


def get_entity_by_interval(interval):
    entity = None
    if interval == '1d':
        entity = coin_line_day
    elif interval == '60m':
        entity = coin_line_60m
    elif interval == '15m':
        entity = coin_line_15m
    elif interval == '5m':
        entity = coin_line_5m
    elif interval == '1m':
        entity = coin_line_1m
    return entity


def get_start_time_by_interval(interval):
    start_time_str = DEFAULT_COIN_START_DATE
    if interval == "5m" or interval == "1m":
        start_time_str = DEFAULT_COIN_START_DATE_M
    return start_time_str


def get_msg_json(msg, status=False):
    return {"status": status, "msg": msg}


def json_f2d(json_str):
    params = eval(json_str)
    for key, value in params.items():
        if isinstance(value, float):
            params[key] = Decimal.from_float(value).quantize(Decimal("0.00"))
    return params


def dic_f2d(params):
    for key, value in params.items():
        if isinstance(value, float):
            params[key] = Decimal.from_float(value).quantize(Decimal("0.00"))
    return params


def dic_f2d_level2(params_araay):
    for params in params_araay:
        for key, value in params.items():
            if isinstance(value, float):
                params[key] = Decimal.from_float(value).quantize(Decimal("0.00"))
    return params_araay
