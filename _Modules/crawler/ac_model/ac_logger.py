# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/6 22:26
# @FileName : ac_logger.py
# @SoftWare : PyCharm

import os
import logging
import logging.config as log_conf
import datetime
import coloredlogs


def standard_path(root, relative_path):
    return os.path.realpath(os.path.join(root, relative_path))


log_dir = os.path.realpath(os.path.dirname(os.path.dirname(__file__)) + os.sep + 'logs')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
today = datetime.datetime.now().strftime("%Y%m")

process_path = standard_path(log_dir, 'frame_{today}.process.log'.format(today=today))   # 过程级别：中等
users_path = standard_path(log_dir, 'frame_{today}.users.log'.format(today=today))        # 用户级别：简单
debugs_path = standard_path(log_dir, 'frame_{today}.debugs.log'.format(today=today))     # 代码级别：详细

log_config = {
    'version': 1.0,

    'formatters': {
        'colored_console': {
            '()': 'coloredlogs.ColoredFormatter',
            'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            'datefmt': '%H:%M:%S'
        },
        'detail': {
            'format': '%(asctime)s - %(name)s - %(thread)d - %(module)s - %(lineno)d - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'middle': {
            'format': '%(asctime)s - %(name)s - %(thread)d - %(module)s - %(lineno)d - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },

    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',                   # 日志打印到屏幕显示的类。
            'level': 'INFO',
            'formatter': 'colored_console'
        },
        'process_handler': {
            'class': 'logging.handlers.RotatingFileHandler',    # 日志打印到文件的类。
            'maxBytes': 1024 * 1024 * 1024,                     # 单个文件最大内存
            'backupCount': 1,                                   # 备份的文件个数
            'filename': process_path,                           # 日志文件名
            'level': 'INFO',                                    # 日志等级
            'formatter': 'middle',                              # 调用上面的哪个格式
            'encoding': 'utf-8'                                 # 编码
        },
        'users_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 1024,
            'backupCount': 1,
            'filename': users_path,
            'level': 'INFO',
            'formatter': 'simple',
            'encoding': 'utf-8'
        },
        'debugs_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 1024,
            'backupCount': 1,
            'filename': debugs_path,
            'level': 'DEBUG',
            'formatter': 'detail',
            'encoding': 'utf-8'
        },
    },

    'loggers': {
        'process': {
            'handlers': ['process_handler'],  # 只打印屏幕
            'level': 'DEBUG',  # 只显示错误的log
        },
        'debugs': {
            'handlers': ['debugs_handler'],
            'level': 'DEBUG',
        },
        'users': {
            'handlers': ['users_handler', 'console_handler'],
            'level': 'INFO',
        }
    }
}

log_conf.dictConfig(log_config)

process_logger = logging.getLogger('process')
users_logger = logging.getLogger('users')
debugs_logger = logging.getLogger('debugs')
coloredlogs.install(level='INFO', logger=users_logger)
