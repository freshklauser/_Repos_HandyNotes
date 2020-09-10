# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/9/10 23:17
# @FileName : feature_engine.py
# @SoftWare : PyCharm

"""
jupyter 添加虚拟环境 kernel:

    conda install -n python_env ipykernel
"""

import numpy as np
import pandas as pd
import sklearn.preprocessing as sp
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from ac_model.ac_logger import process_logger

COLUMNS = ['service', 'quality', 'oil', 'discount', 'space', 'price', 'level']


def init_data(cols=COLUMNS, fraction=1):
    """
    后续可把数据存为 .h5 格式, 异步读取 .h5 文件加载数据集
    打乱data顺序且按比例返回数据，且重置索引 data.sample(frac=0.5)
    :return:
    """
    data = []
    with open('car.txt', 'r') as f:
        for line in f.readlines():
            data.append(line[:-1].split(','))
    data = pd.DataFrame(data, columns=cols)
    return data.sample(frac=fraction).reset_index(drop=True)


def data_describe(data):
    """
    :param data: DataFrame
    :return:
    """
    # process_logger.info('\n{}\n'.format(data.info))
    print(data.info(), end='\n\n')
    print(data.describe(), end='\n\n')
    print(data.isnull().sum(), end='\n\n')
    print(data.isnull().sum()[data.isnull().sum() != 0], end='\n\n')
    print(data.level.unique())
    print(data.head(5), '\n\n')
    print(data.service.unique())
    print(data.quality.unique())
    print(data.space.unique())
    print(data.price.unique())
    print(data.discount.unique())
    print(data.oil.unique())


def label_encoder(arr_like):
    """
    对给定样本列数据进行标签编码,离散型变量转换成连续的数值型变量
    编码后是 int 类型
    :param arr_like: shape[n_samples], list, arr or DataFrame or arr_like
    :return:
    """
    encoder = sp.LabelEncoder()
    arr_encoded = encoder.fit_transform(arr_like)
    return arr_encoded, encoder


def label_decoder(arr_encoded, encoder):
    """
    对给定样本列用之前编码的编码器进行解码
    :param arr_encoded:
    :param encoder:
    :return:
    """
    return encoder.inverse_transform(arr_encoded)


def test_label_encode():
    # label = pd.DataFrame(['audi', 'ford', 'ford', 'bmw', 'toyota', 'ford', 'audi'])
    # label = np.array(['audi', 'ford', 'ford', 'bmw', 'toyota', 'ford', 'audi'])
    label = ['audi', 'ford', 'ford', 'bmw', 'toyota', 'ford', 'audi']
    label_encoded, encoder = label_encoder(label)
    label_decoded = label_decoder(label_encoded, encoder)
    print(label_encoded)
    print(label_decoded)


def data_pretreat(data):
    # 类别映射, 偏序性类别变量转化为int型连续数字
    data['level'] = data['level'].apply(lambda x: {'unacc': 1, 'acc': 2, 'good': 3, 'vgood': 4}[x])
    data['service'] = data['service'].apply(lambda x: {'low': 1, 'med': 2, 'high': 3, 'vhigh': 4}[x])
    data['quality'] = data['quality'].apply(lambda x: {'low': 1, 'med': 2, 'high': 3, 'vhigh': 4}[x])
    data['space'] = data['space'].apply(lambda x: {'small': 1, 'med': 2, 'big': 3}[x])
    data['price'] = data['price'].apply(lambda x: {'low': 1, 'med': 2, 'high': 3}[x])
    data['discount'] = data['discount'].astype('category')
    data['discount'] = data['discount'].str.replace('more', '3').astype(np.int64)
    data['oil'] = data['oil'].str.replace('5more', '5').astype(np.int64)
    print(data.dtypes)
    return data


def data_encoder(data):
    """
    对 DataFrame 的每一列进行编码
    :param data: DataFrame
    :return:
    """
    pass


def standard_data(data):
    x_ = data.iloc[:, data.columns != 'level']
    y_ = data.iloc[:, data.columns == 'level']
    return x_, y_


def split_data(X, y, fraction=0.25):
    """
    划分数据集
    :param data:
    :param fraction: [0, 1]
    :return:
    """
    tx, vx, ty, vy = train_test_split(X, y, test_size=fraction)
    for df in [tx, vx, ty, vy]:
        df.index = range(df.shape[0])
    return tx, vx, ty, vy


if __name__ == '__main__':
    # test_label_encode()
    data_org = init_data()
    data_describe(data_org)
    data= data_pretreat(data_org)
    X, y = standard_data(data)
    print(X.columns)
    train_x, test_x, train_y, test_y = split_data(X, y)

    # print(data_org.head(15))
