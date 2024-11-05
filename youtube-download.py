#!/usr/bin/env python3

""" youtube-download.py at https://github.com/wilsonmar/python-samples/blob/main/youtube-download.py

CURRENT STATUS: WORKING for single file.
git commit -m "v006 + YOUTUBE_PREFIX :youtube-download.py"

Based on https://www.geeksforgeeks.org/pytube-python-library-download-youtube-videos/
"""

import os

# NOTE: pytube.io had errors.
# pip3 install yt_dlp because with Conda a non-default solver backend (libmamba) but it was not recognized. Choose one of: classic
import yt_dlp
from datetime import datetime


# Globals:
READ_LIST_PATH = ""  # On Linux: //mount/?to_do


def download_video(url,out_path):
    """ Download a YouTube based on URL See https://ostechnix.com/yt-dlp-tutorial/
    """
    ydl_opts = {
        'format': 'best',  # Download the 'bestaudio/best' available quality
#        'download_ranges': lambda _: [{'start_time': 10, 'end_time': 20}],
#        'outtmpl': '%(title)s.%(ext)s',  # Set filename to video title
        'outtmpl': out_path,
        'noplaylist': True,  # Download single video if URL is part of a playlist
        'quiet': False,  # Show download progress in the console
        'ignoreerrors': False,  # Continue even if an error is encountered
        'no_warnings': False,  # Suppress warnings
#        'postprocessors': [{
#            'key': 'FFmpegExtractAudio',
#            'preferredcodec': 'mp3',
#            'preferredquality': '192',
#         }],
    }

    try:  # Use yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
        print("*** Download completed successfully.")
    except Exception as err:
        print(f"*** ERROR: {err}")


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
            print("*** Connection Error")

        #filters out all the files with "mp4" extension
        mp4files = yt.filter('mp4')

        download_a_file(URL_TO_DOWNLOAD)

    print('Task Completed!')


#### Main:
if __name__ == "__main__":

    # Path to save downloaded videos:
    SAVE_PATH = "/Users/johndoe/Downloads"
    # On Linux: //mount/?to_do
    # Blank = current path (program-samples)

    if SAVE_PATH == "":
        SAVE_PATH=os.getcwd()  # cwd=current working directory.
        print("*** SAVE_PATH is blank from os.getcwd()!")

    if os.path.isdir(SAVE_PATH):  # Confirmed a directory:
        print("*** Downloading to:  ",SAVE_PATH)
    else:
        print("*** Folder",SAVE_PATH," does not exist!")
        exit()

    if READ_LIST_PATH == "":
        YOUTUBE_PREFIX = "google-colab"
        YOUTUBE_ID = "V7RXyqFUR98"  # Supercharge your Programming in Colab with AI-Powered tools by Google Research
        # YOUTUBE_ID = "ix9cRaBkVe0"  # Python Full Course for free 🐍 (2024) by Bro Code
        # YOUTUBE_ID = "fDAPJ7rvcUw"  # How AI Discovered a Faster Matrix Multiplication Algorithm
        # = "qrnjYfs-xVw"  # CS50x 2024 - Cybersecurity
        # YouTube URL to download (with time start and playlist):
        URL_TO_DOWNLOAD="https://www.youtube.com/watch?v=" + YOUTUBE_ID

        now = datetime.now()
        formatted_datetime = now.strftime("%Y%m%dT%H%M%SZ")
        YOUTUBE_FILE_NAME = YOUTUBE_PREFIX + "-" YOUTUBE_ID + "-" + formatted_datetime + ".mp4"
        # TODO: Add local time zone to local timezone instead of Z for UTC.

        # On Linux & Macos:
        YOUTUBE_FILE_PATH=SAVE_PATH+"/"+YOUTUBE_FILE_NAME
        # print("*** Downloading file:",YOUTUBE_FILE_PATH)

        download_video(URL_TO_DOWNLOAD,YOUTUBE_FILE_PATH)
        # *** SAVE_PATH is blank!
        # *** Downloading to:   /Users/johndoe/github-wilsonmar/python-samples
        # *** Downloading file: /Users/johndoe/github-wilsonmar/python-samples/whatever-20241104T211954.mp4
        # [youtube] Extracting URL: https://www.youtube.com/watch?v=fDAPJ7rvcUw
        # [youtube] fDAPJ7rvcUw: Downloading webpage
        # [youtube] fDAPJ7rvcUw: Downloading ios player API JSON
        # [youtube] fDAPJ7rvcUw: Downloading mweb player API JSON
        # [youtube] fDAPJ7rvcUw: Downloading player 4e23410d
        # [youtube] fDAPJ7rvcUw: Downloading m3u8 information
        # [info] fDAPJ7rvcUw: Downloading 1 format(s): 251
        # [download] Destination: How AI Discovered a Faster Matrix Multiplication Algorithm.webm
        # [download] 100% of   13.27MiB in 00:00:02 at 6.16MiB/s
        # *** Download completed successfully.

    else:
        print("*** Downloading several files from list at ",READ_LIST_PATH)
        download_several(READ_LIST_PATH)
