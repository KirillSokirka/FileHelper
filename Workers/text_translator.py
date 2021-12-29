from configs.config import TEXT_TO_TRANSLATE, RESOURCES_PATH
from converterextensions.utils.file_downloader import FileManager

import os
from googletrans import Translator, LANGUAGES


class TextTranslator:

    def __init__(self):
        self.translator = Translator()

    @staticmethod
    def check_language(language):
        return LANGUAGES.get(language)

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
        FileManager.remove(source)
        return target
