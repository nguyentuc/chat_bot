# -*- encoding: utf-8 -*-

import unicodedata
import regex
from nlp_tools import tokenizer



my_regex = regex.regex()

def is_exist(dictionary, element):
    try:
        _ = dictionary[element]
        return True
    except:
        return False


def preprocessing(data, tokenize=True):
    data = unicodedata.normalize('NFKC', data)
    if tokenize:
        data = tokenizer.predict(data)
    data = my_regex.detect_url.sub(u'', data)
    data = my_regex.detect_url2.sub(u'', data)
    data = my_regex.detect_email.sub(u'', data)
    data = my_regex.detect_datetime.sub(u'', data)
    data = my_regex.detect_num.sub(u'', data)
    data = my_regex.normalize_special_mark.sub(u' \g<special_mark> ', data)
    data = my_regex.detect_exception_chars.sub(u'', data)
    data = my_regex.detect_special_mark.sub(u'', data)
    data = my_regex.detect_special_mark2.sub(u'', data)
    data = my_regex.detect_special_mark3.sub(u'', data)
    data = my_regex.normalize_space.sub(u' ', data)
    return data.strip()