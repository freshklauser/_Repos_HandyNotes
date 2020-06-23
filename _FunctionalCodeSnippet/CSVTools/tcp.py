# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/21 18:52
# @FileName : tcp.py
# @SoftWare : PyCharm

"""
packages = {'tcp': [p1, p2, p3, ...], 'http': [h1, h2, ...]}
"""

import os
import pyshark

# 路径统一通过 path_params.py 文件引用

PCAP_FILE_PATH = 'E:/_Jun/_Python/pcap_data'
PCAP_FILE_NAME = 'test.pcapng'

protocol_filter = 'tcp || http || dhcp || mdns || lldp '
mac = '18:1d:ea:ab:f8:a1'
mac_filter_ = 'eth.src'


file_abs_path = os.path.join(PCAP_FILE_PATH, PCAP_FILE_NAME)

# capture = pyshark.FileCapture(file_abs_path, display_filter=protocol_filter)    # 17102
capture = pyshark.FileCapture(file_abs_path, display_filter='http')    # 17102
packages = []
index = 0
user_agent_list = []
for pkt in capture:
    packages.append(pkt)
    # first layer
    first_layers = [item for item in dir(pkt) if not item.startswith('_')]
    http_layers = [item for item in dir(pkt.http) if not item.startswith('_')]
    # print(http_layers)
    # print(type(http_layers[-1]))
    if 'user_agent' in http_layers:
        print('UserAgent: ', pkt.http.user_agent)
    else:
        print('UserAgent: ')
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>> {} <<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(index))
    index += 1
    if index >= 20:
        capture.close()
        break
print(index)
# pkt = packages[15]


def tcp(pkg):
    print()
    pass