# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from kafka import KafkaProducer

class TutorialPipeline(object):

    def __init__(self):
        self.producer = None


    def process_item(self, item, spider):
        # todo:从配置读取
        topic = "test"
        self.producer.send(topic, )
        return item

    def open_spider(self, spider):
        """
        called when the spider is opened.
        :param spider:
        :return:
        """
        self.producer = KafkaProducer(bootstrap_servers='localhost:9002')

    def close_spider(self, spider):
        """
        called when the spider is closed.
        :param spider:
        :return:
        """
        pass