
class TranslationDto:

    def __init__(self):
        self.file_path = ''
        self.source_language = ''
        self.destination_language = ''

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        if not isinstance(value, str):
            raise TypeError
        self.__file_path = value

    @property
    def source_language(self):
        return self.__source_lan

    @source_language.setter
    def source_language(self, value):
        if not value:
            if not isinstance(value, str):
                raise TypeError
        self.__source_lan = value

    @property
    def destination_language(self):
        return self.__dest_lan

    @destination_language.setter
    def destination_language(self, value):
        if not isinstance(value, str):
            raise TypeError
        self.__dest_lan = value