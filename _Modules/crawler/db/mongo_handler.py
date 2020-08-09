# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/6 23:18
# @FileName : mongo_handler.py
# @SoftWare : PyCharm

"""
内置函数globals和locals分别返回全局名字空间,和本地名字空间字典.
    print(id(locals()))
    print(id(globals()))
"""
import os
import pprint

import pymongo

from config.logger import storage
from config.params import DB_CONFIGS
from utils.general import reg_pwd, status_mapper, md5_salt


class Mongo(object):

    def __init__(self):
        self.__dict__.update(**DB_CONFIGS)
        self.__init_client()

    def __init_client(self):
        # Client initialize
        self.client = pymongo.MongoClient('mongodb://{host}:{port}'.format(
            host=self.host, port=self.port))
        # Authentication
        self.db = self.client.admin
        pass_word = os.getenv("MONGO_PASSWORD")
        auth_status = self.db.authenticate(self.user, reg_pwd(pass_word))
        del pass_word
        storage.info("database authenticate: {}".format(status_mapper(auth_status)))
        if auth_status:
            self.db = self.client[self.db_name]
        return self

    def test_db(self):
        data = self.db['mycol2'].find()
        res = [item for item in data]
        pprint.pprint(res)
        return res


if __name__ == '__main__':
    mongo = Mongo()
    # print(mongo.__dict__)
    print(mongo.db)
    # mongo.find_data()
    mongo.test_db()
