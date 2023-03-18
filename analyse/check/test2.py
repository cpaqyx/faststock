# from datetime import datetime
#
# import matplotlib.pyplot as plt
# import pytz
# import seaborn as sns
# import talib as ta
# from empyrical import cum_returns, annual_return, sharpe_ratio, max_drawdown
# from matplotlib.dates import DateFormatter
# from zipline import run_algorithm
# from zipline.api import symbol, order, record
# from zipline.finance import commission, slippage
#
#
# def initialize(context):
#     # 记录股票代码，通过股票代码获取股票对象
#     context.asset = symbol('AAPL')
#
#     # 定义是否买入股票的标记
#     context.invested = False
#
#     # 设置交易的手续费，股票成交时，手续费按成交金额一定比例收取
#     # 设置手续费率和最低费用
#     context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
#
#     # 设置模拟真实交易的滑价，当实际下单交易时，下单订单将影响市场。买单驱使价格上涨，卖单驱使价格下滑;
#     # 这通常被称为交易的“价格影响”。价格影响的大小取决于订单与当前交易量相比有多大。
#     context.set_slippage(slippage.VolumeShareSlippage(volume_limit=0.025, price_impact=0.1))
#
#
# def handle_data(context, data):
#     # 获取历史股票数据
#     # context.asset表示股票列表
#     # fields – 历史数据项或集合，项可以为’close’, ‘open’, ‘high’, ‘low’, ‘price’
#     # bar_count – 获取多少单位时间
#     # frequency – 可以取值‘1m’ 或 ‘1d’。 ‘1m’表示分钟单位, ‘1d’表示日单位, 现在只支持日单位
#     trailing_window = data.history(context.asset, ['high', 'low', 'close', 'open'], 40, '1d')
#
#     # 数据为空则返回
#     if trailing_window.isnull().values.any():
#     return
#
#     # 计算cci指标
#     cci = ta.CCI(trailing_window['high'].values, trailing_window['low'].values, trailing_window['close'].values,
#     timeperiod=14)
#
#     # 定义买入和卖出的标志位
#     buy = False
#     sell = False
#
#     if (cci[-1] >= 50) and not context.invested:
#     # 买卖股票，按股票数量生成订单，amount为负，表示做空。
#     # 参数:
#     # asset – 股票
#     # amount – 交易数量, 正数表示买入, 负数表示卖出
#     # style –（可选参数）指定下单类型，默认为市价单，可用的下单类型如下：
#     #   style=MarketOrder()，下市价单
#     #   style=StopOrder(stop_price)，下止损单，通常用来止损或者锁定利润
#     #   style=LimitOrder(limit_price)，下限价单，限定一个价格买入或卖出
#     #   style=StopLimitOrder(limit_price=price1, stop_price=price2)，指定限价和止损价格
#     order(context.asset, 100)
#     # 设置买入
#     context.invested = True
#     buy = True
#     elif (cci[-1] < 50) and context.invested:
#     order(context.asset, -100)
#     context.invested = False
#     sell = True
#
#     # 记录函数，在交易执行时记录用户自定义数据，该数据存放在回测输出结果中
#     record(open=data.current(context.asset, "open"),
#         high=data.current(context.asset, "high"),
#         low=data.current(context.asset, "low"),
#         close=data.current(context.asset, "close"),
#         cci=cci[-1],
#         buy=buy,
#         sell=sell)
#
#
# # 定义分析回测效果的函数
# def analyze(context=None, results=None):
#     pass
#
#
# def draw_return_rate_line(result):
#     sns.set_style('darkgrid')
#     sns.set_context('notebook')
#     ax = plt.axes()
#     # 设置时间显示格式
#     years_fmt = DateFormatter('%Y-%m-%d')
#     ax.xaxis.set_major_formatter(years_fmt)
#     # 让x轴坐标旋转45度
#     labels = ax.get_xticklabels()
#     plt.setp(labels, rotation=35, horizontalalignment='right')
#     # 画出收益率曲线
#     sns.lineplot(x='period_close',
#     y='algorithm_period_return',
#     data=result,
#     label="AAPL")
#     sns.lineplot(x='period_close',
#         y='benchmark_period_return',
#         data=result, label="SPX")
#
#     plt.legend(loc='upper left')
#     plt.title("return rate of AAPL and SPX")
#     plt.xlabel('time')
#     plt.ylabel('return rate')
#     plt.show()
#
#
# if __name__ == '__main__':
#     capital_base = 10000
#     start = datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc)
#     end = datetime(2017, 1, 1, 0, 0, 0, 0, pytz.utc)
#
#     # 运行算法
#     result = run_algorithm(start=start, end=end, initialize=initialize,
#         capital_base=capital_base, handle_data=handle_data,
#         bundle='quandl', analyze=analyze)
#
#     # 画出收益曲线图
#     draw_return_rate_line(result)
#
#     return_list = result['returns']
#
#     # 计算年化收益率
#     ann_return = annual_return(return_list)
#
#     # 计算累计收益率
#     cum_return_list = cum_returns(return_list)
#
#     # 计算sharp ratio
#     sharp = sharpe_ratio(return_list)
#
#     # 最大回撤
#     max_drawdown_ratio = max_drawdown(return_list)
#
#     print("年化收益率 = {:.2%}, 累计收益率 = {:.2%}, 最大回撤 = {:.2%}, 夏普比率 = {:.2f} ".format
#         (ann_return, cum_return_list[-1], max_drawdown_ratio, sharp))