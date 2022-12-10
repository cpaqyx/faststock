__author__ = 'fastwave'
# @Time : 2022/12/10 20:08
# @Author : fastwave 363642626@qq.com

import os
import json
from sqlalchemy import create_engine

DEFAULT_DB_TYPE = 'mysql'
DEFAULT_DB_NAME = 'fast_stock'


def get_config_data(config_file='../configure/config.json'):
    json_file = os.path.join(os.path.dirname(__file__), config_file)
    with open(json_file, 'r', encoding='utf8') as f:
        _config = json.load(f)
        return _config


config = get_config_data()


def config_dict(*args):
    result = config
    for arg in args:
        try:
            result = result[arg]
        except Exception as e:
            print(e)
            print('找不到对应的key')
            return None

    return result


class DBSelector(object):
    # 数据库选择类
    def __init__(self):
        self.json_data = config

    def config(self, db_type, db_name):
        db_dict = self.json_data[db_type][db_name]
        user = db_dict['user']
        password = db_dict['password']
        host = db_dict['host']
        port = db_dict['port']
        return user, password, host, port

    def get_engine(self, db_type, db_name):
        return self.get_engine(db_type, db_name)

    def get_engine(self):
        user, password, host, port = self.config(DEFAULT_DB_TYPE, DEFAULT_DB_NAME)
        try:
            engine = create_engine(
                'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(user, password, host, port, DEFAULT_DB_NAME))
        except Exception as e:
            print(e)
            return None
        return engine

    def get_mysql_conn(self, db_type=DEFAULT_DB_TYPE, db_name=DEFAULT_DB_NAME):
        import pymysql
        user, password, host, port = self.config(db_type, db_name)
        try:
            conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db_name, charset='utf8')
        except Exception as e:
            print(e)
            return None
        else:
            return conn


if __name__ == '__main__':
    pass
