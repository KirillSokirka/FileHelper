from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from json import dump
from xmltodict import parse


class XmlToJsonStrategy(AbstractStrategy):
    def convert(self, source, target):
        dict_data = ''
        with open(source, 'r') as source_file:
            dict_data = parse(source_file.read())
        dump(dict_data, indent=4)
