#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong

import time

import scrapy
from scrapy.loader import ItemLoader

from common_crawler.BaseSpider import BaseSpider
from common_crawler.instance.tutorial.items import NewsContext
# from dealer.log.logger import get_logger
#
# logger = get_logger("TutorialSpider")


class TutorialSpider(BaseSpider):
    name = "tutorial"
    task_domain = "www.bbc.com"
    # logger.info("start tutorial spider")

    def start_requests(self):
        urls = [
            'https://www.bbc.com/zhongwen/simp'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for detail_link in response.css(".title-link::attr(href)").re(r'.+?chinese-news.+|.+?world-.+|.+?business-.+'):
            yield response.follow(detail_link, self.parse_detail)
            # break

    def parse_detail(self, response):
        title = response.css(".story-body h1::text")
        content = "".join(response.css('div[property=articleBody] p::text').extract())
        if title and content:
            loader = ItemLoader(item=NewsContext(), response=response)
            loader._add_value("url", response.url)
            loader._add_value("title", title)
            loader._add_value("content", content)
            loader.add_value("date", int(time.time()))
            loader.add_value("domain", self.task_domain)
            return loader.load_item()

aa = TutorialSpider()
aa.start_hook(aa)