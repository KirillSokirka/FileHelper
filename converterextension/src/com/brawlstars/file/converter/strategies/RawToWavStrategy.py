from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from pydub import AudioSegment


class RawToWavStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        AudioSegment.converter = 'ffmpeg\\bin\\ffmpeg.exe'
        mp3_audio = AudioSegment.from_file(file=source, frame_rate=44100, channels=2, sample_width=2)
        mp3_audio.export(target, format='wav')
