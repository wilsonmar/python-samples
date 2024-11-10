#!/usr/bin/env python3

""" youtube-download.py at https://github.com/wilsonmar/python-samples/blob/main/youtube-download.py

CURRENT STATUS: WORKING for single file.
git commit -m "v009 + LOGGER :youtube-download.py"

./youtube-download.py -d ai-database-ops -vid 4SnvMieJiuw -o Downloads -v

This program has a full set of features:
1. Specify first line #!/usr/bin/env python3 to run program directly.
2. Define github URL where program is located in docstring
3. STATUS of program defined (WORKING or not)
4. Latest changed defined in docstring.

5. Get parameters as arguments specified in call within CLI.
6. Default for production values.
7. Read secrets from .env file outside the program and GitHub, cloud (akeyless.com)
8. Display (Python operating system versions) environmnet being used.

9. Measure duration of each function call for process scope.
10. Output log entries with duration (and file bytes) for process scope.
11. Define a unique code for each message.

12. Positive and negative unit tests for each function (PyTest?)
13. Read CSV file for multiple iterations.

NOT APPLICABLE:
12. Define OpenTelemetry (OTel) spans for tracing.

"""

# pip install argparse
import argparse

# pip3 install yt_dlp because with Conda a non-default solver backend (libmamba) but it was not recognized. Choose one of: classic
import yt_dlp  # yt_dlp-2024.11.4
   # NOTE: Alternative pytube.io had errors.
# pip install logging
import logging  # error.
from logging.handlers import RotatingFileHandler

# Defaults:
import sys
import os
from datetime import datetime
from time import perf_counter_ns
import time
import platform


# Globals:
start_time = time.time()  # start the program-level timer.

if os.name == "nt":  # Windows operating system
    SLASH_CHAR = "\\"
    # if platform.system() == "Windows":
    print(f"*** Windows Edition: {platform.win32_edition()} Version: {platform.win32_ver()}")
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

if SHOW_VERBOSE == None:
    SHOW_VERBOSE = False
else:
    SHOW_VERBOSE = True

SAVE_FOLDER = args.folder
# SAVE_PATH = os.getcwd()  # cwd=current working directory.
SAVE_PATH = os.path.expanduser("~")  # user home folder path
# On Linux: //mount/?to_do
if SAVE_FOLDER == None:
    SAVE_PATH = SAVE_PATH + SLASH_CHAR + "Downloads"
else:
    SAVE_PATH = SAVE_PATH + SLASH_CHAR + SAVE_FOLDER

if not os.path.isdir(SAVE_PATH):  # Confirmed a directory:
    print(f"*** ERROR: Folder {SAVE_PATH} does not exist. Exiting.")
    exit()

LOGGER_FILE_PATH = SAVE_PATH + SLASH_CHAR + os.path.basename(__file__) + '.log'
LOGGER_NAME = os.path.basename(__file__)  # program script name.py

INCLUDE_DATE_OUT = False

ISSUE_ERROR = True


def display_run_env():
    print(f"*** {os.name} {sys.version_info}")
    print(f"*** Python version: {sys.version}")


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
        ns_start = perf_counter_ns()  # Start task time stamp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download(url)
        ns_stop = time.perf_counter_ns()  # Stop task time stamp
        ns_duration_ns = (ns_stop - ns_start)      # naonseconds (ns)
        ns_duration_µs = ns_duration_ns / 1000      # microseconds (µs)
        ns_duration_ms = ns_duration_µs / 1000      # milliseconds (ms)
        ns_duration_secs = ns_duration_ms / 1000    #      seconds (secs)
        ns_duration_mins = ns_duration_secs / 1000  #      minutes (mins)

        file_bytes = get_file_size_on_disk(out_path)  # type = number
        if result:  # True = good:
            return_text = f"{out_path} - {file_bytes:,} bytes in {t_ns_duration_secs:,.3f} secs."
        else:
            return_text = f"{out_path} - {file_bytes:,} bytes - EXISTS"
        return return_text
    except Exception as err:
        print(f"*** ERROR: {err}")
        return False


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



