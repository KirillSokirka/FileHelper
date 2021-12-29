from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from docx2pdf import convert


class DocxToPdfStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        convert(source, target)
