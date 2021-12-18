import requests
import os


class FileManager:
    @staticmethod
    def download(url, file_name):
        r = requests.get(url, allow_redirects=True)
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        with open(file_name, 'wb') as f:
            f.write(r.content)

    @staticmethod
    def remove_files(*file_names):
        for file_name in file_names:
            if os.path.exists(file_name):
                os.remove(file_name)
