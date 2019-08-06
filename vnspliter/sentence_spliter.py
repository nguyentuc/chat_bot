# -*- coding: utf-8 -*-

import os.path
import re
import utils
from feature.feature import Feature
from regex import Regex
import traceback


class SentenceSpliter():
    def __init__(self, is_training=False):
        self.classifier = None
        self.feature_model = None
        self.regex_rule = Regex()
        if not is_training:
            self.classifier = utils.load(os.path.join('vnspliter/model', 'model.pkl'))
            if self.classifier is None:
                print "Unable to load model!"
                exit(-1)

    def make_feature(self, file=None):
        features_list = []
        label_list = []
        self.feature_model = Feature()
        if file is None:
            return features_list, label_list
        else:
            features_list, label_list = self.feature_model.gen_feature_matrix(file)
        return features_list, label_list

    def split_paragraph(self, par):
        sens = []
        try:
            new_par = self.regex_rule.fn_normalize_special_mark(par)
            paragraph, number, url, url2, email, datetime, hard_rules, non_vnese, mark, mark3, mark4 = \
                self.regex_rule.run_regex_predict(new_par)
            features, _ = self.make_feature(paragraph)
            if not features:
                sens.append(par)
                return sens
            labels = self.classifier.predict(features)
            idx = 0
            pos_start = 0
            pos_end = 0
            for c in paragraph:
                if Feature.is_splitter_candidate(c):
                    if idx < len(labels) and labels[idx] == 1:
                        sens.append(paragraph[pos_start:pos_end + 1].strip())
                        pos_start = pos_end + 1
                    idx += 1
                pos_end += 1
            if pos_start < len(paragraph):
                sens.append(paragraph[pos_start:].strip())
            paragraph = '\n'.join(sens)
            paragraph = self.regex_rule.restore_info(paragraph, number, url, url2, email, datetime, hard_rules, non_vnese, mark, \
                                               mark3, mark4)
            # paragraph = self.regex_rule.normalize_special_mark.sub(u' \g<special_mark> ', paragraph)
            # paragraph = self.regex_rule.normalize_space.sub(u' ', paragraph)
            sens = paragraph.split('\n')
            return sens
        except Exception as e:
            print(traceback.format_exc())
            sens.append(par)
            return sens

    def split(self, pars):
        sens = []
        try:
            pars = pars.replace(u'\r', u'\n')
            pars = re.compile(u'\n+').sub(u'\n', pars)
            pars = pars.split('\n')
            for par in pars:
                if par.strip():
                    s = self.split_paragraph(par)
                    sens += s
            return sens
        except:
            sens.append(pars)
            return sens
