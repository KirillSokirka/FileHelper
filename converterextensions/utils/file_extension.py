class FileExtensions:
    __supported_extensions = {'jpg': ['png'],
                              'png': ['jpg'],
                              'mp4': ['mp3'],
                              'wav': ['raw', 'mp3'],
                              'raw': ['wav', 'mp3'],
                              'mp3': ['wav', 'raw'],
                              'docx': ['txt', 'pdf'],
                              'xml': ['json'],
                              'json': ['xml']
                              }

    @classmethod
    def is_supported(cls, extension):
        return extension in cls.__supported_extensions

    @classmethod
    def get_possible_conversion_for(cls, extension):
        return cls.__supported_extensions.get(extension)

    @classmethod
    def get_supported_extensions(cls):
        return cls.__supported_extensions.keys()
