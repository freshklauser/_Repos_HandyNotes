# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2020-03-31 20:03:30
# @Last Modified by:   sniky-lyu
# @Last Modified time: 2020-03-31 20:32:16


import os
import time
import logging
import logging.handlers


class LoggerHelper:
    """docstring for LoggerHelper"""

    def __init__(self, logger_name, dir_name='logs'):
        super(LoggerHelper, self).__init__()
        self.logger_name = logger_name
        self.dir_name = dir_name
        # 创建logs文件夹（不存在的话）
        self.__create_directory()

    def set_logger(self):
        # 创建一个logger, 指定logger的名字为 self.logger_name
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件 FileHandler or RotatingFileHandler(可设置maxBytes和backupCount) or TimeRotatingFileHandler
        # fh = logging.FileHandler(filename, mode="a")
        # 循环日志文件handler，log文件限制大小10M，以模块功能和日期(年月日)命名，备份数量1，utf-8编码
        filename = os.path.join(os.getcwd(), '{}/{}-{}.log'.format(self.dir_name,
                                                                   self.logger_name,
                                                                   time.strftime('%Y%m%d', time.localtime())))
        file_handler = logging.handlers.RotatingFileHandler(filename, mode="a", maxBytes=10485760, backupCount=1, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('\n%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s -\n%(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # 记录一条日志
        # logger.info('hello world, i\'m log helper in python, may i help you')
        return logger

    def __create_directory(self):
        dir_abspath = os.path.join(os.getcwd(), self.dir_name)        # 路径连接
        print(os.getcwd(), dir_abspath)
        try:
            if not os.path.exists(dir_abspath):
                os.mkdir(dir_abspath)
                # print('%s 文件夹创建成功' % self.dir_name)
            else:
                # print('%s 文件夹已经存在' % self.dir_name)
                pass
            dir_status = 0
        except Exception as e:
            print(e)
            dir_status = 1
        return dir_status


if __name__ == '__main__':
    logger_name = 'test-logger'
    helper = LoggerHelper(logger_name)
    logger = helper.set_logger()
    logger.info('sssssssssssss')
    logger.debug('debug test')
    logger.warn('warn test')
    logger.error('error test')
