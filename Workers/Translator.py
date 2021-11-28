import os

from googletrans import Translator


class TextTranslator:

    def __init__(self):
        self.translator = Translator()

    def translate_file(self, _filepath, src_lan=None, dest_lan=None):
        filepath = _filepath.split('/')[-1]
        if not TextTranslator.__validate_file(filepath):
            return False, None
        with open('result.txt', 'w') as result_file:
            with open('text.txt', 'r') as file:
                for line in file:
                    result_file.write(
                        self.translator.translate(line, dest='ru').text + '\n'
                    )
        return True, 'result.txt'

    @staticmethod
    def __validate_file(filepath: str) -> bool:
        return filepath.lower().endswith('.txt')
