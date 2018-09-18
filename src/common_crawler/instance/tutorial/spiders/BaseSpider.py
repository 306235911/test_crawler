#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import scrapy
from scrapy.crawler import CrawlerProcess


class BaseSpider(scrapy.Spider):

    def start_hook(self):
        process = CrawlerProcess({
            'ITEM_PIPELINES': {'tutorial.pipelines.TutorialPipeline': 300},
            'LOG_FILE': "/home/pwx/logs/log.log",
            'DOWNLOAD_DELAY': 3,
            'LOG_LEVEL': 'INFO'

        })
        process.crawl(self.__class__)
        process.start()  # the script will block here until the crawling is finished
