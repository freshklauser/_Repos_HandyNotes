# -*- coding: utf-8 -*-
# @Author: sniky-lyu
# @Date:   2020-04-09 22:31:53
# @Last Modified by:   KlausLyu
# @Last Modified time: 2020-04-10 14:23:48


class Spam:
    numInstances = 0

    def __init__(self):
        Spam.numInstances += 1

    # 方式1： 将 printNumInstances 方法转化为静态方法--直接在方法上添加 @staticmethod
    # @staticmethod
    def printNumInstances():
        print('Number of instances:', Spam.numInstances)
    # 方式2： 将 printNumInstances 方法转化为静态方法
    printNumInstances = staticmethod(printNumInstances)


# ------------------------- decorator ----------------------------------



if __name__ == '__main__':
    a = Spam()
    b = Spam()
    b.printNumInstances()
    Spam.printNumInstances()
