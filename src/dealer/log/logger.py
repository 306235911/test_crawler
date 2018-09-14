#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import logging
from logging.handlers import TimedRotatingFileHandler, WatchedFileHandler

LOGGER_FILE_PATH = "/home/pwx/log/"
LOGGER_FORMAT = '[%(asctime)s] [%(name)s:%(lineno)d] [%(levelname)s] %(message)s'

def get_logger(name):
    logger = logging.getLogger(name)
    if logger and logger.handlers:
        return logger
    logger = logging.getLogger(name=name)
    if logger and logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    logger.info('use default logger level: DEBUG')
    logger.propagate = False
    # file_handler = logging.FileHandler(config.LOGGER_FILE_PATH)
    if name == "heartbeat.py":
        logger.info("get heartbeat.py handler")
        # 因为需要在规定的日志滚动时间 when 时有写日志的操作才会发生日志滚动，所以选常写日志的默认 heartbeat 进程使用 TimedRotating
        file_handler = TimedRotatingFileHandler(LOGGER_FILE_PATH, when="MIDNIGHT", interval=1, backupCount=5)
    else:
        # 除heartbeat进程外其他进程的logger使用WatchedFileHandler防止多次滚动日志文件
        file_handler = WatchedFileHandler(LOGGER_FILE_PATH)
    file_handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
    logger.addHandler(file_handler)
    return logger
