# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/3 0:05
# @FileName : demo_sync.py
# @SoftWare : PyCharm

import time, asyncio

from utils.SpindleJsonCreation import SpindleJsonCreation
from utils.SpindleRealTimeAnalysis import SpindleRealTimeAnalysis


def data_to_json(index):
    data = SpindleRealTimeAnalysis().get_data(index)
    SpindleJsonCreation().save_local_json(data)
    print('to json success')


def offline_main_index(index):
    # 离线数据测试
    data = SpindleRealTimeAnalysis().get_data(index)
    print(data.keys())
    print('get data success')
    return data


def do_work(x):
    print('waitting:', x)
    time.sleep(x)
    return 'Don after {}s'.format(x)


start = time.time()
do_work(1)
do_work(8)
do_work(2)
offline_main_index(10)
data_to_json(3)
print('TIME:', time.time()-start)


# 同步
# waitting: 1
# waitting: 8
# waitting: 2
# dict_keys(['module', 'machineip', 'topic', 'infos', 'times', 'freqs', 'ecode'])
# get data success
# to json success
# TIME: 16.277764320373535
