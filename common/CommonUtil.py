import datetime as dt


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
