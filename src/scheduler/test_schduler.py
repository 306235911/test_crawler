#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from common_crawler.instance.tutorial.spiders.tutorial_spider import TutorialSpider

process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl(TutorialSpider)
process.start() # the script will block here until the crawling is finished