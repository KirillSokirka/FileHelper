from PIL.Image import Image


class PdfConverter:

    def __init__(self):
        self.__images = []

    @property
    def images(self):
        return self.__images

    def append(self, *value):
        if not all(isinstance(v, Image) for v in list(value)):
            raise TypeError('U can send only images')
        self.__images.append(list(value))

    @property
    def path(self):
        return self.__path
