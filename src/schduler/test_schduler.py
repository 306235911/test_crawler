#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from common_crawler.tutorial.tutorial.spiders.tutorial_spider import TutorialSpider

spider = TutorialSpider()
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run() # the script will block here until the spider_closed signal was sent