# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/6 23:18
# @FileName : motor_handler.py
# @SoftWare : PyCharm

"""
异步mongodb
    core.py: motor的核心api
    cursor.py: api 查询 pymongo
    (1) 查询一个文档（find_one）-- find_one 需要异步 awaite, 没有 sort方法
        使用 find_one() 得到匹配查询的第一个文档。例如，要获取密钥“i”的值小于1的文档：
        async def do_find_one():
            document = await db.test_collection.find_one({'i': {'$lt': 1}}) # find_one只能查询一条数据
    (2) 查询多个文档（find） -- find 不需要异步， 有sort
        使用 find() 要查询的一组文档。 find() 没有I / O，也不需要 await 表达式。它只是创建一个 AsyncIOMotorCursor 实例。
        当您调用 to_list() 或为循环执行异步时 (async for) ，查询实际上是在服务器上执行的。
        async def do_find():
            cursor = db.test_collection.find({'i': {'$lt': 5}}).sort('i')
            for document in await cursor.to_list(length=100):
            pprint.pprint(document)

    dir(__cursor):
        ['add_option', 'address', 'alive', 'batch_size', 'clone', 'close', 'closed', 'collation', 'collection',
        'comment', 'cursor_id', 'delegate', 'distinct', 'each', 'explain', 'fetch_next', 'get_io_loop', 'hint',
        'limit', 'max', 'max_await_time_ms', 'max_scan', 'max_time_ms', 'min', 'next_object', 'remove_option',
        'rewind', 'session', 'skip', 'sort', 'started', 'to_list', 'where']
"""


import asyncio
import os
import pprint

from motor.motor_asyncio import AsyncIOMotorClient

from config.logger import storage
from config.params import DB_CONFIGS, MAX_DOCS_RETURN
from utils.general import reg_pwd, status_mapper


class MotorBase(object):

    def __init__(self):
        self.__dict__.update(**DB_CONFIGS)
        # Client initialize
        pass_word = reg_pwd(os.getenv("MONGO_PASSWORD"))
        self.__motor_uri = "mongodb://{user}:{password}@{host}:{port}".format(
            user=self.user, password=pass_word, host=self.host, port=self.port
        )
        del pass_word
        self.client = AsyncIOMotorClient(self.__motor_uri)
        self.db = self.client[self.db_name]

    async def do_query_many(self, collection, query=None, projection=None, sortby=None):
        """
        to_list(length): maximum number of documents to return for this call
        :param collection:
        :param query:
        :param projection:
        :param sortby:
        :return: <class 'motor.motor_asyncio.AsyncIOMotorCursor'>
        """
        __cursor = self.db[collection].find(query, projection).sort(sortby)
        # 两种查询结果的方式
        async_data = [item async for item in __cursor]
        # async_data = [item for item in await __cursor.to_list(length=MAX_DOCS_RETURN)]
        # print(type(__cursor))       # <class 'motor.motor_asyncio.AsyncIOMotorCursor'>
        for item in async_data:
            print(item)
        return async_data

    async def do_insert_many(self, collection, documents):
        try:
            result = await self.db[collection].insert_many(documents)
        except (KeyboardInterrupt, NotImplementedError) as err:
            storage.error('[ERROR] data insert failed.', exc_info=True, stack_info=True)
        else:
            storage.info('status: {}'.format(result.acknowledged))
        return result

    async def clear(self):
        """ 清空collection """
        pass


if __name__ == '__main__':
    # _args = ('mycol2', {}, {"name": 1, '_id': 0, "age": 1}, [('age', 1), ("name", -1)])
    # _args = ('mycol2', None, {'_id': 0}, [('age', -1), ("name", 1)])
    docs = [{'name': 'b', 'age': 18, 'gender': 0}, {'name': 'c', 'age': 28, 'gender': 1}]
    _args = ('mycols', docs)
    motor = MotorBase()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(motor.do_insert_many(*_args))
