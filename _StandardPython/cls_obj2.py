# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/19 22:39
# @FileName : cls_obj.py
# @SoftWare : PyCharm

"""
可以看成是静态方法已经跟这个类没关系了，相当于已经脱离了这个类，是一个完全独立的函数，
只是调用的时候必须通过这个类, 或者为了规范代码而将函数放到类中
"""


class Spam(object):
    numInstance = 0

    @staticmethod
    def count():
        Spam.numInstance += 1

    def __init__(self):
        self.count()
        print(self, self.numInstance, '--------')


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
    print(Spam.numInstance, Sub.numInstance, Other.numInstance)
#
# <__main__.Spam object at 0x00000251539AA358> 1 --------
# <__main__.Sub object at 0x00000251539AA3C8> 0 --------
# <__main__.Sub object at 0x00000251539AA400> 0 --------
# <__main__.Other object at 0x00000251539AA438> 0 --------
# <__main__.Other object at 0x00000251539AA470> 0 --------
# <__main__.Other object at 0x00000251539AA4A8> 0 --------
# 6
# 0
# 0
# 0
# 0
# 0
# 6 0 0
