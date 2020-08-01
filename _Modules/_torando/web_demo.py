# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/7/26 19:33
# @FileName : web_demo.py
# @SoftWare : PyCharm


import json
import os
from typing import Awaitable, Optional

import pymysql
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

from tornado.options import define, options

from utility import NpEncoder

define('port', default=3306, type=int, help="run on the given port")


class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])


class StudentsHandler(tornado.web.RequestHandler):
    def initialize(self):
        """ 初始化，会在http行为方法前自动调用 """
        self.conn = pymysql.connect(host='192.168.13.130',
                                    port=3306,
                                    user='root',
                                    password='asd123456',
                                    database='stu_manager')
        self.cursor = self.conn.cursor()
        print('initialize')

    def prepare(self) -> Optional[Awaitable[None]]:
        """ 调用请求处理（`get、post`等）方法之前的资源预处理等操作 """
        sql = 'select * from students'
        sql_desc = 'desc students'
        self.cursor.execute(sql_desc)
        cols_info = self.cursor.fetchall()
        cols = [item[0] for item in cols_info][:-1]

        self.cursor.execute(sql)
        stu_info = self.cursor.fetchall()
        students = []

        # TODO: 将数据库转化为字典，然后通过json序列化进行网络传输
        # for item in stu_info:
        #     item = bytes(str(item), encoding='utf-8')
        #     print(item)
        #     for col, value in item:
        #         print(col, '-->', str(value))
        # print(students)
        # students_dict = {item[0]: list(item[1:]) for item in students}
        # students_json = json.dumps(students_dict, cls=NpEncoder)
        # print(type(students_json), students_json)
        print('prepare')

    def get(self):
        self.write(str(self.students_info[0][1]).encode('utf-8'))
        print('get method')

    def on_finish(self):
        self.conn.close()
        print("on-finish")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # 模板渲染
        self.render('index.html')


class BookHandler(tornado.web.RequestHandler):
    def get(self):
        # 模板渲染
        self.render(
            'book.html',
            title='Home Page',
            header='Books recommended',
            books=[
                "Learning Python",
                "macs",
                "Programming Collective Intelligence",
                "Restful Web Services"
            ]
        )


def make_app():
    return tornado.web.Application(
        handlers=[
            # 如有地址
            (r'/reverse/(\w+)', ReverseHandler),
            (r'/students/', StudentsHandler),
            (r'/index/', IndexHandler),
            (r'/books/', BookHandler)
        ],
        # 模板路径
        template_path=os.path.realpath(os.path.join(os.getcwd(), 'templates'))
    )


def start():
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    start()
