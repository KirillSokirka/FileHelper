from converterextension.src.com.brawlstars.file.converter.strategies.AbstractStrategy import AbstractStrategy

import pypandoc


class DocxToTxtStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        pypandoc.convert_file(source, 'plain', outputfile=target)
