# -*- encoding: utf-8 -*-

import config
import utils
import data_loader
from sklearn.externals import joblib
from preprocessing import preprocessing
from sklearn.neighbors import NearestNeighbors
from duplicate_documents.minhash_lsh import duplicate_docs as lsh
import warnings
from logger import logger
from abbreviation_map import cmnd, cccd
import unicodedata

warnings.filterwarnings('ignore', category=UserWarning)


class brain_bot:
    def __init__(self):
        self.lsh = lsh()
        self.QA_dict = {}
        self.questions = {}
        self.questions_full = {}
        self.logger = logger
        self.default_answer = u'Câu hỏi của bạn đã được chuyển đến cho tư vấn viên hỗ trợ.'

    def load_model(self):
        try:
            QA_dict = joblib.load(config.QA_DICT)
            questions = joblib.load(config.QUESTIONS)
            questions_full = joblib.load(config.QUESTIONS_FULL)
            lsh_forest = joblib.load(config.LSH_BIN)
            return QA_dict, questions, questions_full, lsh_forest
        except:
            return None, None, None, None

    def save_model(self):
        print('save model...')
        utils.mkdir(config.MODEL_DIR)
        joblib.dump(self.QA_dict, config.QA_DICT)
        joblib.dump(self.questions, config.QUESTIONS)
        joblib.dump(self.questions_full, config.QUESTIONS_FULL)
        joblib.dump(self.lsh, config.LSH_BIN)

    def push_data_to_lsh(self):
        questions = {utils.id_generator(size=8): q for q in self.QA_dict.keys()}
        self.questions = questions
        self.lsh.run(questions)

    def thinking(self, question):
        question = unicodedata.normalize('NFKC', question)
        question = preprocessing(question, tokenize=False).lower()
        question = utils.normalize_abb(question)

        if cmnd in question:
            question = utils.emphasize_token(cmnd, question, n=3)
        if cccd in question:
            question = utils.emphasize_token(cccd, question, n=3)

        # candidates = self.lsh.query(question)
        #
        # if len(candidates) == 0:
        #     return self.default_answer
        #
        # candidates_content = [self.questions[can] for can in candidates]

        candidates = self.questions.keys()
        candidates_content = self.questions.values()

        all_content = candidates_content + [question]
        vectorizer = utils.tfidf_vectorizer(all_content)
        candidates_vector = vectorizer.transform(candidates_content)
        video_query_vector = vectorizer.transform([question])

        n_neighbors = min(10, len(candidates))
        nbrs = NearestNeighbors(n_neighbors=n_neighbors,
                                leaf_size=30,
                                metric='cosine',
                                algorithm='auto')
        nbrs.fit(candidates_vector)

        distances, indices = nbrs.kneighbors(video_query_vector)

        if distances[0][0] > config.DISTANCE_THRESHOLD:
            return self.default_answer

        # for debugging
        x = []
        xx = []
        for i in xrange(n_neighbors):
            x.append(self.questions_full[candidates_content[indices[0][i]]])
            xx.append(candidates_content[indices[0][i]])

        related_question = self.questions_full[candidates_content[indices[0][0]]]
        # self.logger.info('question: %s\nrelated_question: %s' % (question, related_question))

        answer = self.QA_dict[candidates_content[indices[0][0]]]

        # return u'\n'.join([related_question, answer])
        return answer

    def run(self):
        QA_dict, questions, question_full, lsh_forest = self.load_model()
        if QA_dict is None or questions is None or \
                question_full is None or lsh_forest is None:
            self.QA_dict = data_loader.load_casual_data(config.CASUAL_DATASET)

            for q in self.QA_dict.keys():
                self.questions_full.update({q: q})

            pattern, question_full = data_loader.load_business_data(config.BUSINESS_DATASET)
            self.QA_dict.update(pattern)

            self.questions_full.update(question_full)

            self.push_data_to_lsh()
            self.save_model()
        else:
            self.QA_dict = QA_dict
            self.questions = questions
            self.questions_full = question_full
            self.lsh = lsh_forest
