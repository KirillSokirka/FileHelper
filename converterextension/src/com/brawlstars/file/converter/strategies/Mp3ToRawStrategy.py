from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from pydub import AudioSegment


class Mp3ToRawStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        mp3_audio = AudioSegment.from_mp3(source)
        mp3_audio.export(target, format='raw')
