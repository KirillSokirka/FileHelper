from converterextension.src.com.brawlstars.file.converter.strategies.DocxToPdfStrategy import DocxToPdfStrategy
from converterextension.src.com.brawlstars.file.converter.strategies.DocxToTxtStrategy import DocxToTxtStrategy
from converterextension.src.com.brawlstars.file.converter.strategies.JpgToPngStrategy import JpgToPngStrategy
from converterextension.src.com.brawlstars.file.converter.strategies.JsonToXmlStrategy import JsonToXmlStrategy
from converterextension.src.com.brawlstars.file.converter.strategies.Mp3ToRawStrategy import Mp3ToRawStrategy
from converterextension.src.com.brawlstars.file.converter.strategies.Mp3ToWavStrategy import Mp3ToWavStrategy
from converterextension.src.com.brawlstars.file.converter.strategies.PngToJpgStrategy import PngToJpgStrategy
from converterextension.src.com.brawlstars.file.converter.strategies.Mp4ToMp3Strategy import Mp4ToMp3Strategy
from converterextension.src.com.brawlstars.file.converter.strategies.RawToMp3Strategy import RawToMp3Strategy
from converterextension.src.com.brawlstars.file.converter.strategies.RawToWavStrategy import RawToWavStrategy
from converterextension.src.com.brawlstars.file.converter.strategies.WavToMp3Strategy import WavToMp3Strategy
from converterextension.src.com.brawlstars.file.converter.strategies.WavToRawStrategy import WavToRawStrategy
from converterextension.src.com.brawlstars.file.converter.strategies.XmlToJsonStrategy import XmlToJsonStrategy


class StrategyManager:
    __strategies = {'jpg_to_png': JpgToPngStrategy(),
                    'png_to_jpg': PngToJpgStrategy(),
                    'mp4_to_mp3': Mp4ToMp3Strategy(),
                    'wav_to_mp3': WavToMp3Strategy(),
                    'wav_to_raw': WavToRawStrategy(),
                    'mp3_to_raw': Mp3ToRawStrategy(),
                    'mp3_to_wav': Mp3ToWavStrategy(),
                    'raw_to_mp3': RawToMp3Strategy(),
                    'raw_to_wav': RawToWavStrategy(),
                    'docx_to_txt': DocxToTxtStrategy(),
                    'docx_to_pdf': DocxToPdfStrategy(),
                    'xml_to_json': XmlToJsonStrategy(),
                    'json_to_xml': JsonToXmlStrategy()
                    }

    @classmethod
    def get_strategy_for(cls, conversion_name):
        if conversion_name not in cls.__strategies:
            raise ValueError('Sorry, but strategy for conversion ' + conversion_name + ' is not implemented')
        return cls.__strategies.get(conversion_name)
