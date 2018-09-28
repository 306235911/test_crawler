#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import json

import happybase
import jieba
from gensim import corpora, models
from gensim.similarities import MatrixSimilarity, Similarity
from gensim.test.utils import get_tmpfile, common_dictionary, common_corpus


def to_hbase():
    connection = happybase.Connection('localhost', autoconnect=False)
    connection.open()
    table = connection.table('testtable')
    title_list = []

    # 提取标题列表
    for key, data in table.scan():
        jdata = json.loads(data[b'cf1:'].decode(encoding='utf-8'))
        split_word(jdata["content"])
        if "<h1 " in jdata['title']:
            table.delete(key)
            print("bad title del...")
        elif "路透仅提供中文标题" in jdata["content"] or "路透中文快讯将暂不做进一步报导" in jdata["content"]:
            table.delete(key)
            print("bad content del...")
        else:
            title_list.append(jdata['content'])
    print("content length: %s" % len(title_list))
    # 分词，停用词
    spilted_words = split_word(title_list)

    # 计算 TF-IDF 矩阵
    dictionary = corpora.Dictionary(spilted_words)
    text = [dictionary.doc2bow(words) for words in spilted_words]
    tfidf_model = models.TfidfModel(text)
    text_tfidf = tfidf_model[text]
    # 构建 LSI 模型，计算文本相似度
    # todo:Similarity -> MatrixSimilarity
    # Similarity 用于从文件中读取索引，因此既然这里已经把content读到ram，可以直接用 MatrixSimilarity
    # index_tmpfile = get_tmpfile("index")
    # sim_index = Similarity(text_tfidf, common_corpus, num_features=len(common_dictionary))

    sim_index = MatrixSimilarity(text_tfidf)
    print(sim_index[text_tfidf[-1]])
    print(list(enumerate(sim_index[text_tfidf[-1]])))
    sort_sims = sorted(enumerate(sim_index[text_tfidf[-1]]), key=lambda item: item[1], reverse=True)
    print(sort_sims[0:10])
    for j in [i[0] for i in sort_sims[0:10]]:
        print(j, "\n", title_list[j])


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
