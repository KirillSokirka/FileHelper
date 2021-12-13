from converterextension.src.com.brawlstars.file.converter.utils.FileExtensions import FileExtensions
from converterextension.src.com.brawlstars.file.converter.strategies.StrategyManager import StrategyManager

import os


class ExtendedConverter:
    def __init__(self, source_file_name, target_file_name):
        self.source_file_name = source_file_name
        self.target_file_name = target_file_name

    @property
    def source_file_name(self):
        return self.__source_file_name

    @source_file_name.setter
    def source_file_name(self, value):
        if not isinstance(value, str):
            raise TypeError('file name must be of type str')
        if not os.path.exists(value):
            raise IOError(value + ' file doesn\'t exist')
        self.__source_file_name = value

    @property
    def target_file_name(self):
        return self.__target_file_name

    @target_file_name.setter
    def target_file_name(self, value):
        if not isinstance(value, str):
            raise TypeError('file name must be of type str')
        self.__target_file_name = value

    def perform_convert(self):
        conversion_name = self.source_file_name.split('.')[-1] + '_to_' + self.__target_file_name.split('.')[-1]
        conversion_strategy = StrategyManager.get_strategy_for(conversion_name)
        conversion_strategy.convert(source=self.source_file_name, target=self.target_file_name)
