# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/2 0:05
# @FileName : conf_handler.py
# @SoftWare : PyCharm

import os
import configparser
import sqlite3


class ConfigHandler:
    DB_CONF_NAME = 'rule_db.ini'

    def __init__(self):
        """
        初始化参数,
        cur_path: main程序所在的路径
        """
        self.cur_path = os.path.realpath(os.getcwd())
        self.cfg_path = os.path.join(self.cur_path, self.DB_CONF_NAME)
        # 创建管理对象
        self.parser = configparser.ConfigParser()
        # 读取配置文件
        self.parser.read(self.cfg_path, encoding='utf-8')

    @property
    def get_sections(self):
        return self.parser.sections()

    def get_options(self, section):
        return self.parser.options(section)

    @property
    def get_http(self):
        return self.get_options('http')

    @property
    def get_db_table(self):
        return self.get_options('db_table')


class SqliteHandler:

    def __init__(self, db_path):
        """
        初始化参数，创建数据库连接
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()


if __name__ == '__main__':
    obj = ConfigHandler()
    print(obj.get_sections)     # ['sqlite3', 'mysql', 'db_table', 'http']
    print(obj.get_options('sqlite3'))
    print(obj.get_http)
    print(obj.get_db_table)
