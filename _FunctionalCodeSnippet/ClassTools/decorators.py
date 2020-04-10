# -*- coding: utf-8 -*-
# @Author: sniky-lyu
# @Date:   2020-04-09 23:00:03
# @Last Modified by:   KlausLyu
# @Last Modified time: 2020-04-10 17:31:40

'''decorator tools
'''

import sys
import time
import datetime
from functools import wraps


class tracer:
    '''独立函数调用次数计数器
    Sample goes to person.py
    '''

    def __init__(self, func):
        self.call = 0
        self.func = func

    def __call__(self, *args, **kwargs):
        self.call += 1
        print("Function '{}' is called {} times".format(self.func.__name__, self.call))
        self.func(*args, **kwargs)


def decorator_timmer(func):
    '''计时装饰器: 监控函数运行时间
    [对 类函数 或 独立函数 计时监控，输出msg到file中，print函数实现]
    Arguments:
        func {[object]} -- [需要监控的函数]
    Tips:
        TODO 部分，可自定义实现log日志采集
    Returns:
        [wrapper] -- [description]
    '''
    # @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        res = func(*args, **kwargs)
        time_consumed = time.perf_counter() - t1

        'TODO: 输出函数运行时间信息至 console 或 file, 或传入自定义的logger,写入logger.info(xxx)'
        msg = "< Timestamp:{:.0f}(ms),\ttime-consumed: {:.4f}(s) for function '{}' >\n ".format(
                    time.time()*1000,
                    time_consumed,
                    func.__name__)
        file = 'log-{}.txt'.format(datetime.datetime.today().strftime('%Y%m%d'))
        print(msg, file=open(file, 'a'))
        print(res, '~~~~~~~~~~')
        return res
    return wrapper


if __name__ == '__main__':
    class Spam:
        def __init__(self, nums):
            self.nums = nums

        # @tracer
        @decorator_timmer
        def spam(self):
            time.sleep(0.2258369)
            print(self.nums)

    @tracer             # 只针对独立函数有效
    @decorator_timmer
    def sum_ab(a, b):
        time.sleep(0.2210)
        return a ** 2 + a * b + b ** 2

    # a = decorator_timmer(sum_ab(11, 22))
    # print('a: ', a.__name__)

    res = sum_ab(3,6)
    print(type(res))
    'TODO: 返回的res到底是个啥，返回的不是 计算结果，显然是有问题'
    '问题：添加了decorator之后，返回的类型都是 NoneType， 不是预期的结果'
    print(res, '-----+++++++++++++++++')
    # nums = [1, 2, 3, 4]
    # cl = Spam(nums)
    # cl.spam()

