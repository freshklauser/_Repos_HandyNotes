# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/21 20:55
# @FileName : post_main.py
# @SoftWare : PyCharm

from path_params import constant
from postpro import addOSRule, veriftyDevice
from postpro import addDevice, post_process, full_post_process


rule_abs_path = constant.RULE_CSV_PATH
device_tree_abs_path = constant.DEVICE_TREE_CSV_PATH
output_abs_path = constant.NEW_LABEL_CSV_PATH
rule_dealed_abs_path = constant.RULE_DEALED_CSV_PATH

print(rule_abs_path)
print(rule_dealed_abs_path)
print(output_abs_path)
print(device_tree_abs_path)

addOSRule.add_os_rule(rule_abs_path, device_tree_abs_path)

veriftyDevice.verify_device(rule_abs_path, device_tree_abs_path)

addDevice.add_device(output_abs_path, device_tree_abs_path)

post_process.post_process(rule_abs_path, device_tree_abs_path)

full_post_process.full_post_proc(rule_abs_path)