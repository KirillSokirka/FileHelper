from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

from comtypes.client import CreateObject
import pythoncom


class DocxToPdfStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        pythoncom.CoInitialize()
        word = CreateObject('Word.Application')
        document = word.Documents.Open(source)
        document.SaveAs(target, FileFormat=17)
        document.Close()
        word.Quit()
