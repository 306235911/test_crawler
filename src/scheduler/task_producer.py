#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import importlib

import time

import os
from redis import Redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dealer.log.logger import get_logger

logger = get_logger("worker")
redis = Redis(host="localhost", port=6379, db=1)
settings_file_path = 'common_crawler.instance.tutorial.settings'  # The path seen from root, ie. from main.py
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
settings = get_project_settings()
crawler_process = CrawlerProcess(settings)


def worker(spider):
    crawler_process.crawl(spider)
    logger.info("start spider %s" % spider.__class__.__name__)
    crawler_process.start()  # the script will block here until the crawling is finished


def up_worker():
    redis_task_queue = "crawler:task:queue"
    while (True):
        interval = 10
        task = redis.lpop(redis_task_queue)
        if task:
            logger.info("worker get task")
            spider_class = importlib.import_module(task.decode("utf-8").rsplit(".", 1)[0])
            spider = getattr(spider_class, task.decode("utf-8").rsplit(".", 1)[1])()
            worker(spider)
            interval = 1
        logger.info("sleep %d s" % interval)
        time.sleep(interval)


if __name__ == '__main__':
    up_worker()
