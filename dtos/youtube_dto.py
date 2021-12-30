class YouTubeDTO:
    def __init__(self, url='', format='video', resolution=''):
        self.url = url
        self.format = format
        self.resolution = resolution

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        if not isinstance(value, str):
            raise TypeError
        self.__url = value

    @property
    def format(self):
        return self.__format

    @format.setter
    def format(self, value):
        if not isinstance(value, str):
            raise TypeError
        self.__format = value

    @property
    def resolution(self):
        return self.__resolution

    @resolution.setter
    def resolution(self, value):
        if not isinstance(value, str):
            raise TypeError
        self.__resolution = value