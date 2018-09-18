#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class BaseSpider(scrapy.Spider):

    def start_hook(self):
        process = CrawlerProcess(get_project_settings())
        process.crawl(self.__class__)
        process.start()
