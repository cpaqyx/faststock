from datetime import datetime

import mplfinance as mpf
import pandas as pd
from sqlalchemy.orm import sessionmaker

from common.base_service import BaseService
from common.common_util import cat_date
from model.StockBasicInfo import StockBasicInfo


class ChartTools(BaseService):
    def show_k_line(self, code_or_name, start_date, end_date, mav):
        # 获取股票基本信息
        db_session = sessionmaker(self.engine)
        session = db_session()
        basic_info = session.query(StockBasicInfo).filter(
            (StockBasicInfo.ts_code == code_or_name) | (StockBasicInfo.name.like('%{}%'.format(code_or_name)))).first()

        if basic_info is None:
            self.logger.info("{}找不到".format(code_or_name))
            return

        ts_code = basic_info.ts_code

        # 获取股票要展示记录
        sql = f"""
                select str_to_date(trade_date,'%%Y%%m%%d') as `Date`, `open` as `Open`, high as `High`, low as `Low`,
                case when open/close < 0.98 then close else null end as buy_flag,
                case when open/close > 1.03 then open else null end as sell_flag,
                `close` as `Close`, amount as `Volume` from stock_line_day
                where ts_code ='{ts_code}' and trade_date >= '{start_date}' and trade_date < '{end_date}' order by trade_date asc;
                """
        stock_list = pd.read_sql(sql, self.engine)
        stock_list.index = pd.DatetimeIndex(stock_list['Date'])

        # 自定义样式
        # 样式参考：https://github.com/matplotlib/mplfinance/blob/master/src/mplfinance/_styledata/binance.py
        my_color = mpf.make_marketcolors(up='red', down='green', volume='inherit')
        my_style = mpf.make_mpf_style(marketcolors=my_color, rc={'font.family': 'SimHei', 'font.size': '24'})

        # 在k线上添加买卖点
        # add_plot =
        # [mpf.make_addplot(stock_list['buy_flag'], type='scatter', markersize=120, marker='^', color='green')]

        # add_plot = [
        #     # mpf.make_addplot(stock_list[['Open', 'High']]),
        #         mpf.make_addplot(stock_list['buy_flag'], scatter=True, markersize=800, marker='^', color='blue'),
        #        mpf.make_addplot(stock_list['sell_flag'], scatter=True, markersize=800, marker='v', color='yellow')]

        # stock_list['buy_flag']:该值是显示的位置，应该同收盘价差不多，就会显示到当天的K线附近
        add_plot = [
            mpf.make_addplot(stock_list['buy_flag'], type='scatter', markersize=800, marker='^', color='g'),
            mpf.make_addplot(stock_list['sell_flag'], type='scatter', markersize=800, marker='v', color='r')]

        # 绘制
        mpf.plot(stock_list, type='candle', style=my_style, figsize=(45, 16),
                 title='{}{}-{} K线图'.format(basic_info.name, start_date, end_date),
                 mav=mav, volume=True, addplot=add_plot)


    def show_k_lines(self, code_or_name, start_date, option_flag='shape_v1', volume_show=False, end_date='', mav=(5,10,30)):
        # 获取股票基本信息
        db_session = sessionmaker(self.engine)
        session = db_session()
        basic_info = session.query(StockBasicInfo).filter(
            (StockBasicInfo.ts_code == code_or_name) | (StockBasicInfo.name.like('%{}%'.format(code_or_name)))).first()

        if basic_info is None:
            self.logger.info("{}找不到".format(code_or_name))
            return

        if end_date == '':
            end_date = datetime.strftime(datetime.now(), '%Y%m%d')

        ts_code = basic_info.ts_code

        cat_list = cat_date(start_date, end_date)
        for item in cat_list:
            start_date = item[0]
            end_date = item[1]

            table_name = 'stock_strategy_result'

            # 获取股票要展示记录
            sql = f"""
                select
                    str_to_date(LD.trade_date,'%%Y%%m%%d') as `Date`, 
                    LD.Open, LD.High, LD.Low, LD.Close, LD.amount as `Volume`,
                    SD.option_type, SD.option_flag, SD.sell_profit_percent, SD.option_price, SD.sell_order_cnt,
                    case when SD.option_type = 'buy' then SD.option_price end as buy_price,
                    case when SD.option_type = 'sell' then SD.option_price end as sell_price
                from
                    stock_line_day_qfq LD
                    left join (select * from {table_name} where ts_code = '{ts_code}' and option_flag='{option_flag}') SD on LD.ts_code = SD.ts_code and LD.trade_date = SD.option_date
                where
                    LD.ts_code = '{ts_code}' and LD.trade_date >= '{start_date}' and LD.trade_date <= '{end_date}'
                order by 
                    LD.trade_date asc;
            """

            stock_list = pd.read_sql(sql, self.engine)
            stock_list.index = pd.DatetimeIndex(stock_list['Date'])

            # 自定义样式
            my_color = mpf.make_marketcolors(up='red', down='green', volume='inherit')
            my_style = mpf.make_mpf_style(marketcolors=my_color, rc={'font.family': 'SimHei', 'font.size': '24'})

            # 防止全为空时，报错
            buys = stock_list[['buy_price']][stock_list['buy_price'] > 0]
            sells = stock_list[['sell_price']][stock_list['sell_price'] > 0]

            add_plot = []
            if buys.shape[0] > 0:
                add_plot.append(mpf.make_addplot(stock_list['buy_price'], type='scatter', markersize=800,
                                                 marker='^', color='g'))
            if sells.shape[0] > 0:
                add_plot.append(mpf.make_addplot(stock_list['sell_price'], type='scatter', markersize=800,
                                                 marker='v', color='r'))

            # 绘制
            mpf.plot(stock_list, type='candle', style=my_style, figsize=(45, 16),
                     title='{}{}-{} K线图'.format(basic_info.name, start_date, end_date),
                     mav=mav, volume=volume_show, addplot=add_plot)

def main():
    # ChartTools().show_k_line("600036.SH", "20220001", "20221230", (5, 10, 30))
    # ChartTools().show_k_lines("中国铝业", "20210101", "20221230", (5, 10, 30))
    # ChartTools().show_k_line("中国铝业1", "20220001", "20221230", (5, 10, 30))
    # ChartTools().show_k_line("中国铝业", "20210101")
    ChartTools().show_k_lines("002357.SZ", "20210101")


if __name__ == '__main__':
    main()
