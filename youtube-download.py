#!/usr/bin/env python3

""" youtube-download.py at https://github.com/wilsonmar/python-samples/blob/main/youtube-download.py

CURRENT STATUS: WORKING for single file.
git commit -m "v020 + colors & icons for msgs :youtube-download.py"

This program has a full set of features:
1. Specify first line #!/usr/bin/env python3 to run program directly.
2. Define github URL where program is located in docstring
3. STATUS of program defined (WORKING or not)
4. Latest change defined in docstring.

5. Read secrets from .env file outside the program and GitHub, cloud (akeyless.com)

6. Get parameters as arguments specified in call within CLI.
7. Set default attributes for production usage (minimal lines to STDOUT)
8. Enable attributes to be set for verbosity for each type of output (DEBUG).
9. TODO: Use different icons and colors to highlight each severity of message, etc.
10. TODO: Use feature flags for A/B testing (using Flagsmith?).

11. Display (Python operating system versions) environmnet being used.
12. Display status of progress within long tasks (SHOW_DOWNLOAD_PROGRESS).

13. Measure the duration of each function call and its processing scope.
14. TODO: Define OpenTelemetry (OTel) spans for tracing time across several tasks.
15. Output log entries with duration (and file bytes) for processing scope.
16. Zero-fill incremented numbers in displays.
17. Maintain a count of tasks performed (for normalizing ops times).
18. Output a summary log of total time, disk used to correlate with count of tasks.

19. TODO: Define a unique code for each message output.
20. TODO: Define positive and negative unit tests for each function (PyTest?)

21. Read CSV file for multiple iterations.
22. Set sleep time between each iteration to avoid overwhelming the server.
23. Stop after processing rather than KeyboardInterrupt which creates .part files.

24. List actions in CLI before running program.
25. Define in docstrings actions sample usage commands in CLI to run program.

Before running this program:
brew install miniconda
conda create -n py312
conda activate py312
conda config --set solver classic   # ModuleNotFoundError: No module named 'pycups'
conda install -c conda-forge python=3.12 argparse logging
brew install yt-dlp
chmod +x youtube-download.py
    python -m venv
    source venv/bin/activate
source venv/activate
python3 -m pip install argparse yt_dlp logging pytz

# USAGE ON CLI:
./youtube-download.py -d ai-database-ops -vid 4SnvMieJiuw -o Downloads -v
./youtube-download.py -f youtube-downloads.csv -v -vv

"""

# import external library (from outside this program):
from colorama import init, Fore, Style  # to style messages
import argparse

# brew install yt-dlp instead of pip3 install yt_dlp and instead of conda
# which issues a non-default solver backend (libmamba) but it was not recognized. Choose one of: classic
import yt_dlp  # yt_dlp-2024.11.4 at https://pypi.org/project/yt-dlp/
    # Import "yt_dlp" could not be resolvedPylancereportMissingImports
    # See https://www.perplexity.ai/search/what-about-the-yt-dlp-python-l-RPFKoI3yTrqsC8w.cI4NtQ
    # NOTE: Alternative pytube.io had errors.
# pip install logging
import logging  # error.
from logging.handlers import RotatingFileHandler


# Built-in libraries (no pip/conda install needed):
from datetime import datetime
from contextlib import redirect_stdout
from datetime import datetime
import io
import os
from pytz import timezone
import signal
import sys
from time import perf_counter_ns
import time
import platform
import random


# Globals to vary program run behavior:
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
parser.add_argument("-l", "--log", help="Log to external file")
parser.add_argument("-m", "--summary", action="store_true", help="Show summary")
parser.add_argument("-s", "--sleepsecs", action="store_true", help="Sleep seconds average")
parser.add_argument("-v", "--verbose", action="store_true", help="Show each download")
parser.add_argument("-vv", "--debug", action="store_true", help="Show debug")
# -h = --help (list arguments)
args = parser.parse_args()

YOUTUBE_PREFIX = args.desc
YOUTUBE_ID = args.vid

READ_LIST_PATH = args.file  # On Linux: //mount/?to_do

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
INCLUDE_DATE_OUT = False  # date/time stamp within file name

