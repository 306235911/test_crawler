#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import time

import scrapy
from scrapy.loader import ItemLoader

from common_crawler.instance.tutorial.items import NewsContext
from common_crawler.instance.tutorial.spiders.BaseSpider import BaseSpider
from dealer.log.logger import get_logger

logger = get_logger("reuters")


class ReutersSpider(BaseSpider):
    name = "reuters"
    task_domain = "cn.reuters.com"
    logger.info("start reuters spider")

    def start_requests(self):
        urls = [
            'https://cn.reuters.com'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for detail_link in response.css(".story-content a").re(r'.+?/article/.+'):
            print(detail_link)
            # yield response.follow(detail_link, self.parse_detail)
            # break

    def parse_detail(self, response):
        title = response.css(".story-body h1::text").extract()
        content = "".join(response.css('div[property=articleBody] p::text').extract())
        if title and content:
            loader = ItemLoader(item=NewsContext(), response=response)
            loader._add_value("url", response.url)
            loader._add_value("title", title)
            loader._add_value("content", content)
            loader.add_value("date", int(time.time()))
            loader.add_value("domain", self.task_domain)
            return loader.load_item()


if __name__ == '__main__':
    aa = ReutersSpider()
    aa.start_hook()
