from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from json import dump
from pandas_read_xml import read_xml


class XmlToJsonStrategy(AbstractStrategy):
    def convert(self, source, target):
        df = read_xml(source)
        with open(target, 'w') as target_file:
            target_file.write(df.to_json(indent=4))
