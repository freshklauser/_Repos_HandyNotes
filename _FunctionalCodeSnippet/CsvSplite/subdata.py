# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/29 22:35
# @FileName : subdata.py
# @SoftWare : PyCharm

import numpy as np
import os
import pandas as pd

from config.features import branch
from config.params import CSV_DEFAULT_DIR

LABELS = ['X', 'Y', 'Z', 'H']
COLUMNS = ['X', 'Y', 'Z', 'H', 'Addr', 'HTTP_UserAgent',
           'DHCP_Option 55', 'DHCP_Option 60', 'DHCP_HostName',
           'LLDP_System Description', 'LLDP_System Name', 'LLDP_Model Name',
           'MDNS_SRV Service', 'MDNS_Answer Model',
           'CDP_Platform']

FILE_DEFAULT_NAME = 'template.csv'


def generate_csv():
    data1 = ['Tablet', 'apple', 'x series', '', '12:34:56', 'mozilla',
            '1,23,55,60,12,255', 'apple', 'local',
            'lldp system desc', 'lldp sys name', 'lldp model',
            'mdns srv', 'mdns model', 'cdp platform']
    data2 = ['printer', 'hp', 'x series', '', '12:34:56', '',
            '1,23,55,60,12,255', 'apple', 'local',
            '', '', '',
            '', '', 'cdp platform']
    data3 = ['voip_device', 'huawei', 'y series', '', '12:34:56', 'mozilla',
            '1,23,55,60,12,255', 'apple', 'local',
            'lldp system desc', '', 'lldp model',
            'mdns srv', 'mdns model', 'cdp platform']
    data4 = ['printer', 'hp', 'x series', '', '66:34:56', '',
             '1,23,55,60,12,255', 'huawei', 'remote',
             '', '', '',
             '', '', 'cdp platform']
    arr = np.array([data1, data2, data3, data4]).reshape((4, -1))
    df = pd.DataFrame(arr, columns=COLUMNS, dtype=object)
    file_abs_path = os.path.realpath(os.path.join(CSV_DEFAULT_DIR, FILE_DEFAULT_NAME))
    df.to_csv(file_abs_path, index=False, encoding='utf-8')


def subdata():
    file_abs_path = os.path.realpath(os.path.join(CSV_DEFAULT_DIR, FILE_DEFAULT_NAME))
    df = pd.read_csv(file_abs_path, encoding='utf-8')

    # DataFrame 按照 L0 将数据划分为 distinct(L0) 个子数据并分别存为csv
    unique_L0 = df['X'].unique()

    for i, item in enumerate(unique_L0):
        # 按 X 列筛选 子DataFrame
        sub_df_tmp = df[df['X'].isin([unique_L0[i]])]

        # X 的值对应需要的 columns
        sub_cols = LABELS + branch[unique_L0[i].lower()] + ['Addr']
        print(item, '-->', sub_cols)

        # 提取对应columns的子数据并分别保存为csv文件
        sub_df = sub_df_tmp[sub_cols]
        sub_file_abs_path = os.path.realpath(os.path.join(CSV_DEFAULT_DIR, item.lower() + '.csv'))
        sub_df.to_csv(sub_file_abs_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    generate_csv()
    subdata()
