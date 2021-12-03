from configs.config import TEXT_TO_TRANSLATE

import os
from googletrans import Translator, LANGUAGES


class TextTranslator:

    def __init__(self):
        self.translator = Translator()

    def check_if_language_avaliable_(self, language):
        if LANGUAGES.get(language):
            return True
        return False

    def translate_file(self, dto):
        filepath = dto.file_path.split('/')[-1]
        with open(filepath, 'w') as result_file:
            with open(TEXT_TO_TRANSLATE, 'r') as source_file:
                for line in source_file:
                    if dto.source_lan:
                        result_file.write(
                            self.translator.translate(line,
                                                  src=dto.source_lan,
                                                  dest=dto.dest_lan).text + '\n'
                        )
                    else:
                        result_file.write(
                            self.translator.translate(line,
                                                      dest=dto.dest_lan).text + '\n'
                        )
        os.remove('text_to_translate.txt')
        return filepath
