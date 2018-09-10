#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong

import scrapy


class TutorialSpider(scrapy.Spider):
    name = "tutorial"

    def start_requests(self):
        urls = [
            'https://www.bbc.com/zhongwen/simp'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for i in response.css(".title-link").re(r'.+?chinese-news.+|.+?world-.+?|.+?business-.+?'):
            print(i)