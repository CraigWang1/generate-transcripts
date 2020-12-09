#!/bin/bash
# Install everything needed to automatically fetch automatically generated subtitles from youtube video.

# Install dependencies
sudo pip3 install requirements.txt

# Install selenium geckodriver
wget -O geckodriver_download https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux32.tar.gz
tar -xzf geckodriver_download
rm geckodriver_download 