LOGGER_FILE_PATH = SAVE_PATH + SLASH_CHAR + os.path.basename(__file__) + '.log'
LOGGER_NAME = os.path.basename(__file__)  # program script name.py
LOG_DOWNLOADS = args.log
if SAVE_FOLDER == None:  # write logs outside the program
    LOG_DOWNLOADS = False  # hard-coded default

SHOW_SUMMARY = args.summary
SHOW_VERBOSE = args.verbose
if SHOW_VERBOSE:  # -vv
    SHOW_DOWNLOAD_PROGRESS = True
    SHOW_SUMMARY = True
else:
    SHOW_DOWNLOAD_PROGRESS = False

SHOW_DEBUG = args.debug  # print metadata before use by code during troubleshooting
if SHOW_DEBUG:  # -vv
    SHOW_DOWNLOAD_PROGRESS = True
    print(f"*** -desc {args.desc}, -vid {args.vid} -file {args.file} {args.verbose}")
    print(f"*** SHOW_VERBOSE={SHOW_VERBOSE} SHOW_DEBUG={SHOW_DEBUG} SHOW_DOWNLOAD_PROGRESS={SHOW_DOWNLOAD_PROGRESS}")

SLEEP_SECS = args.sleepsecs  # average seconds to wait between tasks to not overwhelm server.
if SLEEP_SECS == None:
   SLEEP_SECS = 0.5  # hard-coded default

SHOW_VERBOSE = args.verbose


# Functions:


class bcolors:  # ANSI escape sequences:
    BOLD = '\033[1m'       # Begin bold text
    UNDERLINE = '\033[4m'  # Begin underlined text

    HEADING = '\033[37m'   # [37 white
    FAIL = '\033[91m'      # [91 red
    ERROR = '\033[91m'     # [91 red
    WARNING = '\033[93m'   # [93 yellow
    INFO = '\033[92m'      # [92 green
    VERBOSE = '\033[95m'   # [95 purple
    TRACE = '\033[96m'     # [96 blue/green
                 # [94 blue (bad on black background)
    CVIOLET = '\033[35m'
    CBEIGE = '\033[36m'
    CWHITE = '\033[37m'

    RESET = '\033[0m'   # switch back to default color

def print_separator():
    """ A function to print a blank line."""
    print(" ")

def print_heading(text_in):
    if show_heading:
        if str(show_dates_in_logs) == "True":
            print('\n***', get_log_datetime(), bcolors.HEADING+bcolors.UNDERLINE,f'{text_in}', bcolors.RESET)
        else:
            print('\n***', bcolors.HEADING+bcolors.UNDERLINE,f'{text_in}', bcolors.RESET)

def print_fail(text_in):  # when program should stop
    if show_fail:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.FAIL, "FAIL:", f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.FAIL, "FAIL:", f'{text_in}', bcolors.RESET)

def print_error(text_in):  # when a programming error is evident
    if show_fail:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.ERROR, "ERROR:", f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.ERROR, "ERROR:", f'{text_in}', bcolors.RESET)

def print_warning(text_in):
    if show_warning:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.WARNING, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.WARNING, f'{text_in}', bcolors.RESET)

def print_todo(text_in):
    if show_todo:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.CVIOLET, "TODO:", f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.CVIOLET, "TODO:", f'{text_in}', bcolors.RESET)

def print_info(text_in):
    if show_info:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.INFO+bcolors.BOLD, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.INFO+bcolors.BOLD, f'{text_in}', bcolors.RESET)

def print_verbose(text_in):
    if show_verbose:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.VERBOSE, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.VERBOSE, f'{text_in}', bcolors.RESET)

def print_trace(text_in):  # displayed as each object is created in pgm:
    if show_trace:
        if str(show_dates_in_logs) == "True":
            print('***',get_log_datetime(), bcolors.TRACE, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.TRACE, f'{text_in}', bcolors.RESET)

