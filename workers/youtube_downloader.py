from pytube import YouTube
from dtos.youtube_dto import YouTubeDTO
import os


class YouTubeDownloader:
    """
    Class used to manage the process of downloading from YouTube
    """

    @staticmethod
    def check_url(yt_dto):
        """
        Static method used to validate url
        :param yt_dto: YouTubeDTO
            instance of class YouTubeDTO that contains url, format and resolution
        :return: bool
        """
        try:
            YouTube(yt_dto.url).check_availability()
        except:
            return False
        return True

    @classmethod
    def download(cls, yt_dto):
        """
        Class method used to used directly for the video download process

        Checks availability of url. Then creates instance of class YouTube from pytube module.
        According to user choice of format(video or audio) and quality (high, low) streams the video.
        Uses download() method from pytube module to download streamed video.
        Converts video to audio if needed.

        :param yt_dto: YouTubeDTO
            instance of class YouTubeDTO that contains url, format and resolution
        :raises ValueError
            if url is invalid
        :raises OSError
            if file is too large
        :return: file_name
        """
        if not cls.check_url(yt_dto):
            raise ValueError
        yt = YouTube(yt_dto.url)
        if yt_dto.format == 'audio':
            video = yt.streams.filter(only_audio=True).first()
        else:
            if yt_dto.resolution == 'high':
                video = yt.streams.get_highest_resolution()
            else:
                video = yt.streams.get_lowest_resolution()
        video.download()
        file_name = video.default_filename
        if yt_dto.format == 'audio':
            base, ext = os.path.splitext(file_name)
            new_name = base + '.mp3'
            os.rename(file_name, new_name)
            file_name = new_name
        if os.path.getsize(file_name) > 2 * 10 ** 9:
            raise OSError
        return file_name
