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

"""
    twisted 本身是多线程的，所以在外层使用多线程会 raise Exception，所以这里不用线程池
"""


def worker(spider):
    pass


# def run_task(task_class):
#     try:
#         process = CrawlerProcess(get_project_settings())
#         process.crawl(task_class)
#         process.start()
#     except Exception as e:
#         logger.error(traceback.format_exc())


def up_worker():
    def run_task(task_class):
        try:
            process = CrawlerProcess(get_project_settings())
            process.crawl(task_class)
            process.start()
        except Exception as e:
            logger.error(traceback.format_exc())

    redis_task_queue = "crawler:task:queue"
    spider_list = []
    while (True):
        interval = 10
        task = redis.lpop(redis_task_queue)
        if task:
            logger.info("worker get task")
            spider_class = importlib.import_module(task.decode("utf-8").rsplit(".", 1)[0])
            spider = getattr(spider_class, task.decode("utf-8").rsplit(".", 1)[1])()
            spider_list.append(spider)
            interval = 1
            # reactor不允许 restart，所以通过子进程跑
            # 判断若没有任务或pool已满就开跑一波

            # twisted 本身是多线程的，所以在外层使用多线程会 raise Exception，所以这里
            # if (interval == 10 and len(spider_list) > 0) or len(spider_list) == 2:
            #     pool = Pool(2)
            #     # 只能 pickle top-level 的方法
            #     pool.map(run_task, spider_list)
            #     pool.close()
            #     pool.join()
            # 可调用本地方法
            p = Process(target=run_task, args=(spider,))
            p.start()
            p.join()
            logger.info("task finished")
            # worker(spider)
            spider_list = []
        logger.info("sleep %d s" % interval)
        time.sleep(interval)


if __name__ == '__main__':
    up_worker()
