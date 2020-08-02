# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/1 22:02
# @FileName : main.py
# @SoftWare : PyCharm


import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options, parse_command_line

from views.server import MonitorHandler

define('port', default=8090, type=int, help="define the port with a default value")


# TODO: 可参考github上的方式，定义一个类, tornado.web.Application.__ini__(self, application, **setting)
def make_app():
    return tornado.web.Application(handlers=[
        (r'/monitor/', MonitorHandler)
    ])


def start():
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


start()