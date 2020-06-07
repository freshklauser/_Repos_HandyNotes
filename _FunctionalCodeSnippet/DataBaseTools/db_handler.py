# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/4 20:49
# @FileName : db_handler.py
# @SoftWare : PyCharm

"""
TODO:
    mysql常见可空数据类型：  varchar, time
           不可空数据类型： int, float, date, datetime
    sql语句太长可以用括号括起来，然后分行显示
"""


import sys
import datetime
import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from pymysql import ProgrammingError, DatabaseError
from attrdict import AttrDict

from _FunctionalCodeSnippet.DataBaseTools import conf_handler


class DatabaseHandler:
    """
    FIXME:
        0) mysql中定义好类型之后，dataframe中除了数值型，都可以直接用str 即 object 类型，上传后会自动按照msyql的类型解读
           但如果mysql中定义的date或datetime类型数据在dataframe中为object，则必须对其进行空值填充处理
           如果mysql中日期类数据为空时希望显示空，则需在mysql中指定字段类型为 VARCHAR
        1）pymysql的占位符是 %s； sqlite的占位符是？
        2）Date 类型的占位符如何表示：直接 %s 或者 str_to_date(%s,'%%Y-%%m-%%d')
            前提: 列表或tuple中的Date类型数据为 str 格式化的日期 2020-01-02 规范格式
            错误示例： 2020.01.02(格式错误) 或者 2020.01(不完整，格式错误) 或者 2020-01(不完整)
        3）不管是 DataFrame 的类型转换 还是 mysql 的数据写入，都不能有空值，需要空值填充
           空值处理：
              (1) str： 不处理，可直接上传数据库
              (2) int or float: 空值需填充预设值，否则 df 类型转换 或 mysql 数据上传均会报错
              (3) Date or Datetime：
                    按照 mysql 对这些类型的格式要求对空值填充预设值，比如 Date 格式 2020-06-05
                  Time: 空值会自动填充 00：00：00， 不需要手动填充
        4）DataFrame或ndarray均无法直接逐行按1维数据写入mysql, 都需要先转化为 list 或 tuple 后采用传参的形式写入
    """

    def __init__(self, db_type='mysql'):
        self.db_type = db_type
        self._conn = None
        self._cursor = None
        self.conn_status = 0

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

    def connect(self):
        params = self.db_conf
        _kwargs = dict(host=params.host,
                       port=int(params.port),
                       user=params.user,
                       passwd=params.passwd,
                       db=params.db,
                       charset=params.charset)
        print(_kwargs)
        try:
            self._conn = pymysql.connect(**_kwargs)
        except DatabaseError as err:
            print("------------------ CONNECTION FAILURE --------------------")
            print('Connect Error Occurred: ', err)
            # log.error('ERROR', err)
        else:
            self.conn_status = 1
            self._cursor = self._conn.cursor()
            print("------------------ CONNECTION SUCCESS --------------------")

    def close(self):
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()
        return True

    def query(self, sql_qry):
        # TODO:
        #  查询需要在 cursor.execute 后 通过 cursor.fetchall 获取所有数据
        #  插入需要在 execute 后执行 conn.commit() 操作

        if not self._conn:
            self.connect()
        try:
            self._cursor.execute(sql_qry)
            # self._conn.commit()
            res = self._cursor.fetchall()
        except ProgrammingError as err:
            print('Execute({}) Error Occurred: {}'.format(
                sys._getframe().f_code.co_name,
                err))
            # log.error('ERROR', err)
        return res

    def insert(self, sql_qry, args):
        """
        注意事项：
            在将 DataFrame 进行插入之前，必须对空值进行处理，mysql 中如果插入字段为空，会报错如下：
            eg.: pymysql.err.DataError: (1265, "Data truncated for column 'weight' at row 1")
                 即 行1中字段`weight`数据为空
        TODO:
            查询需要在 cursor.execute 后 通过 cursor.fetchall 获取所有数据
            插入需要在 execute 后执行 conn.commit() 操作
        """
        if not self._conn:
            self.connect()
        try:
            self._cursor.execute(sql_qry, args)
        except ProgrammingError as err:
            print('Execute({}) Error Occurred: {}'.format(
                sys._getframe().f_code.co_name,
                err))
            raise
            # log.error('ERROR', err)
        try:
            self._conn.commit()
        except ProgrammingError as err:
            print('Commit({}) Error Occurred: {}'.format(
                sys._getframe().f_code.co_name,
                err))
            self._conn.callback()
            # log.error('ERROR', err)
            raise

    def excute_sql_file(self, sql_file):
        pass

    @property
    def db_conf(self):
        return self.__init_db_conf()


