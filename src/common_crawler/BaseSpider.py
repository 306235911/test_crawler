#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import scrapy
from scrapy.crawler import CrawlerProcess


class BaseSpider(scrapy.Spider):

    def start_hook(self, spider_class):
        process = CrawlerProcess()
        process.crawl(spider_class)
        process.start()
