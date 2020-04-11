# -*- coding: utf-8 -*-
# @Author: sniky-lyu
# @Date:   2020-04-09 23:00:03
# @Last Modified by:   sniky-lyu
# @Last Modified time: 2020-04-11 21:21:58

'''decorator tools
---> 需要根据自己的业务逻辑和需求来定义符合自己要求的装饰器
---> 优先建议使用 类装饰器
---> 场景： 日志打印，用户授权，运行计时等
---> 类装饰器使用： @decorator_class()   ----- ()不能少， 装饰实例

装饰器 = 高阶函数 + 嵌套函数
高阶函数：以函数作为参数的函数，返回值仍是函数
嵌套函数：在函数里面定义函数
'''

# import sys
import time
import datetime
from functools import wraps
from classtools import create_directory

'<-------------------------------- 类装饰器 ----------------------------------->'


class decor_tracer:
    '''函数调用次数计数器 （类装饰器 -- 包裹函数带参数风格写法）
    类的装饰器写法 -- 带参数

    <-- Tips--Anthoer style of class-decorator as below:
    类的装饰器写法---不带参数

    class decor_tracer:
        def __init__(self, func):
            self.call = 0
            self.func = func

        def __call__(self, *args, **kwargs):
            self.call += 1
            print("Function '{}' was called {} times".format(self.func.__name__, self.call))
            return self.func(*args, **kwargs)

    相对而言，不推荐Tips中的这种写法，无法使用wraps修复技术，返回的函数结构发生变化
    比如 程序中执行 sum_ab.__name__出错--!>
    '''

    def __init__(self):
        self.call = 0

    def __call__(self, func):
        print("Decorator '%s' is running" % self.__class__.__name__)

        @wraps(func)
        def inner(*args, **kwargs):
            self.call += 1
            print("Function '{}' is running within decorator '{}'.".format(func.__name__, self.__class__.__name__))
            print("Function '{}' was called {} times".format(func.__name__, self.call))
            return func(*args, **kwargs)
        return inner


class decor_logitimmer:
    '''运行计时和日志输出装饰器 （类装饰器）-- 包裹函数带参数的类装饰器
    类的装饰器写法 -- 带参数
    '''

    def __init__(self, log_prefix='log-', log_suffix='.log', log_dir='logs/'):
        '''
        Keyword Arguments:
            log_prefix {str} -- [输出日志文件的前缀] (default: {'log-'})
            log_suffix {str} -- [输出日志文件的后缀] (default: {'.log'})
            log_dir {str}    -- [输出日志文件所在的目录] (default: {'logs/'})
        Tips:
            log_dir 需要在主程序初始化的时候直接判断生成，这里默认已经创建好
        '''
        self.log_prefix = log_prefix
        self.log_suffix = log_suffix
        self.log_dir = log_dir

    def __call__(self, func):
        print("Decorator '%s' is running" % self.__class__.__name__)
        today_string = datetime.datetime.today().strftime('%Y%m%d')
        log_file = self.log_dir + self.log_prefix + today_string + self.log_suffix

        @wraps(func)
        def inner(*args, **kwargs):
            print("Function '{}'' is running within decorator '{}'.".format(func.__name__, self.__class__.__name__))
            t1 = time.perf_counter()
            res = func(*args, **kwargs)
            time_consumed = time.perf_counter() - t1

            'TODO<klaus-20190411>: output to log file, 或传入自定义的logger, 如写入logger.info(xxx)'
            msg = "< Timestamp:{:.0f}(ms),\ttime-consumed: {:.4f}(s) for function '{}' >\n ".format(
                time.time() * 1000,
                time_consumed,
                func.__name__)
            print(msg, file=open(log_file, 'a'))

            return res
        return inner


'<-------------------------------- 函数装饰器 ----------------------------------->'


