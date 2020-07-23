# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/7/22 22:23
# @FileName : test.py
# @SoftWare : PyCharm

import tornado.web
import tornado.ioloop


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *arg, **kwargs):
        self.write('hello world.')


# 创建application对象
app = tornado.web.Application([r'/', IndexHandler])

# 绑定监听端口
app.listen(6666)

#
tornado.ioloop.IOLoop.install().start()
