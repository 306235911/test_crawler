#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class BaseSpider(scrapy.Spider):

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "ITEM_PIPELINES": {
            'common_crawler.instance.tutorial.pipelines.TutorialPipeline': 300,
        },
        "LOG_FILE": "/home/pwx/logs/log.log",
        # "LOG_LEVEL": "INFO"
    }

    def start_hook(self):
        process = CrawlerProcess(get_project_settings())
        process.crawl(self.__class__)
        process.start()
