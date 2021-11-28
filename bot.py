import configs.config
from configs.config import BOT_TOKEN, APP_URL, TEXT_TO_TRANSLATE
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
