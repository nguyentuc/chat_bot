# -*- encoding: utf-8 -*-
__author__ = 'nobita'

import re
import utils


class Regex:
    def __init__(self):
        self.rm_except_chars = re.compile(
            u'[^\w\s\d…\-–\./_,\(\)$%“”\"\'?!;:@#^&*\+=<>\[\]\{\}²³áÁàÀãÃảẢạẠăĂắẮằẰẳẲặẶẵẴâÂấẤầẦẩẨậẬẫẪđĐéÉèÈẻẺẽẼẹẸêÊếẾềỀễỄểỂệỆíÍìÌỉỈĩĨịỊóÓòÒỏỎõÕọỌôÔốỐồỒổỔỗỖộỘơƠớỚờỜởỞỡỠợỢúÚùÙủỦũŨụỤưƯứỨừỪửỬữỮựỰýÝỳỲỷỶỹỸỵỴ]')
        self.normalize_space = re.compile(u' +')
        self.multi_newline_regex = re.compile("\n+")
        self.detect_url = re.compile(u'(https|http|ftp|ssh)://[^\s\[\]\(\)\{\}]+', re.I)
        self.detect_url2 = re.compile(
            u'[^\s\[\]\(\)\{\}]+(\.com|\.net|\.vn|\.org|\.info|\.biz|\.mobi|\.tv|\.ws|\.name|\.us|\.ca|\.uk)', re.I)
        self.detect_num = re.compile(ur'(\d+\,\d+\w*)|(\d+\.\d+\w*)|(\w*\d+\w*)')
        self.detect_email = re.compile(u'[^@|\s]+@[^@|\s]+')
        self.detect_datetime = re.compile(u'\d+[\-/\.]\d+[\-/\.]*\d*')
        self.change_to_space = re.compile(u'\t')
        self.filter_hard_rules = self.filter_hard_rules()
        self.detect_special_mark = re.compile(u'[,;\-\(\)\[\]\{\}\<\>“”\"\']')
        self.detect_special_mark3 = re.compile(u'[/\$%–@#^&*+=]')
        self.detect_special_mark4 = re.compile(u'\.\.\.|[?:!…\.]')
        self.detect_non_vnese = self.detect_non_vietnamese()
        self.normalize_special_mark = re.compile(u'(?P<special_mark>[\.,\(\)\[\]\{\};!?:“”\"\'/\<\>])')
        self.normalize_special_mark2 = re.compile(u' (?P<special_mark2>[\.,\)\]\};!?:/\>])')
        self.normalize_special_mark3 = re.compile(u'(?P<special_mark3>[\(\[\{/\<]) ')


    def run_regex_training(self, data):
        s = self.multi_newline_regex.sub(u'\n', data)
        s = self.detect_num.sub(u'1', s)  # replaced number to 1
        s = self.detect_url.sub(u'2', s)
        s = self.detect_url2.sub(u'0', s)
        s = self.detect_email.sub(u'3', s)
        s = self.detect_datetime.sub(u'4', s)
        s = self.change_to_space.sub(u' ', s)
        s = self.rm_except_chars.sub(u'', s)
        if self.filter_hard_rules:
            s = self.filter_hard_rules.sub(u'5', s)
        s = self.detect_non_vnese.sub(u'6', s)
        s = self.detect_special_mark.sub(u'7', s)
        s = self.detect_special_mark3.sub(u'9', s)
        s = self.normalize_space.sub(u' ', s)
        s = self.detect_special_mark4.sub(u'.', s)

        return s.strip()

    def replace(self, reobj, mask, s):
        values = []
        new_str = s
        bias = 0
        finditer = reobj.finditer(s)
        for m in finditer:
            x = m.regs[0]
            values.append(s[x[0]:x[1]])
            new_str = new_str[:x[0] - bias] + mask + new_str[x[1] - bias:]
            bias += x[1] - x[0] - 1
        return new_str, values

    def run_regex_predict(self, query):
        s = self.multi_newline_regex.sub(u'\n', query)
        s, number = self.replace(self.detect_num, u'1', s)
        s, url = self.replace(self.detect_url, u'2', s)
        s, url2 = self.replace(self.detect_url2, u'0', s)
        s, email = self.replace(self.detect_email, u'3', s)
        s, datetime = self.replace(self.detect_datetime, u'4', s)
        s = self.change_to_space.sub(u' ', s)
        s = self.rm_except_chars.sub(u'', s)
        if self.filter_hard_rules:
            s, hard_rules = self.replace(self.filter_hard_rules, u'5', s)
        else:
            hard_rules = []
        s, non_vnese = self.replace(self.detect_non_vnese, u'6', s)
        s, mark = self.replace(self.detect_special_mark, u'7', s)
        s, mark3 = self.replace(self.detect_special_mark3, u'9', s)
        s = self.normalize_space.sub(u' ', s)
        s, mark4 = self.replace(self.detect_special_mark4, u'.', s)
        return s.strip(), number, url, url2, email, datetime, hard_rules, non_vnese, mark, mark3, mark4

    def restore_info(self, q, number, url, url2, email, datetime, hard_rules, non_vnese, mark, mark3, mark4):
        q = self.restore_info_ex(q, mark4, u'\.')
        q = self.restore_info_ex(q, mark3, u'9')
        q = self.restore_info_ex(q, mark, u'7')
        q = self.restore_info_ex(q, non_vnese, u'6')
        q = self.restore_info_ex(q, hard_rules, u'5')
        q = self.restore_info_ex(q, datetime, u'4')
        q = self.restore_info_ex(q, email, u'3')
        q = self.restore_info_ex(q, url2, u'0')
        q = self.restore_info_ex(q, url, u'2')
        q = self.restore_info_ex(q, number, u'1')
        return q

    def detect_non_vietnamese(self):
        vowel = [u'a', u'e', u'i', u'o', u'u', u'y']
        vowel2 = [u'a', u'e', u'i', u'o', u'y']
        vowel3 = [u'y']
        double_vowel = [w + w for w in vowel]
        double_vowel = list(set(double_vowel) - set([u'uu']))
        double_vowel2 = utils.add_to_list(vowel3, vowel)
        double_vowel2 = list(set(double_vowel2) - set([u'yy']))
        consonant = [u'b', u'c', u'd', u'g', u'h', u'k', u'l', u'm', u'n', u'p', u'q',
                     u'r', u's', u't', u'v', u'x']
        consonant2 = [u'b', u'd', u'g', u'h', u'k', u'l', u'q', u'r', u's', u'v', u'x']
        consotant3 = [u'm', u'p']
        consonant4 = [u'p', u'q']
        consonant5 = [u'b', u'c', u'd', u'g', u'n', u'r']
        special_pattern = [u'ch', u'gh', u'kh', u'nh', u'ng', u'ph', u'th', u'tr']
        special_pattern2 = [u'ae', u'ea', u'ei', u'ey', u'iy', u'oy', u'ya', u'yi', u'yo', u'yu']
        special_pattern3 = [u'gh', u'kh', u'ph', u'th', u'tr']
        special_pattern4 = [u'ge', u'gy', u'ka', u'ko', u'ku', u'ry']
        english_chars = [u'f', u'j', u'w', u'z']
        double_consonant = utils.add_to_list(consonant, consonant)
        double_consonant = list(set(double_consonant) - set(special_pattern))
        non_vietnamese = double_vowel + double_consonant + utils.add_to_list(vowel, consonant2)
        non_vietnamese += consotant3 + special_pattern2 + utils.add_to_list(vowel, special_pattern3)
        non_vietnamese += utils.add_to_list(vowel, utils.add_to_list(consonant, vowel))
        non_vietnamese += special_pattern4 + utils.add_to_list(consonant4, vowel2) + \
                          utils.add_to_list(consonant, double_vowel2) + utils.add_to_list(consonant5, vowel3)
        non_vietnamese = self.filter_non_vnese(set(non_vietnamese)) + english_chars
        s = u'|'.join(non_vietnamese)
        return re.compile(ur'\w*(' + s + ur')\w*', re.I)

    def filter_non_vnese(self, s):
        two = filter(lambda x: len(x) == 2, s)
        three = list(set(s) - set(two))
        new_three = []
        for x1 in three:
            flag = False
            if len(x1) != 3: continue
            for x2 in two:
                if x2 in x1:
                    flag = True;
                    break
            if not flag: new_three.append(x1)
        return two + new_three

    def restore_info_ex(self, q, data, mask):
        q = q.replace(u'%', u'%%')
        q = re.sub(mask, u'%s', q)
        data = tuple(data)
        try:
            q = q % data  # use format string to get best performance
        except:
            pass
        q = q.replace(u'%%', u'%')
        return q

    def filter_hard_rules(self):
        rules = utils.load_hard_rules()
        if rules:
            rgx = ur'%s' % '|'.join(rules)
            return re.compile(rgx)
        return None


    def fn_normalize_special_mark(self, s):
        s = self.normalize_special_mark2.sub(u'\g<special_mark2>', s)
        s = self.normalize_special_mark3.sub(u'\g<special_mark3>', s)
        s = self.normalize_space.sub(u' ', s)
        return s