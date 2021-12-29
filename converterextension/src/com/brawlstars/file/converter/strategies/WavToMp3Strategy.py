from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from pydub import AudioSegment


class WavToMp3Strategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        wav_audio = AudioSegment.from_wav(source)
        wav_audio.export(target, format='mp3')
