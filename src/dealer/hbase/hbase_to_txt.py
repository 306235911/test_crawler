#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import json

import gensim
import happybase
import jieba
import nltk
from gensim import corpora, models
from gensim.matutils import corpus2dense
from gensim.similarities import MatrixSimilarity
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
    dictionary = corpora.Dictionary(spilted_words)
    text = [dictionary.doc2bow(words) for words in spilted_words]
    tfidf_model = models.TfidfModel(text)
    text_tfidf = tfidf_model[text]
    # 构建 LSI 模型，计算文本相似度
    sim_index = MatrixSimilarity(text_tfidf)
    print(sim_index[text_tfidf[0]])
    print(list(enumerate(sim_index[text_tfidf[0]])))
    sort_sims = sorted(enumerate(sim_index[text_tfidf[0]]), key=lambda item: item[1], reverse=True)
    print(sort_sims[0:10])
    for j in [i[0] for i in sort_sims[0:10]]:
        print(j, "\n", title_list[j])



    # 利用 gensim 库构建文档-词项矩阵
    # todo:改成词向量
    # dictionary = corpora.Dictionary(spilted_words)
    # word_count = [dictionary.doc2bow(text) for text in spilted_words]
    # dtm_matrix = corpus2dense(word_count, len(dictionary))
    # km = KMeansClusterer(num_means=3, distance=nltk.cluster.util.euclidean_distance)
    # km.cluster(dtm_matrix)
    # for i in dtm_matrix:
    #     print(i, km.classify(i))



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
