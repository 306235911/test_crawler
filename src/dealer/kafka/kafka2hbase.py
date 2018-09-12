#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import json

from kafka import KafkaConsumer

def consumer():
    # 获取数据的kafka topic
    kafka_topic = "test"
    # kafka 的节点
    bootstrap_servers = ["localhost:9092"]
    # 为kafka动态分区所用到的group name
    group_id = "test_group"
    # 用于反序列化数据的方法
    # value_deserializer = lambda v: json.dumps(v)
    # kafka读取数据时最小的返回数据量
    # fetch_min_bytes = 1
    consumer = KafkaConsumer(kafka_topic, bootstrap_servers=bootstrap_servers)
    for msg in consumer:
        print(msg.topic)
        print(msg.partition)
        print(msg.offset)
        print(msg.key)
        print(msg.value)

consumer()