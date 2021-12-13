import requests
import os

from configs import config


class FileDownloader:
    @staticmethod
    def download(url, file_name):
        r = requests.get(url, allow_redirects=True)
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        with open(file_name, 'wb') as f:
            f.write(r.content)
