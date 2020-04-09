# -*- coding: utf-8 -*-
# @Author: sniky-lyu
# @Date:   2020-04-09 23:00:03
# @Last Modified by:   sniky-lyu
# @Last Modified time: 2020-04-09 23:09:44

'''decorator tools
'''


class tracer:
    '''函数调用次数计数器
    Sample goes to person.py
    '''

    def __init__(self, func):
        self.call = 0
        self.func = func

    def __call__(self, *args, **kargs):
        self.call += 1
        print("Function '{}' is called {} times".format(self.func.__name__, self.call))
        self.func(*args, **kargs)


if __name__ == '__main__':
    class Spam:
        def __init__(self, nums):
            self.nums = nums

        # @tracer
        def spam(self):
            print(self.nums)

    nums = [1, 2, 3, 4]
    cl = Spam(nums)
    cl.spam()

