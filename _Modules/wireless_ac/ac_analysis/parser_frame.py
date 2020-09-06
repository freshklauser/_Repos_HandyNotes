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
import pyshark

from ac_configuration.logger import users_logger
from ac_configuration.params import PCAP_PATH, FILTERS


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
        if pkt:
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


def get_frame_features(path_, filter_, to_df=False, csv_file=''):
    frame_cap = get_frame_cap(path_, filter_)
    return get_pkts_features(frame_cap, to_df, csv_file)


class FrameThreading(threading.Thread):
    def __init__(self, name, func, args, kwargs):
        super(FrameThreading, self).__init__()
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def run(self):
        self.result = self.func(*self.args, **self.kwargs)

    def get_result(self):
        if self.result:
            return self.result
        else:
            raise Exception("The current thread is not executed")


def start():
    """
    Multithreading to implement parser of probe, association and manage_frame
    :return:
    """
    path = PCAP_PATH
    features = {}
    thread_pool = []

    users_logger.info('-------------------------- THREADING: START --------------------------')
    for field, filter_ in FILTERS.items():
        args = (path, filter_)
        kwargs = {'to_df': True, 'csv_file': field}
        t = FrameThreading(name=field, func=get_frame_features, args=args, kwargs=kwargs)
        thread_pool.append(t)

    for thread in thread_pool:
        thread.start()

    for thread in thread_pool:
        thread.join()
        users_logger.info('Current thread: {}'.format(thread.name))
        features.update({thread.name: thread.get_result()[0]})

    users_logger.info('-------------------------- THREADING: END --------------------------')

    return features


if __name__ == '__main__':
    res = start()
