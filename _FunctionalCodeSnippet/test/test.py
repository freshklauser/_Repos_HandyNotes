# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/1 23:38
# @FileName : test.py
# @SoftWare : PyCharm


import configparser

from _FunctionalCodeSnippet.Configs import conf_handler
from _FunctionalCodeSnippet.ClassTools import constant

# 定义常量
constant.NAME = "klaus"
constant.AGE = 18

# constant.AGE = 15

obj = conf_handler.ConfigHandler()
