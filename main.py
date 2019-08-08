# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import os
from unidecode import unidecode
import aiml
import json
import bot_brain_intent
from logger import logger

app = Flask(__name__)

bot = bot_brain_intent.brain_bot()
bot.run()


@app.route("/")
def hello():
    return render_template('chat.html')


@app.route("/ask", methods=['POST'])
def ask():
    message = request.form['messageText'].encode('utf-8').strip()
    # nhan input va khu dau tieng viet
    string_input = unidecode(message.decode('utf8'))

    kernel = aiml.Kernel()

    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile="bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles=os.path.abspath("z_learningFileList.aiml"), commands="LEARN AIML")
        kernel.saveBrain("bot_brain.brn")

    # kernel now ready for use
    while True:
        if string_input == "quit":
            exit()
        elif string_input == "save":
            kernel.saveBrain("bot_brain.brn")
        else:
            reply = kernel.respond(string_input)
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
                logger.info('question_aiml: %s, answer_aiml: %s' % (string_input, answer))
                if link == "":
                    return jsonify({'status': 'OK',
                                    'answer': answer,
                                    'flag': 0})
                return jsonify({'status': 'OK',
                                'answer': answer,
                                'link': link,
                                'flag': 1})
            elif bot.thinking(unicode(message, "utf-8")):
                logger.info(
                    'question_sys2tuongdong: %s, answer_sys2tuongdong: %s' % (
                        string_input, bot.thinking(unicode(message, "utf-8"))))
                return jsonify({'status': 'OK',
                                'answer': bot.thinking(unicode(message, "utf-8")),
                                'flag': 2})
            else:
                return jsonify({'status': 'OK',
                                'answer': "Tôi đang không hiểu ý bạn là gì, bạn hãy đưa câu hỏi cụ thể hơn được không ?"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