def print_secret(secret_in):
    """ Outputs only the first few characters (like Git) with dots replacing the rest 
    """
    # See https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
    if show_secrets:  # program parameter
        if str(show_dates_in_logs) == "True":
            now_utc=datetime.now(timezone('UTC'))
            print('*** ',now_utc,bcolors.CBEIGE, "SECRET: ", f'{secret_in}', bcolors.RESET)
        else:
            print('***', bcolors.CBEIGE, "SECRET: ", f'{secret_in}', bcolors.RESET)
    else:
        # same length regardless of secret length to reduce ability to guess:
        secret_len = 32
        if len(secret_in) >= 20:  # slice
            secret_out = secret_in[0:4] + "."*(secret_len-4)
        else:
            secret_out = secret_in[0:4] + "."*(secret_len-1)
            if str(show_dates_in_logs) == "True":
                print('***', get_log_datetime(), bcolors.WARNING, f'{text_in}', bcolors.RESET)
            else:
                print('***', bcolors.CBEIGE, " SECRET: ", f'{secret_out}', bcolors.RESET)


def signal_handler(sig, frame):
    print("\n*** Manual Interrupt control+C or ctrl+C received.")
    sys.exit(0)


def display_run_env():
    print(f"*** {os.name} {sys.version_info}")
    print(f"*** Python version: {sys.version}")


#  if show_dates:  https://medium.com/tech-iiitg/zulu-module-in-python-8840f0447801
def get_log_datetime() -> str:

    # getting the current time in UTC timezone
    now_utc = datetime.now(timezone('UTC'))

    # TODO: Give datetime the user or system defined LOCALE:
    MY_DATE_FORMAT = "%Y-%m-%d %H:%M:%S %Z%z"
    # Format the above DateTime using the strftime() https://stackoverflow.com/questions/7588511/format-a-datetime-into-a-string-with-milliseconds
    time_str=datetime.utcnow().strftime('%F %T.%f')
       # ISO 8601-1:2019 like 2023-06-26 04:55:37.123456 https://www.iso.org/news/2017/02/Ref2164.html
    # time_str=now_utc.strftime(MY_DATE_FORMAT)

    # TODO: Converting to Asia/Kolkata time zone using the .astimezone method:
    # now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    # Format the above datetime using the strftime()
    # print('Current Time in Asia/Kolkata TimeZone:',now_asia.strftime(format))

    return time_str


