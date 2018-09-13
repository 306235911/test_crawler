#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import json

from kafka import KafkaConsumer, TopicPartition
from redis import Redis
import happybase

redis = Redis(host="localhost", port=6379,
              db=1)


def toHbase():
    connection = happybase.Connection('localhost', autoconnect=False)
    connection.open()
    # todo:从配置读取
    table = connection.table('testtable')
    table.put("row1", {"cf1:": "1"})


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
        for msg in consumer:
            print(msg.topic)
            print(msg.partition)
            print(msg.offset)
            # print(msg.value)
            parseData(msg.value)
            break
            if msg.offset == lastOffset - 1:
                redis.set(kafka_offset_key, lastOffset)
                break

def parseData(value):
    print(json.dumps(value.decode('utf-8'))["domain"])

consumer()
