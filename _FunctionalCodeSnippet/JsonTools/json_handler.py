# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/2 22:34
# @FileName : json_handler.py
# @SoftWare : PyCharm

import time
import json


class NpEncoder(json.JSONEncoder):
    """json序列化方法
    自定义继承于json.JSONEncoder的序列化方法 解决numpy数据格式引起的TypeError
    Extends:
        json.JSONEncoder
    Notes:
        如果json.dumps或json.loads转化ndarray类型数据，需函数参数中增加cls=NpEncoder
    """
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
    """将dict转化为json
    [description]
    Arguments:
        data_dict {[dict]} -- 字典格式的数据
    Keyword Arguments:
        encoder {[object]} -- 序列化对象 (default: {NpEncoder}),解决numpy数据格式引起的TypeError
    Returns:
        [type] -- [description]
    """
    data_json = json.dumps(data_dict, cls=encoder)
    return data_json


def dict_to_json_file(data_dict, json_file_name, cls_encoder=NpEncoder):
    """
    dict数据存储到json文件中
    json_file_name: user_information.json
    """
    with open(json_file_name, 'w') as f:
        json.dump(data_dict, f, cls=cls_encoder)


def data_receive_error_map(v):
    """数据接收过程错误码映射
    通过字典映射, 将错误int码映射为error code定义的字典格式
    Arguments:
        v {[int]} -- 错误int码
    Returns:
        [dict] -- 定义好的固定格式的error code
    """
    if v not in (0, 1, 2):
        print("Error: there is no matching error code defined, please double check when receiving data.")
        v = str(2)
    else:
        v = v if isinstance(v, str) else str(v)
    dictSeq = {'0': {"code": "0904000", "message": "OK:数据接收正常!", "source": "192.168.1.18", "timestap": int(time.time() * 1000)},
               '1': {"code": "0904001", "message": "ERROR:数据请求超时!", "source": "192.168.1.18", "timestap": int(time.time() * 1000)},
               '2': {"code": "0904002", "message": "ERROR:数据请求其他异常!", "source": "192.168.1.18", "timestap": int(time.time() * 1000)}
               }
    return dictSeq[v]