def decorator_timmer(func):
    '''函数装饰器--计时装饰器: 监控函数运行时间
    [对 类函数 或 独立函数 计时监控，输出msg到file中，print函数实现]
    Arguments:
        func {[object]} -- [需要监控的函数]
    Tips:
        TODO 部分，可自定义实现log日志采集
    Returns:
        [wrapper] -- [description]
    '''
    @wraps(func)
    def inner(*args, **kwargs):
        t1 = time.perf_counter()
        res = func(*args, **kwargs)
        time_consumed = time.perf_counter() - t1

        'TODO: 输出函数运行时间信息至 console 或 file, 或传入自定义的logger,写入logger.info(xxx)'
        'UPDATED: 将output的文件名从闭包外层函数传入，即再封装一层外层函数'
        msg = "< Timestamp:{:.0f}(ms),\ttime-consumed: {:.4f}(s) for function '{}' >\n ".format(
            time.time() * 1000,
            time_consumed,
            func.__name__)
        file = 'log-{}.txt'.format(datetime.datetime.today().strftime('%Y%m%d'))
        print(msg, file=open(file, 'a'))
        # print(msg, '-----------')
        return res
    return inner


def log_timmer(log_dir):
    '''
    高级函数装饰器： 装饰器外增加一个包裹函数，该包裹函数可接收参数
    文件输出装饰器： 将msg输出到log_file中
    Decorators:
        wraps
    Arguments:
        log_dir {str} -- [log文件所在文件夹]
    '''
    # 判断文件是否存在，不存在则创建文件 ---> 创建文件夹的逻辑建议以后不要放在这里，可以在初始化中进行
    create_directory(log_dir)
    log_file = '{}\\log-{}.txt'.format(log_dir, datetime.datetime.today().strftime('%Y%m%d'))

    def timmer(func):
        '''计时装饰器: 监控函数运行时间
        [对 类函数 或 独立函数 计时监控，输出msg到file中，print函数实现]
        Arguments:
            func {[object]} -- [需要监控的函数]
        Tips:
            TODO 部分，可自定义实现log日志采集
        Returns:
            [wrapper] -- [description]
        '''
        @wraps(func)
        def inner(*args, **kwargs):
            t1 = time.perf_counter()
            res = func(*args, **kwargs)
            time_consumed = time.perf_counter() - t1

            'TODO<klaus-20190411>: 输出函数运行时间信息至 console 或 file, 或传入自定义的logger,写入logger.info(xxx)'
            msg = "< Timestamp:{:.0f}(ms),\ttime-consumed: {:.4f}(s) for function '{}' >\n ".format(
                time.time() * 1000,
                time_consumed,
                func.__name__)
            print(msg, file=open(log_file, 'a'))

            # print(msg, '-----------')
            return res
        return inner
    return timmer


if __name__ == '__main__':
    class Spam:
        '''测试spam
        wraps的作用
        '''

        def __init__(self, nums, other):
            self.nums = nums
            self.other = other

        # @tracer
        @decorator_timmer
        # @log_timmer
        def spam(self):
            time.sleep(0.2258369)
            if self.nums >= 10:
                self.nums += self.other
            else:
                self.nums = self.other
            return self.nums

    # spam = Spam(20, -5).spam()
    # print(spam)

    # @log_timmer(log_dir='logs')
    # @decorator_timmer
    @decor_tracer()             # 只针对独立函数有效
    @decor_logitimmer(log_suffix='.log')           # 类装饰器需要()  --> sum_ab = logitimmer().__call__(sum_ab)
    def sum_ab(a, b):
        time.sleep(0.2210)
        return a ** 2 + a * b + b ** 2

    res = sum_ab(3, 2)
    print(res, '-----+++++++++++++++++')
    print(type(res))
    # print(sum_ab.__name__)      # def inner上没有@wraps(func)时，输出inner, 有@wraps时，输出sum_ab
    import inspect
    print()
    # 获得函数源码
    print(inspect.getsource(sum_ab))
