# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/23 23:27
# @FileName : basic.py
# @SoftWare : PyCharm

"""
DataFrame SettingWithCopyWarning
"""

import pdb
import numpy as np
import pandas as pd
# import pandas_profiling


data = pd.DataFrame({'name': ['gz', 'lg', 'zx'], 'score': [80, 96, 60]})
print(data)
print()
pdb.set_trace()

# 条件选择 并 增加一列score是否不小于80
data['perfect'] = data.score >= 95
data['good'] = (data.score >= 85) & (data.score < 95)
data['normal'] = (data['score'] < 85) & (data['score'] >= 60)
print(data)
print()
pdb.set_trace()

# 删除某列
# del data['perfect']
# print(data)
# print()

# 列索引
print(data['name'])
print(data.name)
print('-+-'*15)
# 行索引
print(data.loc[1])
print('-/-'*15)
# 单元格索引
print(data.loc[1, ['name', 'score']])
print(data.loc[1, 'name'])
print(data.iloc[0, 1])
print(data.at[1, 'name'])
print(data.iat[0, 2])
print('--'*15)

# 赋值正确方法(不是副本) ---> 推荐赋值用 df.at[row, col] = value, df.loc可能隐私链式索引
data.loc[data.name=='zx', 'score'] = 100
data.at[data.name=='lg', 'score'] = 99      # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
print(data)
print('*-'*15)

# 以下方法并不会更改data的值
# 链式索引（Chaining） - 连续使用多个索引操作，例如data[1:5][1:3]
# data[data.name=='zx']['score'] = 10     # 警告 SettingWithCopyWarning，不会改变原值
# print(data)
# print('**'*15)
# data.score[data.name=='zx'] = 99        # SettingWithCopyWarning， 会改变原值
# print(data)

print('++'*15)
subdata = data[data.name=='gz']
# subdata.loc[0, 'score'] = 55            # SettingWithCopyWarning， 会改变原值
subdata.at[0, 'score'] = 150              # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
print(subdata, '------')
print('++'*15)
# print(data.profile_report())


print(help(pdb))

