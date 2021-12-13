from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from PIL import Image


class JpgToPngStrategy(AbstractStrategy):
    def convert(self, source, target):
        image = Image.open(source)
        image.save(target)
