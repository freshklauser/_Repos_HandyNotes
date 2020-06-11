# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/11 22:35
# @FileName : pcap_main.py
# @SoftWare : PyCharm


"""
输入：(path, mac, pcap_file)
输出：json (df.to_json()  or json --- 最好空值不输出key)

CMD:
    usage:
        pcap_main.py [-h] [-mac MAC] [-fp FP] [-fn FN] [-forbidden FORBIDDEN]
    tips:
        FORBIDDEN is a tuple
    example:
        python pcap_main.py -mac 12-15-25 -fp /root/path/tools -fn test.txt -forbidden a
        --> args.forbidden: <class 'tuple'> ('a',)




TODO:
    1) log 日志写入
    2) 进度条
"""

import argparse
import os
import sys

from pcap_tools.loghelper import LogHandler
from pcap_tools.pcap_process import PcapHandler


class UnpackProcess(object):
    logger = LogHandler().logger()

    def __init__(self):
        self.__args = self.params

    @staticmethod
    def __parse_params():
        """
        Parse the input params from command.
        :return:
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-mac', type=str, default='00-00-00', required=True, help='get the mac.')
        parser.add_argument('-fp', type=str, default='filepath', required=True, help='get the file path.')
        parser.add_argument('-fn', type=str, default='filename', required=True, help='get the pcap file name.')
        parser.add_argument('-forbidden', type=tuple, required=False, help='blacklist for protocols without need to extract.')
        args = parser.parse_args()
        return args

    @property
    def params(self):
        """ Can not set this attribute """
        return self.__parse_params()

    def protocol_check(self):
        """
        Check if some protocols' information has no need to extract.
        Blacklist can be added for these protocols without need to extract.
        :return:
        """
        pass

    def unpack_pcap_process(self):
        """
        outout 与 out_put_rename 通过 filename 字段为键对齐标签的么？？
        :return:
        """
        mac = self.__args.mac
        file_path = self.__args.fp
        file_name = self.__args.fn
        # TODO: 遍历所有的 pcap_process 中的function来拆包，如果有不拆的协议，可以添加协议校验
        print(self.params.forbidden)
        # obj = PcapHandler()
        # func_list = [item for item in obj.]

    def start(self):
        """
        cmd： python main -m <mac> -p <file_path> -f <file_name> []
        :return:
        """
        obj = UnpackProcess()
        obj.unpack_pcap_process()

        # try:
        #     self.params = 125
        #     print(self.params.mac)
        # except AttributeError: as err:
        #     raise


UnpackProcess().start()

# 需要注意命令行执行和pydev执行时当前的可选路径
# print(sys.path)
