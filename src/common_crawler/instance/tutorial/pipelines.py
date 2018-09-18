# -*- coding: utf-8 -*-

import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback

from kafka import KafkaProducer
from redis import Redis
import hashlib

# todo:从配置读
from dealer.log.logger import get_logger

redis = Redis(host="localhost", port=6379,
              db=1)
logger = get_logger("piplines.py")


class TutorialPipeline(object):

    def __init__(self):
        self.producer = None

    def process_item(self, item, spider):

        # 去重
        domain = item["domain"][0]
        md5_domain = hashlib.md5(domain.encode()).hexdigest()
        md5_url = hashlib.md5(item["url"][0].encode()).hexdigest()
        unique_prefix = "unique:url:"
        if redis.sismember(unique_prefix+md5_domain, item["url"][0]):
            logger.warn("重复的url")
            return
        redis.sadd(unique_prefix+md5_domain, item['url'][0])
        item["id"] = md5_url

        # 写入kafka
        # todo:从配置读取
        try:
            topic = "test"
            item = dict(item)
            # 指定了用来序列化消息记录的类，如果有key的话还可以指定一个用来序列化key的类(方法?)key_serializer
            self.producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            self.producer.send(topic, item)
        except Exception as e:
            logger.info("error item: " + str(item))
            logger.error(traceback.print_exc())
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
