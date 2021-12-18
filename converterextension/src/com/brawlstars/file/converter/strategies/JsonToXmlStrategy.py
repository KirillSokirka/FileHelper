from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from json import load
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


class JsonToXmlStrategy(AbstractStrategy):
    def convert(self, source, target):
        xml = ''
        with open(source, 'r') as source_file:
            xml = dicttoxml(load(source_file), attr_type=False)
        xml_dom = parseString(xml)
        with open(target, 'w') as target_file:
            target_file.write(xml_dom.toprettyxml())
