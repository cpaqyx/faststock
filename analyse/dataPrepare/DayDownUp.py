__author__ = 'fastwave'
# @Time : 2023/1/15 22:45
# @Author : fastwave 363642626@qq.com

from analyse.entity.StockLineDayUpDown import StockLineDayUpDown


# 统计N天内涨跌：N天统计当天的前N天，统计前N天的情况，含：上涨下跌天数、最大连续上涨/下跌天数、大涨/跌天数
# 统计结果：后面一天、3天、5天，10天，30天涨跌
# 前N天和后N天累计涨跌幅度
def down_up_total(stock_day_list, method_params):
    day_cnt = method_params[0]
    big_percent = method_params[1]

    analyse_list = []
    for row_index, row in stock_day_list.iterrows():
        # print(row_index)
        # 前面几天的不统计
        if row_index < day_cnt:
            continue

        analyse = StockLineDayUpDown(ts_code=row["ts_code"], trade_date=row["trade_date"], pre_days=day_cnt,
                                     cur_change_percent=row["change_percent"])
        up_days = 0
        down_days = 0
        max_continue_up_days = 0
        max_continue_down_days = 0
        temp_max_continue_up_days = 0
        temp_max_continue_down_days = 0
        last_continue_days = 0
        last_continue_up_days = 0
        last_continue_down_days = 0
        change_percent = 0.0
        last_change_percent = 0.0
        last_change_up_percent = 0.0
        last_change_down_percent = 0.0
        big_up_days = 0
        big_down_days = 0
        big_max_continue_up_days = 0
        temp_big_max_continue_up_days = 0
        big_max_continue_down_days = 0
        temp_big_max_continue_down_days = 0
        big_last_change_percent = 0.0
        big_last_change_up_percent = 0.0
        big_last_change_down_percent = 0.0
        big_last_continue_up_days = 0
        big_last_continue_down_days = 0
        is_pre_up = True
        is_pre_down = True
        is_pre_big_up = True
        is_pre_big_down = True

        # 统计这一天的前几天涨跌情况
        pre_list = stock_day_list[(row_index - day_cnt): row_index]
        # print(pre_list)
        for pre_index, pre_row in pre_list.iterrows():
            cur_change = pre_row["change_percent"]

            # 上涨天数、最近最大连续上涨天数、最近上涨百分点
            if cur_change > 0:
                up_days = up_days + 1
                last_continue_up_days = last_continue_up_days + 1
                last_change_up_percent = last_change_up_percent + cur_change
            else:
                last_continue_up_days = 0
                last_change_up_percent = 0.0

            # 下跌天数、最近最大连续下跌天数、最近下跌百分点
            if cur_change < 0:
                down_days = down_days + 1
                last_continue_down_days = last_continue_down_days + 1
                last_change_down_percent = last_change_down_percent + cur_change
            else:
                last_continue_down_days = 0
                last_change_down_percent = 0.0

            # 最大连续上涨天数
            if cur_change > 0 and is_pre_up:
                temp_max_continue_up_days = temp_max_continue_up_days + 1
            else:
                if temp_max_continue_up_days > max_continue_up_days:
                    max_continue_up_days = temp_max_continue_up_days
                    temp_max_continue_up_days = 0
                if cur_change > 0 and not is_pre_up:
                    temp_max_continue_up_days = 1

            # 最大连续下跌天数
            if cur_change < 0 and is_pre_down:
                temp_max_continue_down_days = temp_max_continue_down_days + 1
            else:
                if temp_max_continue_down_days > max_continue_down_days:
                    max_continue_down_days = temp_max_continue_down_days
                    temp_max_continue_down_days = 0
                if cur_change < 0 and not is_pre_down:
                    temp_max_continue_down_days = 1

            # 累计上涨或下跌百分点, 上涨为正数，下跌为负数
            change_percent = change_percent + cur_change

            # 大涨天数，超2%
            if cur_change > big_percent:
                big_up_days = big_up_days + 1
                big_last_continue_up_days = big_last_continue_up_days + 1
                big_last_change_up_percent = big_last_change_up_percent + cur_change
            else:
                big_last_continue_up_days = 0
                big_last_change_up_percent = 0.0

            # 大跌天数，超2%
            if cur_change < -big_percent:
                big_down_days = big_down_days + 1
                big_last_continue_down_days = big_last_continue_down_days + 1
                big_last_change_down_percent = big_last_change_down_percent + cur_change
            else:
                big_last_continue_down_days = 0
                big_last_change_down_percent = 0.0

            # 最大大涨天数，超2%
            if cur_change > big_percent and is_pre_big_up:
                temp_big_max_continue_up_days = temp_big_max_continue_up_days + 1
            else:
                if temp_big_max_continue_up_days > big_max_continue_up_days:
                    big_max_continue_up_days = temp_big_max_continue_up_days
                    temp_big_max_continue_up_days = 0
                if cur_change > big_percent and not is_pre_big_up:
                    temp_big_max_continue_up_days = 1

            # 最大大跌天数，超2%
            if cur_change < -big_percent and is_pre_big_down:
                temp_big_max_continue_down_days = temp_big_max_continue_down_days + 1
            else:
                if temp_big_max_continue_down_days > big_max_continue_down_days:
                    big_max_continue_down_days = temp_big_max_continue_down_days
                    temp_big_max_continue_down_days = 0
                if cur_change < -big_percent and not is_pre_big_down:
                    temp_big_max_continue_down_days = 1

            # 标识设置
            is_pre_up = cur_change > 0
            is_pre_down = cur_change < 0
            is_pre_big_up = cur_change > big_percent
            is_pre_big_down = cur_change < -big_percent

        # 最大值设置
        if temp_max_continue_up_days > max_continue_up_days:
            max_continue_up_days = temp_max_continue_up_days
        if temp_max_continue_down_days > max_continue_down_days:
            max_continue_down_days = temp_max_continue_down_days
        if temp_big_max_continue_up_days > big_max_continue_up_days:
            big_max_continue_up_days = temp_big_max_continue_up_days
        if temp_big_max_continue_down_days > big_max_continue_down_days:
            big_max_continue_down_days = temp_big_max_continue_down_days

        # 最近涨跌
        if last_continue_up_days > 0:
            last_continue_days = last_continue_up_days
        else:
            last_continue_days = -last_continue_down_days

        if last_change_up_percent > 0:
            last_change_percent = last_change_up_percent
        else:
            last_change_percent = last_change_down_percent

        # 最近大涨跌
        if big_last_continue_up_days > 0:
            big_last_continue_days = big_last_continue_up_days
        else:
            big_last_continue_days = -big_last_continue_down_days

        if big_last_change_up_percent > 0:
            big_last_change_percent = big_last_change_up_percent
        else:
            big_last_change_percent = big_last_change_down_percent

        analyse.up_days = up_days
        analyse.down_days = down_days
        analyse.max_continue_up_days = max_continue_up_days
        analyse.max_continue_down_days = max_continue_down_days
        analyse.last_continue_days = last_continue_days
        analyse.change_percent = change_percent
        analyse.last_change_percent = last_change_percent
        analyse.big_up_days = big_up_days
        analyse.big_down_days = big_down_days
        analyse.big_max_continue_up_days = big_max_continue_up_days
        analyse.big_max_continue_down_days = big_max_continue_down_days
        analyse.big_last_continue_days = big_last_continue_days
        analyse.big_last_change_percent = big_last_change_percent

        # 统计这一天的后几天涨跌情况
        after_1day_change_percent = 0.0
        after_2day_change_percent = 0.0
        after_3day_change_percent = 0.0
        after_5day_change_percent = 0.0
        after_7day_change_percent = 0.0
        after_10day_change_percent = 0.0
        after_15day_change_percent = 0.0
        after_30day_change_percent = 0.0
        after_list = stock_day_list[row_index + 1: row_index + 30]
        for after_index, after_row in after_list.iterrows():
            after_change = after_row["change_percent"]
            if after_index - row_index <= 1:
                after_1day_change_percent = after_3day_change_percent + after_change

            if after_index - row_index <= 2:
                after_2day_change_percent = after_3day_change_percent + after_change

            if after_index - row_index <= 3:
                after_3day_change_percent = after_3day_change_percent + after_change

            if after_index - row_index <= 5:
                after_5day_change_percent = after_5day_change_percent + after_change

            if after_index - row_index <= 7:
                after_7day_change_percent = after_3day_change_percent + after_change

            if after_index - row_index <= 10:
                after_10day_change_percent = after_10day_change_percent + after_change

            if after_index - row_index <= 15:
                after_15day_change_percent = after_10day_change_percent + after_change

            if after_index - row_index <= 30:
                after_30day_change_percent = after_30day_change_percent + after_change

        analyse.after_1day_change_percent = after_1day_change_percent
        analyse.after_2day_change_percent = after_2day_change_percent
        analyse.after_3day_change_percent = after_3day_change_percent
        analyse.after_5day_change_percent = after_5day_change_percent
        analyse.after_7day_change_percent = after_7day_change_percent
        analyse.after_10day_change_percent = after_10day_change_percent
        analyse.after_15day_change_percent = after_15day_change_percent
        analyse.after_30day_change_percent = after_30day_change_percent

        # print(analyse)
        analyse_list.append(analyse)

    return analyse_list
