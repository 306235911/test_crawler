#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import utc
from redis import Redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from common_crawler.instance.tutorial.spiders.tutorial_spider import TutorialSpider
from dealer.log.logger import get_logger

logger = get_logger("test_scheduler")


def process():
    crawler_prosecc = CrawlerProcess(get_project_settings())

    crawler_prosecc.crawl(TutorialSpider)
    crawler_prosecc.start()  # the script will block here until the crawling is finished


# 定时调度
# def up_process():
#     sched = BlockingScheduler(timezone=utc)
#     sched.add_job(func=process, trigger='cron', second='0', minute='*/10', hour='*/6')
#     sched.start()
def up_process():
    redis_queue = "crawler:task:queue"
    redis = Redis(host="localhost", port=6379, db=1)
    while(True):
        task = redis.lpop(redis_queue)
        #sleep


if __name__ == '__main__':
    up_process()