def setup_logger(log_file=LOGGER_FILE_PATH, console_level=logging.INFO, file_level=logging.DEBUG):
    """Set up and configure the logger."""
    # Create a logger
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)  # Set to lowest level to capture all logs

    # Create formatters
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)

    # File Handler (with rotation)
    file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    file_handler.setLevel(file_level)
    file_handler.setFormatter(file_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_event(logger, event_type, message, level='info'):
    """Log an event with the specified type and message."""
    log_levels = {
        'debug': logger.debug,
        'info': logger.info,
        'warning': logger.warning,
        'error': logger.error,
        'critical': logger.critical
    }
    log_func = log_levels.get(level.lower(), logger.info)
    log_func(f'{event_type}: {message}')


def main():

    logger = setup_logger()

    if SHOW_VERBOSE:  # Log some example events
        log_event(logger, 'USER_LOGIN', 'User John Doe logged in successfully')
        log_event(logger, 'FILE_UPLOAD', 'File "document.pdf" uploaded', 'debug')
        log_event(logger, 'SYSTEM_ERROR', 'Database connection failed', 'error')
        log_event(logger, 'SECURITY_ALERT', 'Multiple failed login attempts detected', 'warning')

    # Example of aZeroDivisionError exception being logged:
    if ISSUE_ERROR:
        try:
            1 / 0
        except Exception as e:
            logger.exception("**** ERROR: %s", str(e))


#### Main:
if __name__ == "__main__":

    logger = setup_logger()
    if SHOW_VERBOSE: display_run_env()

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
        YOUTUBE_FILE_NAME = YOUTUBE_PREFIX + "-" + YOUTUBE_ID
        if INCLUDE_DATE_OUT:
            # Add local time zone to local timezone instead of Z for UTC:
            formatted_datetime = now.strftime("%Y%m%dT%H%M%SZ")
            YOUTUBE_FILE_NAME = YOUTUBE_FILE_NAME + "-" + formatted_datetime
        YOUTUBE_FILE_NAME = YOUTUBE_FILE_NAME + ".mp4"

        # On Linux & Macos:
        YOUTUBE_FILE_PATH=SAVE_PATH+"/"+YOUTUBE_FILE_NAME
        if SHOW_VERBOSE:
            print(f"*** YOUTUBE_FILE_PATH = {YOUTUBE_FILE_PATH}")

        result = download_video(URL_TO_DOWNLOAD,YOUTUBE_FILE_PATH)
        if result:  # any text returned = good:
            perf_log_text = f"{result}"
        else:
            perf_log_text = f"EXISTS"
        if SHOW_VERBOSE:
            print(f"*** {perf_log_text}")
        log_event(logger, "INFO", perf_log_text)
    else:
        print("*** Downloading several files from list at ",READ_LIST_PATH)
        download_several(READ_LIST_PATH)


# STEP: Calculate the execution time:
end_time = time.time()
execution_time = end_time - start_time
if SHOW_VERBOSE == True:
    print(f"*** INFO: {os.path.basename(__file__)} took {execution_time:.4f} seconds to run all tasks.")
      # *** PERF: Program took 0.5052 seconds to run all tasks.


""" OUTPUT:
*** posix sys.version_info(major=3, minor=12, micro=7, releaselevel='final', serial=0)
*** Python version: 3.12.7 | packaged by conda-forge | (main, Oct  4 2024, 15:57:01) [Clang 17.0.6 ]
*** YOUTUBE_FILE_PATH = /Users/johndoe/Downloads/ai-database-ops-4SnvMieJiuw.mp4
[youtube] Extracting URL: https://www.youtube.com/watch?v=4SnvMieJiuw
[youtube] 4SnvMieJiuw: Downloading webpage
[youtube] 4SnvMieJiuw: Downloading ios player API JSON
[youtube] 4SnvMieJiuw: Downloading mweb player API JSON
[youtube] 4SnvMieJiuw: Downloading m3u8 information
[info] 4SnvMieJiuw: Downloading 1 format(s): 18
[download] /Users/johndoe/Downloads/ai-database-ops-4SnvMieJiuw.mp4 has already been downloaded
[download] 100% of   45.78MiB
*** /Users/johndoe/Downloads/ai-database-ops-4SnvMieJiuw.mp4 - 48,001,024 bytes - EXISTS
2024-11-09 18:19:28,932 - INFO - INFO: /Users/johndoe/Downloads/ai-database-ops-4SnvMieJiuw.mp4 - 48,001,024 bytes - EXISTS
*** INFO: youtube-download.py took 2.6612 seconds to run all tasks.
"""