#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Please reference .pylintrc for PEP8 formatting according to https://peps.python.org/pep-0008/
# conda install black  # to reformat
# pylint: disable=line-too-long trailing-newlines
"""
This is download-youtube.py at
https://github.com/wilsonmar/python-samples/blob/main/download-youtube.py

CURRENT STATUS: NOT WORKING

gas "v001 new :download-youtube.py"

Based on https://www.geeksforgeeks.org/pytube-python-library-download-youtube-videos/
"""

# pip3 install pytube (not in conda)
from pytube import YouTube   # https://pytube.io/en/latest/user/quickstart.html

    # pytube is a lightweight, Pythonic, dependency-free, library (and command-line utility) for downloading YouTube Videos.
    # from pytube.streams import Stream

# where to save
READ_LIST_PATH = ""  # On Linux: //mount/?to_do
# Path to save downloaded videos:
SAVE_PATH = ""  # On Linux: //mount/?to_do
# YouTube URL to download (with time start and playlist):
URL_TO_DOWNLOAD="https://www.youtube.com/watch?v=qrnjYfs-xVw"
#URL_TO_DOWNLOAD="https://www.youtube.com/watch?v=qrnjYfs-xVw&t=1m&list=PLDVrhnY7hFVr0Qykievv5qn0ApwCSYnHB&index=12&pp=iAQB"

yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')


def download_a_file(URL_TO_DOWNLOAD):

    print(">>> Downloading",URL_TO_DOWNLOAD)
    # get the video with the extension and
    # resolution passed in the get() function
    try:
        d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)
        # downloading the video
        d_video.download(SAVE_PATH)
    except:
        print("Some Error!")
        return f"Error!", None


def download_several(read_list_path):

    # link of the video to be downloaded
    # opening the file
    link=open(read_list_path,'r')

    for i in link:
        try:
            # object creation using YouTube
            # which was imported in the beginning
            yt = YouTube(i)
        except:

            #to handle exception
            print("Connection Error")

        #filters out all the files with "mp4" extension
        mp4files = yt.filter('mp4')

        download_a_file(URL_TO_DOWNLOAD)

    print('Task Completed!')


#### Main:
#
#### Audit parameters:
if SAVE_PATH == "":
    print(">>> Downloading to current folder!")
else:
    print(">>> Downloading to ",SAVE_PATH)

if READ_LIST_PATH == "":
    print(">>> Downloading a single file.")
    download_a_file(URL_TO_DOWNLOAD)
else:
    print(">>> Downloading a several files from list at ",READ_LIST_PATH)
    download_several(READ_LIST_PATH)




