#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import json

import happybase
import jieba
import nltk
from gensim import corpora
from gensim.matutils import corpus2dense
from nltk.cluster import KMeansClusterer


def to_hbase():
    connection = happybase.Connection('localhost', autoconnect=False)
    connection.open()
    table = connection.table('testtable')
    title_list = []
    for key, data in table.scan():
        jdata = json.loads(data[b'cf1:'].decode(encoding='utf-8'))
        split_word(jdata["content"])
        if "<h1 " in jdata['title']:
            table.delete(key)
            print("bad title del...")
        else:
            title_list.append(jdata['title'])
    spilted_words = split_word(title_list)
    # 利用 gensim 库构建文档-词项矩阵
    dictionary = corpora.Dictionary(spilted_words)
    word_count = [dictionary.doc2bow(text) for text in spilted_words]
    dtm_matrix = corpus2dense(word_count, len(dictionary))
    km = KMeansClusterer(num_means=3, distance=nltk.cluster.util.euclidean_distance)
    km.cluster(dtm_matrix)
    for i in dtm_matrix:
        print(i, km.classify(i))



def split_word(titles):
    # 加载停用词
    with open("/home/pwx/stopwords/中文停用词表.txt") as f:
        read = f.read()
        stop_words = read.splitlines()
    stop_words = read.splitlines()
    texts = []
    for i in titles:
        title_seg = []
        segs = jieba.cut(i)  # 分词处理
        for seg in segs:
            if seg not in stop_words:  # 过滤停用词
                title_seg.append(seg)
        texts.append(title_seg)
    return texts


if __name__ == "__main__":
    to_hbase()
