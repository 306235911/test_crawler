#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import importlib
import time

from redis import Redis

from dealer.log.logger import get_logger

logger = get_logger("worker")
redis = Redis(host="localhost", port=6379, db=1)


def worker(spider):
    pass


def up_worker():
    redis_task_queue = "crawler:task:queue"
    while (True):
        interval = 10
        task = redis.lpop(redis_task_queue)
        if task:
            logger.info("worker get task")
            spider_class = importlib.import_module(task.decode("utf-8").rsplit(".", 1)[0])
            spider = getattr(spider_class, task.decode("utf-8").rsplit(".", 1)[1])()
            spider.start_hook()
            # worker(spider)
            interval = 1
        logger.info("sleep %d s" % interval)
        time.sleep(interval)


if __name__ == '__main__':
    up_worker()
