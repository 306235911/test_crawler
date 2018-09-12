#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import json

from kafka import KafkaConsumer, TopicPartition


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
    tp = TopicPartition(kafka_topic, 0)
    consumer.assign([tp])
    consumer.seek_to_end(tp)
    lastOffset = consumer.position(tp)
    consumer.assignment()
    # consumer.seek_to_beginning(tp)
    for msg in consumer:
        print(msg.topic)
        print(msg.partition)
        print(msg.offset)
        print(msg.key)
        print(msg.value)
        if msg.offset == lastOffset - 1:
            break

consumer()