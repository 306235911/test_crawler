#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class BaseSpider(scrapy.Spider):

    def start_hook(self):
        runner = CrawlerRunner()
        d = runner.crawl(self.__class__)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()  # the script will block here until the crawling is finished
