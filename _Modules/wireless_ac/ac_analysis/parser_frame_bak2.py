# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/9/2 23:13
# @FileName : parser_frame.py
# @SoftWare : PyCharm

"""
后续转成多进程
"""
import threading

import pandas as pd
from pprint import pprint

import pyshark

from ac_configuration.logger import users_logger, process_logger, debugs_logger
from ac_configuration.params import PCAP_PATH, PROBE_FILTER, ASSOCIATION_FILTER, MANAGE_FRAME_FILTER


def _get_frame(path_, filter_):
    _frame_cap = pyshark.FileCapture(path_, display_filter=filter_)
    _frame_cap.load_packets()
    _frame_pkts = _frame_cap._packets
    _frame_cap.close()
    return _frame_cap, _frame_pkts


def get_frame_cap(path_, filter_):
    return _get_frame(path_, filter_)[0]


def get_frame_pkts(path_, filter_):
    return _get_frame(path_, filter_)[1]


def get_pkts_features(cap, to_df, csv_file):
    """
    obtain all features of one cap
    :param cap:
    :param to_df: Bool
    :param csv_file: str, effective only when to_df is True
    :return:
    """
    if not isinstance(cap, pyshark.capture.file_capture.FileCapture):
        raise TypeError('[ERROR] incorrect parameters')

    pkts_features_list = []

    def get_pkt_features(pkt):
        """
        obtain features of one pkt(probe request or association request) for wireless 802.11 protocol
        :param pkt:
        :return: list or DataFrame
        """
        if not isinstance(pkt, pyshark.packet.packet.Packet):
            raise TypeError('[ERROR] incorrect parameters')

        pkt_features = {}
        if not pkt:
            return pkt_features

        # wlan_radio
        wlan_radio_fields = pkt.wlan_radio.field_names  # 6
        for field in wlan_radio_fields:
            pkt_features.update({field: pkt.wlan_radio.get_field_value(field)})

        # wlan.mgt
        wlan_mgt_fields = pkt['wlan.mgt'].field_names  # 117
        for field in wlan_mgt_fields:
            pkt_features.update({field: pkt['wlan.mgt'].get_field_value(field)})

        pkts_features_list.append(pkt_features)

    cap.apply_on_packets(get_pkt_features)

    if pkts_features_list:
        shape_ = (len(pkts_features_list), len(pkts_features_list[0]))
    else:
        shape_ = (0, 0)

    if to_df:
        pkts_features_df = pd.DataFrame.from_dict(pkts_features_list)
        if csv_file:
            localiza_csv = '{}.csv'.format(csv_file)
            pkts_features_df.to_csv('../ac_output/{}'.format(localiza_csv), index=False)
        return pkts_features_df, shape_
    else:
        return pkts_features_list, shape_


def get_probe_features(path_, filter_=PROBE_FILTER, to_df=False, csv_file=''):
    probe_cap = get_frame_cap(path_, filter_)
    return get_pkts_features(probe_cap, to_df, csv_file)


def get_association_features(path_, filter_=ASSOCIATION_FILTER, to_df=False, csv_file=''):
    association_cap = get_frame_cap(path_, filter_)
    return get_pkts_features(association_cap, to_df, csv_file)


def get_mgt_features(path_, filter_=MANAGE_FRAME_FILTER, to_df=False, csv_file=''):
    mgt_cap = get_frame_cap(path_, filter_)
    return get_pkts_features(mgt_cap, to_df, csv_file)


def get_frame_features():
    """
    多进程或多线程实现 probe, association, manage_frame 的解析
    :return:
    """


class FrameThreading(threading.Thread):
    def __init__(self, func, arg):
        super(FrameThreading, self).__init__()
        self.func = func
        self.arg = arg

    def run(self):
        self.func(self.arg)


if __name__ == '__main__':
    path = PCAP_PATH
    filter_probe = PROBE_FILTER
    filter_association = ASSOCIATION_FILTER
    filter_mgt = MANAGE_FRAME_FILTER

    probe_features, _ = get_probe_features(path_=path, filter_=filter_probe, to_df=True)
    print(probe_features.shape)

    association_features, _ = get_association_features(path_=path, filter_=filter_association, to_df=True)
    print(association_features.shape)

    mgt_features, _ = get_mgt_features(path_=path, filter_=filter_probe, to_df=True)
    print(mgt_features.shape)
