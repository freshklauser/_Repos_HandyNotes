# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/4 22:55
# @FileName : exe_sql_file.py
# @SoftWare : PyCharm

import os
import pymysql
from pymysql import DatabaseError

try:
    db = pymysql.connect(user='root',
                         passwd='spindle123456',
                         host='192.168.13.129',
                         port=3306,
                         db='platform',
                         charset='utf8')
    c = db.cursor()

    with open('newboy.sql', 'r+') as f:
        sql_list = f.read().split(';')[:-1]  # sql文件最后一行加上;
        sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
        print(sql_list)

    for sql_item in sql_list:
        print(sql_item)
        c.execute(sql_item)
except DatabaseError as err:
    print(err)
finally:
    c.close()
    db.commit()
    db.close()