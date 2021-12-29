from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from pydub import AudioSegment


class WavToMp3Strategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        # AudioSegment.converter = 'ffmpeg\\bin\\ffmpeg.exe'
        wav_audio = AudioSegment.from_wav(source)
        wav_audio.export(target, format='mp3')
