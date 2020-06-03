# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/2 22:58
# @FileName : pcap_handler.py
# @SoftWare : PyCharm

import os
import json
import pandas as pd
import pyshark


# class PcapHandler:
PCAP_PKGS = "E:/_Jun/_Python/capture_test.pcapng"


def get_capture_count():
    p = pyshark.FileCapture(PCAP_PKGS, keep_packets=False)

    count = []

    def counter(*args):
        count.append(args[0])

    p.apply_on_packets(counter, timeout=100000)

    return len(count)


if __name__ == '__main__':
    print(get_capture_count())
