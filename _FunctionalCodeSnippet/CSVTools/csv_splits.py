# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/21 14:03
# @FileName : csv_splits.py
# @SoftWare : PyCharm


"""
labels: java传入，格式 'L0/L1/L2/L3', 若为空则填-，如 Tablet/Apple/plus/-，不可能中间或前面为空
pcap_file output: columns=FEATURE_LIST
summary_template columns:  [L0, L1, L2, L3] + FEATURE_LIST + [vendor, Mac]
split_template columns: 根据大类需要的特征来确定
                        [L0, L1, L2, L3] + FEATURE_NEEDS + [vendor, Mac]
vendor字段去掉， 规则提取和终端识别用不上该字段

前提和注意事项：
    (1) pcap提取出来的数据对应同一个mac和labels
--->(2) java传入的 标签名不能有空格， 需要再java端先map映射到规则提取需要的固定的文件名
        比如： 前端输入 VoIP Device, 需映射为 VoIP_Device(假设规则提取的csv输入文件名要求为 VoIP_Device)
"""

import numpy as np
import os
import pandas as pd
import random

from columns import L0_LIST, FEATURES_LIST, branch, LABELS

CSV_OUTPUT_PATH = os.path.realpath('E:\_Jun\_Python\csvfiles')
SUMMARY_TABLE = 'features_summary_table.csv'


def generate_pcap_output():
    """
    模拟pcap拆包生成的 DataFrame
    """
    cols = FEATURES_LIST
    random.seed(13)
    rnd1 = random.choices('123456789abcdefghijklmnopqrstuvwxyz', k=len(cols))
    rnd2 = random.choices('123456789abcdefghijklmnopqrstuvwxyz', k=len(cols))
    rnd3 = random.choices('123456789abcdefghijklmnopqrstuvwxyz', k=len(cols))
    data = np.array([rnd1, rnd2, rnd3]).reshape((3, -1))
    pcap_output = pd.DataFrame(data, columns=cols, dtype=str)
    return pcap_output

def generate_features_template(mac, labels, df_from_pcap):
    """ 生成该L0下所有特征的数据文件
    java pcap上传，同时传入 mac 和 labels
    dataframe交换列的位置： df= df.reindex(columns=[new_cols_list])
    dataframe重命名： df = df.rename(columns={old_col1: new_col1, old_col2: new_col2}, inplace=True)
    dataframe改变类数据类型：df[cols].astype(str)
    """
    row_, col_ = df_from_pcap.shape

    # 1. label+mac --> dataframe (1, 5);  else None 否则 df.isnull() 没有非空，不能使用df.fillna()
    prefix_list = [item if item != '-' else None for item in labels.split('/')]
    prefix_list.append(mac)
    prefix_arr = np.array([prefix_list] * row_)
    prefix_cols = LABELS + ['Mac']
    prefix_df = pd.DataFrame(prefix_arr, columns=prefix_cols)

    # 2. label+mac+df_from_pcap --> 总表
    summary_tb = pd.concat([prefix_df, df_from_pcap], axis=1)
    re_cols = LABELS + FEATURES_LIST + ['Mac']
    summary_tb = summary_tb.reindex(columns=re_cols)
    summary_tb.fillna('', inplace=True)

    # 3. save to local csv file
    summary_csv_file = os.path.join(CSV_OUTPUT_PATH, SUMMARY_TABLE)
    summary_tb.to_csv(summary_csv_file)

    return summary_tb


def generate_L0_file(mac, labels, pcap_output, local_csv=True):
    """
    生成给定的L0对应的规则提取需要的csv文件，文件名即L0
    """
    row_, col_ = pcap_output.shape

    # 1. output的文件名和路径， file_name 通过java传入的label确定
    file_name = labels.split('/')[0]
    file_abs_path = os.path.join(CSV_OUTPUT_PATH, file_name + '.csv')

    # 2. label+mac --> dataframe (1, 5);  else None 否则 df.isnull() 没有非空，不能使用df.fillna()
    prefix_list = [item if item != '-' else None for item in labels.split('/')]
    prefix_list.append(mac)
    prefix_arr = np.array([prefix_list] * row_)
    prefix_cols = LABELS + ['Mac']
    prefix_df = pd.DataFrame(prefix_arr, columns=prefix_cols)

    # 3. label+mac+l0_features
    target_cols = branch.get(file_name)
    target_df = pcap_output[target_cols]
    output = pd.concat([prefix_df, target_df], axis=1)
    re_cols = LABELS + target_cols + ['Mac']
    output = output.reindex(columns=re_cols)
    output.fillna('', inplace=True)

    # 4. save to csv
    if local_csv:
        output.to_csv(file_abs_path, index=False, encoding='utf-8')

    return output


def call_rule_extraction():
    # TODO: 可能要用 subprocess 模块来调用命令行； 或者改一下源码的main.py, 封装一下传参调用
    #   建议改 main.py 的源码，封装后以传参的方式调用
    pass


if __name__ == '__main__':
    pcap_output = generate_pcap_output()
    # print(pcap_output)
    labels = 'Tablet/Apple/plus/-'
    mac = '00-50-56-C0-00-08'
    # res = generate_features_template(mac, labels, pcap_output)
    res = generate_L0_file(mac, labels, pcap_output)
    print(res, res.columns)
