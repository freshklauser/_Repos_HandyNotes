# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/9/2 23:13
# @FileName : params.py
# @SoftWare : PyCharm


PCAP_PATH = '../data/wifis.cap'

PROBE_FILTER = 'wlan.fc.type_subtype==0x04 && not wlan.fc.type_subtype==0x08 && wlan.sa==5e:d3:77:26:5f:9a'
ASSOCIATION_FILTER = 'wlan.fc.type_subtype==0x00 && not wlan.fc.type_subtype==0x08 && wlan.sa==5e:d3:77:26:5f:9a'
# wifi管理帧（不包含Beacon帧）
MANAGE_FRAME_FILTER = 'wlan.fc.type==0 && not wlan.fc.type_subtype==0x08 && wlan.sa==5e:d3:77:26:5f:9a'

FILTERS = {'probe': PROBE_FILTER, 'association': ASSOCIATION_FILTER, 'manage': MANAGE_FRAME_FILTER}

CORE = 3
