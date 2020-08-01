# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/7/26 22:22
# @FileName : utility.py
# @SoftWare : PyCharm

import numpy as np
import json


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


def dict_to_json(data_dict, encoder=NpEncoder):
    '''将dict转化为json

    [description]

    Arguments:
        data_dict {[dict]} -- 字典格式的数据

    Keyword Arguments:
        encoder {[object]} -- 序列化对象 (default: {NpEncoder}),解决numpy数据格式引起的TypeError

    Returns:
        [type] -- [description]
    '''
    data_json = json.dumps(data_dict, cls=encoder)
    return data_json
