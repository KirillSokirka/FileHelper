class FileExtensions:
    __supported_extensions = {'jpg': ['png'],
                              'png': ['jpg'],
                              'mp4': ['mp3'],
                              'wav': ['raw', 'mp3'],
                              'raw': ['wav', 'mp3'],
                              'mp3': ['wav', 'raw'],
                              'docx': ['txt', 'pdf'],
                              'xml': ['json'],
                              'json': ['xml'],
                              'images': ['png', 'jpg']
                              }

    @classmethod
    def is_supported(cls, extension):
        return extension.lower() in cls.__supported_extensions

    @classmethod
    def get_possible_conversion_for(cls, extension):
        return cls.__supported_extensions.get(extension.lower())

    @classmethod
    def get_supported_extensions(cls):
        return cls.__supported_extensions.keys()

    @classmethod
    def is_photo(cls, extension):
        return extension.lower() in cls.__supported_extensions['images']
