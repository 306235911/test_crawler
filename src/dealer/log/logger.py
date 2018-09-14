#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import logging
from logging.handlers import TimedRotatingFileHandler, WatchedFileHandler

LOGGER_FILE_PATH = "/home/pwx/log/log.log"
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
    if name == "TutorialSpider":
        logger.info("get heartbeat.py handler")
        file_handler = TimedRotatingFileHandler(LOGGER_FILE_PATH, when="MIDNIGHT", interval=1, backupCount=5)
    else:
        file_handler = WatchedFileHandler(LOGGER_FILE_PATH)
    file_handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
    logger.addHandler(file_handler)
    return logger
