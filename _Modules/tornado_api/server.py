# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/1 22:12
# @FileName : main.py
# @SoftWare : PyCharm

import numpy as np
import json
import tornado.gen
import tornado.web

from utils.SpindleRealTimeAnalysis import SpindleRealTimeAnalysis
from utils.utility import NpEncoder


class MonitorHandler(tornado.web.RequestHandler):
    def get(self):
        # self.set_header("Cache-Control", "no-cache, must-revalidate")
        # self.set_header("Expires", "Mon, 26 Jul 1997 05:00:00 GMT")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        monitor_data = SpindleRealTimeAnalysis().offline_main()
        self.write(json.dumps(monitor_data, cls=NpEncoder))


# class AsyncMonitorHandler(tornado.web.RequestHandler):
    # # TODO: 还未定义
    # @tornado.web.asyncchronous
    # @tornado.gen.coroutine
    # def get(self):
        # self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # monitor_data = SpindleRealTimeAnalysis().offline_main()
        # self.write(json.dumps(monitor_data, cls=NpEncoder))


class NpEncoder(json.JSONEncoder):
    '''json序列化方法
    自定义继承于json.JSONEncoder的序列化方法 解决numpy数据格式引起的TypeError
    Extends:
        json.JSONEncoder
    Notes:
        如果json.dumps或json.loads转化ndarray类型数据，需函数参数中增加cls=NpEncoder
    '''

    def default(self, obj):
        import datetime
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        else:
            return super(NpEncoder, self).default(obj)