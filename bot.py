from configs.config import BOT_TOKEN, APP_URL
from Workers.Translator import TextTranslator
from Models.TranslationDTO import TranslationDTO

import os
from telebot import TeleBot, types
from flask import request, Flask
import requests
from pytube import YouTube

app = Flask(__name__)
bot = TeleBot(BOT_TOKEN)
translator = TextTranslator()
translation_dto = TranslationDTO

@bot.message_handler(commands=['start'])
def download_video_start(message: types.Message):
    bot.send_message(message.from_user.id, 'Hi!\n'
                                           'I\'ll help you to convert files, download videos and '
                                           'even translate documents\n'
                                           '/convert_files - choose this command to convert files\n'
                                           '/download_from_youtube - choose this command to '
                                           'download video from youtube\n'
                                           '/translate - choose this command to translate document(only .txt)')


@bot.message_handler(commands=['download_from_youtube'])
def download_video_start(message: types.Message):
    bot.send_message(message.from_user.id, 'Enter video url')


@bot.message_handler(regexp='^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$')
def validate_youtube_link(message: types.Message):
    try:
        YouTube(message.text).check_availability()
    except:
        bot.send_message(message.from_user.id, 'Url is incorrect')
    else:
        youtube_buttons(message)


def youtube_buttons(message: types.Message):
    choose_format = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton('Video')
    button2 = types.KeyboardButton('Audio')
    choose_format.add(button1, button2)
    choice = bot.send_message(message.from_user.id, 'Choose type of downloaded file: ', reply_markup=choose_format)
    bot.register_next_step_handler(choice, download, message.text)


def download(message: types.Message, url):
    yt = YouTube(url)
    if message.text.lower() == 'audio':
        video = yt.streams.filter(only_audio=True).first()
    else:
        video = yt.streams.get_highest_resolution()
    bot.send_message(message.from_user.id, 'Downloading...')
    video.download()
    file_name = video.default_filename
    if message.text.lower() == 'audio':
        base, ext = os.path.splitext(file_name)
        new_name = base + '.mp3'
        os.rename(file_name, new_name)
        file_name = new_name
    if os.path.getsize(file_name) > 2 * 10 ** 9:
        bot.send_message(message.from_user.id, 'File is too large')
    else:
        with open(file_name, 'rb') as file:
            bot.send_document(message.from_user.id, file)
    os.remove(file_name)


@bot.message_handler(commands=['translate'])
def translate_file(message: types.Message):
    bot.send_message(message.from_user.id, 'Upload file to translate')
    bot.register_next_step_handler(message, translation_get_filepath)


def translation_get_filepath(message: types.Message):
    if message.content_type != 'document':
        bot.send_message(message.from_user.id, 'You should upload only files')
        return
    telegram_filepath = bot.get_file(message.document.file_id).file_path
    download_file_from_telegram(telegram_filepath)
    result, result_filepath = translator.translate_file(telegram_filepath)
    if result is None:
        bot.send_message(message.from_user.id, 'File\'s format isn\'t correct')
        return
    with open(result_filepath, 'r') as file:
        bot.send_document(message.from_user.id, file)


def download_file_from_telegram(filepath):
    url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{filepath}'
    r = requests.get(url, allow_redirects=True)
    with open('translation_text.txt', 'wb') as f:
        f.write(r.content)


@bot.message_handler(commands=['convert_files'])
def convert_files(message: types.Message):
    bot.send_message(message.from_user.id, 'Upload file to convert')
    bot.register_next_step_handler(message, validate_file)


def validate_file(message: types.Message):
    bot.send_message(message.from_user.id, message.text)
    # here we look at file format and
    # offer formats to be converted


@bot.message_handler(func=lambda message: message.text in ['png', 'jpeg', 'mp4'])
def confirm_converting_format(message):
    # process file and return it to user
    file = ()
    convert_file(file, message.text)


def convert_file(file, type):
    # convert file
    pass


@bot.message_handler(content_types='text')
def echo(message: types.Message):
    bot.send_message(message.from_user.id, message.text)


@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode("utf-8")
    update = types.Update.de_json(json_string)
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
