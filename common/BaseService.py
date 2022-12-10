__author__ = 'fastwave'
# @Time : 2022/12/10 20:08
# @Author : fastwave 363642626@qq.com

import tushare as ts
from common.ConfigTool import DBSelector, config_dict
from loguru import logger


class BaseService(object):

    def __init__(self, logfile='../log/default.log'):
        # tushare
        ts_token = config_dict('ts_token')
        ts.set_token(ts_token)
        self.pro = ts.pro_api()

        # logger
        self.logger = logger
        self.logger.add(logfile)

        # db
        self.engine = DBSelector().get_engine()


if __name__ == '__main__':
    pass
