#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import json

import happybase
import jieba
from jieba import posseg
from collections import Counter


def to_hbase():
    connection = happybase.Connection('localhost', autoconnect=False)
    connection.open()
    table = connection.table('testtable')
    title_list = []
    for key, data in table.scan():
        # print(key.decode("utf-8"))
        jdata = json.loads(data[b'cf1:'].decode(encoding='utf-8'))
        # print(jdata)
        # split_word(jdata["content"])
        if "<h1 " in str(jdata['title']):
            table.delete(key)
            print("bad title del...")
        else:
            title_list.append(jdata["title"])
    print(title_list)
    print(len(title_list))

def split_word(content):
    # 加载停用词
    with open("/home/pwx/stopwords/中文停用词表.txt") as f:
        read = f.read()
        stop_words = read.splitlines()

    review_segs = []
    # 创建空列表 review_seg 用于存放每条评论的分词结果
    review_seg = []
    segs = jieba.cut(content)
    for seg in segs:
        if seg not in stop_words:
            # 对于每条评论分词后的词汇，如果不在停用词表中就添加到该条评论的分词列表中，也就是说，如果是停用词就过滤掉
            review_seg.append(seg)
    # 将每条评论的分词结果添加到列表 review_segs 中
    review_segs.append(review_seg)
    print(review_segs)
    review_pos = []
    for a, b in posseg.lcut(content):
        if a not in stop_words:
            review_pos.append((a, b))
    review_n = []
    review_a = []
    for i in review_pos:
        # 分别存储名词和形容词
        if i[1] == "n":
            review_n.append(i[0])
        elif i[1] == "a":
            review_a.append(i[0])
    c1 = Counter(review_n)
    for i in c1.most_common(5):
        print(i[0], i[1])
    c2 = Counter(review_a)
    for i in c2.most_common(5):
        print(i[0], i[1])


if __name__ == "__main__":
    to_hbase()
