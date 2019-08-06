# -*- encoding: utf-8 -*-

import os
from document import document
from datasketch import MinHashLSHForest
import config, utils
from sklearn.externals import joblib
import unicodedata
import sys




class duplicate_docs:
    def __init__(self):
        self.lsh = MinHashLSHForest(num_perm=config.LSH_CONFIG['num_permutation'])


    def load(self, model):
        print('loading %s ...' % (model))
        if os.path.isfile(model):
            return joblib.load(model)
        else:
            return None


    def save(self, model, path):
        print('saving %s ...' % (path))
        joblib.dump(model, path)
        return


    # load data from list documents
    def run(self, docs):
        count = 1
        for itemid, content in docs.items():
            try:
                doc = document(content)
                self.insert(doc, key=itemid)
                print('\rpushed %d items' % (count)),
                sys.stdout.flush()
                count += 1
            except:
                pass
        self.lsh.index()
        print('')


    def run_ex(self, itemid, content, call_index=True):
        try:
            doc = document(content)
            self.insert(doc, key=itemid)
            if call_index:
                self.lsh.index()
        except:
            pass


    def query(self, doc, topn=1000):
        try:
            unicodedata.normalize('NFKC', doc)
            doc = document(doc)
            minhash = doc.get_minhash(doc.k_shingles,
                                      config.MINHASH_CONFIG['num_permutation'])
            return self.lsh.query(minhash, topn)
        except:
            return []


    # insert a document object
    # output: key if document does not exist duplicate item
    # otherwise return alert duplication.
    def insert(self, doc, key=None):
        if key is None:
            key = utils.id_generator()
        minhash = doc.get_minhash(doc.k_shingles,
                                  config.MINHASH_CONFIG['num_permutation'])
        if len(doc.k_shingles) == 0:
            return u'Does not insert this document to database.\nDocument\'s shingle = 0.\nDocument need to contain at least %d word' \
                   % (config.SHINGLE_CONFIG['k'])
        self.lsh.add(key, minhash)


    def load_model(self):
        self.lsh = self.load('model/lsh.pkl')
        self.docs = self.load('model/docs.pkl')
        self.docs_time = self.load('model/docs_time.pkl')
        if self.lsh != None and self.docs != None and self.docs_time != None:
            return True
        return False


    def save_model(self):
        utils.mkdir('model')
        self.save(self.lsh, 'model/lsh.pkl')
        self.save(self.docs, 'model/docs.pkl')
        self.save(self.docs_time, 'model/docs_time.pkl')
