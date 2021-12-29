from configs.config import RESOURCES_PATH
from converterextensions.utils.file_downloader import FileManager

import os
from googletrans import Translator, LANGUAGES

"""
Class that process text translating
"""
class TextTranslator:

    def __init__(self):
        self.translator = Translator()

    @staticmethod
    def check_language(language):
        """
            Static method for checking if inputed language is correct or not
        :param language: language getted from user
        :return: bool
        """
        return LANGUAGES.get(language)

    def translate_file(self, dto, source):
        """
            Method that translates file
        :param dto: object that contains result file path, source and dest language
        :param source: source file
        :return:
        """
        ext = dto.file_path.split('.')[-1]
        filepath = dto.file_path.split('.')[-2] + '_translated_to_' + dto.destination_language + "." + ext
        target = os.path.join(RESOURCES_PATH, filepath)
        with open(target, 'w') as result_file:
            with open(source, 'r', encoding='utf-8') as source_file:
                for line in source_file:
                    if not line.rstrip():
                        continue
                    if dto.source_language:
                        result_file.write(
                            self.translator.translate(line,
                                                      src=dto.source_language,
                                                      dest=dto.destination_language).text + '\n'
                        )
                    else:
                        result_file.write(
                            self.translator.translate(line,
                                                      dest=dto.destination_language).text + '\n'
                        )
        FileManager.remove(source)
        return target
