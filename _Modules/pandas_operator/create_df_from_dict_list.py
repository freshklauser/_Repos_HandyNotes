# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/27 1:07
# @FileName : create_df_from_dict_list.py
# @SoftWare : PyCharm

import pandas as pd

adict = {'dhcp': [125, 56], 'tcp': [54, 24], 'num': ['as', 'td']}
bdict = {'dhcp': 12, 'tcp': 5, 'num': 'ai'}
cdict = {'dhcp': 325, 'tcp': 514, 'num': 'ast'}
ddict = {'dhcp': 125, 'tcp': 1514, 'num': 'asst'}

df = pd.DataFrame.from_dict(adict, orient='columns')
print(df)

alist = []
alist.append(bdict)
alist.append(cdict)
alist.append(ddict)
alist.append({})
alist.append({})


dd = pd.DataFrame.from_dict(alist, orient='columns')
print(dd)

dd.dropna(axis=0, how='all')
print(dd)
