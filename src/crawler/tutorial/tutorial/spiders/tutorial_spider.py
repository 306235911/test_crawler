#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong

import scrapy
import time
from scrapy.loader import ItemLoader

from ..items import NewsContext


class TutorialSpider(scrapy.Spider):
    name = "tutorial"

    def start_requests(self):
        urls = [
            'https://www.bbc.com/zhongwen/simp'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for detail_link in response.css(".title-link::attr(href)").re(r'.+?chinese-news.+|.+?world-.+|.+?business-.+'):
            yield response.follow(detail_link, self.parse_detail)
            break

    def parse_detail(self, response):
        loader = ItemLoader(item=NewsContext(), response=response)
        loader._add_value("url", response.url)
        loader.add_css("title", '.story-body h1::text')
        loader._add_value("content", "".join(response.css('div[property=articleBody] p::text').extract()))
        loader.add_value("date", int(time.time()))
        return loader.load_item()
