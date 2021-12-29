#!/bin/bash
sudo apt update
sudo apt-get -y install python-dev build-essential
sudo apt -y install python3-pip
python3 -m pip install -U pip
export PATH="$HOME/.local/bin:$PATH"
pip3 install --upgrade setuptools
git clone https://github.com/sarakhmen/FileHelper.git
cd FileHelper
sudo apt install python3-pip
pip3 install -r requirements.txt
sudo apt-get install ffmpeg
sudo apt-get install pandoc