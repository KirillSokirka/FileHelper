from PIL.Image import Image


class PdfConverter:

    def __init__(self):
        self.__images = []

    @property
    def images(self):
        return self.__images


    @property
    def path(self):
        return self.__path
