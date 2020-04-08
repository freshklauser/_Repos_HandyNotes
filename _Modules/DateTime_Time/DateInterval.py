# -*- coding: utf-8 -*-
# @Author: klaus
# @Date:   2020-03-21 09:25:55
# @Last Modified by:   KlausLyu
# @Last Modified time: 2020-04-08 15:50:03

'''{日期间隔}
self.__class__.__name__:         获取当前的类名
sys._getframe().f_code.co_name： 获取当前所在的函数的函数名
'{}.{}':".format(self.__class__.__name__, sys._getframe().f_code.co_name) : 类名.函数名
'''

import sys
import datetime

class DateInterval:
    """docstring for Date_Interval"""
    def __init__(self, date1, date2, sep="."):
        self.date1 = date1
        self.date2 = date2
        self.__check_type()
        self.instance_flag = False
        FORMATTER = {".": "%Y.%m.%d", "-": "%Y-%m-%d", "/": "%Y/%m/%d"}
        self.DAYS_YEAR = 365
        self.formatter = FORMATTER[sep]
        # print(self.formatter, type(self.formatter))

    def _date_interval(self):
        try:
            std_date1 = datetime.datetime.strptime(self.date1, self.formatter).date()
            std_date2 = datetime.datetime.strptime(self.date2, self.formatter).date()
            if std_date1 > std_date2:
                std_date1, std_date2 = std_date2, std_date1
            interval = std_date2 - std_date1
            # interval: <class 'datetime.timedelta'>, 属性：interval.days, interval.seconds, interval.microseconds
        except Exception as e:
            print("Exception in '{}.{}':".format(self.__class__.__name__, sys._getframe().f_code.co_name), e, sep="\n\t")
        return interval

    def get_days_interval(self):
        days = self._date_interval().days
        print("Interval between '{}' and '{}' is {} days.".format(self.date1, self.date2, days))
        return days

    def get_years_interval(self):
        ''' days --> years (一年按365天计算)'''
        days = self._date_interval().days
        years = round(days / self.DAYS_YEAR, 2)
        print("Interval between '{}' and '{}' is {} years.".format(self.date1, self.date2, years))
        return years

    def __check_type(self):
        if isinstance(self.date1, str) and isinstance(self.date2, str):
            self.instance_flag = True
            # print(sys._getframe().f_code.co_name)
        else:
            raise AttributeError("Please make sure the type of input is correct.. str is needed.")


if __name__ == '__main__':
    days = DateInterval("2019/01/04", "2020/03/21", sep="/").get_days_interval()
    years = DateInterval("2019/01/04", "2018/03/21", sep="/").get_years_interval()
