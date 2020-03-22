
from bot import bot
from flask import Flask, request

import config
import telebot
import os


server = Flask(__name__)


@server.route("/bot", methods=['POST'])
def getMessage():
    response = request.stream.read().decode("utf-8")
    bot.process_new_updates([telebot.types.Update.de_json(response)])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config.HOST)
    return "?", 200


if __name__ == '__main__':
    server.debug = True
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
