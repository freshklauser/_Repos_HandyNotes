# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/22 23:16
# @FileName : protocol_unpack.py
# @SoftWare : PyCharm


"""
基于协议拆包，每个协议函数只负责单个package的拆解，一个capture中的n个packages放在for中执行
json结构(针对tablet)：{L0:xx, L1:xx, L2:xx, L3:xx, DHCP_Option55:XX, DHCP_Option60:XX, HTTP_USER_AGENT:XX, MAC: XX, package_index: 1}
    其中package_index只针对有值的记录生成，且自增
    [{L0:xx, L1:xx, L2:xx, L3:xx, DHCP_Option55:XX, DHCP_Option60:XX, HTTP_USER_AGENT:XX, MAC: XX, package_index: 1},
     {L0:xx, L1:xx, L2:xx, L3:xx, DHCP_Option55:XX, DHCP_Option60:XX, HTTP_USER_AGENT:XX, MAC: XX, package_index: 2}
    ]

L0_JSON_MAPPER = {
    'tablet': {'L0': '', 'L1': '', 'L2': '', 'L3': '', 'DHCP_Option55': '', 'DHCP_Option60': '', 'HTTP_User_Agent': '', 'Mac': '', 'package_index': -1},
    'router': {'L0': 'xx', 'L1': 'xx', 'L2': 'xx', 'L3': 'xx', 'DHCP_Option55': 'XX', 'DHCP_Option60': 'XX', 'Mac': 'XX', 'package_index': 1}
}
规则提取：
    先根据输入的标签判断大类，确定dict的key和默认值，
终端识别：
    直接print后端需要的数据即可
"""

import json
import os

import numpy as np
import pandas as pd
import pyshark


from attrdict import AttrDict

# from column_standard import branch, LABELS

LABELS = ['L0', 'L1', 'L2', 'L3']

# 按照之前的模板来写 features ---- 文件名 column_standard.py
branch = AttrDict()
# branch.mobile_phone = MOBILE_PHONE_FEATURES
# branch.tablet = TABLET
# branch.watch = WATCH_FEATURES
branch.router = ['DHCP_Option55', 'DHCP_Option60', 'HTTP_UserAgent']
# branch.set_top_box = SET_TOP_BOX_FEATURES
# branch.firewall = FIREWALL_FEATURES
# branch.aiv = AIV_FEATURES
# branch.switch = SWITCH_FEATURES
# branch.storage_device = STORAGE_DEVICE_FEATURES
# branch.ap = AP_FEATURES
# branch.printer = PRINTER_FEATURES
# branch.ip_camera = IP_CAMERA_FEATURES
# branch.voip_device = VOIP_DEVICE_FEATURES

# 需要的协议和协议的filter
protocol_filter_mapper = {'router': [['dhcp', 'http'], 'bootp || http'],
                          'tablet': [['http', 'tcp'], 'http || tcp']}

class ProtocolUnpack(object):
    PCAP_FILE_ABS_PATH = os.path.join(os.getcwd(), 'test.pcapng')

    def __init__(self, labels, mac):
        """
        records: 多条record字典组成的列表
        :param labels: l0/l1/l2/l3 (全部小写)
                       labels的输入不能有空格，单词间以下划线连接(set-top box映射为set_top_box)
                       后端根据前端的输入先按此要求预处理再传参调用python
        :param mac:
        """
        self.__labels = [item if item != '-' else None for item in labels.split('/')]
        self.__mac = mac
        self.records = []
        # self.__filter = 'tcp || dhcp || http || mdns || probe || association || lldp'
        self.__filter = self.__init_record_filter
        print(self.__filter)

    @property
    def __init_record_filter(self):
        return protocol_filter_mapper[self.level_zero][1]

    @property
    def level_zero(self):
        return self.__labels[0]     # L0

    @property
    def __init_record_dict(self):
        """
        Data for one package.
        :return:
        """
        key_list = LABELS + branch[self.__labels[0]] + ['Mac', 'package_index']
        rcd = dict.fromkeys(key_list)
        return rcd

    def file_capture(self):
        """
        参照正式代码中的写法

        :return: a dict(default)
        """
        capture = pyshark.FileCapture(self.PCAP_FILE_ABS_PATH, display_filter=self.__filter)
        pacakges = []
        for pkt in capture:
            pass
        return pacakges

    def tcp(self, pkt_index):
        """

        :param pkt_index: for循环packages时的i传入tcp
        :return:
        """
        record = self.__init_record_dict
        record['Mac'] = self.__mac
        record['package_index'] = pkt_index
        for col, value in zip(LABELS, self.__labels):
            record[col] = value
        first_layers = []
        tcp_layers = []

        # 1. mac查找和校验 pkt.eth.mac or pkt.wlan.ta(发射机或其他？？)

        # 2.
        record['DHCP_Option55'] = '15.2.35.6.9'
        record['DHCP_Option60'] = 'vendor-huawei'
        return record

    def http(self, pkg_index):
        pass

    def dhcp(self):
        pass

    def __summary(self, ):
        self.records.append(self.tcp(1))
        self.records.append(self.tcp(2))
        # print(self.records, len(self.records))

    def to_df_csv(self, local_csv=True):
        self.__summary()
        df = pd.DataFrame.from_dict(self.records, orient='columns', dtype=object)
        df['package_index'] = df['package_index'].astype(np.int64)
        if local_csv:
            file_name = self.__labels[0] + '.csv'
            df.to_csv(file_name, index=False, encoding='utf-8')
        return df

    def json_to_mysql(self):
        pass

    def process(self):
        protocol = protocol_filter_mapper[self.level_zero][0]
        print(protocol)
        func = [item for item in dir(self) if item in protocol]
        print(func)
        packages = self.file_capture()
        for pkt in packages:
            # todo: func
            pass


if __name__ == '__main__':
    labels = 'router/huawei/p89/-'
    # labels = 'mobile_phone/huawei/p89/-'
    mac = '15-58-68-b3-34'
    obj = ProtocolUnpack(labels, mac)
    # df = obj.json_list_to_df()
    obj.to_df_csv()
    print(obj.level_zero)
    obj.process()
