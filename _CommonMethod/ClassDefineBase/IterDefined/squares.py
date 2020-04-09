# -*- coding: utf-8 -*-
# @Author: KlausLyu
# @Date:   2020-04-09 08:55:08
# @Last Modified by:   KlausLyu
# @Last Modified time: 2020-04-09 09:43:54

'''{自定义迭代器}
实现自动迭代平方运算
Tips:
    __iter__机制中，__iter__只循环一次，一次循环之后就会变为空
    比如，下列测试代码中，如果执行了 print(list(iter_nums)) 之后，
    list(iter_nusm)就变为空
'''


class Squares:
    def __init__(self, nums):
        self.nums = nums
        self.offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.offset >= len(self.nums):
            raise StopIteration
        else:
            item = self.nums[self.offset]
            self.offset += 1
            return item ** 2


if __name__ == '__main__':
    nums = [1,4,2,6,8,10]
    iter_nums = Squares(nums)
    print(type(iter_nums))          # [1, 16, 4, 36, 64, 100]
    print(list(iter_nums))      # [1, 16, 4, 36, 64, 100]
    print(len(list(iter_nums)))

    print(type(iter_nums))
    # 上面两行执行后就无法执行该for循环了，why??
    for i in iter_nums:
        print('i --> ', i)
