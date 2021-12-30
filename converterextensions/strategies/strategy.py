import pypandoc
import subprocess

from PIL import Image
from json import load
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from pydub import AudioSegment
from moviepy.editor import *
from json import dump
from xmltodict import parse


class AbstractStrategy:
    """
    Class to represent an abstract conversion strategy

    """

    def convert(self, source, target):
        """
        Get file from user
        :param source: a source file name
        :param target: a targed file name
        :return: None

        """

        raise NotImplementedError


class DocxToPdfStrategy(AbstractStrategy):
    """
    Class to represent docx to pdf conversion strategy

    """

    def convert(self, source: str, target: str):
        out_dir = ['/'.join(target.split('/')[:-1])]
        cmd = 'libreoffice --convert-to pdf --outdir'.split() + out_dir + [source]
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        p.wait(timeout=10)
        stdout, stderr = p.communicate()
        if stderr:
            raise subprocess.SubprocessError(stderr)
        os.rename(source.replace('.docx', '.pdf'), target)


class DocxToTxtStrategy(AbstractStrategy):
    """
    Class to represent docx to txt conversion strategy

    """

    def convert(self, source: str, target: str):
        pypandoc.convert_file(source, 'plain', outputfile=target)


class JpgToPngStrategy(AbstractStrategy):
    """
    Class to represent jpg to png conversion strategy

    """

    def convert(self, source, target):
        image = Image.open(source)
        image.save(target)


class JsonToXmlStrategy(AbstractStrategy):
    """
    Class to represent json to xml conversion strategy

    """

    def convert(self, source, target):
        xml = ''
        with open(source, 'r') as source_file:
            xml = dicttoxml(load(source_file), attr_type=False)
        xml_dom = parseString(xml)
        with open(target, 'w') as target_file:
            target_file.write(xml_dom.toprettyxml())


class Mp3ToRawStrategy(AbstractStrategy):
    """
    Class to represent mp3 to raw conversion strategy

    """

    def convert(self, source: str, target: str):
        mp3_audio = AudioSegment.from_mp3(source)
        mp3_audio.export(target, format='raw')


class Mp3ToWavStrategy(AbstractStrategy):
    """
    Class to represent mp3 to wav conversion strategy

    """

    def convert(self, source: str, target: str):
        mp3_audio = AudioSegment.from_mp3(source)
        mp3_audio.export(target, format='wav')


class Mp4ToMp3Strategy(AbstractStrategy):
    """
    Class to represent mp4 to mp3 conversion strategy

    """

    def convert(self, source, target):
        video = VideoFileClip(source)
        video.audio.write_audiofile(target)
        video.close()


class PngToJpgStrategy(AbstractStrategy):
    """
    Class to represent png to jpg conversion strategy

    """

    def convert(self, source, target):
        image = Image.open(source)
        rgb_image = image.convert('RGB')
        rgb_image.save(target)


class RawToMp3Strategy(AbstractStrategy):
    """
    Class to represent raw to mp3 conversion strategy

    """

    def convert(self, source: str, target: str):
        raw_audio = AudioSegment.from_file(file=source, frame_rate=44100, channels=2, sample_width=2)
        raw_audio.export(target, format='mp3')


class RawToWavStrategy(AbstractStrategy):
    """
    Class to represent raw to wav conversion strategy

    """

    def convert(self, source: str, target: str):
        mp3_audio = AudioSegment.from_file(file=source, frame_rate=44100, channels=2, sample_width=2)
        mp3_audio.export(target, format='wav')


class WavToMp3Strategy(AbstractStrategy):
    """
    Class to represent wav to mp3 conversion strategy

    """

    def convert(self, source: str, target: str):
        wav_audio = AudioSegment.from_wav(source)
        wav_audio.export(target, format='mp3')


class WavToRawStrategy(AbstractStrategy):
    """
    Class to represent wav to raw conversion strategy

    """

    def convert(self, source: str, target: str):
        wav_audio = AudioSegment.from_wav(source)
        wav_audio.export(target, format='raw')


class XmlToJsonStrategy(AbstractStrategy):
    """
    Class to represent xml to json conversion strategy

    """

    def convert(self, source, target):
        dict_data = ''
        with open(source, 'r') as source_file:
            dict_data = parse(source_file.read())
        with open(target, "w") as target_file:
            dump(dict_data, target_file, indent=4)


class ImagesToPdfStrategy(AbstractStrategy):
    """
    Class to represent images to pdf conversion (building) strategy

    """

    def convert(self, source, target):
        images = []
        for image_source in source:
            image = Image.open(image_source)
            images.append(image.convert('RGB'))
        images[0].save(target, save_all=True, append_images=images[1:])
