from pytube import YouTube
import os

class YouTubeDownloader:
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

    def check_url(self):
        try:
            YouTube(self.url).check_availability()
        except:
            return False
        return True

    def download(self):
        if not self.check_url():
            raise ValueError
        yt = YouTube(self.url)
        if self.format == 'audio':
            video = yt.streams.filter(only_audio=True).first()
        else:
            if self.resolution == 'high':
                video = yt.streams.get_highest_resolution()
            else:
                video = yt.streams.get_lowest_resolution()
        video.download()
        file_name = video.default_filename
        if self.format == 'audio':
            base, ext = os.path.splitext(file_name)
            new_name = base + '.mp3'
            os.rename(file_name, new_name)
            file_name = new_name
        if os.path.getsize(file_name) > 2 * 10 ** 9:
            raise OSError
        return file_name
