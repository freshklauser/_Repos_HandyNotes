# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/9/3 23:37
# @FileName : common.py
# @SoftWare : PyCharm
import os


def standard_path(root, relative_path):
    return os.path.realpath(os.path.join(root, relative_path))
