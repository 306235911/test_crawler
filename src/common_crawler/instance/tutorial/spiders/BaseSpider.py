#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class BaseSpider(scrapy.Spider):

    def start_hook(self):
        settings_file_path = 'common_crawler.instance.tutorial.settings'  # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        process = CrawlerProcess(get_project_settings())
        process.crawl(self.__class__)
        process.start()  # the script will block here until the crawling is finished
