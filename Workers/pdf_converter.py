class ToPDFConverter:
    def __init__(self):
        self.__list_image = {}

    @property
    def list_image(self):
        return self.__list_image

    @property
    def path(self):
        return self.__path
