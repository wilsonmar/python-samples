#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Please reference .pylintrc for PEP8 formatting according to https://peps.python.org/pep-0008/
# conda install black  # to reformat
# pylint: disable=line-too-long trailing-newlines
"""
This is youtube-download.py at
https://github.com/wilsonmar/python-samples/blob/main/youtube-download.py

CURRENT STATUS: NOT WORKING
gas "v005 add YOUTUBE_FILE_PATH verif :download-youtube.py"

Based on https://www.geeksforgeeks.org/pytube-python-library-download-youtube-videos/
"""

import os

# pip3 install pytube (not in conda)
from pytube import YouTube   # https://pytube.io/en/latest/user/quickstart.html

    # pytube is a lightweight, Pythonic, dependency-free, library (and command-line utility) for downloading YouTube Videos.
    # from pytube.streams import Stream

# where to save
READ_LIST_PATH = ""  # On Linux: //mount/?to_do
# Path to save downloaded videos:
SAVE_PATH = ""  # On Linux: //mount/?to_do
# YouTube URL to download (with time start and playlist):
URL_TO_DOWNLOAD="https://www.youtube.com/watch?v=fDAPJ7rvcUw"
# https://www.youtube.com/watch?v=qrnjYfs-xVw"
#URL_TO_DOWNLOAD="https://www.youtube.com/watch?v=qrnjYfs-xVw&t=1m&list=PLDVrhnY7hFVr0Qykievv5qn0ApwCSYnHB&index=12&pp=iAQB"
YOUTUBE_FILE_NAME="whatever.mp4"


def download_a_file(URL_TO_DOWNLOAD,YOUTUBE_FILE_PATH):

    print(">>> Downloading from:",URL_TO_DOWNLOAD)
    try:
        # object creation using YouTube
        yt = YouTube(link)
    except Exception as err:
        print(f">>> Link error {err=}, {type(err)=}")
        return f">>> Error!", None

     # get the video with the extension and
    # resolution passed in the get() function
    # Get all streams and filter for mp4 files
    mp4_streams = yt.streams.filter(file_extension='mp4').all()

    # get the video with the highest resolution:
    d_video = mp4_streams[-1]

    try:
        d_video.download(YOUTUBE_FILE_PATH)  # where SAVE_PATH is global
            # d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)
        print('>>> Video downloaded successfully!')

    except Exception as err:
        print(f">>> Unexpected {err=}, {type(err)=}")
        return f">>> Error!", None


def download_several(read_list_path):

    # link of the video to be downloaded
    # opening the file
    link=open(read_list_path,'r')
    # get YOUTUBE_FILE_NAME

    for i in link:
        try:
            # object creation using YouTube
            # which was imported in the beginning
            yt = YouTube(i)
        except:
            # TODO: handle exception
            print("Connection Error")

        #filters out all the files with "mp4" extension
        mp4files = yt.filter('mp4')

        download_a_file(URL_TO_DOWNLOAD)

    print('Task Completed!')


#### Main:
#
#### Audit parameters:
if SAVE_PATH == "":
    SAVE_PATH=os.getcwd()  # cwd=current working directory.
    print(">>> SAVE_PATH is blank!")

if os.path.isdir(SAVE_PATH):
    print(">>> Downloading to:  ",SAVE_PATH)
else:
    print(">>> Folder",SAVE_PATH," does not exist!")
    exit()


if READ_LIST_PATH == "":
    # On Linux & Macos:
    YOUTUBE_FILE_PATH=SAVE_PATH+"/"+YOUTUBE_FILE_NAME
    print(">>> Downloading file:",YOUTUBE_FILE_PATH)
    download_a_file(URL_TO_DOWNLOAD,YOUTUBE_FILE_PATH)
else:
    print(">>> Downloading a several files from list at ",READ_LIST_PATH)
    download_several(READ_LIST_PATH)

