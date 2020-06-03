# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/3 20:18
# @FileName : df_to_mysql.py
# @SoftWare : PyCharm

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from pymysql import ProgrammingError, DatabaseError
from attrdict import AttrDict

from _FunctionalCodeSnippet.DataBaseTools import conf_handler


class DataFrameToMysql:

    def __init__(self, db_type='mysql'):
        self.db_type = db_type

    def __init_db_conf(self):
        """
        Initial database config from rule_db.ini file based on given database type.
        """
        _handler = conf_handler.ConfigHandler()
        sections = _handler.get_sections
        if self.db_type not in sections:
            return None
        if self.db_type == 'mysql':
            cfg = AttrDict(_handler.mysql_conf)
        elif self.db_type == 'redis':
            cfg = AttrDict(_handler.redis_conf)
        # AttrDict 可以使用获取属性的方式访问字典
        elif self.db_type == 'sqlite':
            cfg = AttrDict(_handler.sqlite_conf)
        return cfg

    def __init_mysql_engine(self):
        """
        Initialize mysql engine.
        """
        params = self.db_conf
        eng = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
            user=params.user,
            password=params.password,
            host=params.host,
            port=params.port,
            database=params.database
        )
        try:
            engine = create_engine(eng, encoding='utf-8')
        except DatabaseError as err:
            print('Engine Initiation Error Occurred: ', err)
            # log.error('ERROR', err)
        return engine

    def df_to_mysql(self,
                    data_frame,
                    table_name,
                    conn=None,
                    exist_flag='replace'):
        """
        Transfer a DataFrame to mysql database.
        No need to build the table in db in advance.
        conn: default None, engine will be automatically called in function
        """
        if isinstance(data_frame, pd.DataFrame) \
                or isinstance(data_frame, pd.Series):
            if not conn:
                conn = self.__init_mysql_engine()
            try:
                data_frame.to_sql(table_name, conn, if_exists=exist_flag)
            except ProgrammingError as err:
                print('DataFrame To Mysql Error Occurred: ', err)
                # log.error('ERROR', err)
        else:
            raise TypeError(
                'DataFrame or Series is expected instead of {}'.format(
                    type(data_frame)))

    @property
    def db_conf(self):
        return self.__init_db_conf()


if __name__ == '__main__':
    obj = DataFrameToMysql('mysql')
    conf = obj.db_conf
    print(conf.keys(), conf.host, conf.user)
    df = pd.DataFrame(np.arange(1, 13).reshape((4, 3)),
                      columns=list('abc'))
    print(df)
    obj.df_to_mysql(df, 'numbers')
