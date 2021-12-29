import requests

from configs.config import BOT_TOKEN, TEXT_TO_TRANSLATE, RESOURCES_PATH, APP_URL
from converterextensions.utils.file_downloader import FileManager
from converterextensions.utils.file_extension import FileExtensions
from converterextensions.workers.converter import ExtendedConverter
from workers.text_translator import TextTranslator
from dtos.translation_dto import TranslationDto
from workers.youtube_downloader import YouTubeDownloader
from workers.pdf_converter import PdfConverter

import os
from io import BytesIO
from telebot import TeleBot, types
from flask import request, Flask
from PIL import Image

app = Flask(__name__)
bot = TeleBot(BOT_TOKEN)
translator = TextTranslator()
translation_dto = TranslationDto
youtube_downloader = YouTubeDownloader()
pdf_converter = PdfConverter()
convert_file_name = ''


@bot.message_handler(commands=['start'])
def download_video_start(message: types.Message):
    bot.send_message(message.from_user.id, 'Hi!\n'
                                           'I\'ll help you to convert files, download videos and '
                                           'even translate documents\n'
                                           '/convert_files - choose this command to convert files\n'
                                           '/download_from_youtube - choose this command to '
                                           'download video from youtube\n'
                                           '/translate - choose this command to translate document(only .txt)\n'
                                           '/pdf - choose this command to convert images to pdf format')


@bot.message_handler(commands=["pdf"])
def pdf_conversion(message):
    bot.send_message(message.from_user.id, "Send me a set of images,\n"
                                           "which u want to convert to pdf set...")


@bot.message_handler(content_types=["photo"])
def add_photo(message : types.Message):
    if len(pdf_converter.images) >= 50:
        bot.reply_to(message, "Sorry! Only 50 images can be converted for now")
        return
    download_photos(message.photo, message.from_user.id)
    bot.reply_to(message,
                 f"Success add image, send command /convert if finish")


def download_photos(photos, id):
    file_path = bot.get_file(photos[-1].file_id).file_path
    file = bot.download_file(file_path)
    image_to_append = Image.open(BytesIO(file))
    dest = os.path.join(RESOURCES_PATH, str(id) + ".jpg")
    if os.path.exists(dest):
        existed_image = Image.open(dest)
        new_image = Image.new('RGB', (existed_image.width, image_to_append.height + existed_image.height))
        new_image.paste(existed_image, (0,0))
        new_image.paste(image_to_append, (0, existed_image.height))
        new_image.save(dest)
    else:
        image_to_append.save(dest)


@bot.message_handler(commands=["convert"])
def finish(message):
    path = os.path.join(RESOURCES_PATH, str(id) + ".pdf")
    bot.send_document(message.from_user.id, open(path, "rb"), caption="From BRAWL STARS⭐️")
    FileManager.remove(path)


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
        download_from_youtube(message)


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
    download_from_youtube(message)


def download_from_youtube(message: types.Message):
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
        FileManager.remove(file_path)


@bot.message_handler(commands=['translate'])
def translate_file(message: types.Message):
    bot.send_message(message.from_user.id, 'Upload file to translate')
    bot.register_next_step_handler(message, translation_get_filepath)


def translation_get_filepath(message: types.Message):
    if message.content_type != 'document':
        bot.send_message(message.from_user.id, 'You should upload only files')
        bot.register_next_step_handler(message, translate_file)
        return
    translation_dto.init_name = message.text
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
        translation_dto.source_language = None
        choose_dest_language(answer)
    else:
        source_lan = bot.send_message(answer.from_user.id, 'Enter a source language (in this format \'en\')')
        bot.register_next_step_handler(source_lan, get_source_lan_from_user)


def get_source_lan_from_user(message: types.Message):
    if not TextTranslator.check_language(message.text):
        bot.send_message(message.from_user.id, "This language isn\'t available")
        bot.register_next_step_handler(message, choose_source_language)
        return
    translation_dto.source_language = message.text
    choose_dest_language(message)


def choose_dest_language(message: types.Message):
    dest_lan = bot.send_message(message.from_user.id, 'Enter a dest language (in this format \'en\')')
    bot.register_next_step_handler(message, confirm_dest_language)
    pass


def confirm_dest_language(message: types.Message):
    if not translator.check_language(message.text):
        bot.send_message(message.from_user.id, "This language isn\'t available")
        bot.register_next_step_handler(message, choose_dest_language)
        return
    translation_dto.destination_language = message.text
    translation_process_file(message.from_user.id)


def translation_process_file(user_id):
    url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{translation_dto.file_path}'
    target_file = os.path.join(RESOURCES_PATH, TEXT_TO_TRANSLATE)
    FileManager.download(url, target_file)
    result_filepath = translator.translate_file(translation_dto, target_file)
    with open(result_filepath, 'r') as file:
        bot.send_document(user_id, file)
    FileManager.remove(result_filepath)


@bot.message_handler(commands=['convert_files'])
def convert_files(message: types.Message):
    supported_extensions = ', '.join(FileExtensions.get_supported_extensions())
    bot.send_message(message.from_user.id,
                     f'Upload file to convert. Supported input extensions: {supported_extensions}')
    bot.register_next_step_handler(message, validate_file)


def validate_file(message: types.Message):
    file_name = ''
    if message.content_type == 'document':
        file_name = bot.get_file(message.document.file_id).file_path
    elif message.content_type == 'photo':
        file_name = bot.get_file(message.photo[-1].file_id).file_path
    elif message.content_type == 'video':
        file_name = bot.get_file(message.video.file_id).file_path
    elif message.content_type == 'audio':
        file_name = bot.get_file(message.audio.file_id).file_path

    extension = file_name.split('.')[-1]
    if FileExtensions.is_supported(extension):
        global convert_file_name
        convert_file_name = file_name
        format_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
        for ext in FileExtensions.get_possible_conversion_for(extension):
            format_keyboard.add(types.KeyboardButton(ext))
        choice = bot.send_message(message.from_user.id, 'Select the extension you want to convert to: ',
                                  reply_markup=format_keyboard)
        bot.register_next_step_handler(choice, confirm_converting_format)
    else:
        bot.send_message(message.from_user.id, f'Sorry, but I cannot convert files with extension = "{extension}"')


def confirm_converting_format(message):
    from_extension = convert_file_name.split('.')[-1]
    to_extension = message.text.lower()
    if to_extension in FileExtensions.get_possible_conversion_for(from_extension):
        url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{convert_file_name}'
        source = os.path.join(RESOURCES_PATH, convert_file_name)
        target = source.replace('.' + from_extension, '_converted.' + to_extension)
        try:
            FileManager.download(url, source)
            converter = ExtendedConverter(source, target)
            converter.perform_convert()
            with open(target, 'rb') as file:
                bot.send_document(message.from_user.id, file)
        except Exception as e:
            bot.send_message(message.from_user.id, 'Oops, something went wrong! ' + str(e))
        finally:
            FileManager.remove(source, target)
    else:
        bot.send_message(message.from_user.id, 'Unsupported file extension!')


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


def main():
    if os.getenv('Heroku'):
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    else:
        bot.remove_webhook()
        bot.polling(none_stop=True)


if __name__ == '__main__':
    if os.getenv('Heroku'):
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    else:
        bot.remove_webhook()
        bot.polling(none_stop=True)
