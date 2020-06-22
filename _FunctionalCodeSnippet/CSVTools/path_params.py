# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/21 21:02
# @FileName : path_params.py
# @SoftWare : PyCharm

import os
import constant

# .pcap file path



# local csv path
constant.CSV_OUTPUT_PATH = os.path.realpath('E:\_Jun\_Python\csvfiles')
constant.RULE_CSV_NAME = 'rule_summary.csv'
constant.RULE_CSV_PATH = os.path.join(constant.CSV_OUTPUT_PATH, constant.RULE_CSV_NAME)

constant.DEVICE_TREE_CSV_NAME = 'device_tree.csv'
constant.DEVICE_TREE_CSV_PATH = os.path.join(constant.CSV_OUTPUT_PATH, constant.DEVICE_TREE_CSV_NAME)

# 生成新标签列表，调用addDevice.py添加到设备树
constant.NEW_LABEL_CSV_NAME = 'output.csv'
constant.NEW_LABEL_CSV_PATH = os.path.join(constant.CSV_OUTPUT_PATH, constant.NEW_LABEL_CSV_NAME)

constant.RULE_DEALED_CSV_NAME = 'rule_summary.csv'
constant.RULE_DEALED_CSV_PATH = os.path.join(constant.CSV_OUTPUT_PATH, constant.RULE_DEALED_CSV_NAME)