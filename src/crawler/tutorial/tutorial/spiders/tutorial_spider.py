#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import json

import scrapy
import time
from scrapy.loader import ItemLoader

from src.dealer.log.logger import get_logger
from ..items import NewsContext

logger = get_logger("TutorialSpider")

class TutorialSpider(scrapy.Spider):
    name = "tutorial"
    task_domain = "www.bbc.com"

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

            logger.info(json.dumps(dict(loader.load_item())))
            return loader.load_item()
