# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/2 22:58
# @FileName : pcap_handler.py
# @SoftWare : PyCharm

import os
import json
import pandas as pd
import pyshark

PCAP_PKGS = "capture_test.pcapng"

# captures = pyshark.FileCapture(PCAP_PKGS, keep_packets=False)


def get_capture_list(captures):
    """
    将所有的数据包加入到一个列表返回
    """
    packs = []

    def counter(*args):
        packs.append(args[0])

    captures.apply_on_packets(counter, timeout=100000)
    return packs


def print_conversation_header(pkt):
    try:
        protocol = pkt.transport_layer
        src_addr = pkt.ip.src
        src_port = pkt[pkt.transport_layer].srcport
        dst_addr = pkt.ip.dst
        dst_port = pkt[pkt.transport_layer].dstport
        print(
            '%s  %s:%s --> %s:%s' %
            (protocol,
             src_addr,
             src_port,
             dst_addr,
             dst_port))
    except AttributeError as e:
        # ignore packets that aren't TCP/UDP or IPv4
        pass


# captures.apply_on_packets(print_conversation_header, timeout=100)


if __name__ == '__main__':
    # packages = get_capture_list()
    # print(packages[:3], type(packages[0]), len(packages))

    # capture = pyshark.FileCapture(PCAP_PKGS)
    # print(type(capture))
    # print(dir(capture))
    # print(capture.get_parameters())     # ['-r', 'capture_test.pcapng']
    # print(capture[0])
    # for cap in capture:
    #     # print(cap)
    #     print(type(cap))
    #     break

    captures = pyshark.FileCapture(PCAP_PKGS)
    # captures.apply_on_packets(print_conversation_header, timeout=100)
    for cap in captures:
        # print(cap)
        layer1 = [item for item in dir(cap) if not item.startswith("_")]
        print(layer1)
        print(cap['ip'].src, cap.ip.src)
        print(cap.ip.dst)
        print(cap.ip.flags)
        print(cap.ip)
        print(cap.ip.ttl)
        print('ip' in cap)
        print(cap.eth)
        print(cap.eth.dst)
        break
