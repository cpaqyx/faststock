import mplfinance as mpf
import pandas as pd
from sqlalchemy.orm import sessionmaker

from common.BaseService import BaseService
from datahub.entity.StockBasicInfo import StockBasicInfo


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
                `close` as `Close`, amount as `Volume` from stock_line_day 
                where ts_code ='{ts_code}' and trade_date >= '{start_date}' and trade_date < '{end_date}' order by trade_date asc; 
                """
        stock_list = pd.read_sql(sql, self.engine)
        stock_list.index = pd.DatetimeIndex(stock_list['Date'])

        # 自定义样式
        # 样式参考：https://github.com/matplotlib/mplfinance/blob/master/src/mplfinance/_styledata/binance.py
        my_color = mpf.make_marketcolors(up='red', down='green', volume='inherit')
        my_style = mpf.make_mpf_style(marketcolors=my_color, rc={'font.family': 'SimHei', 'font.size': '24'})
        # 绘制
        mpf.plot(stock_list, type='candle', style=my_style, figsize=(32, 16),
                 title='{}{}-{} K线图'.format(basic_info.name, start_date, end_date),
                 mav=mav, volume=True)


def main():
    # ChartTools().show_k_line("600036.SH", "20220001", "20221230", (5, 10, 30))
    ChartTools().show_k_line("中国铝业", "20220001", "20221230", (5, 10, 30))
    # ChartTools().show_k_line("中国铝业1", "20220001", "20221230", (5, 10, 30))


if __name__ == '__main__':
    main()