def file_creation_datetime(path_to_file):
    """ Get the datetime stamp that a file was created, 
    falling back to when it was last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    WARNING: Use of epoch time means resolution is to the seconds (not microseconds)
    """
    if path_to_file is None:
        print_trace("path_to_file="+path_to_file)
    # print_trace("platform.system="+platform.system())
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            timestamp = os.path.getmtime(path_to_file)
            # Convert the timestamp to a human-readable datetime format:
            mod_time = datetime.fromtimestamp(timestamp)
            # Format the datetime to a string:
            formatted_timestamp = mod_time.strftime("%Y-%m-%dT%H:%M:%S")
            # if SHOW_DEBUG: print(f"formatted_timestamp={formatted_timestamp}")
            #return stat.st_birthtime # epoch datestamp like 1696898774.0
            return formatted_timestamp
        except AttributeError as e:
            print(f"*** ERROR: {e}")
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def get_file_size_on_disk(file_path):
    """Returns integer bytes from the OS for a file path """
    try:
        stat_result = os.stat(file_path)
        return stat_result.st_blocks * 512  # st_blocks is in 512-byte units
    except FileNotFoundError:
        print(f"*** File not found: {file_path}")
        return None
    except Exception as e:
        print(f"*** Error getting file size: {e}")
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
    #    if SHOW_VERBOSE:  # Log some example events
    #        log_event(logger, 'USER_LOGIN', 'User John Doe logged in successfully')
    #        log_event(logger, 'FILE_UPLOAD', 'File "document.pdf" uploaded', 'debug')
    #        log_event(logger, 'SYSTEM_ERROR', 'Database connection failed', 'error')
    #        log_event(logger, 'SECURITY_ALERT', 'Multiple failed login attempts detected', 'warning')
    log_levels = {
        'debug': logger.debug,
        'info': logger.info,
        'warning': logger.warning,
        'error': logger.error,
        'critical': logger.critical
    }
        # Success	Green	Checkmark or thumbs up
        # Error	Red	Exclamation mark or cross
        # Warning	Yellow	Triangle with an exclamation point
        # Informational	Blue	Information symbol (i)
        # Neutral/Draft	Gray	Document icon

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
    """ Download a YouTube based on URL.
    See https://ostechnix.com/yt-dlp-tutorial/
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
        if SHOW_DOWNLOAD_PROGRESS:
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

        file_create_datetime = file_creation_datetime(out_path)
        file_bytes = get_file_size_on_disk(out_path)  # type = number
        if SHOW_DEBUG:
            print(f"*** result = {result}")
        return_text = f"{out_path} {file_create_datetime} - {file_bytes:,} bytes"
        if result:  # True = good:
            return_text += f" in {t_ns_duration_secs:,.3f} secs."
        else:
            return_text += f" - EXISTS"
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
            downloads_count = 0
            # Iterate through rows, each with a line_number:
            for line_number, line in enumerate(file, start=1):
                row = line.strip().split(',')
                  # = ['N', '4SnvMieJiuw', 'i-database-ops', '19:07', '']
                row_sel = row[0]
                youtube_id = row[1]
                youtube_prefix = row[2]
                if downloads_count > 1:  # after the first one:
                    sleep_duration = int(SLEEP_SECS)
                        # FIXME: divide by zero
                        # sleep_duration = random.expovariate(SLEEP_SECS)
                    print(f"*** DEBUG: {downloads_count} ROW:{line_number} sleep_duration={sleep_duration}")
                    time.sleep(sleep_duration)  # to avoid inundating the server.
                if row_sel.upper() == "N":
                    if SHOW_VERBOSE:
                        print(f"*** ROW {str(line_number).zfill(4)}: {row_sel} vid={youtube_id} desc={youtube_prefix} SKIPPED.")
                    continue  # to next row.
                if SHOW_DEBUG:
                    print(f"*** ROW {str(line_number).zfill(4)}: {row_sel} vid={youtube_id} desc={youtube_prefix}")
                result = download_one_video(youtube_prefix,youtube_id)
                if not result.find("EXISTS"):  # if result NOT contains "EXISTS":
                    downloads_count += 1
                if SHOW_DEBUG:
                    print(f"*** RUN {downloads_count}: {result}")
                if LOG_DOWNLOADS:
                    log_event(logger, "INFO", result)
                if SHOW_VERBOSE:
                    print(f"*** ROW {str(line_number).zfill(4)}: {result}")
        return line_number, downloads_count
    # control+C on macOS or Ctrl+C on Windows.
    except SystemExit:  # instead of KeyboardInterrupt
        print(f"*** SystemExit gracefully after KeyboardInterrupt.")
        return line_number, downloads_count
    except Exception as e:
        print(f"*** ERROR {read_list_path} {e}")
        return None, None



if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    if LOG_DOWNLOADS:
        logger = setup_logger()
    if SHOW_DEBUG: display_run_env()
    downloads_count = 0

    if SHOW_DEBUG:
        print(f"*** READ_LIST_PATH={READ_LIST_PATH}")
    if READ_LIST_PATH:
        rows_count, downloads_count = download_youtube_from_csv(READ_LIST_PATH)
    else:
        result = download_one_video( YOUTUBE_PREFIX,YOUTUBE_ID )
        rows_count = 1


    # STEP: Calculate the program execution time:
    end_time = time.time()
    execution_time = end_time - start_time
    summary = (f"{os.path.basename(__file__)}" +
            f" took {execution_time:.4f} secs" +
            f" for {downloads_count} downloads" +
            f" in {rows_count} rows.")
    if SHOW_SUMMARY:
        print(f"*** RUN SUMMARY: {summary}")
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
FIXME: *** /Users/johndoe/Downloads/ai-database-ops-4SnvMieJiuw.mp4 - 48,001,024 bytes - EXISTS
2024-11-09 18:19:28,932 - INFO - INFO: /Users/johndoe/Downloads/ai-database-ops-4SnvMieJiuw.mp4 - 48,001,024 bytes - EXISTS
FIXNE: *** SUMMARY: youtube-download.py took 2.7077 seconds for 0 downloads in 2 rows.
"""