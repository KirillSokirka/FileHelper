import configs.config
from configs.config import BOT_TOKEN, APP_URL, TEXT_TO_TRANSLATE
from Workers.Translator import TextTranslator
from Models.TranslationDTO import TranslationDTO
from Workers.YouTubeDownloader import YouTubeDownloader

import os
from telebot import TeleBot, types
from flask import request, Flask
import requests
from pytube import YouTube

app = Flask(__name__)
bot = TeleBot(BOT_TOKEN)
translator = TextTranslator()
translation_dto = TranslationDTO
youtube_downloader = YouTubeDownloader()


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
    bot.send_message(message.from_user.id, 'Enter video URL')


@bot.message_handler(regexp='^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$')
def get_youtube_link(message: types.Message):
    youtube_downloader.url = message.text
    choose_format(message)


def choose_format(message: types.Message):
    format_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
    format_keyboard.add(types.KeyboardButton('Video'), types.KeyboardButton('Audio'))
    choice = bot.send_message(message.from_user.id, 'Choose type of downloaded file: ', reply_markup=format_keyboard)
    bot.register_next_step_handler(choice, confirm_format)


def confirm_format(message: types.Message):
    if message.text.lower() not in ('video', 'audio'):
        bot.send_message(message.from_user.id, 'Incorrect input!')
        bot.register_next_step_handler(message, choose_format)
        return
    youtube_downloader.format = message.text.lower()
    if message.text.lower() == 'video':
        choose_resolution(message)
    else:
        download(message)


def choose_resolution(message: types.Message):
    resolution_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
    resolution_keyboard.add(types.KeyboardButton('High'), types.KeyboardButton('Low'))
    choice = bot.send_message(message.from_user.id, 'Choose quality: ', reply_markup=resolution_keyboard)
    bot.register_next_step_handler(choice, confirm_resolution)


def confirm_resolution(message: types.Message):
    if message.text.lower() not in ('high', 'low'):
        bot.send_message(message.from_user.id, 'Incorrect input!')
        bot.register_next_step_handler(message, choose_resolution)
        return
    youtube_downloader.resolution = message.text.lower()
    download(message)


def download(message: types.Message):
    bot.send_message(message.from_user.id, 'Downloading...')
    file_path = ''
    try:
        file_path = youtube_downloader.download()
    except ValueError:
        bot.send_message(message.from_user.id, 'Something went wrong! Check if URL is correct')
    except OSError:
        bot.send_message(message.from_user.id, 'File is too large!')
    if file_path:
        with open(file_path, 'rb') as file:
            bot.send_document(message.from_user.id, file)
        os.remove(file_path)


@bot.message_handler(commands=['translate'])
def translate_file(message: types.Message):
    bot.send_message(message.from_user.id, 'Upload file to translate')
    bot.register_next_step_handler(message, translation_get_filepath)


def translation_get_filepath(message: types.Message):
    if message.content_type != 'document':
        bot.send_message(message.from_user.id, 'You should upload only files')
        return
    temp = bot.get_file(message.document.file_id).file_path
    if not temp.lower().endswith('.txt'):
        bot.send_message(message.from_user.id, 'File\'s format isn\'t correct')
        bot.register_next_step_handler(message, translate_file)
        return
    translation_dto.file_path = temp
    choose_source_language(message.from_user.id)


def choose_source_language(id):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton('Choose'),
        types.KeyboardButton('Skip')
    )
    answer = bot.send_message(id, "Do u wanna choose source language "
                                  "or let bot to do it instead of u?", reply_markup=keyboard)
    bot.register_next_step_handler(answer, confirm_source_language)


def confirm_source_language(answer: types.Message):
    if answer.text not in ['Choose', 'Skip']:
        bot.send_message(answer.from_user.id, 'Sorry, I don\'t understand, try again')
        bot.register_next_step_handler(answer, choose_source_language)
        return
    if answer.text == 'Skip':
        translation_dto.source_lan = None
        choose_dest_language(answer)
    else:
        source_lan = bot.send_message(answer.from_user.id, 'Enter a source language (in this format \'en\')')
        bot.register_next_step_handler(source_lan, get_source_lan_from_user)


def get_source_lan_from_user(message: types.Message):
    if not translator.check_if_language_avaliable_(message.text):
        bot.send_message(message.from_user.id, "This language isn\'t available")
        bot.register_next_step_handler(message, choose_source_language)
        return
    translation_dto.source_lan = message.text
    bot.register_next_step_handler(message, choose_dest_language)


def choose_dest_language(message: types.Message):
    dest_lan = bot.send_message(message.from_user.id, 'Enter a dest language (in this format \'en\')')
    bot.register_next_step_handler(message, confirm_dest_language)
    pass


def confirm_dest_language(message: types.Message):
    if not translator.check_if_language_avaliable_(message.text):
        bot.send_message(message.from_user.id, "This language isn\'t available")
        bot.register_next_step_handler(message, choose_dest_language)
        return
    translation_dto.dest_lan = message.text
    translation_process_file(message.from_user.id)


def translation_process_file(user_id):
    download_file_from_telegram(translation_dto.file_path)
    result_filepath = translator.translate_file(translation_dto)
    with open(result_filepath, 'r') as file:
        bot.send_document(user_id, file)
    os.remove(result_filepath)


def download_file_from_telegram(filepath):
    url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{filepath}'
    r = requests.get(url, allow_redirects=True)

    with open(TEXT_TO_TRANSLATE, 'wb') as f:
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
