#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import importlib
import time
import traceback

from redis import Redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from common_crawler.instance.tutorial.spiders.tutorial_spider import TutorialSpider
from dealer.log.logger import get_logger

logger = get_logger("worker")
redis = Redis(host="localhost", port=6379, db=1)


def worker(spider):

    pass


def up_worker():
    redis_task_queue = "crawler:task:queue"
    process = CrawlerProcess(get_project_settings())
    try:
        while (True):
            interval = 10
            task = redis.lpop(redis_task_queue)
            if task:
                logger.info("worker get task")
                spider_class = importlib.import_module(task.decode("utf-8").rsplit(".", 1)[0])
                spider = getattr(spider_class, task.decode("utf-8").rsplit(".", 1)[1])()
                process.crawl(spider)
                process.start(stop_after_crawl=False)
                # worker(spider)
                interval = 1
            logger.info("sleep %d s" % interval)
            time.sleep(interval)
    except Exception:
        process.stop()
        logger.error(traceback.format_exc())
    finally:
        if process:
            process.stop()


if __name__ == '__main__':
    up_worker()
