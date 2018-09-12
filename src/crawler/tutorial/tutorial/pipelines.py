# -*- coding: utf-8 -*-

import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from kafka import KafkaProducer
from redis import Redis
import hashlib

# todo:从配置读
redis = Redis(host="localhost", port=6379,
              db=1)


class TutorialPipeline(object):

    def __init__(self):
        self.producer = None

    def process_item(self, item, spider):

        # 去重
        domain = item["domain"][0]
        md5 = hashlib.md5()
        md5.update(domain)
        md5_domain = md5.hexdigest()
        unique_prefix = "unique:url:"
        if redis.sismember(unique_prefix+md5_domain, item["url"]):
            # todo:log
            print("重复的url")
            return
        redis.sadd(unique_prefix+md5_domain, item['url'])

        # 写入kafka
        # todo:从配置读取
        try:
            topic = "test"
            item = json.dumps(dict(item))
            self.producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            self.producer.send(topic, item)
        except Exception as e:
            print(e)
            self.producer.close()
        return item

    def open_spider(self, spider):
        """
        called when the spider is opened.
        :param spider:
        :return:
        """
        # 连接kafka
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')

    def close_spider(self, spider):
        """
        called when the spider is closed.
        :param spider:
        :return:
        """
        if self.producer:
            self.producer.close()
