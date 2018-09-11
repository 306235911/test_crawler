# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        """
        called when the spider is opened.
        :param spider:
        :return:
        """
        pass

    def close_spider(self, spider):
        """
        called when the spider is closed.
        :param spider:
        :return:
        """
        pass