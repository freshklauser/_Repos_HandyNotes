# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/7/22 22:23
# @FileName : hello.py
# @SoftWare : PyCharm

"""
Tornado包括了一个有用的模块（tornado.options）来从命令行中读取设置
"""


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define('port', default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *arg, **kwargs):
        greeting = self.get_argument('greeting', 'Hello')
        location = self.get_argument('city', 'Shenzhen')
        self.write(greeting + ', friendly user! Here is ' + location)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r'/demo', IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    # http://127.0.0.1:8000/demo --> Hello, friendly user! Here is Shenzhen
    # http://127.0.0.1:8000/demo?greeting=Nice to meet you --> Nice to meet you, friendly user! Here is Shenzhen
    # TODO: 两个参数的url如何输入变量


