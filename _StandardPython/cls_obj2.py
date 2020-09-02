# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/19 22:39
# @FileName : cls_obj.py
# @SoftWare : PyCharm


class Spam(object):
    numInstance = 0

    @classmethod
    def count(cls):
        cls.numInstance += 1

    def __init__(self):
        self.count()


class Sub(Spam):
    numInstance = 0


class Other(Spam):
    numInstance = 0


if __name__ == '__main__':
    x = Spam()
    y1, y2 = Sub(), Sub()
    z1, z2, z3 = Other(), Other(), Other()
    print(x.numInstance)
    print(y1.numInstance)
    print(y2.numInstance)
    print(z1.numInstance)
    print(z2.numInstance)
    print(z3.numInstance)
