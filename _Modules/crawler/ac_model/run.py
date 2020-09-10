# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/9/11 2:00
# @FileName : run.py
# @SoftWare : PyCharm

"""
dot可视化工具
https://www2.graphviz.org/Packages/stable/windows/10/cmake/Release/

1) https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygraphviz 下载python库.whl  pip install xxx.whl
2) https://www2.graphviz.org/Packages/stable/windows/10/cmake/Release/ 下载window stable 版本的exe
   安装后设置环境变量  如 D:\Program Files\Graphviz 2.44.1\bin
3） dot -version
    dot -c

文件目录下： dot -Tpng .\tree.dot -o .\tree.png


#画图方法2-生成pdf文件

dot_data = tree.export_graphviz(clf, out_file=None,feature_names=clf.feature_importances_,

filled=True, rounded=True, special_characters=True)

graph = pydotplus.graph_from_dot_data(dot_data)

###保存图像到pdf文件

graph.write_pdf("treetwo.pdf")

"""
from pprint import pprint

from sklearn.tree import export_graphviz

from ac_model.ac_dtree import ac_baseline
from ac_model.feature_engine import init_data, data_pretreat, standard_data, split_data

# 属于预处理
data_org = init_data()
data = data_pretreat(data_org)
X, y = standard_data(data)
train_x, test_x, train_y, test_y = split_data(X, y)

# 特征工程

# 基线模型
args = (X, y, train_x, test_x, train_y, test_y)
baseline, score_test, score_cv = ac_baseline(*args)
print(score_test, score_cv)
feature_import = sorted({key: value for key,
                         value in zip(X.columns,
                                      baseline.feature_importances_)}.items(),
                        key=lambda x: x[1],
                        reverse=True)
pprint(feature_import)

# 决策树可视化
dt_dot = './tree_ac.dot'
with open(dt_dot, 'w') as f:
    f = export_graphviz(baseline,
                        feature_names=X.columns,
                        out_file=f,
                        class_names=['unacc', 'acc', 'good', 'vgood'],
                        filled=True,
                        rounded=True,
                        special_characters=True)
