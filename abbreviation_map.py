# -*- encoding: utf-8 -*-

from nlp_tools import tokenizer
from collections import OrderedDict

cmnd = u'cmnd'
cccd = u'cccd'

ABBREVIATION = OrderedDict()

ABBREVIATION[u'chứng minh thư nhân dân'] = cmnd
ABBREVIATION[u'chứng minh thư nd'] = cmnd
ABBREVIATION[u'chứng minh nhân dân'] = cmnd
ABBREVIATION[u'căn cước công dân'] = cccd
ABBREVIATION[u'chứng minh nd'] = cmnd
ABBREVIATION[u'chứng minh thư'] = cmnd
ABBREVIATION[u'căn cước cd'] = cccd
ABBREVIATION[u'cc công dân'] = cccd
ABBREVIATION[u'cmt nd'] = cmnd
ABBREVIATION[u'căn cước'] = cccd
ABBREVIATION[u'cc cd'] = cccd
ABBREVIATION[u'cmtnd'] = cmnd
ABBREVIATION[u'cmt'] = cmnd