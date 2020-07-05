# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/30 22:41
# @FileName : align_id.py
# @SoftWare : PyCharm

import os
import pdb

import pandas as pd

dev_cols = ['Id', 'L0', 'L1', 'L2', 'L3', 'name', 'minProb', 'namePath', 'idPath']
rule_cols = ['L0', 'L1', 'L2', 'L3', 'OS', 'Protocol', 'Field', 'Rule',
             'Release_Time, Precision', 'Total_Precision', 'Recall', 'Number',
             'Origin', 'Rule_Type', 'Rule_Id', 'New_Rule', 'Id']


def generate_csv(cols, file_name):
    # arr = np.array([data1, data2, data3, data4]).reshape((4, -1))
    df = pd.DataFrame(columns=cols, dtype=object)
    file_abs_path = os.path.realpath(file_name)
    df.to_csv(file_abs_path, index=False, encoding='utf-8')


def get_dev_id(dev, rule):
    dfDevTree = pd.read_csv(dev, encoding='utf-8')
    df = pd.read_csv(rule, encoding='utf-8')
    sub_col = ['L0', 'L1', 'L2', 'L3']

    # 需要合并的列的空值填充为空字符串 (数字类型的根据需要可填充默认值)
    df[sub_col] = df[sub_col].fillna('')
    dfDevTree[sub_col] = dfDevTree[sub_col].fillna('')

    # 添加辅助列，作为唯一索引
    df['unique'] = df['L0'] + df['L1'] + df['L2'] + df['L3']
    dfDevTree['unique'] = dfDevTree['L0'] + dfDevTree['L1'] + dfDevTree['L2'] + dfDevTree['L3']

    unique_id_mapper = dfDevTree.set_index('unique')['Id']
    # print(unique_id_mapper)

    # 辅助列映射id生成规则表中每一条记录的设备Id
    df_dev_id = df['unique'].map(unique_id_mapper)
    df['Id'] = df_dev_id
    df.drop_duplicates(subset=['unique'], inplace=True)
    # print(df)
    return df


def get_rule_id(rule_path):
    sub_cols = ['L0', 'L1', 'L2', 'L3', 'Protocol', 'Field', 'Rule', 'Rule_Id']
    rule_df = pd.read_csv(rule_path, encoding='utf-8')

    # Rule_Id 空的数据为新规则，将 ‘New_Rule’ 设为1
    mask = (rule_df.Rule_Id.isnull())
    rule_df.loc[mask, 'New_Rule'] = 1
    print(rule_df)
    
    # 添加辅助列，作为唯一索引
    rule_df['unique'] = rule_df['Protocol'] + rule_df['Field'] + rule_df['Rule']
    print(rule_df[sub_cols + ['unique']])

    # Rule_Id 非空子集的unique作为映射 (即原规则库的unique映射)
    df_with_rule_id = rule_df[rule_df['Rule_Id'].notnull()]
    print(df_with_rule_id[sub_cols + ['unique']])

    # 针对 ['Protocol', 'Field', 'Rule', 'Rule_Id'] 去重
    df_with_rule_id.drop_duplicates(subset=['Protocol', 'Field', 'Rule', 'Rule_Id'], inplace=True)

    # unique作为Rule_Id的映射
    unique_id_mapper = df_with_rule_id.set_index('unique')['Rule_Id']
    print(df_with_rule_id[sub_cols + ['unique']])
    print(unique_id_mapper)

    # 利用 unique_id_mapper 填充 rule_df 中 Rule_Id 为空的行

    # 辅助列映射id生成规则表中每一条记录的设备Id
    df_rule_id = rule_df['unique'].map(unique_id_mapper)
    rule_df['Rule_Id'] = df_rule_id
    print('--'*25)
    print(rule_df[sub_cols + ['unique']])

    rule_df.drop_duplicates(subset=['unique'], inplace=True)
    return rule_df


def re_rule_id(rule):
    sub_cols = ['L0', 'L1', 'L2', 'L3', 'Protocol', 'Field', 'Rule', 'Rule_Id']
    rule_df = pd.read_csv(rule, encoding='utf-8')
    _id = 0
    _compared_str = ''
    rule_df.sort_values(axis=0, ascending=True, by=['Protocol', 'Field', 'Rule'], inplace=True)
    rule_df['Rule_Id'] = range(1, rule_df.shape[0] + 1)
    print(rule_df[sub_cols])
    rule_df.to_csv(rule, index=False, encoding='utf-8')


def get_rule_id_wrong(rule_path):
    sub_cols = ['L0', 'L1', 'L2', 'L3', 'Rule', 'Rule_Id']
    rule_df = pd.read_csv(rule_path, encoding='utf-8')
    print(rule_df.shape)

    _id = 0
    _compared_str = ''
    rule_list = []
    id_list = []
    regex = ['\\', '?', ',', '.', '*', '(', ')']
    for i, row in rule_df.iterrows():
        rule = str(row['Rule']).strip().lower()
        tmp_str = str(row['Protocol']) + str(row['Field']) + rule
        print(rule, tmp_str)
        # pdb.set_trace()
        for reg in regex:
            tmp_rule = rule
            for j in range(len(tmp_rule) - 1, -1, -1):
                if tmp_rule[j] == reg:
                    rule = rule[:j] + '\\' + rule[j:]

        rule = rule.replace('\.\*', '.*')
        rule_list.append(rule)

        if tmp_str == _compared_str:
            id_list.append(_id)
        else:
            _id += 1
            _compared_str = tmp_str
            id_list.append(_id)

    rule_df['Rule'] = rule_list
    rule_df['Rule_Id'] = id_list
    print(rule_df[sub_cols])


if __name__ == '__main__':
    fn_dev = 'device_tree.csv'
    fn_rule = 'rule.csv'
    fn_flag = False
    if fn_flag:
        generate_csv(dev_cols, fn_dev)
        generate_csv(rule_cols, fn_rule)

    # get_dev_id(fn_dev, fn_rule)
    # re_rule_id(fn_rule)

    get_rule_id(fn_rule)


    # df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['Andy1', 'Jacky1', 'Bruce1']})
    # df2 = pd.DataFrame({'id': [1, 2], 'name': ['Andy2', 'Jacky2']})
    # print(df1)
    # print(df2)
    # s = df2.set_index('id')['name']
    # print(type(s), '----------')
    # print()
    # print(df1['id'].map(s))
    # print()
    # print(s)
    # print()
    # print(df1['id'].map(s).fillna(df1['name']).tolist())