# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/6 22:26
# @FileName : logger.py
# @SoftWare : PyCharm

import os
import logging
import logging.config as log_conf
import datetime
import coloredlogs

from utils.general import standard_path

log_dir = os.path.realpath(os.path.dirname(os.path.dirname(__file__)) + os.sep + 'logs')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
today = datetime.datetime.now().strftime("%Y%m%d")

log_path = standard_path(log_dir, 'spider_{today}.log'.format(today=today))
log_path_method_helper = standard_path(log_dir, 'method_{today}.log'.format(today=today))

log_config = {
    'version': 1.0,
    'formatters': {
        'colored_console': {'()': 'coloredlogs.ColoredFormatter',
                            'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 'datefmt': '%H:%M:%S'},
        'detail': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"  # 如果不加这个会显示到毫秒。
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',  # 日志打印到屏幕显示的类。
            'level': 'INFO',
            'formatter': 'colored_console'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',  # 日志打印到文件的类。
            'maxBytes': 1024 * 1024 * 1024,  # 单个文件最大内存
            'backupCount': 1,  # 备份的文件个数
            'filename': log_path,  # 日志文件名
            'level': 'INFO',  # 日志等级
            'formatter': 'detail',  # 调用上面的哪个格式
            'encoding': 'utf-8',  # 编码
        },
        'file_helper': {
            'class': 'logging.handlers.RotatingFileHandler',  # 日志打印到文件的类。
            'maxBytes': 1024 * 1024 * 1024,  # 单个文件最大内存
            'backupCount': 1,  # 备份的文件个数
            'filename': log_path_method_helper,  # 日志文件名
            'level': 'INFO',  # 日志等级
            'formatter': 'detail',  # 调用上面的哪个格式
            'encoding': 'utf-8',  # 编码
        },
    },
    'loggers': {
        'crawler': {
            'handlers': ['console', 'file'],  # 只打印屏幕
            'level': 'DEBUG',  # 只显示错误的log
        },
        'parser': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'other': {
            'handlers': ['console', 'file_helper'],
            'level': 'INFO',
        },
        'storage': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
}

log_conf.dictConfig(log_config)

crawler = logging.getLogger('crawler')
storage = logging.getLogger('storage')      # 数据库日志
helper = logging.getLogger('other')      # 方法相关的理解日志
coloredlogs.install(level='DEBUG', logger=crawler)
coloredlogs.install(level='DEBUG', logger=storage)
