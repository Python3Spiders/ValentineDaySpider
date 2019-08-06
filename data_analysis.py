# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_time:      2019/8/3 21:34
# file_name:        data_analysis.py
# github            https://github.com/inspurer
# qq邮箱            2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

import pandas as pd

import jieba

df = pd.read_csv("answers.csv")

def chinese_word_cut(text):
    return " ".join(jieba.cut(text))

df["answer"] = df.answer.apply(chinese_word_cut)


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# 向量化
n_features = 1000

tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features=n_features,
                                stop_words='english',
                                max_df = 0.5,
                                min_df = 10)
tf = tf_vectorizer.fit_transform(df.answer)

from sklearn.decomposition import LatentDirichletAllocation

n_topics = 5
# LDA 处理
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)

lda.fit(tf)

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % topic_idx)
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

n_top_words = 20
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)

import pyLDAvis
import pyLDAvis.sklearn

data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)


pyLDAvis.show(data)#可视化主题模型