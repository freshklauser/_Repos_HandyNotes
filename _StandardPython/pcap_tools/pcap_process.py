# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/11 22:35
# @FileName : pcap_process.py
# @SoftWare : PyCharm


from _Modules import pandas as pd


class PcapHandler:
    def __init__(self, filter, file_path):
        self.__filter = filter
        self.__path = file_path

    def tcp(self, mac, file_name):
        cols = ['tcp-0', 'tcp_1', 'tcp_2']
        data = ['10-25-51-34', 'tcp-1', 'tcp-2']
        df = pd.DataFrame(data, cols)
        return df

    def dhcp(self, mac, file_name):
        cols = ['dhcp-0', 'dhcp_1', 'dhcp_2']
        data = ['x85', 'dhcp-1', 'dhcp-2']
        df = pd.DataFrame(data, cols)

    def lldp(self, mac, file_name):
        cols = ['lldp_0', 'lldp_1', 'lldp_2']
        data = ['tablet', 'lldp-1', 'lldp-2']
        df = pd.DataFrame(data, cols)
