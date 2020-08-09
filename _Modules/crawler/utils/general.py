# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/8 14:52
# @FileName : general.py
# @SoftWare : PyCharm


import hashlib
import json
import numpy as np
import os
import re
import secrets
import uuid


def standard_path(root, relative_path):
    return os.path.realpath(os.path.join(root, relative_path))


def reg_pwd(s):
    tmp = re.search(r"(.*http:\/\/)(.*#)(.*)#.*#", s)[3]
    res = re.findall(r"(?![lujynx])(?![\W])\w", tmp)
    return ''.join(res)


def md5_salt(password, salt=None):
    """
    暂时用不上，纯测试代码的函数
    salt不指定的话默认为32, 每次都是随机生成
    secrets.token_hex: Return a random text string, in hexadecimal
    :param password:
    :param salt: int or None(default redirct to 32)
    :return:
    """
    if salt is None or not isinstance(salt, int):
        salt = secrets.token_hex(32)
    else:
        salt = secrets.token_hex(salt)
    password = str(password + salt).encode()
    m = hashlib.md5(password)
    return m.hexdigest()


def generate_uuid(name, namespace=uuid.NAMESPACE_DNS):
    return uuid.uuid5(namespace, name).hex


def generate_document(brand, model):
    name = brand + ':' + model
    uuid = generate_uuid(name)
    return {'uuid': uuid, 'brand': brand, 'model': model}


def status_mapper(status):
    status = bool(status)
    return "SUCCESS" if status else "FAILED"


class NpEncoder(json.JSONEncoder):
    """
    json序列化方法
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


if __name__ == '__main__':
    job_id = generate_uuid(os.path.dirname(__file__))
    print(job_id, type(job_id))
    print(type(secrets.token_hex(31)))
    # res = md5_salt('asd')
    # print('--', res)    # fcf9d987db0f12ad05476246a9bfa1f0

    res = md5_salt('asd')
    res1 = md5_salt('asd')
    print(res == res1)
