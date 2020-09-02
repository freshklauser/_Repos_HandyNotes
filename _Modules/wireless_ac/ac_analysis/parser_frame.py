# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/9/2 23:13
# @FileName : parser_frame.py
# @SoftWare : PyCharm
from pprint import pprint

import pyshark

from ac_configuration.params import pcap_path, probe_filter, association_filter, manage_frame_filter

probe_cap = pyshark.FileCapture(pcap_path, display_filter=probe_filter)
association_cap = pyshark.FileCapture(pcap_path, display_filter=association_filter)
manage_cap = pyshark.FileCapture(pcap_path, display_filter=manage_frame_filter)

probe_cap.load_packets()
association_cap.load_packets()
manage_cap.load_packets()

probe_pkts = probe_cap._packets
association_pkts = association_cap._packets
manage_pkts = manage_cap._packets
print(len(probe_pkts))
print(len(association_pkts))
print(len(manage_pkts))         # list

i = 0
for manage_pkt in manage_pkts:
    i += 1
    if i == 4:
        print(dir(manage_pkt))
        print(type(manage_pkt))

        print(manage_pkt.layers)
        print(manage_pkt.wlan_radio)
        print(manage_pkt['netmon_802_11'])
        print(manage_pkt['wlan_radio'])         # .wlan_radio 或者 ['wlan_radio'] 都可以
        print(manage_pkt.length)             # .layers 和.length 都不能用['layers'] [length]的方式获取
        print()
        print()
        print()
        # print(manage_pkt.wlan)

        # -------------------------- 无线信号特征 -----------------------------
        print(dir(manage_pkt.wlan_radio))
        print(manage_pkt.wlan_radio.frequency)      # 信号频率
        print(manage_pkt.wlan_radio.data_rate)      # 数据传输速率 ？？
        print(manage_pkt.wlan_radio.channel)        # 信道
        print(manage_pkt.wlan_radio.phy)            # 物理层协议 802.11n（HT）（7）
        print(manage_pkt.wlan_radio.signal_dbm)     # 信号强度

        # -------------------------- wifi管理帧特征：能力集IEs -----------------------------
        print(dir(manage_pkt['wlan.mgt']))          # 不能 manage_pkt.wlan.mgt
        print(manage_pkt['wlan.mgt'].wlan_asel_rx)
        print(manage_pkt['wlan.mgt'].wlan_txbf_channelest)
        break


probe_cap.close()
association_cap.close()
manage_cap.close()
