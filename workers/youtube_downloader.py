from pytube import YouTube
import os


class YouTubeDownloader:
    @staticmethod
    def check_url(yt_dto):
        try:
            YouTube(yt_dto.url).check_availability()
        except:
            return False
        return True

    @classmethod
    def download(cls, yt_dto):
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