if __name__ == '__main__':
    handler = DatabaseHandler('mysql')
    conf = handler.db_conf
    print(conf.keys(), conf.host, conf.user)
    # sql = """CREATE TABLE `platform`.`student` (
    #           `seq` INT NOT NULL,
    #           `num` INT NULL,
    #           `age` INT NULL,
    #           `name` VARCHAR(45) NULL,
    #           `friend` VARCHAR(45) NULL,
    #           time DATE NULL,
    #           PRIMARY KEY (`seq`))
    #         ENGINE = InnoDB
    #         DEFAULT CHARACTER SET = utf8;"""
    # handler.execute(sql)

    # df = pd.DataFrame(np.arange(601, 613).reshape((4, 3)),
    #                   columns=list('abc'))
    # # print(df)
    # tm = pd.DataFrame(['2020-06-01', '2020-06-02', '2020-06-03', '2020-06-04'], columns=['f'])
    # print(tm, '---------------------++++++++++++++++++++++++')
    # tmp = pd.DataFrame([['age', 'as'], ['tom', 'tim'], ['hi', 'she'], [
    #                    'she', 'iet']], columns=['d', 'e'])
    # tmp = pd.concat([df, tmp, tm], axis=1)
    # print(tmp)
    # # print(tmp.dtypes)
    # # obj.df_to_mysql(tmp, 'student')
    #
    # # 逐行读取dataframe数据，写入mysql
    # # for i, row in tmp.iterrows():
    # #     print(row)
    # #     break
    #
    # # list 写入 mysql
    # print('==' * 20)
    # res = handler.query('select * from student')
    # print(res)
    # df_to_list = tmp.to_numpy().tolist()
    # # print(tmp.to_numpy().tolist())
    # # FIXME: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # #  利用占位符传递参数。这里要注意，无论整数、字符串，占位符都为 %s，且不需加引号。
    # #  日期格式的数据，占位符 也是 %s ,也可以str_data(%s, '%%Y-%%m-%%d')
    # # sql = "INSERT INTO student(seq, num, age, name, friend) VALUES (%s, %s, %s, %s, %s)"
    # # sql = "INSERT INTO student(seq, num, age, name, friend, times) VALUES (%s, %s, %s, %s, %s, %s)"
    # sql = "INSERT INTO student(seq, num, age, name, friend, times) VALUES (%s, %s, %s, %s, %s, str_to_date(%s,'%%Y-%%m-%%d'))"
    # for item in df_to_list:
    #     # args = tuple(item[:-1])         # OK, tuple传参
    #     # args = item[:-1]                # OK, list传参
    #     args = item                       # Date类型数据的占位符 %s 或 str_to_date(%s, "%%Y-%%m-%%d"), Datetime的改成相应的string格式
    #     handler.insert(sql, args)
    #     # break

    # for i in range(tmp.shape[0]):
    #     row = tmp.iloc[i, :]            # DataFrame 和 ndarray 都不能直接写入，需要转化为 list 或 tuple 后再写入
    #     print(tuple(row.values.tolist()), type(tuple(row.values.tolist())), type(row.values.tolist()[3]))
    #     args = row[:-1].values
    #     print(args, type(row[:-1]), type(row[:-1].values), type(args))
    # handler.insert(sql, args)


    # ======================================= write to msyql ==========================================
    new_df = pd.DataFrame([[44, 'qqq', 35.2, '2020-06-03', '2020-06-04 12:12:12'],
                           [25, 'aaa', 57.2, '2020-06-05', '2020-06-06 12:12:12']],
                          columns=['age', 'name', 'grade', 'dates', 'times'])
    print(new_df)
    sql = "INSERT INTO newboy(age, name, grade) VALUES (%s, %s, %s)"
    new_list = new_df.to_numpy().tolist()
    for item in new_list:
        args = item[:-2]
        print(args)
        handler.insert(sql, args)       # ok, 占位符全部用 %s 即可
    #
    # tb_name = 'newboy'
    # # TODO: 换行必须每行都用 引号.
    # #        table 也传参，虽然能写入数据库，但会报错 ProgrammingError
    # sql = "INSERT INTO `newboy`(age, name, grade, dates, times) VALUES " \
    #               "(%(age)s, %(name)s, %(grade)s, %(dates)s, %(times)s)"
    # new_list = new_df.to_numpy().tolist()
    # for item in new_list:
    #     args = {'age': item[0],
    #             'name': item[1],
    #             'grade': item[2],
    #             'dates': item[3],
    #             'times': item[4]}
    #     print(args)
    #     handler.insert(sql, args)
