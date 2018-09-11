#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong

import scrapy

from src.crawler.tutorial.tutorial.items import NewsContext


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
        def extract_with_css(query):
            return response.css(query).extract_first(default="").strip()

        news = NewsContext(url=response.url, title=extract_with_css('.story-body h1::text'), content="".join(response.css('div[property=articleBody] p::text').extract(default="")))
        yield {
            news
        }
