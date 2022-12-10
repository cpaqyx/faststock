__author__ = 'fastwave'
# @Time : 2022/12/10 20:08
# @Author : fastwave 363642626@qq.com

import datetime
import time
from common.BaseService import BaseService


class SyncStockBasic(BaseService):

    def sync_stock_basic_info(self, retry=5):
        # 需要添加异常处理 重试次数
        count = 0
        df = None
        while count < retry:
            try:
                df = self.pro.stock_basic(exchange='', list_status='', fields='')
            except Exception as e:
                self.logger.info(e)
                time.sleep(10)
                count += 1
                continue
            else:
                break

        if count == retry:
            self.notify(title=f'{self.__class__.__name__}获取股市基本数据失败')
            exit(0)

        if df is not None:
            df = df.reset_index(drop=True)
            df.rename(columns={'symbol': 'code'}, inplace=True)
            df['update_date'] = datetime.datetime.now()

            try:
                df.to_sql('stock_basic_info', self.engine, if_exists='replace')

            except Exception as e:
                self.logger.error(e)
                self.notify(title=f'{self.__class__}mysql入库出错')

        self.notify(title=f'{self.__class__.__name__}获取股市基本数据成功')

    def notify(self, title):
        pass


def main():
    obj = SyncStockBasic()
    obj.sync_stock_basic_info()


if __name__ == '__main__':
    main()
