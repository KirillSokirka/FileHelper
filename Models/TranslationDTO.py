
class TranslationDTO:

    def __init__(self):
        self.file_path = ''
        self.source_lan = ''
        self.dest_lan = ''

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        if not isinstance(value, str):
            raise TypeError
        self.__file_path = value

    @property
    def source_lan(self):
        return self.__source_lan

    @source_lan.setter
    def source_lan(self, value):
        if not value:
            if not isinstance(value, str):
                raise TypeError
        self.__source_lan = value

    @property
    def dest_lan(self):
        return self.__dest_lan

    @dest_lan.setter
    def dest_lan(self, value):
        if not isinstance(value, str):
            raise TypeError
        self.__dest_lan = value