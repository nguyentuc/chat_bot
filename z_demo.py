# -*- coding: utf-8 -*-
from unidecode import unidecode
import aiml
import json

k = aiml.Kernel()
k.learn("z_learningFileList.aiml")
k.respond("LEARN AIML")

while True:
    # nhan input va khu dau tieng viet
    raw = raw_input("User > ")
    string_input = unidecode(raw.decode('utf8'))
    reply = k.respond(string_input)
    if reply:
        # match reply voi cau tra loi co dau trong file .json
        with open('rule.json', 'r') as myfile:
            data = myfile.read()

        rules = json.loads(data)['rules']
        answer = ""
        link = ""
        for r in rules:
            if r['key'] == reply:
                answer = r['value']
                link = r['link']
                break

        print "Bot > ", answer
        print "Bot > Bạn có thể tham khảo thêm thông tin ở đây:", link
    else:
        print "Bot > Tôi đang không hiểu ý bạn là gì, bạn có thể đặt câu hỏi cụ thể hơn được không ạ ?"
