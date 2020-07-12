# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/7/12 16:04
# @FileName : dev_edit_distance.py
# @SoftWare : PyCharm
import math

from _Modules.uaparser.data import map_phone

# 最好转小写后去重相同键的数据
mapper = {key.lower(): value for key, value in map_phone.items()}


def build_hardware_info():
    hardware_keys = map_phone.keys()
    info_set = set()
    # hardware_keys 写入文件中，全部换小写
    with open('hardware_info.txt', 'w+', encoding='utf-8') as f:
        for info in hardware_keys:
            if info.lower() not in info_set:
                info_set.add(info.lower())
                f.write(info.lower() + '\n')


def get_info_pool():
    """
    with open('hardware_info.txt', 'r', encoding='utf-8') as f:
        content = f.readlines()
        for line in content:
            info_pool.append(line.strip())
    :return:
    """
    info_pool = []
    with open('hardware_info.txt', 'r', encoding='utf-8') as f:
        for line in f:
            info_pool.append(line.strip())
    return info_pool


def minDistance(word1, word2):
    row = len(word1)
    col = len(word2)
    if row * col == 0:
        return row + col
    # 考虑到位空的情况，需添加第0行第0列代表为空，这样第i个字符才是word1[i-1]
    # dp[i][j]: word1的前i个字符word1[:i]与word2的前j个字符word2[:j]之间的最短编辑距离
    dp = [[0] * (col + 1) for _ in range(row + 1)]
    # base case
    for i in range(row + 1):
        dp[i][0] = i
    for j in range(col + 1):
        dp[0][j] = j
    # 二维表格边界：即0行和0列
    for i in range(1, row + 1):
        for j in range(1, col + 1):
            down = dp[i][j - 1] + 1
            left = dp[i - 1][j] + 1
            left_down = dp[i - 1][j - 1]
            if word1[i - 1] != word2[j - 1]:  # 第 i 个字符对应下标不是 i-1
                left_down += 1
            dp[i][j] = min(down, left, left_down)
    return dp, dp[row][col]


def sim_hardware_info(target, info_pool):
    sim_hardware_indice = 0
    edit_dist_min = math.inf
    for i, info in enumerate(info_pool):
        edit_dist = minDistance(target, info)[1]
        if edit_dist < edit_dist_min:
            edit_dist_min = edit_dist
            sim_hardware_indice = i
    sim_dev = mapper[info_pool[sim_hardware_indice]]
    return sim_dev


if __name__ == '__main__':
    # build_hardware_info()
    info_pool = get_info_pool()
    target = 'nen-al01'
    res = sim_hardware_info(target, info_pool)
    print(res)

    # word1 = "kiw-al10"
    # word2 = "lnd-al40"
    # dp, res = minDistance(word1, word2)
    # print(res)
