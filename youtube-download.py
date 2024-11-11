#!/usr/bin/env python3

""" youtube-download.py at https://github.com/wilsonmar/python-samples/blob/main/youtube-download.py

CURRENT STATUS: WORKING for single file.
git commit -m "v011 + download CSV :youtube-download.py"

USAGE ON CLI:
./youtube-download.py -d ai-database-ops -vid 4SnvMieJiuw -o Downloads -v
./youtube-download.py -f youtube-downloads.csv -v

This program has a full set of features:
1. Specify first line #!/usr/bin/env python3 to run program directly.
2. Define github URL where program is located in docstring
3. STATUS of program defined (WORKING or not)
4. Latest changed defined in docstring.

5. Get parameters as arguments specified in call within CLI.
6. Default for production values.
7. Read secrets from .env file outside the program and GitHub, cloud (akeyless.com)
8. Display (Python operating system versions) environmnet being used.

9. Use flags to display status of progress (using Flagsmith?)
10. Measure duration of each function call for process scope.
11. Output log entries with duration (and file bytes) for process scope.
12. Define a unique code for each message.

13. Positive and negative unit tests for each function (PyTest?)
14. Read CSV file for multiple iterations.
15. Maintain a count of tasks performed (for normalizing ops times).

NOT APPLICABLE:
16. Define OpenTelemetry (OTel) spans for tracing.

Before running this program:
brew install miniconda
conda create -n py312
conda activate py312
conda config --set solver classic
conda install -c conda-forge python=3.12 matplotlib numpy scienceplots
   # ModuleNotFoundError: No module named 'pycups'
pip install pycups  docx  docx2pdf  
chmod +x print-cups.py  # pycups-2.0.4
./print-cups.py

"""

# pip instaly
#
# y
# yl argparse
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

import io
from contextlib import redirect_stdout

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
parser.add_argument("-f", "--file", help="Input CSV to create files")
parser.add_argument("-o", "--folder", help="Folder output to user Home path")
parser.add_argument("-s", "--summary", action="store_true", help="Show summary")
parser.add_argument("-v", "--verbose", action="store_true", help="Show each download")
parser.add_argument("-x", "--debug", action="store_true", help="Show debug")
args = parser.parse_args()

YOUTUBE_PREFIX = args.desc
YOUTUBE_ID = args.vid
READ_LIST_PATH = args.file  # On Linux: //mount/?to_do
SHOW_SUMMARY = args.summary
SHOW_VERBOSE = args.verbose
SHOW_DEBUG = args.debug
SHOW_DOWNLOAD_DETAILS = False
if SHOW_DEBUG:
    print(f"*** -desc {args.desc}, -vid {args.vid} -file {args.file} {args.verbose}")
    print(f"*** SHOW_VERBOSE={SHOW_VERBOSE} SHOW_DEBUG={SHOW_DEBUG} SHOW_DOWNLOAD_DETAILS={SHOW_DOWNLOAD_DETAILS}")

INCLUDE_DATE_OUT = False
ISSUE_ERROR = True

SAVE_FOLDER = args.folder
# SAVE_PATH = os.getcwd()  # cwd=current working directory.
SAVE_PATH = os.path.expanduser("~")  # user home folder path
# On Linux: //mount/?to_do
if SAVE_FOLDER == None:
    SAVE_PATH = SAVE_PATH + SLASH_CHAR + "Downloads"
else:
    SAVE_PATH = SAVE_PATH + SLASH_CHAR + SAVE_FOLDER

LOG_DOWNLOADS = True
if not os.path.isdir(SAVE_PATH):  # Confirmed a directory:
    print(f"*** ERROR: Folder {SAVE_PATH} does not exist. Exiting.")
    exit()
LOGGER_FILE_PATH = SAVE_PATH + SLASH_CHAR + os.path.basename(__file__) + '.log'
LOGGER_NAME = os.path.basename(__file__)  # program script name.py


# Functions:


def display_run_env():
    print(f"*** {os.name} {sys.version_info}")
    print(f"*** Python version: {sys.version}")


def get_file_size_on_disk(file_path):
    """Returns integer bytes from the OS for a file path """
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


