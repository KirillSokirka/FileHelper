from configs.config import TEXT_TO_TRANSLATE, RESOURCES_PATH

import os
from googletrans import Translator, LANGUAGES

from converterextension.src.com.brawlstars.file.converter.utils.file_manager import FileManager

"""
    Class that translates source file to dest language
"""
class TextTranslator:

    def __init__(self):
        self.translator = Translator()

    """
        Helper method that checks if 
        language inputted by user is available or not
    """
    @staticmethod
    def check_if_language_available(language):
        if LANGUAGES.get(language):
            return True
        return False

    """
        Method that translates files
    """
    def translate_file(self, dto, source):
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
        FileManager.remove_files(source)
        return target
