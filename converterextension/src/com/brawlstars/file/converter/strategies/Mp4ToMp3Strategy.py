from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from moviepy.editor import *


class Mp4ToMp3Strategy(AbstractStrategy):
    def convert(self, source, target):
        video = VideoFileClip(source)
        video.audio.write_audiofile(target)
        video.close()
