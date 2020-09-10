# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/9/10 22:57
# @FileName : ac_dtree.py
# @SoftWare : PyCharm

"""
https://www.imooc.com/article/277642?block_id=tuijian_wz  refer
"""


from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier


def ac_baseline(X, y, train_x, test_x, train_y, test_y):
    base_ac_dtree = DecisionTreeClassifier(criterion='entropy')
    base_ac_dtree = base_ac_dtree.fit(train_x, train_y)
    score_test = base_ac_dtree.score(test_x, test_y)
    score_cv = cross_val_score(base_ac_dtree, X, y, cv=5).mean()
    return base_ac_dtree, score_test, score_cv



