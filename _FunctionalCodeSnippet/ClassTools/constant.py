# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/1 23:20
# @FileName : constant.py
# @SoftWare : PyCharm


import sys


class _Constant:
    """ 自定义常量类 """

    class ConstError(PermissionError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConstError(
                "No permission to change a constant {}".format(key))

        if not key.isupper():
            raise self.ConstCaseError(
                "Constant {} should be all uppercase.".format(key))

        self.__dict__[key] = value


sys.modules[__name__] = _Constant()
