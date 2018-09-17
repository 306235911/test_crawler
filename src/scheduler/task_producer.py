#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import importlib

import time
from redis import Redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dealer.log.logger import get_logger

logger = get_logger("task_producer")
redis = Redis(host="localhost", port=6379, db=1)


def worker(spider):
    crawler_prosecc = CrawlerProcess(get_project_settings())
    crawler_prosecc.crawl(spider)
    logger.info("start spider %s" % spider.__class__.__name__)
    crawler_prosecc.start()  # the script will block here until the crawling is finished


def up_worker():
    redis_task_queue = "crawler:task:queue"
    while (True):
        interval = 10
        task = redis.lpop(redis_task_queue)
        if task:
            logger.info("worker get task")
            spider_class = importlib.import_module(task.rsplit(".", 1)[0])
            spider = getattr(spider_class, task.rsplit(".", 1)[1])()
            worker(spider)
            interval = 1
        logger.info("sleep %d s" % interval)
        time.sleep(interval)


if __name__ == '__main__':
    up_worker()