def download_one_video(youtube_prefix,youtube_id):
    # Uses globals SHOW_VERBOSE, INCLUDE_DATE_OUT, SLASH_CHAR, LOG_DOWNLOADS

    URL_TO_DOWNLOAD="https://www.youtube.com/watch?v=" + youtube_id
    # https://www.youtube.com/watch?v=rISzLipRm7Y hd-spin-right
    # YOUTUBE_PREFIX = "google-colab"
    # YOUTUBE_ID = "V7RXyqFUR98"  # Supercharge your Programming in Colab with AI-Powered tools by Google Research
    # YOUTUBE_ID = "ix9cRaBkVe0"  # Python Full Course for free 🐍 (2024) by Bro Code
    # YOUTUBE_ID = "fDAPJ7rvcUw"  # How AI Discovered a Faster Matrix Multiplication Algorithm
    # = "qrnjYfs-xVw"  # CS50x 2024 - Cybersecurity
    # YouTube URL to download (with time start and playlist):

    # Build: /Users/johndoe/Downloads/ai-database-ops-4SnvMieJiuw.mp4
    YOUTUBE_FILE_NAME = youtube_prefix + "-" + youtube_id
    if INCLUDE_DATE_OUT:
        # Add local time zone to local timezone instead of Z for UTC:
        now = datetime.now()
        YOUTUBE_FILE_NAME += "-" + now.strftime("%Y%m%dT%H%M%SZ")+".mp4"
    else:
        YOUTUBE_FILE_NAME += ".mp4"

    YOUTUBE_FILE_PATH = SAVE_PATH + SLASH_CHAR + YOUTUBE_FILE_NAME
    if SHOW_DEBUG:
        print(f"*** YOUTUBE_FILE_PATH = {YOUTUBE_FILE_PATH}")

    result = download_video(URL_TO_DOWNLOAD,YOUTUBE_FILE_PATH)
    return result


def download_video(in_url,out_path):
    """ Download a YouTube based on URL See https://ostechnix.com/yt-dlp-tutorial/
    """
    ydl_opts = {
        'format': 'best',  # Download the 'bestaudio/best' available quality
#        'download_ranges': lambda _: [{'start_time': 10, 'end_time': 20}],
        'outtmpl': out_path,  # Set filename to video title
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
        if SHOW_DOWNLOAD_DETAILS:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.download(in_url)
        else:
            with redirect_stdout(io.StringIO()):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    result = ydl.download(in_url)
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


def download_youtube_from_csv(read_list_path):
    """Returns file size from each download based on line in CSV file."""
    try:
        with open(read_list_path,'r', newline='') as file:
            # Instead of creating a csv.reader(file) object:
            header = file.readline().strip().split(',')
            if SHOW_DEBUG:
                print(f"*** header = {header}")   # list
                      # *** header = ['_sel', '_vid', '_desc', '_len', '_notes']
            # Iterate through rows, each with a line_number:
            downloads_count = 0
            for line_number, line in enumerate(file, start=1):
                row = line.strip().split(',')
                  # = ['N', '4SnvMieJiuw', 'i-database-ops', '19:07', '']
                row_sel = row[0]
                youtube_id = row[1]
                youtube_prefix = row[2]
                if row_sel.upper() == "N":
                    if SHOW_VERBOSE:
                        print(f"*** ROW {line_number}: {row_sel} vid={youtube_id} desc={youtube_prefix} SKIPPED.")
                    continue  # to next row.
                if SHOW_DEBUG:
                    print(f"*** ROW {line_number}: {row_sel} vid={youtube_id} desc={youtube_prefix}")
                result = download_one_video(youtube_prefix,youtube_id)
                if not result.find("EXISTS"):  # if result NOT contains "EXISTS":
                    downloads_count += 1
                if SHOW_DEBUG:
                    print(f"*** RUN {downloads_count}: {result}")
                if LOG_DOWNLOADS:
                    log_event(logger, "INFO", result)
                if SHOW_VERBOSE:
                    print(f"*** ROW {line_number}: {result}")
        return line_number, downloads_count
    except Exception as e:
        print(f"*** ERROR {read_list_path} {e}")
        return None


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



if __name__ == "__main__":

    logger = setup_logger()
    if SHOW_DEBUG: display_run_env()
    downloads_count = 0

    if READ_LIST_PATH == None:
        result = download_one_video( YOUTUBE_PREFIX,YOUTUBE_ID )
        rows_count = 1
    else:
        if SHOW_DEBUG:
            print(f"*** Downloading file {READ_LIST_PATH}")
        rows_count, downloads_count = download_youtube_from_csv(READ_LIST_PATH)


    # STEP: Calculate the program execution time:
    end_time = time.time()
    execution_time = end_time - start_time
    if SHOW_SUMMARY:
        summary = (f"{os.path.basename(__file__)}" +
                f" took {execution_time:.4f} seconds" +
                f" for {downloads_count} downloads" +
                f" in {rows_count} rows.")
        print(f"*** SUMMARY: {summary}")
        if LOG_DOWNLOADS:
            log_event(logger, "SUMMARY", summary)


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
[download] Destination: /Users/johndoe/Downloads/hd-spin-right-rISzLipRm7Y.mp4
[download] 100% of   35.21MiB in 00:00:04 at 8.01MiB/s
*** /Users/johndoe/Downloads/ai-database-ops-4SnvMieJiuw.mp4 - 48,001,024 bytes - EXISTS
2024-11-09 18:19:28,932 - INFO - INFO: /Users/johndoe/Downloads/ai-database-ops-4SnvMieJiuw.mp4 - 48,001,024 bytes - EXISTS
*** SUMMARY: youtube-download.py took 2.7077 seconds for 0 downloads in 2 rows.
"""