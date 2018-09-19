#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import importlib
import time
import traceback
from multiprocessing import Process

from redis import Redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dealer.log.logger import get_logger

logger = get_logger("worker")
redis = Redis(host="localhost", port=6379, db=1)


def worker(spider):
    pass


def up_worker():
    def run_task(task_class):
        try:
            process = CrawlerProcess(get_project_settings())
            process.crawl(task_class)
            process.start()
        except Exception as e:
            logger.error(traceback.format_exc())

    redis_task_queue = "crawler:task:queue"
    while (True):
        interval = 10
        task = redis.lpop(redis_task_queue)
        if task:
            logger.info("worker get task")
            spider_class = importlib.import_module(task.decode("utf-8").rsplit(".", 1)[0])
            spider = getattr(spider_class, task.decode("utf-8").rsplit(".", 1)[1])()
            # process = CrawlerProcess(get_project_settings())
            # process.crawl(spider)
            # process.start()
            p = Process(target=run_task, args=(spider,))
            p.start()
            p.join()
            logger.info("task finished")
            # worker(spider)
            interval = 1
        logger.info("sleep %d s" % interval)
        time.sleep(interval)


if __name__ == '__main__':
    up_worker()
