# -*- coding: utf-8 -*-
__author__ = 'nobita'

import os
from io import open
import shutil
from datetime import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from sklearn.feature_extraction.text import TfidfVectorizer
import random, string
import math
from stopwords import stopwords
from abbreviation_map import ABBREVIATION



# return list of string
def load_data_from_dict(data_file):
    d = {}
    with open(data_file, 'r', encoding='utf-8') as f:
        for data in f:
            data = data.strip(u'\n').strip().lower()
            d.update({data:True})
    return d


def load_data_from_list(data_file):
    l = []
    with open(data_file, 'r', encoding='utf-8') as f:
        for data in f:
            l.append(data.strip(u'\n').strip().lower())
    return l


def mkdir(dir):
    if (os.path.exists(dir) == False):
        try:
            os.mkdir(dir)
        except Exception as e:
            print(e.message)


def delete_dir(dir):
    ## Try to remove tree; if failed show an error using try...except on screen
    try:
        shutil.rmtree(dir)
    except OSError, e:
        print ("Error: %s - %s." % (e.filename, e.strerror))


def push_data_to_stack(stack, file_path, file_name):
    sub_folder = os.listdir(file_path)
    for element in sub_folder:
        element = file_name + '/' + element
        stack.append(element)


def update_dict_from_value(d1, d2):
    for k, v in d1.items():
        for kk, vv in v.items():
            d2[k].update({vv:kk})
    return


def string2bytearray(s):
    l = [c for c in s]
    return l


def add_to_list(l1, l2):
    l = []
    for x in l1:
        for xx in l2:
            l.append(x+xx)
    return l


def get_max(l):
    maximum = max(l)
    return (l.index(maximum), maximum)


def vector_normarize(v):
    total = sum(v)
    return map(lambda x: float(x) / float(total), v)


def connect2mongo(host, port, user, pwd, db_name):
    connection = MongoClient(host, port)
    db = connection[db_name]
    if user != '' and pwd != '':
        db.authenticate(user, pwd)
    return connection, db


def create_mongo_index(collection, field, type=u'ascending'):
    try:
        if type == u'ascending':
            collection.create_index([(field, ASCENDING)])
        else: # descending
            collection.create_index([(field, DESCENDING)])
    except Exception as e:
        print('exception raise in create_mongo_index: %s' % e.message)


def get_time_at_present():
    now = datetime.now()
    return now.strftime('%Y-%m-%dT%H:%M:%S.%f')


def convert_date_to_string(date):
    return date.strftime('%Y-%m-%d')


def get_keywords(docs, max_feature, stopwords=None):
    vectorizer = TfidfVectorizer(max_features=max_feature,
                                 min_df=3,
                                 stop_words=stopwords)
    try:
        vectorizer.fit(docs)
    except:
        vectorizer.min_df = 1
        vectorizer.max_features = 30
        vectorizer.fit(docs)
    return vectorizer.vocabulary_


def tfidf_vectorizer(list_docs):
    vectorizer = TfidfVectorizer(stop_words=stopwords)
    vectorizer.fit(list_docs)
    return vectorizer


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def is_nan(value):
    try:
        return math.isnan(value)
    except:
        return False


def get_init_value(l):
    try:
        return l[0]
    except:
        return u''


def get_bigram_content(content):
    words = content.split()
    if len(words) < 2:
        return u''
    bigram = []
    for i in xrange(len(words) - 1):
        bigram.append(words[i] + u'_' + words[i + 1])
    return u' '.join(bigram)


def normalize_abb(content):
    new_content = content
    for abb, full in ABBREVIATION.items():
        if abb not in content:
            continue
        new_content = content.replace(abb, full)
        break
    return new_content


def emphasize_token(token, question, n=3):
    new_question = question
    for i in xrange(n):
        new_question += u' ' + token
    return new_question



if __name__ == '__main__':
    ind, m = get_max([1,4,2,3,5,0])
    pass