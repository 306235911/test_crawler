#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import time

# from apscheduler.schedulers.blocking import BlockingScheduler
# from pytz import utc
from redis import Redis

from dealer.log.logger import get_logger

logger = get_logger("test_scheduler")
redis = Redis(host="localhost", port=6379, db=1)


def get_task():
    raw_task_key = "crawler:task"
    redis_task_queue = "crawler:task:queue"

    while (True):
        interval = 10
        rst_list = redis.zrange(raw_task_key, 0, -1, withscores=True)
        timestamp = int(time.time())
        logger.info("get task length: %d" % len(rst_list))
        for task_withscores in rst_list:
            spider_class = task_withscores[0].decode("utf-8")
            socre = int(task_withscores[1])
            if timestamp > socre:
                logger.info("put class %s to running queue" % spider_class)
                redis.lpush(redis_task_queue, spider_class)
                redis.zadd(raw_task_key, spider_class, timestamp + 3600 * 6)
                interval = 1
        logger.info("sleep %d s" % interval)
        time.sleep(interval)


# 定时调度
# def up_process():
#     sched = BlockingScheduler(timezone=utc)
#     sched.add_job(func=get_task, trigger='cron', second='0', minute='*/10', hour='*/6')
#     sched.start()


if __name__ == '__main__':
    get_task()
