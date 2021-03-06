#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import json

import happybase
from kafka import KafkaConsumer, TopicPartition
from redis import Redis

from dealer.log.logger import get_logger

redis = Redis(host="localhost", port=6379,
              db=1)
logger = get_logger("toHbase.py")


def toHbase(datas):
    connection = happybase.Connection('localhost', autoconnect=False)
    connection.open()
    # todo:从配置读取
    table = connection.table('testtable')

    try:
        for jdata in datas:
            try:
                url = jdata["url"][0]
                title = jdata["title"][0]
                content = jdata["content"][0]
                date = jdata["date"][0]
                domain = jdata["domain"][0]
                data_id = jdata["id"]
                cf1 = {"url": url,
                       "title": title,
                       "content": content}
                cf2 = {"date": date}
                cf3 = {"domain": domain}
                table.put(data_id,
                          {"cf1:": json.dumps(cf1),
                           "cf2:": json.dumps(cf2),
                           "cf3:": json.dumps(cf3)})
            except Exception as e:
                logger.error(e)
    finally:
        connection.close()


def consumer():
    # 获取数据的kafka topic
    kafka_topic = "test"
    # kafka 的节点
    bootstrap_servers = ["localhost:9092"]
    # 为kafka动态分区所用到的group name
    # group_id = "test_group"
    # 用于反序列化数据的方法
    # value_deserializer = lambda v: json.dumps(v)
    # kafka读取数据时最小的返回数据量
    # fetch_min_bytes = 1
    # 一般用法，一开始指定topic
    # consumer = KafkaConsumer(kafka_topic, bootstrap_servers=bootstrap_servers)
    # 缓存的数据量大小
    cache_data = 10

    # 在后面设置topic
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)

    # todo:从redis/mysql中读取offset
    kafka_offset_key = "kafka:offset"
    kafka_offset = redis.get(kafka_offset_key)
    tp = TopicPartition(kafka_topic, 0)
    consumer.assign([tp])
    consumer.seek_to_end(tp)
    lastOffset = consumer.position(tp)

    # 若要从最新的消息消费kafka 则调用 assignment 方法
    # consumer.assignment()

    # 从最旧的数据开始消费
    # consumer.seek_to_beginning(tp)

    consumer.seek(tp, int(kafka_offset))
    if int(kafka_offset) < int(lastOffset):
        data_list = []
        for msg in consumer:
            logger.info("message topic: %s" % msg.topic)
            logger.info("message partition: %s" % msg.partition)
            logger.info("message offset: %s" % msg.offset)
            data_list.append(parseData(msg.value))

            if len(data_list) > cache_data:
                toHbase(data_list)
                data_list = []
            if msg.offset == lastOffset - 1:
                if len(data_list) > 0:
                    toHbase(data_list)
                redis.set(kafka_offset_key, lastOffset)
                break
    else:
        logger.info("no new data")


def parseData(value):
    jdata = json.loads(value.decode(encoding='utf-8'))
    return jdata


consumer()
