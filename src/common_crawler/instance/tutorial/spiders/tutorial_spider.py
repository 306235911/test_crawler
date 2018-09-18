#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong

import time

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings

from common_crawler.instance.tutorial.items import NewsContext
from dealer.log.logger import get_logger

logger = get_logger("TutorialSpider")


class TutorialSpider(scrapy.Spider):
    name = "tutorial"
    task_domain = "www.bbc.com"
    logger.info("start tutorial spider")

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

    @staticmethod
    def start_hook(name):
        process = CrawlerProcess(get_project_settings())
        process.crawl(name)
        process.start()  # the script will block here until the crawling is finished


if __name__ == '__main__':
    TutorialSpider.start_hook("tutorial")
