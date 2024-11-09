#!/usr/bin/env python3

""" youtube-download.py at https://github.com/wilsonmar/python-samples/blob/main/youtube-download.py

CURRENT STATUS: WORKING for single file.
git commit -m "v008 + disk size :youtube-download.py"

./youtube-download.py -d ai-database-ops -vid 4SnvMieJiuw -o Downloads -v

Based on https://www.geeksforgeeks.org/pytube-python-library-download-youtube-videos/
"""

# pip install argparse
import argparse
# NOTE: pytube.io had errors.
# pip3 install yt_dlp because with Conda a non-default solver backend (libmamba) but it was not recognized. Choose one of: classic
import yt_dlp  # yt_dlp-2024.11.4

# Defaults:
import os
from datetime import datetime
from time import perf_counter_ns
import time  # for sleep.
import platform


# Globals:
start_time = time.time()  # start the program-level timer.

if os.name == "nt":  # Windows operating system
    SLASH_CHAR = "\\"
else:
    SLASH_CHAR = "/"


parser = argparse.ArgumentParser(description="YouTube download")
parser.add_argument("-d", "--desc", help="Description (file prefix)")
parser.add_argument("-vid", "--vid", help="YouTube Video ID")
parser.add_argument("-f", "--file", help="Input file name")
parser.add_argument("-o", "--folder", help="Folder output to user Home path")
parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
args = parser.parse_args()

YOUTUBE_PREFIX = args.desc
YOUTUBE_ID = args.vid
READ_LIST_PATH = args.file  # On Linux: //mount/?to_do
SHOW_VERBOSE = args.verbose
# print(f"*** -desc {args.desc}, -vid {args.vid} -file {args.file} {args.verbose}")

SAVE_FOLDER = args.folder
# SAVE_PATH = os.getcwd()  # cwd=current working directory.
SAVE_PATH = os.path.expanduser("~")  # user home folder path
# On Linux: //mount/?to_do
if SAVE_FOLDER == None:
    SAVE_PATH = SAVE_PATH + SLASH_CHAR + "Downloads"
else:
    SAVE_PATH = SAVE_PATH + SLASH_CHAR + SAVE_FOLDER

if os.path.isdir(SAVE_PATH):  # Confirmed a directory:
    if SHOW_VERBOSE:
        print(f"*** INFO: Downloading to folder: {SAVE_PATH}")
else:
    print(f"*** ERROR: Folder {SAVE_PATH} does not exist. Exiting.")
    exit()

if SHOW_VERBOSE == None:
    SHOW_VERBOSE = True
else:
    SHOW_VERBOSE = False

INCLUDE_DATE_OUT = False



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



def get_file_size_on_disk(file_path):
    try:
        stat_result = os.stat(file_path)
        return stat_result.st_blocks * 512  # st_blocks is in 512-byte units
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error getting file size: {e}")
        return None


#### Main:
if __name__ == "__main__":

    if READ_LIST_PATH == None:
        # https://www.youtube.com/watch?v=rISzLipRm7Y spin-right-mag-drives
        #YOUTUBE_PREFIX = "google-colab"
        # YOUTUBE_ID = "V7RXyqFUR98"  # Supercharge your Programming in Colab with AI-Powered tools by Google Research
        # YOUTUBE_ID = "ix9cRaBkVe0"  # Python Full Course for free 🐍 (2024) by Bro Code
        # YOUTUBE_ID = "fDAPJ7rvcUw"  # How AI Discovered a Faster Matrix Multiplication Algorithm
        # = "qrnjYfs-xVw"  # CS50x 2024 - Cybersecurity
        # YouTube URL to download (with time start and playlist):
        URL_TO_DOWNLOAD="https://www.youtube.com/watch?v=" + YOUTUBE_ID

        now = datetime.now()
        formatted_datetime = now.strftime("%Y%m%dT%H%M%SZ")
            # TODO: Add local time zone to local timezone instead of Z for UTC.
        YOUTUBE_FILE_NAME = YOUTUBE_PREFIX + "-" + YOUTUBE_ID
        if INCLUDE_DATE_OUT:
            YOUTUBE_FILE_NAME = YOUTUBE_FILE_NAME + "-" + formatted_datetime
        YOUTUBE_FILE_NAME = YOUTUBE_FILE_NAME + ".mp4"

        # On Linux & Macos:
        YOUTUBE_FILE_PATH=SAVE_PATH+"/"+YOUTUBE_FILE_NAME
        if SHOW_VERBOSE:
            print(f"*** YOUTUBE_FILE_PATH = {YOUTUBE_FILE_PATH}")

        t_ns_start = perf_counter_ns()  # Start task time stamp
        download_video(URL_TO_DOWNLOAD,YOUTUBE_FILE_PATH)
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
        # End timing
        # Log:
        t_ns_stop = time.perf_counter_ns()  # Stop task time stamp
        t_ns_duration_ns = (t_ns_stop - t_ns_start)      # naonseconds (ns)
        t_ns_duration_µs = t_ns_duration_ns / 1000      # microseconds (µs)
        t_ns_duration_ms = t_ns_duration_µs / 1000      # milliseconds (ms)
        t_ns_duration_secs = t_ns_duration_ms / 1000    #      seconds (secs)
        t_ns_duration_mins = t_ns_duration_secs / 1000  #      minutes (mins)
        file_bytes = get_file_size_on_disk(YOUTUBE_FILE_PATH)
        print(f"*** INFO: {YOUTUBE_FILE_NAME} % {t_ns_duration_secs:,.3f} secs % {file_bytes:,} bytes.")
    else:
        print("*** Downloading several files from list at ",READ_LIST_PATH)
        download_several(READ_LIST_PATH)


# STEP: Calculate the execution time:
end_time = time.time()
execution_time = end_time - start_time
if SHOW_VERBOSE == True:
    print(f"*** PERF: Program took {execution_time:.4f} seconds to run all tasks.")
      # *** PERF: Program took 0.5052 seconds to run all tasks.