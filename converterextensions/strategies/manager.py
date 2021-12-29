from converterextensions.strategies.strategy import JpgToPngStrategy, PngToJpgStrategy, Mp4ToMp3Strategy, \
    WavToMp3Strategy, WavToRawStrategy, Mp3ToRawStrategy, Mp3ToWavStrategy, RawToMp3Strategy, RawToWavStrategy, \
    DocxToTxtStrategy, DocxToPdfStrategy, XmlToJsonStrategy, JsonToXmlStrategy


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
