# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/9/2 23:13
# @FileName : params.py
# @SoftWare : PyCharm


pcap_path = '../data/wifis.cap'

probe_filter = 'wlan.fc.type_subtype==0x04'
association_filter = 'wlan.fc.type_subtype==0x00'
# wifi管理帧（不包含Beacon帧）
manage_frame_filter = 'wlan.fc.type==0 && not wlan.fc.type_subtype==0x08'
