import telebot
import config
import pyowm
import os

from flask import Flask, request


bot = telebot.TeleBot(config.TOKEN)
owm = pyowm.OWM('9e74b4669f6a8cf98cab1138c031c5fb', language="ru")
server = Flask(__name__)


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config.HOST + config.TOKEN)
    return "ХАЙ Я ЧЕБУПЕЛЯ БОТ", 200


@server.route('/' + config.TOKEN, methods=['POST'])
def updater():
    response = request.stream.read().decode("utf-8")
    bot.process_new_updates([telebot.types.Update.de_json(response)])
    return "!", 200


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Здарова, я чебупеля бот')
    bot.reply_to(message, 'Напиши мне названия города и я расскажу шо там с погодой')


@bot.message_handler(content_types=['text'])
def lalala(message):
    user_text = message.text.lower()

    print(message.chat.username, user_text)

    observation = find_observation(user_text)

    if observation is None:
        bot.send_message(message.chat.id, "Напиши нормальный город, буду признателен")
        return

    w = observation.get_weather()
    temp = w.get_temperature('celsius')["temp"]

    first_message = "В городе " + user_text + " сейчас " + w.get_detailed_status()
    second_message = "Температура сейчас в районе " + str(temp) + " градусов цельсия"

    bot.send_message(message.chat.id, first_message)
    bot.send_message(message.chat.id, second_message)

    sovet_message = "погода - высший пилотаж, харе дома сидеть"

    if temp < 10:
        sovet_message = "ОДЕВАЙ ПОДШТАННИКИ, ДУРАЧИШКА. Тебе ещё детей ростить"
    elif temp > 10:
        sovet_message = "чо нарядился как капуста, сегодня можно на легке, я разрешаю"

    bot.send_message(message.chat.id, sovet_message)


def find_observation(place):
    try:
        return owm.weather_at_place(place)
    except:
        return None

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
