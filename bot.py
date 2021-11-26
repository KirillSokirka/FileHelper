import os

import telebot

from configs.config import BOT_TOKEN, APP_URL

from telebot import TeleBot
from flask import request, Flask

app = Flask(__name__)
bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['convert_files'])
def convert_files(message: telebot.types.Message):
    bot.send_message(message.from_user.id, 'Upload file to convert')
    bot.register_next_step_handler(message, validate_file)


def validate_file(message: telebot.types.Message):
    bot.send_message(message.from_user.id, message.text)
    # here we look at file format and
    # offer formats to be converted


@bot.message_handler(lambda text: text in ['text', 'text'])
def confirm_converting_format(message):
    # process file and return it to user
    file = ()
    process_file(file, message.text)


def process_file(file, type):
    # convert file
    pass


@bot.message_handler(content_types='text')
def echo(message: telebot.types.Message):
    bot.send_message(message.from_user.id, message.text)


@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "Ok", 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return "Ok", 200


if __name__ == '__main__':
    if os.getenv('Heroku'):
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    else:
        bot.remove_webhook()
        bot.polling(none_stop=True)