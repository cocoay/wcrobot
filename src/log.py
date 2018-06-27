#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
# 不会自动导入子模块
from logging.handlers import RotatingFileHandler
import sys
import os
from constant import log_path, maxBytes

# 判断文件是否存在，不存在就创建
if not os.path.exists(log_path):
    os.system(log_path)

# 日志级别
FATAL = logging.FATAL
ERROR = logging.ERROR
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG

# doc：http://python.jobbole.com/86887/


def gen_logger(name, level=INFO):
    # 初始化
    logger = logging.getLogger(name)
    # level
    logger.level = level
    # 输出格式化
    fmt = '%(asctime)s %(name)s %(levelname)s %(funcName)s: %(message)s'
    formatter = logging.Formatter(fmt)
    # handler
    file_handler = RotatingFileHandler(log_path, maxBytes=maxBytes)
    file_handler.formatter = formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    # 增加handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def main():
    logger = gen_logger("logger.py")
    logger.info("测试logger")


if __name__ == '__main__':
    main()
