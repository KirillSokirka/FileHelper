import configs.config
from configs.config import BOT_TOKEN, APP_URL, TEXT_TO_TRANSLATE, RESOURCES_PATH
from workers.translator import TextTranslator
from models.translation_dto import TranslationDto
from workers.youtube_downloader import YouTubeDownloader
from workers.pdf_converter import ToPDFConverter
from converterextension.src.com.brawlstars.file.converter.utils.file_extensions import FileExtensions
from converterextension.src.com.brawlstars.file.converter.utils.file_manager import FileManager
from converterextension.src.com.brawlstars.file.converter.workers.extended_converter import ExtendedConverter


import os
from io import BytesIO
from telebot import TeleBot, types
from flask import request, Flask
import requests
from pytube import YouTube
from conversiontools import ConversionClient
from PIL import Image

app = Flask(__name__)
bot = TeleBot(BOT_TOKEN)
translator = TextTranslator()
translation_dto = TranslationDto
youtube_downloader = YouTubeDownloader()
to_pdf = ToPDFConverter()
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


@bot.message_handler(content_types = ["photo"])
def add_photo(message):
    if not isinstance(to_pdf.list_image.get(message.from_user.id), list):
        bot.reply_to(message, "Send /pdf for initialization")

        return

    if len(to_pdf.list_image[message.from_user.id]) >=50:
        bot.reply_to(message, "Sorry! Only 50 images can be converted for now")
        return

    file = bot.get_file(message.photo[1].file_id)
    downloaded_file = bot.download_file(file.file_path)
    image = Image.open(BytesIO(downloaded_file))

    to_pdf.list_image[message.from_user.id].append(image)
    bot.reply_to(message, f"[{len(to_pdf.list_image[message.from_user.id])}] Success add image, send command /toPDF if finish")


@bot.message_handler(commands = ["pdf"])
def PDF(message):
    bot.send_message(message.from_user.id, "Get Set Send me images...")

    if not isinstance(to_pdf.list_image.get(message.from_user.id), list):
        to_pdf.list_image[message.from_user.id] = []


@bot.message_handler(commands = ["toPDF"])
def FINISH(message):
    images = to_pdf.list_image.get(message.from_user.id)

    if isinstance(images, list):
        del to_pdf.list_image[message.from_user.id]

    if not images:
        bot.send_message(message.from_user.id, "First send me images..")
        return

    path = str(message.from_user.id) + ".pdf"
    images[0].save(path, save_all = True, append_images = images[1:])
    bot.send_document(message.from_user.id, open(path, "rb"), caption = "From BRAWL STARS⭐️")
    FileManager.remove_files(path)


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
        FileManager.remove_files(file_path)


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
    if not TextTranslator.check_if_language_available(message.text):
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
    if not translator.check_if_language_available(message.text):
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
    FileManager.remove_files(result_filepath)


@bot.message_handler(commands=['convert_files'])
def convert_files(message: types.Message):
    supported_extensions = ', '.join(FileExtensions.get_supported_extensions())
    bot.send_message(message.from_user.id, f'Upload file to convert. Supported input extensions: {supported_extensions}')
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
            FileManager.remove_files(source, target)
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


if __name__ == '__main__':
    if os.getenv('Heroku'):
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    else:
        bot.remove_webhook()
        bot.polling(none_stop=True)
