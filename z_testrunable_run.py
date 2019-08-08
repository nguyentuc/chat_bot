# -*- coding: utf-8 -*-
__author__ = 'nobita'

import config
import bot_brain_intent
from flask import Flask, request
import HTMLParser


bot = bot_brain_intent.brain_bot()
bot.run()

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')

@app.route('/', methods = ['GET'])
def homepage():
    return app.send_static_file('index.html')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/get_answer', methods=['POST'])
def process_request():
    data = request.form['data']
    data = HTMLParser.HTMLParser().unescape(data)
    return bot.thinking(data)


if __name__ == '__main__':
    app.run(config.SERVER_ADDR, port=config.SERVER_PORT)
