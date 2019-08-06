# -*- encoding: utf-8 -*-

from io import open
import pandas as pd
from preprocessing import preprocessing
import utils
import re
from abbreviation_map import cmnd, cccd
import unicodedata

normalize_space = re.compile(u' +')


def load_casual_data(data_path):
    question_signal = u'Người báo tin:'
    answer_signal = u'Chatbot:'

    QA_dict = {}

    with open(data_path, 'r', encoding='utf-8') as fp:
        flag = False
        question = None
        answer = None
        for sen in fp:
            sen = sen.strip()
            if question_signal in sen:
                flag = True
                question = sen.split(question_signal)[1]
                question = preprocessing(question, tokenize=False)
            elif answer_signal in sen and flag:
                flag = False
                answer = sen.split(answer_signal)[1]
                # answer = preprocessing(answer).lower()
                QA_dict.update({question.lower(): answer.strip()})
            else:
                continue

    return QA_dict


def load_business_data(data_path):
    patterns = {}
    question_full = {}
    df = pd.read_excel(data_path, header=0, sheet_name=u'Working Sheet đợt 1')
    for row in df.iterrows():
        try:
            data = row[1]
            question = unicodedata.normalize('NFKC', data[2])
            response = unicodedata.normalize('NFKC', data[15])
            revise = data[8]

            if utils.is_nan(revise):
                if not utils.is_nan(data[3]):
                    principal_npvp = unicodedata.normalize('NFKC', data[3]).strip()
                    principal_npvp = map(lambda x: x.strip(), principal_npvp.split(u','))
                    principal_npvp = u' '.join(principal_npvp)
                else:
                    principal_npvp = u''

                if not utils.is_nan(data[4]):
                    npvp = unicodedata.normalize('NFKC', data[4]).strip()
                    npvp = map(lambda x: x.strip(), npvp.split(u','))
                    npvp = u' '.join(npvp)
                else:
                    npvp = u''

                if not utils.is_nan(data[5]):
                    verb = unicodedata.normalize('NFKC', data[5]).strip()
                    verb = map(lambda x: x.strip(), verb.split(u','))
                    verb = u' '.join(verb)
                else:
                    verb = u''

                if not utils.is_nan(data[6]):
                    wh_question = unicodedata.normalize('NFKC', data[6]).strip()
                    wh_question = map(lambda x: x.strip(), wh_question.split(u','))
                    wh_question = u' '.join(wh_question)
                else:
                    wh_question = u''
            else:
                if not utils.is_nan(data[9]):
                    principal_npvp = unicodedata.normalize('NFKC', data[9]).strip()
                    principal_npvp = map(lambda x: x.strip(), principal_npvp.split(u','))
                    principal_npvp = u' '.join(principal_npvp)
                else:
                    principal_npvp = u''

                if not utils.is_nan(data[10]):
                    npvp = unicodedata.normalize('NFKC', data[10]).strip()
                    npvp = map(lambda x: x.strip(), npvp.split(u','))
                    npvp = u' '.join(npvp)
                else:
                    npvp = u''

                if not utils.is_nan(data[11]):
                    verb = unicodedata.normalize('NFKC', data[11]).strip()
                    verb = map(lambda x: x.strip(), verb.split(u','))
                    verb = u' '.join(verb)
                else:
                    verb = u''

                if not utils.is_nan(data[12]):
                    wh_question = unicodedata.normalize('NFKC', data[12]).strip()
                    wh_question = map(lambda x: x.strip(), wh_question.split(u','))
                    wh_question = u' '.join(wh_question)
                else:
                    wh_question = u''
        except:
            continue

        question = preprocessing(question, tokenize=False)
        s = normalize_space.sub(u' ', u' '.join([principal_npvp, npvp, verb, wh_question]))
        words = []
        for w in question.lower().split():
            if w not in s:
                continue
            words.append(w)

        pattern = u' '.join(words)
        pattern = preprocessing(pattern, tokenize=False)
        pattern = utils.normalize_abb(pattern)
        # bigram_pattern = utils.get_bigram_content(pattern)
        # pattern = u' '.join([pattern, bigram_pattern])

        # patterns.update({pattern : response})
        # question_full.update({pattern : question})

        pattern = utils.normalize_abb(pattern)

        if cmnd in pattern:
            pattern = utils.emphasize_token(cmnd, pattern, n=3)
        if cccd in pattern:
            pattern = utils.emphasize_token(cccd, pattern, n=3)

        if pattern == u'':
            continue

        patterns.update({pattern: response})
        question_full.update({pattern: question})

    return patterns, question_full


if __name__ == '__main__':
    # load_casual_data('dataset/data.txt')
    load_business_data('dataset/business_data.xlsx')
