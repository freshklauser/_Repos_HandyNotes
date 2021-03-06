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
        """ 获取配置参数所有 sections """
        return self.parser.sections()

    def get_options(self, section):
        """ 获取配置参数中指定 section 下的 key """
        return self.parser.options(section)

    @property
    def get_http(self):
        """ 获取配置参数的 "http" 下的 key """
        return self.get_options('http')

    @property
    def get_db_table(self):
        """ 获取配置参数的 'db_table' 下的 key """
        return self.get_options('db_table')

    @property
    def get_mysql(self):
        """ 获取配置参数的 'mysql' 下的 key """
        return self.get_options('mysql')

    @property
    def mysql_conf(self):
        """ 获取配置参数 'mysql' 的元组 (key, value) """
        return self.parser.items('mysql')

    @property
    def redis_conf(self):
        """ 获取配置参数 'mysql' 的元组 (key, value) """
        return self.parser.items('redis')

    @property
    def sqlite_conf(self):
        """ 获取配置参数 'sqlite3' 的元组 (key, value) """
        return self.parser.items('sqlite3')


class SqliteHandler:
    REFER = 'https://blog.csdn.net/qq_40302523/article/details/86252919'

    # TODO-2: dataframe 写入 .db 的封装类
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
    print(obj.get_mysql, '===')
    print(obj.mysql_conf)
    print(obj.sqlite_conf)
    # TODO-1: refer https://blog.csdn.net/songlh1234/article/details/83316468?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-4
    print()

