#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click",
#   "cryptography",
#   "geopy",
#   "keyring",
#   "opentelemetry-api",
#   "opentelemetry-sdk",
#   "psutil",
#   "pyAesCrypt",
#   "python-dotenv",
#   "qrcode",
#   "requests",
#   "timezonefinder",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

#### SECTION 01: Define

"""myutils.py here.

This Python module provides utility functions called by my other custom programs running on macOS:
opentelemetry.py, gcp-services.py, etc.

Functions provided show OS properties, process directories, files, strings, etc.

For use by gcp-setup.sh, etc.

BEFORE RUNNING, on Terminal:
   # cd to a folder to receive folder (such as github-wilson):
   git clone https://github.com/wilsonmar/python-samples.git --depth 1
   cd python-samples
   # uv init was run to set pyproject.toml & .python-version 
   python3 -m pip install uv
   python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
   uv venv .venv
   source .venv/bin/activate       # on macOS & Linux
        # ./scripts/activate       # PowerShell only
        # ./scripts/activate.bat   # Windows CMD only
   uv add contextlib getpass keyring subprocess --frozen

   ruff check myutils.py
   chmod +x myutils.py
   uv run myutils.py -v
      # -v for verbose
      # -vv to trace
      # Terminal should not freeze.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__

"""
#### SECTION 02: Dundar variables for git command gxp to git add, commit, push

# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-04-01"
__commit_msg__ = "26-04-01 v012 fix uv :myutils.py"
__repository__ = "https://github.com/bomonike/google/blob/main/myutils.py"
# __repository__ = "https://github.com/wilsonmar/python-samples/blob/main/myutils.py"
__status__ = "WORKING: ruff check myutils.py => All checks passed!"
# STATUS: Python 3.13.3 working on macOS Sequoia 15.3.1

# from https://github.com/trkonduri/myutils/blob/master/myutils.py


#### SECTION 02: Capture pgm start date/time from the earliest point:

# ruff: noqa: E402 Module level import not at top of file
# See https://bomonike.github.io/python-samples/#StartingTime
# Built-in libraries (no pip/conda install needed):
import time  # for timestamp
from datetime import datetime, timezone

# POLICY: Display local wall clock date & time on program start.
# pgm_strt_datetimestamp = datetime.now() has been deprecated.
pgm_strt_timestamp = time.monotonic()

# from zoneinfo import ZoneInfo  # For Python 3.9+ https://docs.python.org/3/library/zoneinfo.html
# TODO: Display Z (UTC/GMT) instead of local time
pgm_strt_epoch_timestamp = time.time()
pgm_strt_local_timestamp = time.localtime()
# NOTE: Can't display the dates until formatting code is run below


#### SECTION 03: Built-in Local Python libraries imports:

# POLICY: Capture start time for measuring standard python library load time.
# from time import perf_counter_ns
std_strt_timestamp = time.monotonic()

import argparse
import ast
import gc
import hashlib

# UNUSED: import http.client
import importlib.util
import inspect
import io
import json

# UNUSED: import logging   # see https://realpython.com/python-logging/
# UNUSED: import math
import os
from pathlib import Path

import platform  # https://docs.python.org/3/library/platform.html
import pwd  # https://www.geeksforgeeks.org/pwd-module-in-python/

# UNUSED: import random
import resource
import secrets
import shutil  # for disk space calcs
import site
import smtplib
import socket
import string
import subprocess
import sys

# import boto3  # for aws python
# UNUSED: from collections import OrderedDict
from collections import defaultdict
from typing import Any, Dict

# UNUSED: import base64
import click

# UNUSED: import urllib.request
# UNUSED: from urllib import request
# UNUSED: from urllib import parse
# UNUSED: from urllib import error
# UNUSED: import uuid

# POLICY: Capture stop time for measuring standard python library load time.
std_stop_timestamp = time.monotonic()


#### SECTION 04: Third-party External Python libraries (requiring pip install):

# POLICY: Capture start time for measuring external python library load time.
xpt_strt_timestamp = time.monotonic()

# Each module should be in requirements.txt:
try:
    # pylint: disable=wrong-import-position
    # UNUSED: import statsd
    # UNUSED: from tabulate import tabulate
    import tracemalloc
    from contextlib import redirect_stdout
    from email.mime.text import MIMEText

    # UNUSED: import pandas as pd
    from pathlib import Path

    import keyring  # on macOS
    import psutil  #  psutil-5.9.5

    # UNUSED: from pythonping import ping
    import pyAesCrypt  # pip install pyAesCrypt

    # UNUSED: import pytz   # time zones
    import qrcode
    import requests
    from cryptography.fernet import Fernet  # pip install cryptography
    from cryptography.hazmat.primitives import (
        serialization,  # uv pip install cryptography
    )
    from cryptography.hazmat.primitives.asymmetric import (
        rsa,  # uv pip install cryptography
    )
    from dotenv import load_dotenv  # install python-dotenv
#◦  opentelemetry-api>=1.30.0
#◦  opentelemetry-sdk>=1.30.0
#◦  opentelemetry-instrumentation>=0.51b0
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
except Exception as e:
    print(f"Python module import failed: {e}")
    # pyproject.toml file exists
    # print_?() not used becuase they are defined after this line:
    print("Please activate your virtual environment:\n  python3 -m venv venv && source .venv/bin/activate")
    exit(9)

# POLICY: Capture stop time for measuring external python library load time.
xpt_stop_timestamp = time.monotonic()


#### SECTION 05: Capture starting memory usage:

env_file = "~/python-samples.env"

def memory_used() -> float:
    """Return memory used."""
    # import os, psutil  #  psutil-5.9.5
    process = psutil.Process()
    mem = process.memory_info().rss / (1024**2)  # in bytes
    print(str(process))
    print("memory used()=" + str(mem) + " MiB")
    return mem


def diskspace_free() -> float:
    """Return displace free."""
    # import os, psutil  #  psutil-5.9.5
    disk = psutil.disk_usage("/")
    free_space_gb = disk.free / (1024 * 1024 * 1024)  # = 1024 * 1024 * 1024
    print(f"diskspace_free()={free_space_gb:.2f} GB")
    return free_space_gb


pgm_strt_mem_used = memory_used()
pgm_strt_disk_free = diskspace_free()


#### SECTION 05: Time utility functions:


def day_of_week(local_time_obj) -> str:
    """Return day of week name from weekday() number."""
    # str(days[local_time_obj.weekday()])  # Monday=0 ... Sunday=6
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return str(days[local_time_obj.weekday()])


def test_datetime():
    """Test function to verify datetime functionality."""
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d-%H:%M")
    return formatted_time


def get_user_local_time() -> str:
    """Return a string formatted with datetime stamp in local timezone.

    Not used in logs which should be in UTC.
    Example: "07:17 AM (07:17:54) 2025-04-21 MDT"
    """
    now: datetime = datetime.now()
    local_tz = datetime.now(timezone.utc).astimezone().tzinfo
    return f"{now:%I:%M %p (%H:%M:%S) %Y-%m-%d} {local_tz}"


def get_user_local_timestamp(format_str: str = "yymmddhhmm") -> str:
    """Return a string formatted with datetime stamp in local timezone.

    Not used in logs which should be in UTC.
    Example: "07:17 AM (07:17:54) 2025-04-21 MDT"
    """
    current_time = time.localtime()  # localtime([secs])
    year = str(current_time.tm_year)[-2:]  # Last 2 digits of year
    month = str(current_time.tm_mon).zfill(2)  # .zfill(2) = zero fill
    day = str(current_time.tm_mday).zfill(2)  # Day with leading zero
    hour = str(current_time.tm_hour).zfill(2)  # Day with leading zero
    minute = str(current_time.tm_min).zfill(2)  # Day with leading zero
    if format_str == "yymmdd":
        return f"{year}{month}{day}"
    if format_str == "yymmddhhmm":
        return f"{year}{month}{day}{hour}{minute}"


# TODO: Google lasStepTimestamp": "2025-06-07T23:51:54.757-07:00",


def filetimestamp(filename):
    """Obtain file timestamp.

    USAGE: print(f"File last modified: {myutils.filetimestamp("myutils.py")} ")
    # TODO: Add time zone info. 📢
    """
    created = os.path.getmtime(filename)
    modified = os.path.getctime(filename)
    if created == modified:
        return f"{ctimestamp(filename)}"
    else:
        return f"{mtimestamp(filename)}"


def mtimestamp(filename):
    """Print mtime.

    USAGE: print(f"File last modified: {myutils.mtimestamp("myutils.py")} ")
    """
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t).strftime("%Y-%m-%d-%H:%M")


def ctimestamp(filename):
    """Print time.

    USAGE: print(f"File created: {myutils.ctimestamp("myutils.py")}")
    Fixed datetime import issue
    """
    t = os.path.getctime(filename)
    # Use the imported datetime class correctly
    return datetime.fromtimestamp(t).strftime("%Y-%m-%d-%H:%M")


def list_files(basepath, validexts=None, contains=None):
    """List files.

    USAGE: print(myutils.list_files("./"))
    List files in a directory with optional filters.
    Args:
        basePath: Base directory to search for files
        validExts: Optional tuple of valid file extensions
        contains: Optional string to filter file names
    Yields:
        File paths that match the filters
    """
    for rootdir, dirnames, filenames in os.walk(basepath):
        for filename in filenames:
            if contains is not None and filename.find(contains) == -1:
                continue
            # reverse find the "." from back wards
            ext = filename[filename.rfind(".") :]
            if validexts is None or ext.endswith(validexts):
                file = os.path.realpath(os.path.join(rootdir, filename))
                yield file


RUNID = get_user_local_timestamp()  # "yymmddhhmm"
PROGRAM_NAME = os.path.basename(os.path.normpath(sys.argv[0]))
global_env_path = None


#### SECTION 03: Print utility globals and functions (as early in pgm as possible)


## Global variables: Colors Styles:
class Bcolors:
    """ANSI escape sequences.

    See https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
    """

    BOLD = "\033[1m"  # Begin bold text
    UNDERLINE = "\033[4m"  # Begin underlined text

    INFO = "\033[92m"  # [92 green
    HEADING = "\033[37m"  # [37 white
    VERBOSE = "\033[91m"  # [91 beige
    WARNING = "\033[93m"  # [93 yellow
    ERROR = "\033[95m"  # [95 purple
    TRACE = "\033[35m"  # CVIOLET
    TODO = "\033[96m"  # [96 blue/green
    FAIL = "\033[31m"  # [31 red
    # [94 blue (bad on black background)
    STATS = "\033[36m"  # [36 cyan
    CVIOLET = "\033[35m"
    CBEIGE = "\033[36m"
    CWHITE = "\033[37m"
    GRAY = "\033[90m"

    RESET = "\033[0m"  # switch back to default color


# Starting settings:
show_secrets = False  # Always False to not show
show_heading = True  # -q  Don't display step headings before attempting actions
show_fail = True  # Always show
show_error = True  # Always show
show_warning = True  # Always show
show_trace = True  # -vv Display responses from API calls for debugging code
show_verbose = True  # -v  Display technical program run conditions
show_sys_info = True
show_todo = True
show_info = True
SHOW_DEBUG = True
show_dates_in_logs = False
print_prefix = "***"

SHOW_SUMMARY_COUNTS = True


def no_newlines(in_string):
    """Strip new line from in_string."""
    return "".join(in_string.splitlines())


def print_separator():
    """Print a blank line in CLI output.

    Used in case the technique changes throughout this code.
    """
    print(" ")


def print_heading(text_in):
    """Print underlined words for several additional lines to follow."""
    if show_heading:
        # Backhand Index Pointing Down Emoji highlights content below was approved as part of Unicode 6.0 in 2010 under the name "White Down Pointing Backhand Index" and added to Emoji 1.0 in 2015.
        print("👇", end="")
        if show_dates_in_logs:
            print(get_log_datetime(), end="")
        print(Bcolors.HEADING + Bcolors.UNDERLINE, f"{text_in}", Bcolors.RESET)


def print_fail(text_in):
    """Print when program should stop."""
    if show_fail:  # typically a programming error.
        # The ⛔ No Entry (Stop sign) Emoji indicates forbidden. approved as part of Unicode 5.2 in 2009 and added to Emoji 1.0 in 2015.
        print("❌", end="")
        if show_dates_in_logs:
            print(get_log_datetime(), end="")
        print(Bcolors.FAIL, f"{text_in}", Bcolors.RESET)
        # PROTIP: For easier debugging, use a program exit command at point of failure rather than here.


def print_error(text_in):
    """Print when a programming error is evident."""
    if show_fail:
        print("⭕", end="")
        if show_dates_in_logs:
            print(get_log_datetime(), end="")
        print(Bcolors.ERROR, f"{text_in}", Bcolors.RESET)


def print_warning(text_in):
    """Print warning about the conditions of data."""
    if show_warning:
        print("⚠️", end="")
        if show_dates_in_logs:
            print(get_log_datetime(), end="")
        print(Bcolors.WARNING, f"{text_in}", Bcolors.RESET)


def print_todo(text_in):
    """Print tasks programmer should remember to do."""
    if show_todo:
        # The 🛠️ hammer and wrench emoji is commonly used for various content concerning tools, building, construction, and work, both manual and digital
        print("💡", end="")
        if show_dates_in_logs:
            print(get_log_datetime(), end="")
        print(Bcolors.TODO, f"{text_in}", Bcolors.RESET)


def print_info(text_in):
    """Print info for user."""
    if show_info:
        # Alternately: print("👍", end="")
        print("✅", end="")
        if show_dates_in_logs:
            print(get_log_datetime(), end="")
        print(Bcolors.INFO + Bcolors.BOLD, f"{text_in}", Bcolors.RESET)


def print_verbose(text_in):
    """Print program operation internals."""
    if show_verbose:
        # The 📣 speaker emoji is used to represent sound, noise, or speech.
        print("📢", end="")
        if show_dates_in_logs:
            print(get_log_datetime(), end="")
        print(Bcolors.VERBOSE, f"{text_in}", Bcolors.RESET)


def print_trace(text_in):
    """Print as each object is created in pgm."""
    if show_trace:
        # The 🔍 magnifying glass is a classic for searching, looking, inspecting, approved as part of Unicode 6.0 in 2010 under the name "Left-Pointing Magnifying Glass" and added to Emoji 1.0 in 2015.
        print("⚙️", end="")
        if show_dates_in_logs:
            print(get_log_datetime(), end="")
        # The fingerprint emoji was approved as part of Unicode 16.0 in 2024 and added to Emoji 16.0 in 2024.
        print(Bcolors.TRACE, f"{text_in}", Bcolors.RESET)


def print_secret(secret_in: str) -> None:
    """Output secrets discreetly as count of characters instead of the secret itself.

    display only the first few characters (like Git) with dots replacing the rest.
    """
    # See https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
    if show_secrets:  # program parameter
        # The triangular red flag on post emoji signals a problem or issue. Approved as part of Unicode 6.0 in 2010  added to Emoji 1.0 in 2015.
        print("🚩", end="")
        if show_dates_in_logs:
            print(get_log_datetime(), end="")

        secret_len = 3
        if len(secret_in) <= 10:  # slice
            # Regardless of secret length, to reduce hacker ability to guess:
            print(Bcolors.GRAY, "secret too small to print.", Bcolors.RESET)
            # print(Bcolors.GRAY,"\"",secret_in,"\"", Bcolors.RESET)
        else:
            print(
                Bcolors.WARNING,
                "WARNING: Secret specified to be shown. POLICY VIOLATION: ",
                Bcolors.RESET,
            )
            # WARNING NOTE: secrets should not be printed to logs.
            secret_out = secret_in[0:4] + "." * (secret_len - 1)
            print(Bcolors.GRAY, '"', secret_out, '..."', Bcolors.RESET)
    return None


def show_print_samples() -> None:
    """Display what different type of output look like."""
    # See https://wilsonmar.github.io/python-samples/#PrintColors
    print_heading("print_heading( show_print_samples():")
    print_fail("print_fail() -> sample fail")
    print_error("print_error() -> sample error")
    print_warning("print_warning() -> sample warning")
    print_todo("print_todo() -> sample task to do")
    print_info("print_info() -> sample info")
    print_verbose("print_verbose() -> sample verbose")
    print_trace("print_trace() -> sample trace")
    print_secret("123456")
    return None


def do_clear_cli() -> None:
    """Clear the CLI screen."""
    print_trace(f"At {sys._getframe().f_code.co_name}()")
    # import os
    # QUESTION: What's the output variable?
    lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")
    return None


#### SECTION 05: Python .env (environment) variables:


# See https://bomonike.github.io/python-samples/#ParseArguments


def open_env_file(global_env_path: str = None) -> str:
    """Load global variables from .env file based on hard-coded default location.

    Args: global ENV_FILE
    See https://wilsonmar.github.io/python-samples/#envLoad
    See https://stackoverflow.com/questions/40216311/reading-in-environment-variables-from-an-environment-file
    """
    # from pathlib import Path
    # See https://wilsonmar.github.io/python-samples#run_env
    if not global_env_path:  # specified or None.
        global_env_path = str(Path.home()) + "/" + "python-samples.env"  # concatenate path

    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        global_env_path = None
        print_error(f'{sys._getframe().f_code.co_name}(): global_env_path: not at "{global_env_path}" ')
        return None

    # import pathlib
    # path = pathlib.Path(global_env_path)
    # print_info(f"{sys._getframe().f_code.co_name}(): path: \"{path}\" ")

    # Based on: pip3 install python-dotenv
    # from dotenv import load_dotenv
    # See https://www.python-engineer.com/posts/dotenv-python/
    # See https://pypi.org/project/python-dotenv/
    load_dotenv(global_env_path)  # using load_dotenv
    # Wait until variables for print_trace are retrieved:
    print_verbose(f'{sys._getframe().f_code.co_name}(): at global_env_path: "{global_env_path}" ')
    return global_env_path


def get_str_from_env_file(key_in) -> bool:
    """Return a value of string data type from OS environment or .env file.

    (using pip python-dotenv)
    """
    env_value = os.environ.get(key_in)  # TODO
    if not env_value:  # yes, defined=True, use it:
        print_trace(f'{sys._getframe().f_code.co_name}(): "{key_in}") not found in .env file.')
        return None

    print_info(f'{sys._getframe().f_code.co_name}(): {key_in}: "{env_value}" ')

    #        # PROTIP: Display only first characters of a potentially secret long string:
    #        if len(env_var) > 5:
    #            print_trace(key_in + "=\"" + str(env_var[:5]) +" (remainder removed)")
    #        else:
    #            print_trace(key_in + "=\"" + str(env_var) + "\" from .env")
    #        return str(env_var)

    return env_value


def print_env_vars():
    """List all environment variables, one line each using pretty print (pprint)."""
    # import os
    # import pprint
    environ_vars = os.environ
    print_heading("User's Environment variable:")
    print.pprint(dict(environ_vars), width=1)


def update_env_file(file_path, key, new_value) -> bool:
    """Update a specific key-value pair in a .env file.

    Usage:
        result = update_env_file("key", "new_value")
    Args:
        file_path (str): Path to the .env file
        key (str): The key to update
        new_value (str): The new value for the key
    Returns bool: True if key was found and updated, False if key was not found
    """
    # import os
    # Read the current content:
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print_error(f'{sys._getframe().f_code.co_name}(): File "{file_path}" not found.')
        return False

    key_found = False
    updated_lines = []

    for line in lines:
        # Strip whitespace for comparison but preserve original formatting:
        stripped_line = line.strip()

        # Skip empty lines and comments:
        if not stripped_line or stripped_line.startswith("#"):
            updated_lines.append(line)
            continue

        # Check if this line contains our key:
        if "=" in stripped_line:
            line_key = stripped_line.split("=", 1)[0].strip()
            if line_key == key:
                # Update the line with new value:
                updated_lines.append(f"{key}={new_value}\n")
                key_found = True
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    # If key wasn't found, add it to the end:
    if not key_found:
        updated_lines.append(f"{key}={new_value}\n")

    # Write the updated content back to the file:
    try:
        with open(file_path, "w") as file:
            file.writelines(updated_lines)
        print_info(f'{sys._getframe().f_code.co_name}(): "{key}" => "{new_value}" ')
        return True
    except Exception as e:
        print_error(f"{sys._getframe().f_code.co_name}(): {e}")
        return False


def update_env_with_quotes(file_path, key, new_value):
    """
    Update a .env file with proper quoting for values containing spaces or special characters.

    Args:
        file_path (str): Path to the .env file
        key (str): The key to update
        new_value (str): The new value for the key

    Returns bool: True if successful, False otherwise
    """
    # import os
    # Add quotes if value contains spaces or special characters
    if " " in new_value or any(char in new_value for char in ["#", '"', "'"]):
        new_value = f'"{new_value}"'

    return update_env_file(file_path, key, new_value)


#### SECTION 07 - Read custom command line (CLI) arguments controlling this program run:


parser = argparse.ArgumentParser(description="gcp-services.py for Google Cloud Authentication")
parser.add_argument("-q", "--quiet", action="store_true", help="Quiet")
parser.add_argument("-v", "--verbose", action="store_true", help="Show each download")
parser.add_argument("-vv", "--debug", action="store_true", help="Show debug")
parser.add_argument("-l", "--log", help="Log to external file")

parser.add_argument("--project", "-p", help="Google Cloud project ID")
parser.add_argument("--service-account", "-acct", type=str, help="Path to service account key file")

parser.add_argument("--setup-adc", action="store_true", help="Set up Application Default Credentials")
parser.add_argument("--adc", action="store_true", help="Use Application Default Credentials (ADC)")
parser.add_argument("--user", action="store_true", help="Use interactive user authentication (email)")
parser.add_argument("--install", action="store_true", help="Install required packages")
parser.add_argument(
    "--format",
    "-fmt",
    choices=["table", "csv", "json"],
    default="table",
    help="Output format (default: table)",
)
parser.add_argument("-do", "--delout", action="store_true", help="Delete output file")
# Load arguments from CLI:
args = parser.parse_args()


#### SECTION 08 - Override defaults and .env file with run-time parms:

SHOW_QUIET = args.quiet
SHOW_VERBOSE = args.verbose
SHOW_DEBUG = args.debug
# args.log

# args.project
# args.service_account

# args.setup_adc
# args.adc
# args.user
# args.install
# args.format

GEN_QR_CODE = False  # TODO: Change in CLI parm
EMAIL_FROM = "loadtesters@gmail.com"  # TODO: Change in CLI parm
EMAIL_TO = "???"

DELETE_OUTPUT_FILE = args.delout  # -de  --delout Delete output file


#### SECTION 04: Python program name:


def print_module_filenames() -> None:
    """Print module filenames.

    USAGE: print_filename()
    """
    print_trace(f"At {sys._getframe().f_code.co_name}()")

    # import inspect
    current_frame = inspect.currentframe()
    filename = inspect.getfile(current_frame)
    print(f"inspect.getfile(currentframe()): {os.path.basename(filename)}")

    filename_no_ext = os.path.splitext(os.path.basename(__file__))[0]
    print(f"__file__ without extension:      {filename_no_ext}     created:  {ctimestamp(__file__)} ")

    # import sys
    current_module = sys.modules[__name__]
    print(f"Filename only:      {os.path.basename(__file__):>23}  modified: {mtimestamp(__file__)}")

    if hasattr(current_module, "__file__"):
        print(f"os.path.basename():              {os.path.basename(current_module.__file__)} ")
        print(f"current_module.__file__:    {current_module.__file__}")

    print(f"os.path.abspath(__file__):  {os.path.abspath(__file__)} ")

    return None


def is_macos() -> str:
    """Return true if the operating system is macOS."""
    # import platform
    # Instead of: return platform.system() == "Darwin"
    patform_system = platform.system()
    print_verbose(f"{sys._getframe().f_code.co_name}(): {patform_system} ")
    if patform_system == "Darwin":
        return True
    else:
        return False


# Alternative approach using specific environment checks:
def is_local_development():
    """Alternative method focusing on common deployment patterns."""
    # Check for containerized environments (usually not local)
    if os.path.exists("/.dockerenv") or os.getenv("KUBERNETES_SERVICE_HOST"):
        return False

    # Check for cloud platform environment variables
    cloud_indicators = [
        "HEROKU_APP_NAME",
        "AWS_EXECUTION_ENV",
        "GOOGLE_CLOUD_PROJECT",
        "AZURE_FUNCTIONS_ENVIRONMENT",
        "VERCEL",
        "NETLIFY",
    ]

    if any(os.getenv(var) for var in cloud_indicators):
        return False

    # If none of the above, likely local
    return True


def get_str_from_os(varname: str) -> str:
    """Get string value from OS environment variable.

    USAGE: api_key = get_str_from_os("OPENAI_API_KEY")
    """
    api_key = os.environ.get(varname, None)
    return api_key


def display_cli_parameters() -> str:
    """Display CLI parameters."""
    args_str = ""  # f"{len(sys.argv)} arguments: "
    for index, arg in enumerate(sys.argv):
        args_str = args_str + f" {arg} "
    return args_str
    # Like: CLI: ./mondrian-gen.py  -v  -vv  -ai  pgm  -dc


def set_cli_parms(count):
    """Present menu and parameters to control program."""

    # import click
    @click.command()
    @click.option("--count", default=1, help="Number of greetings.")
    # @click.option('--name', prompt='Your name',
    #              help='The person to greet.')
    def set_cli_parms(count):
        for x in range(count):
            click.echo("Hello!")

    # Test by running: ./python-examples.py --help


#### SECTION 06: Logging utility functions:


def get_log_datetime() -> str:
    """Return a formatted datetime string in UTC (GMT) timezone so all logs are aligned.

    Example: 2504210416UTC for a minimal with year, month, day, hour, minute, second and timezone code.
    """
    # from datetime import datetime
    # importing timezone from pytz module
    # from pytz import timezone

    # To get current time in (non-naive) UTC timezone
    # instead of: now_utc = datetime.now(timezone('UTC'))
    # Based on https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
    fts = datetime.fromtimestamp(time.time(), tz=timezone.utc)
    time_str = fts.strftime("%y%m%d%H%M%Z")  # EX: "...-250419" UTC %H%M%Z https://strftime.org

    # See https://stackoverflow.com/questions/7588511/format-a-datetime-into-a-string-with-milliseconds
    # time_str=datetime.utcnow().strftime('%F %T.%f')
    # for ISO 8601-1:2019 like 2023-06-26 04:55:37.123456 https://www.iso.org/news/2017/02/Ref2164.html
    # time_str=now_utc.strftime(MY_DATE_FORMAT)

    # Alternative: Converting to Asia/Kolkata time zone using the .astimezone method:
    # now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    # Format the above datetime using the strftime()
    # print('Current Time in Asia/Kolkata TimeZone:',now_asia.strftime(format))
    # if show_dates:  https://medium.com/tech-iiitg/zulu-module-in-python-8840f0447801

    return time_str


# TODO: OpTel (OpenTelemetry) spans and logging:


def export_optel():
    """Create and export a trace to your console.

    https://www.perplexity.ai/search/python-code-to-use-opentelemet-bGjntbF4Sk6I6z3l5HBBSg#0
    """
    # from opentelemetry import trace
    # from opentelemetry.sdk.trace import TracerProvider
    # from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

    # Set up the tracer provider and exporter
    trace.set_tracer_provider(TracerProvider())
    span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
    trace.get_tracer_provider().add_span_processor(span_processor)

    # Get a tracer:
    tracer = trace.get_tracer(__name__)

    # Create spans:
    with tracer.start_as_current_span("parent-span"):
        print_verbose("Doing some work in the parent span")
        with tracer.start_as_current_span("child-span"):
            print_verbose("Doing some work in the child span")


#### SECTION 07: Operating System properties


def mem_usage(tag):
    """Report memory usage.

    USAGE: print(f"Memory used: {myutils.mem_usage("myutils.py")}")
    """
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    denom = 1024
    if sys.platform == "darwin":
        denom = denom**2
    print(f"memory used is at {tag} : {round(mem / denom, 2)} MB")


def beautify_json(file, outfile=None):
    """Beautify JSON string.

    USAGE: myutils.beautify_json("myutils.py"))
    """
    js = json.loads(open(file).read())
    if outfile is None:
        outfile = file
    with open(outfile, "w") as outfilep:
        json.dump(js, outfilep, sort_keys=True, indent=4)


def get_fuid(filename):
    """Return user id (such as "johndoe").

    USAGE: print(f"FUID: {myutils.get_fuid("myutils.py")}")
    """
    return pwd.getpwuid(os.stat(filename).st_uid).pw_name


def execsh(command):
    """Execute CSH.

    USAGE: myutils.execsh("echo")
    FIXME: PIPE?
    """
    pipe = subprocess.PIPE
    result = subprocess.run(command, stdout=pipe, stderr=pipe, universal_newlines=True, shell=True)
    return result.stdout


def force_link(src, linkname):
    """Force link.

    USAGE: myutils.force_link(???)
    """
    try:
        os.symlink(src, linkname)
    except Exception as e:
        if os.path.islink(linkname):
            os.remove(linkname)
            os.symlink(src, linkname)
        print_error(f"{sys._getframe().f_code.co_name}(): {e}")


# See https://bomonike.github.io/python-samples/#run_env


def os_platform():
    """Return a friendly name for the operating system."""
    # import platform # https://docs.python.org/3/library/platform.html
    platform_system = str(platform.system())
    # 'Linux', 'Darwin', 'Java', 'Windows'
    print_trace("platform_system=" + str(platform_system))
    if platform_system == "Darwin":
        my_platform = "macOS"
    elif platform_system == "linux" or platform_system == "linux2":
        my_platform = "Linux"
    elif platform_system == "win32":  # includes 64-bit
        my_platform = "Windows"
    else:
        print_fail("platform_system=" + platform_system + " is unknown!")
        exit(1)  # entire program
    return my_platform


def macos_version_name(release_in):
    """Return the marketing name of macOS versions which are not available.

    from the running macOS operating system.
    """
    # NOTE: Return value is a list!
    # This has to be updated every year, so perhaps put this in an external library so updated
    # gets loaded during each run.
    # Apple has a way of forcing users to upgrade, so this is used as an
    # example of coding.
    # FIXME: https://github.com/nexB/scancode-plugins/blob/main/etc/scripts/homebrew.py
    # See https://support.apple.com/en-us/HT201260 and https://www.wikiwand.com/en/MacOS_version_history
    macos_versions = {
        """Versions of macOS."""
        "22.8": ["Next2025", 2025, "25"],
        "22.7": ["Next2024", 2024, "24"],
        "22.6": ["macOS Sonoma", 2023, "23"],
        "22.5": ["macOS Ventura", 2022, "13"],
        "12.1": ["macOS Monterey", 2021, "21"],
        "11.1": ["macOS Big Sur", 2020, "20"],
        "10.15": ["macOS Catalina", 2019, "19"],
        "10.14": ["macOS Mojave", 2018, "18"],
        "10.13": ["macOS High Sierra", 2017, "17"],
        "10.12": ["macOS Sierra", 2016, "16"],
        "10.11": ["OS X El Capitan", 2015, "15"],
        "10.10": ["OS X Yosemite", 2014, "14"],
        "10.9": ["OS X Mavericks", 2013, "10.9"],
        "10.8": ["OS X Mountain Lion", 2012, "10.8"],
        "10.7": ["OS X Lion", 2011, "10.7"],
        "10.6": ["Mac OS X Snow Leopard", 2008, "10.6"],
        "10.5": ["Mac OS X Leopard", 2007, "10.5"],
        "10.4": ["Mac OS X Tiger", 2005, "10.4"],
        "10.3": ["Mac OS X Panther", 2004, "10.3"],
        "10.2": ["Mac OS X Jaguar", 2003, "10.2"],
        "10.1": ["Mac OS X Puma", 2002, "10.1"],
        "10.0": ["Mac OS X Cheetah", 2001, "10.0"],
    }
    # WRONG: On macOS Monterey, platform.mac_ver()[0]) returns "10.16", which is Big Sur and thus wrong.
    # See https://eclecticlight.co/2020/08/13/macos-version-numbering-isnt-so-simple/
    # and https://stackoverflow.com/questions/65290242/pythons-platform-mac-ver-reports-incorrect-macos-version/65402241
    # and https://docs.python.org/3/library/platform.html
    # So that is not a reliable way, especialy for Big Sur
    # https://bandit.readthedocs.io/en/latest/blacklists/blacklist_imports.html#b404-import-subprocess
    # import subprocess  # built-in
    # from subprocess import PIPE, run
    # p = subprocess.Popen("sw_vers", stdout=subprocess.PIPE)
    # result = p.communicate()[0]
    macos_platform_release = platform.release()
    # Alternately:
    release = ".".join(release_in.split(".")[:2])  # ['10', '15', '7']
    macos_info = macos_versions[release]  # lookup for ['Monterey', 2021]
    print_trace("macos_info=" + str(macos_info))
    print_trace("macos_platform_release=" + macos_platform_release)
    return macos_platform_release


#### SECTION 10: System Networking functions:


def is_running_locally() -> bool:
    """Return True if the program is running in a local development environment.

    Return False if in production/remote environment (within a server/VM).
    """
    # Method 1: Check for common local development indicators:
    local_indicators = [
        # Development environment variables
        os.getenv("DEVELOPMENT") == "true",
        os.getenv("DEBUG") == "true",
        os.getenv("ENV") == "development",
        os.getenv("ENVIRONMENT") == "local",
        # Common local hostnames/IPs:
        socket.gethostname().lower() in ["localhost", "127.0.0.1"],
        # Check if running on local IP ranges
        _is_local_ip(),
        # Development tools/paths present
        Path(".git").exists(),  # Git repository
        Path("requirements.txt").exists() or Path("pyproject.toml").exists(),
        # Interactive terminal (likely local development)
        sys.stdin.isatty() and sys.stdout.isatty(),
    ]

    return any(local_indicators)


def _is_local_ip():
    """Check if running on a local IP address."""
    try:
        # Get local IP by connecting to external address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]

        # Check if IP is in private ranges
        ip_parts = local_ip.split(".")
        if len(ip_parts) == 4:
            first_octet = int(ip_parts[0])
            second_octet = int(ip_parts[1])

            # Private IP ranges: 10.x.x.x, 172.16-31.x.x, 192.168.x.x
            return (
                first_octet == 10
                or (first_octet == 172 and 16 <= second_octet <= 31)
                or (first_octet == 192 and second_octet == 168)
                or local_ip == "127.0.0.1"
            )
    except Exception as e:
        print_error(f"{sys._getframe().f_code.co_name}(): {e}")
        return False


def get_environment_info():
    """Return a dictionary of detailed information about the current environment."""
    return {
        "hostname": socket.gethostname(),
        "platform": sys.platform,
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "environment_vars": {
            "PATH": os.getenv("PATH", ""),
            "HOME": os.getenv("HOME", ""),
            "USER": os.getenv("USER", ""),
            "SHELL": os.getenv("SHELL", ""),
        },
        "is_interactive": sys.stdin.isatty(),
        "has_git": Path(".git").exists(),
        "local_ip": _get_local_ip(),
    }


def _get_local_ip():
    """Return the local IP address such as 192.168.1.23.

    By "connecting" to an external UDP address such as 8.8.8.8 (Google's DNS),
    the operating system's routing table determines which
    local network interface (and its associated IP address)
    is used to reach the internet rather than localhost (127.0.0.1).
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(f"{sys._getframe().f_code.co_name}(): {e}")
        return "Unknown"


#### SECTION 09: OS Process memory handling:


def get_process_memory() -> float:
    """Return MiB of memory used by the current process."""
    # import os, psutil  #  psutil-5.9.5
    process = psutil.Process(os.getpid())
    # Divide by (1024 * 1024) to convert bytes to MB:
    mem = process.memory_info().rss / 1048576
    print_trace(f"{str(process)} MiB from get_process_memory()")
    return float(mem)


def get_all_objects_by_type():
    """Get memory usage by object type."""
    type_sizes = defaultdict(int)
    type_counts = defaultdict(int)

    # Force garbage collection to get more accurate results:
    # import gc
    gc.collect()

    # Get all objects tracked by the garbage collector
    for obj in gc.get_objects():
        try:
            obj_type = type(obj).__name__
            # import sys
            obj_size = sys.getsizeof(obj)
            type_sizes[obj_type] += obj_size
            type_counts[obj_type] += 1
        except Exception as e:
            print_verbose(f"{sys._getframe().f_code.co_name}(): {e} ")
            pass  # Skip objects that can't be processed

    return type_sizes, type_counts


def trace_memory_usage(func):
    """Define decorator to trace memory usage.

    before and after calling a function that uses a dubiously large amount of memory.
    """

    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_memory = get_process_memory()
        print_verbose(f"{'Memory before:':<43} {start_memory:.2f} MB")

        result = func(*args, **kwargs)

        current, peak = tracemalloc.get_traced_memory()
        print_verbose(f"    {'tracemalloc current:':<43} {current / (1024 * 1024):.2f} MB")
        print_verbose(f"    {'tracemalloc peak:':<43} {peak / (1024 * 1024):.2f} MB")
        end_memory = get_process_memory()
        print_verbose(f"    {'Memory after:':<43} {end_memory:.2f} MB")
        print_verbose(f"    {'Memory used:':<43} {end_memory - start_memory:.2f} MB")

        # import tracemalloc
        tracemalloc.stop()
        return result

    return wrapper


def show_memory_profile():
    """Print detailed memory usage information."""
    linkname = 1073741824  # = 1024 * 1024 * 1024 = Terrabyte

    print_verbose("show_memory_profile():")

    system_memory = psutil.virtual_memory()
    print_verbose(
        f"psutil.virtual_memory(): {system_memory.percent}% "
        f"(Available: {system_memory.available / linkname:.2f} GB"
        f", System: {system_memory.total / linkname:.2f} GB)"
    )

    print_verbose(f"{'    Total process memory: ':<43} {get_process_memory():.2f} MB")
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print_verbose(f"{'    RSS (Resident Set Size):':<43} {memory_info.rss / (1024 * 1024):.2f} MB")
    print_verbose(f"{'    VMS (Virtual Memory Size):':<43} {memory_info.vms / (1024 * 1024):.2f} MB")

    # Get memory usage by type
    type_sizes, type_counts = get_all_objects_by_type()

    # Show top 10 memory consumers by type
    print_verbose("Top 10 memory consumers by type:")
    top_types = sorted(type_sizes.items(), key=lambda x: x[1], reverse=True)[:10]
    for obj_type, size in top_types:
        count = type_counts[obj_type]
        print_verbose(f"    {obj_type:<43} {size / (1024 * 1024):.2f} MB ({count} objects)")

    # Show other system information
    # print(f"\nPython version: {sys.version}")


#### SECTION 09: Storage Disk space information:


def get_disk_free() -> (float, str):
    """Return float GB of disk space free and text of percentage free.

    References global GB_BYTES.
    """
    gb_bytes = 1073741824  # = 1024 * 1024 * 1024 = Terrabyte
    # import shutil
    # Replace '/' with your target path (e.g., 'C:\\' on Windows)
    usage = shutil.disk_usage("/")
    pct_free = (float(usage.free) / float(usage.total)) * 100
    disk_gb_free = float(usage.free) / gb_bytes
    disk_pct_free = f"{pct_free:.2f}%"
    # print_verbose(f"get_disk_free(): {disk_gb_free:.2f} ({pct_free:.2f}%) disk free")
    return disk_gb_free, disk_pct_free


#### SECTION 09: Python file handling:


def stats_to_file(filepath) -> bool:
    """Redirect system info stdout to a file using contextlib.

    This is the cleanest and most pythonic way.
    """
    if not filepath:  # if filepath is empty
        filepath = f"{os.getcwd()}/stats_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    elif os.path.isfile(filepath):  # if file exists, so append:
        try:
            with open("append_output.txt", "a") as f:
                original_stdout = sys.stdout
                sys.stdout = f

                macos_sys_info()  # appended to existing file.

                sys.stdout = original_stdout
        except Exception as e:
            print(f'{sys._getframe().f_code.co_name}("{filepath}") append: {e}')
    else:  # not exist:
        try:
            # from contextlib import redirect_stdout
            with open(filepath, "w") as f:
                with redirect_stdout(f):
                    macos_sys_info()
            # print("Back to console")
            return True
        except Exception as e:
            print(f'{sys._getframe().f_code.co_name}("{filepath}") add: {e}')
    return False


def list_files_on_removable_drive(drive_path: str) -> None:
    """List all directories and files on a removable USB volumedrive.

    where drive_path = "/Volumes/DRIVE_VOLUME"
    """
    # import os
    # from pathlib import Path
    drive = Path("/Volumes/" + drive_path)
    if not drive.is_mount():  # NOT mounted:
        print_warning(f'/Volumes/Drive "{drive_path}" not mounted (plugged in). Ignored.')
        return
    else:
        print(f'{drive_path} is --drivepath "DRIVE_PATH":')

    for item in drive.iterdir():
        if item.is_dir():
            print_info(f"Directory: {item.name}")
        elif item.is_file():
            print_info(f"File: {item.name}")
    return None


def count_files_within_path(directory: str) -> int:
    """Return the number of files after looking recursively within a given directory."""
    # import os
    file_count = 0
    for entry in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, entry)):
            file_count += 1
    return file_count


def get_file_size_on_disk(file_path: str) -> int:
    """Return integer bytes from the OS for a file path."""
    try:
        file_size = os.path.getsize(file_path)
        return file_size
        # Alternately:
        # stat_result = os.stat(file_path)
        # return stat_result.st_blocks * 512  # st_blocks is in 512-byte units
    except FileNotFoundError:
        print(f"*** File path not found: {file_path}")
        return 0
    except Exception as e:
        print(f"*** Error getting file size: {e}")
        return 0


#### SECTION 09: Display System information:


def macos_sys_info():
    """Print macOS System info."""
    if not show_sys_info:  # defined among CLI arguments
        return None

    print_heading("macos_sys_info():")

    # or socket.gethostname()
    my_platform_node = platform.node()
    print_trace("my_platform_node = " + my_platform_node + " (machine name)")

    print_trace("user_home_dir_path = " + str(Path.home()))
    # the . in .secrets tells Linux that it should be a hidden file.

    # import platform # https://docs.python.org/3/library/platform.html
    platform_system = platform.system()
    # 'Linux', 'Darwin', 'Java', 'Win32'
    print_trace("platform_system = " + str(platform_system))

    # my_os_platform=localize_blob("version")
    print_trace("my_os_version = " + str(platform.release()))
    #           " = "+str(macos_version_name(my_os_version)))

    my_os_process = str(os.getpid())
    print_trace("my_os_process = " + my_os_process)

    my_os_uname = str(os.uname())
    print_trace("my_os_uname = " + my_os_uname)
    # MacOS version=%s 10.14.6 # posix.uname_result(sysname='Darwin',
    # nodename='NYC-192850-C02Z70CMLVDT', release='18.7.0', version='Darwin
    # Kernel Version 18.7.0: Thu Jan 23 06:52:12 PST 2020;
    # root:xnu-4903.278.25~1/RELEASE_X86_64', machine='x86_64')

    # import pwd   #  https://zetcode.com/python/os-getuid/
    pwuid_shell = pwd.getpwuid(os.getuid()).pw_shell  # like "/bin/zsh" on MacOS
    # preferred over os.getuid())[0]

    # machine_uid_pw_name = psutil.Process().username()
    print_trace("pwuid_shell = " + pwuid_shell)

    # Obtain machine login name:
    # This handles situation when user is in su mode.
    # See https://docs.python.org/3/library/pwd.html
    pwuid_gid = pwd.getpwuid(os.getuid()).pw_gid  # Group number datatype
    print_trace("pwuid_gid = " + str(pwuid_gid) + " (process group ID number)")

    pwuid_uid = pwd.getpwuid(os.getuid()).pw_uid
    print_trace("pwuid_uid = " + str(pwuid_uid) + " (process user ID number)")

    pwuid_name = pwd.getpwuid(os.getuid()).pw_name
    print_trace("pwuid_name = " + pwuid_name)

    pwuid_dir = pwd.getpwuid(os.getuid()).pw_dir  # like "/Users/johndoe"
    print_trace("pwuid_dir = " + pwuid_dir)

    # Several ways to obtain:
    # See https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    # this_pgm_name = sys.argv[0]                     # = ./python-samples.py
    # this_pgm_name = os.path.basename(sys.argv[0])   # = python-samples.py
    # this_pgm_name = os.path.basename(__file__)      # = python-samples.py
    # this_pgm_path = os.path.realpath(sys.argv[0])   # = python-samples.py
    # Used by display_run_stats() at bottom:
    this_pgm_name = os.path.basename(os.path.normpath(sys.argv[0]))
    print_trace("this_pgm_name = " + this_pgm_name)

    # this_pgm_last_commit = __last_commit__
    #    # Adapted from https://www.python-course.eu/python3_formatted_output.php
    # print_trace("this_pgm_last_commit = "+this_pgm_last_commit)

    this_pgm_os_path = os.path.realpath(sys.argv[0])
    print_trace("this_pgm_os_path = " + this_pgm_os_path)
    # Example: this_pgm_os_path=/Users/wilsonmar/github-wilsonmar/python-samples/python-samples.py

    # import site
    site_packages_path = site.getsitepackages()[0]
    print_trace("site_packages_path = " + site_packages_path)

    this_pgm_last_modified_epoch = os.path.getmtime(this_pgm_os_path)
    print_trace("this_pgm_last_modified_epoch = " + str(this_pgm_last_modified_epoch))

    # this_pgm_last_modified_datetime = datetime.fromtimestamp(
    #    this_pgm_last_modified_epoch)
    # print_trace("this_pgm_last_modified_datetime=" +
    #            str(this_pgm_last_modified_datetime)+" (local time)")
    # Default like: 2021-11-20 07:59:44.412845  (with space between date & time)

    # Obtain to know whether to use new interpreter features:
    python_ver = platform.python_version()
    # 3.8.12, 3.9.16, etc.
    print_trace("python_ver = " + python_ver)

    # python_info():
    python_version = no_newlines(sys.version)
    # 3.9.16 (main, Dec  7 2022, 10:16:11) [Clang 14.0.0 (clang-1400.0.29.202)]
    # 3.8.3 (default, Jul 2 2020, 17:30:36) [MSC v.1916 64 bit (AMD64)]
    print_trace("python_version = " + python_version)

    print_trace("python_version_info = " + str(sys.version_info))
    # Same as on command line: python -c "print_trace(__import__('sys').version)"
    # 2.7.16 (default, Mar 25 2021, 03:11:28)
    # [GCC 4.2.1 Compatible Apple LLVM 11.0.3 (clang-1103.0.29.20) (-macos10.15-objc-

    if sys.version_info.major == 3 and sys.version_info.minor <= 6:
        # major, minor, micro, release level, and serial: for sys.version_info.major, etc.
        # Version info sys.version_info(major=3, minor=7, micro=6,
        # releaselevel='final', serial=0)
        print_fail("Python 3.6 or higher is required for this program. Please upgrade.")
        sys.exit(1)

    # TODO: Make this function for call before & after run:
    #    disk_list = get_disk_free()
    #    disk_space_free = disk_list[1]:,.1f / disk_list[0]:,.1f
    #    print_info(localize_blob("Disk space free")+"="+disk_space_free+" GB")
    # left-to-right order of fields are re-arranged from the function's output.

    # is_uv_venv_activated()  # both True:


def show_summary() -> bool:
    """Print summary of timings together at end of run."""
    if not SHOW_SUMMARY_COUNTS:
        return None

    print_separator()
    print_heading(f"{sys._getframe().f_code.co_name}():")

    pgm_stop_mem_diff = get_process_memory() - float(pgm_strt_mem_used)
    print_info(f"{pgm_stop_mem_diff:.2f} MB memory consumed during run {RUNID}.")

    pgm_stop_disk_free, pct_disk_free_now = get_disk_free()
    pgm_stop_disk_diff = pgm_strt_disk_free - pgm_stop_disk_free
    print_info(f"{pgm_stop_disk_diff:.2f} GB disk space consumed during run {RUNID}. {pct_disk_free_now} remaining.")

    print_heading("Monotonic wall timings (seconds):")
    # TODO: Write to log for longer-term analytics

    # For wall time of std imports:
    std_elapsed_wall_time = std_stop_timestamp - std_strt_timestamp
    print_verbose("for import of Python standard libraries: " + f"{std_elapsed_wall_time:.4f}")

    # For wall time of xpt imports:
    xpt_elapsed_wall_time = xpt_stop_timestamp - xpt_strt_timestamp
    print_verbose("for import of Python extra    libraries: " + f"{xpt_elapsed_wall_time:.4f}")

    pgm_stop_timestamp = time.monotonic()
    pgm_elapsed_wall_time = pgm_stop_timestamp - pgm_strt_timestamp
    # pgm_stop_perftimestamp = time.perf_counter()
    print_verbose("for whole program run:                   " + f"{pgm_elapsed_wall_time:.4f}")

    # TODO: Write wall times to log for longer-term analytics
    return True


#### SECTION 08: Python code utilities:


def handle_fatal_exit():
    """Handle fatal exit with a message first."""
    print_trace("handle_fatal_exit() called.")
    sys.exit(9)


def list_pgm_functions(filename):
    """List functions defined in the specified program file.

    USAGE: print(myutils.list_pgm_functions("myutils.py"))
    """
    # import importlib.util
    spec = importlib.util.spec_from_file_location("module", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get all functions:
    # import inspect
    functions = inspect.getmembers(module, inspect.isfunction)

    # Print function names:
    print(f'myutils.list_pgm_functions("{sys.argv[0]}") alphabetically: ')
    for name, func in functions:
        print("    " + name)


def _extract_dunder_variables(filename: str) -> Dict[str, Any]:
    """Extract dunder variables from a Python source file.

    Used by print_dunder_vars(filename) below.
    USAGE:
        dunder_items = myutils.extract_dunder_variables("myutils.py")
        for i, (key, value) in enumerate(dunder_items.items(), 1):
            print(f"{i}. {key}: {value}")
        for key, value in dunder.items():
            print(f"{key}: {value}")

    Args:
        filename: Path to the Python source file
    Returns:
        Dictionary of dunder variable names and their values
    """
    # import ast
    # import sys
    # from typing import Dict, Any
    with open(filename, "r", encoding="utf-8") as file:
        source = file.read()

    # Parse the source code into an AST:
    tree = ast.parse(source)

    dunder_vars = {}  # Dictionary to store dunder variables
    # Find all assignments at the module level
    for node in tree.body:
        # Look for assignment statements
        if isinstance(node, ast.Assign):
            for target in node.targets:
                # Check if the target is a name (variable)
                if isinstance(target, ast.Name):
                    var_name = target.id
                    # Check if it's a dunder (starts and ends with double underscores)
                    if var_name.startswith("__") and var_name.endswith("__"):
                        # Try to evaluate the value
                        try:
                            value = ast.literal_eval(node.value)
                            dunder_vars[var_name] = value
                        except (ValueError, SyntaxError):
                            # If we can't evaluate it, store it as a string representation
                            dunder_vars[var_name] = f"<non-literal value: {ast.dump(node.value)}>"
    return dunder_vars


def print_dunder_vars(filename) -> str:
    """Print programs which contain __last_change__ or other custom dundars."""
    print_trace(f"At {sys._getframe().f_code.co_name}() within {filename}:")
    try:
        dunder_vars = _extract_dunder_variables(filename)
        if not dunder_vars:
            print(f"No dunder variables found in {filename}")
        else:
            for name, value in dunder_vars.items():
                print(f"{name} = {repr(value)}")

    except FileNotFoundError:
        print(f"{sys._getframe().f_code.co_name}() Error: File '{filename}' not found!")
        sys.exit(1)
    except SyntaxError as e:
        print(f"{sys._getframe().f_code.co_name}()Error: Invalid Python syntax in '{filename}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"{sys._getframe().f_code.co_name}() Error: {e}! ")
        sys.exit(1)


#### Encryption on Drives


def get_api_key(app_id: str, account_name: str) -> str:
    """Get API key from macOS Keyring file or .env file (depending on what's available).

    referencing global variables keyring_service_name & keyring_account_name
    USAGE: api_key = get_api_key("anthropic","johndoe")
    """
    print_verbose("get_api_key() app_id=" + app_id + ", account_name=" + account_name)

    if is_macos():
        # Pull sd_api_key as password from macOS Keyring file (and other password manager):
        try:
            # import keyring
            api_key = keyring.get_password(app_id, account_name)
            if api_key:
                print_trace("get_api_key() len(api_key)=" + str(len(api_key)) + " chars.")
                return api_key
            else:
                # FIXME: sd_api_key=None
                print_error("get_api_key() api_key=None")
                return None
        except Exception as e:
            print_error(f"{sys._getframe().f_code.co_name}(): str({e})")
            return None
    else:
        print_error(f"{sys._getframe().f_code.co_name}(): not macOS. Obtain key from .env file?")

    return None


def list_disk_space_by_device() -> None:
    """List each physical drive (storage device hardware).

    such as an internal hard disk drive (HDD) or solid-state drive (SSD)
    """
    print_heading(
        "Logical Disk Device Partitions (sdiskpart):\n"
        + "/mountpoint Drive           /device        fstype  opts (options)\n"
        + "   Total size:    Used:       Free: "
    )
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(partition.mountpoint.ljust(28) + partition.device.ljust(16) + partition.fstype.ljust(8) + partition.opts)
        if partition.mountpoint.startswith("/Volumes/"):
            # Check if the volume is removable
            cmd = f"diskutil info {partition.device}"
            output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            print_verbose(f'{sys._getframe().f_code.co_name}(): output: "{output}" ')
            # if "Removable Media: Yes" in output:
            # FIXME:
            #    removable_volumes.append(partition.mountpoint)
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(
                "   "
                + f"{usage.total / (1024 * 1024 * 1024):.2f} GB".rjust(10)
                + f"{usage.used / (1024 * 1024 * 1024):.2f} GB".rjust(12)
                + f"{usage.free / (1024 * 1024 * 1024):.2f} GB".rjust(12)
            )
        except PermissionError:
            print_error("list_disk_space_by_device() Permission denied to access usage information")

        print()
        return None


def list_macos_volumes() -> None:
    """Like Bash CLI: diskutil list.

    STATUS: NOT WORKING
    volumes = os.listdir(volumes_path)
    """
    volumes_path = "/Volumes"
    print("*** Drive Volumes:")
    removable_volumes = []
    import psutil

    partitions = psutil.disk_partitions(all=True)

    for partition in partitions:
        if partition.mountpoint.startswith("/Volumes/"):
            # Check if the volume is removable
            cmd = f"diskutil info {partition.device}"
            output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            if "Removable Media: Yes" in output:
                removable_volumes.append(partition.mountpoint)

    for volume in removable_volumes:
        print(f"Removable volume: {volume}")

        volume_path = os.path.join(volumes_path, volume)
        if os.path.ismount(volume_path):
            print(f"- {volume}")
    return None


def list_files_by_mountpoint() -> None:
    """List files within get all disk partitions."""
    # import os
    # import psutil
    partitions = psutil.disk_partitions()
    print("Listing first 5 files by mountpoint:")
    for partition in partitions:
        mountpoint = partition.mountpoint
        print(f"\n{mountpoint}")
        print("        Files:")
        try:
            # List files in the mountpoint
            files = os.listdir(mountpoint)
            for file in files[:5]:  # Limit to first 5 files for brevity
                print(f"        - {file}")
            if len(files) > 5:
                print("        ...")
        except PermissionError:
            print("Permission denied to access this mountpoint")
        except Exception as e:
            print(f"Error: {str(e)}")
    return None


def read_file_from_removable_drive(drive_path: str, file_name: str, content: str) -> str:
    """Read content (text) from a file_name on a removable drive on macOS.

    TODO: Example: -d "/Volumes/DriveName"
    """
    write_file_to_removable_drive(drive_path, env_file, content)

    # Find the user's $HOME path:
    # example: /users/john_doe
    global_env_path = str(Path.home()) + "/" + env_file  # concatenate path

    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        print_error("global_env_path " + global_env_path + " not found!")
    else:
        print_info("global_env_path " + global_env_path + " is readable.")

    # import pathlib
    path = Path(global_env_path)
    print_verbose(f'{sys._getframe().f_code.co_name}(): "{path}" ')
    # Based on: pip3 install python-dotenv
    # from dotenv import load_dotenv
    # See https://www.python-engineer.com/posts/dotenv-python/
    # See https://pypi.org/project/python-dotenv/
    load_dotenv(global_env_path)  # using load_dotenv

    # Wait until variables for print_trace are retrieved:
    # print_trace("env_file="+env_file)
    # print_trace("user_home_dir_path="+user_home_dir_path)

    # After pip install envcload
    # from envcloak import load_encrypted_env
    # FIXME: Where is? load_encrypted_env('.env.enc', key_file='mykey.key').to_os_env()
    # Now os.environ contains the decrypted variables

    return global_env_path


def write_file_to_removable_drive(drive_path: str, file_name: str, content: str) -> None:
    """Write content (text) to a file_name on a removable drive on macOS.

    :param drive_path: The path to the removable drive
    See https://www.kingston.com/en/blog/personal-storage/using-usb-drive-on-mac
    """
    # Verify that the drive is mounted and the path exists:
    if not os.path.exists(drive_path):
        # mount point = drive_path = '/Volumes/YourDriveName'
        print_error(f"Drive path {drive_path} not found. Please check if it's properly connected.")
        raise FileNotFoundError(f"The drive path {drive_path} does not exist.")
        # Perhaps permission error?
        list_macos_volumes()
        exit(9)

    try:
        # Write the content to the file
        with open(drive_path, "w") as file:
            file.write(content)
        print(f"File '{file_name}' has been successfully written to {drive_path}")
    except PermissionError:
        print(f"Permission denied. Unable to write to {drive_path}")
    except IOError as e:
        print(f"An error occurred while writing the file: {e}")


def eject_drive(drive_path: str) -> None:
    """Safely eject removeable drive after use.

    where drive_path = '/Volumes/DRIVE_VOLUME'
    """
    try:
        # import subprocess
        subprocess.run(["diskutil", "eject", drive_path], check=True)
        print(f"Successfully ejected {drive_path}")
    except subprocess.CalledProcessError:
        print(f"Failed to eject {drive_path}")
    return None


#### URLs


def shorten_url(long_url: str) -> str:
    """Return a shortened URL using tinyurl.com service (unsafe)."""
    base_url = "http://tinyurl.com/api-create.php?url="
    response = requests.get(base_url + long_url)
    print_trace(f"shorten_url() {response.text}")
    return response.text


def save_url_to_file(filepath: str, url: str) -> None:
    """Create a shareable file that, when clicked, opens a window in the default browser.

    showing the web page at the URL specified in the file.
    filepath = "/Users/johndoe/Desktop/whatever/example.url"
    url such as "https://www.example.com"
    USAGE: save_url_to_file(url, filename)
    """
    print_verbose("save_url_to_file() filepath=" + filepath + ", url=" + url)
    content = "[InternetShortcut]\nURL=" + url
    try:
        with open(filepath, "w") as file:
            file.write(content)
        return True
    except Exception as e:
        print_error("save_url_to_file() " + filepath + " exception: " + str(e))
        return False


#### Strings of words


def reverse_words(input_str: str) -> str:
    """Reverse characters in a word.

    USAGE: print(myutils.reverse_words("The dog jumped"))
    Reverses words in a given string
    >>> sentence = "I love Python"
    >>> reverse_words(sentence) == " ".join(sentence.split()[::-1])
    True
    >>> reverse_words(sentence)
    'Python love I'
    """
    return " ".join(reversed(input_str.split(" ")))


#### Numeric utilities


def is_number(s) -> bool:
    """Return true if variable is a number."""
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_only_numbers(variable):
    """Return true if variable is a number."""
    return str(variable).isdigit()


def is_none(variable):
    """Return true if variable is not assigned."""
    return variable is None


#### Encryption/Decrpytion of secrets


def gen_random_alphanumeric(length=12):
    """Generate a cryptographically secure random alphanumeric string.

    Args:
        length (int): Length of the string to generate (default: 12)

    Returns str: Secure random alphanumeric string
    """
    # import string
    characters = string.ascii_lowercase + string.digits
    # import secrets
    return "".join(secrets.choice(characters) for _ in range(length))
    # WARNING: Avoid printing out secret values.


def is_within_git_folder(output_dir: str) -> bool:
    """Return True (for exit) if output_dir is within/under a .git folder."""
    # (.) in first character resolves to current directory.
    # Substitute tilde (~) in first character of output_dir with User's home directory:
    if output_dir[0] == "~":
        output_dir = str(Path.home()) + output_dir[1:]
        print_verbose(f'{sys._getframe().f_code.co_name}(): output_dir: "{output_dir}"')

    # from pathlib import Path:
    output_dir = Path(output_dir).resolve()
    if output_dir.name == ".git" and output_dir.is_dir():
        print_fail(f'{sys._getframe().f_code.co_name}(): output_dir: "{output_dir}" contains a .git directory!')
        return True
    # Check each parent directory for .git folder:
    for parent in [output_dir] + list(output_dir.parents):
        git_path = parent / ".git"
        if git_path.exists() and git_path.is_dir():
            print_fail(f'{sys._getframe().f_code.co_name}(): {output_dir} is under .git folder: "{git_path}" ')
            return True
    return False


def generate_rsa_keypair(key_size=2048, save_to_files=True, output_dir="~/.keys"):
    """Generate RSA private/public key pair.

    private_key.pem & public_key.pem
    Args:
        key_size (int): Size of the RSA key (default: 2048)
        save_to_files (bool): Whether to save keys to files
        output_dir (str): Directory to save key files,
        where "~/.keys" is a hidden folder in the user's home directory.
    Returns tuple: (private_key_pem, public_key_pem) as bytes
    """
    if is_within_git_folder(output_dir):
        exit(9)

    # Generate private key:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )

    # Get public key from private key:
    public_key = private_key.public_key()

    # Serialize private key to PEM format:
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Serialize public key to PEM format:
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    if save_to_files:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Save private key
        private_key_path = os.path.join(output_dir, "private_key.pem")
        with open(private_key_path, "wb") as f:
            f.write(private_pem)

        # Save public key
        public_key_path = os.path.join(output_dir, "public_key.pem")
        with open(public_key_path, "wb") as f:
            f.write(public_pem)

        # Set appropriate file permissions (readable only by owner)
        os.chmod(private_key_path, 0o600)
        os.chmod(public_key_path, 0o644)

        print(f"Private key saved to: {private_key_path}")
        print(f"Public key saved to:  {public_key_path}")

    return private_pem, public_pem


def generate_encrypted_keypair(password, key_size=2048, output_dir="~/.keys"):
    """Generate RSA key pair with encrypted private key.

    private_key_encrypted.pem & public_key.pem
    Args:
        password (str): Password to encrypt the private key
        key_size (int): Size of the RSA key
        output_dir (str): Directory to save key files
    """
    # (.) in first character resolves to current directory.
    # Substitute tilde (~) in first character of output_dir with User's home directory:
    if is_within_git_folder(output_dir):
        exit(9)

    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )

    public_key = private_key.public_key()

    # Serialize private key with password encryption
    encrypted_private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode()),
    )

    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Save encrypted private key
    private_key_path = os.path.join(output_dir, "private_key_encrypted.pem")
    with open(private_key_path, "wb") as f:
        f.write(encrypted_private_pem)

    # Save public key
    public_key_path = os.path.join(output_dir, "public_key.pem")
    with open(public_key_path, "wb") as f:
        f.write(public_pem)

    # Set file permissions
    os.chmod(private_key_path, 0o600)
    os.chmod(public_key_path, 0o644)

    print(f"Encrypted private key saved to: {private_key_path}")
    print(f"Public key saved to: {public_key_path}")

    return encrypted_private_pem, public_pem


def read_file_to_string(file_path):
    """Return the text contents of a file, as a string."""
    if not file_path:
        print_error(f"{sys._getframe().f_code.co_name}(): file_path is needed but not provided.")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text_content = file.read()
        print_verbose(f'{sys._getframe().f_code.co_name}(): "{len(text_content)}" chars in "{file_path}" ')
        return text_content
    except FileNotFoundError:
        print_error(f'{sys._getframe().f_code.co_name}(): File "{file_path}" not found')
        return None
    except Exception as e:
        print_error(f"{sys._getframe().f_code.co_name}(): {e}")
        return None


def delete_all_files_in_folder(folder_path):
    """Delete all files in folder using pathlib (Python 3.4+)."""
    try:
        folder = Path(folder_path)
        for file_path in folder.iterdir():
            if file_path.is_file():
                file_path.unlink()
                print_trace(f"{sys._getframe().f_code.co_name}(): Deleted: {file_path.name}")
        print_verbose(f"{sys._getframe().f_code.co_name}(): All files deleted from {folder_path}")
    except FileNotFoundError:
        print(f"{sys._getframe().f_code.co_name}(): Folder not found: {folder_path}")
    except PermissionError:
        print(f"{sys._getframe().f_code.co_name}(): Permission denied: {folder_path}")
    except Exception as e:
        print(f"{sys._getframe().f_code.co_name}(): {e}")


def hash_file_sha256(filename: str) -> str:
    """Generate a hash string from file using SHA256 algorithm."""
    # A hash is a fixed length one way string from input data. Change of even one bit would change the hash.
    # A hash cannot be converted back to the input data (unlike encryption).
    # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python

    func_start_timer = time.perf_counter()

    # import hashlib
    sha256_hash = hashlib.sha256()
    # There are also md5(), sha224(), sha384(), sha512()
    buf_size = 65536
    with open(filename, "rb") as f:  # read entire file as bytes
        # Read and update hash string value in blocks of 64K:
        for byte_block in iter(lambda: f.read(buf_size), b""):
            sha256_hash.update(byte_block)
    hash_text = sha256_hash.hexdigest()

    func_duration = time.perf_counter() - func_start_timer
    print_trace(f"hash_file_sha256() {hash_text} in {func_duration:.5f} seconds")
    return hash_text


def encrypt_symmetrically(source_file_path: str, cyphertext_file_path: str) -> str:
    """Encrypt a plaintext file to cyphertext.

    using Fernet symmetric encryption algorithm
    after reading entire file into memory.
    Based on https://www.educative.io/answers/how-to-create-file-encryption-decryption-program-using-python
    """
    func_start_timer = time.perf_counter()

    encryption_key = gen_random_alphanumeric(32)  # like "abc123def456"  # 12 char.

    # Generate a 32-byte random encryption key like J64ZHFpCWFlS9zT7y5zxuQN1Gb09y7cucne_EhuWyDM=
    if not encryption_key:  # global variable
        # pip install cryptography  # cryptography-44.0.0
        # from cryptography.fernet import Fernet
        encryption_key = Fernet.generate_key()
    # Create a Fernet object instance from the encryption key:
    fernet_obj = Fernet(encryption_key)

    # Read file contents:
    with open(source_file_path, "rb") as file:
        file_contents = file.read()
    # WARNING: Measure file size because file.read() reads the wholefile into memory.
    file_bytes = len(file_contents)

    # Encrypt file contents:
    encrypted_contents = fernet_obj.encrypt(file_contents)
    with open(cyphertext_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_contents)
    # Measure encrypted file size:
    encrypted_file_bytes = len(encrypted_file)

    # import io
    key_out = io.BytesIO()
    # WARNING: For better security, we do not output the key out to a file.
    # with open('filekey.key', 'wb') as key_file:
    #    key_out.write(key)

    func_duration = time.perf_counter() - func_start_timer
    print_info(
        f"encrypt_symmetrically() From {file_bytes} bytes to {encrypted_file_bytes} bytes in {func_duration:.5f} seconds"
    )
    return key_out


def encrypt_secret(cleartext_in=None):
    """Encrypt a secret using the Fernet module."""
    # from cryptography.fernet import Fernet   # pip install cryptography
    if not cleartext_in:
        cleartext_in = b"A really secret message. Not for prying eyes."
    key = Fernet.generate_key()
    f = Fernet(key)
    binary_token = f.encrypt(cleartext_in)
    # CAUTION: token is a command which outputs the token b'...(don't do it)
    # decrypted_text = f.decrypt(token)
    # b'A really secret message. Not for prying eyes.'
    print_verbose(f"Encrypted binary token contains {len(str(binary_token))} characters.")
    # CAUTION: It is a security violation to display secure tokens in the console.
    return binary_token


def encrypt_file(file_path: str) -> bool:
    """Encrypt a file using AES-256 encryption.

    USAGE:
        password = "your-strong-password"
        pyAesCrypt.encryptFile("data.txt", "data.txt.aes", password)
        pyAesCrypt.decryptFile("data.txt.aes", "dataout.txt", password)
    """
    # import os, import shutil import datetime
    # import pyAesCrypt
    print_verbose("encrypt_file() " + file_path)
    try:
        # import pyAesCrypt
        pyAesCrypt.encryptFile(file_path, file_path + ".aes")
    except Exception as e:
        print_error("encrypt_file() exception: " + str(e))
        return False

    print_trace("encrypt_file() done with " + file_path)
    return True


def decrypt_file(file_path: str) -> bool:
    """Decrypt a file using AES-256 encryption."""
    # import os, import shutil import datetime
    # import pyAesCrypt
    print_verbose("decrypt_file() " + file_path)
    try:
        # import pyAesCrypt
        pyAesCrypt.decryptFile(file_path, file_path[:-4])
    except Exception as e:
        print_error("decrypt_file() exception: " + str(e))
        return False

    print_trace("decrypt_file() done with " + file_path)
    return True


def save_key_in_keychain(svc: str, acct: str, key: str) -> bool:
    """Save the encryption key (password) in the keychain.

    USAGE:
    1. my_secret_key = create_encryption_key()
    2. encrypt(my_secret_key)
    3. save_key_in_keychain("pgm", "mondrian", "my-secret-key")
    """
    print_verbose(f"{sys._getframe().f_code.co_name}(): {svc} {acct} len={str(len(key))} ")
    # import keyring
    keyring.set_password(svc, acct, key)

    # Retrieve a password:
    retrieved_key = keyring.get_password(svc, acct)
    if retrieved_key != key:
        print_error(f"{sys._getframe().f_code.co_name}(): key not found in Keychain.")
        return False
    else:
        # WARNING: Do not expose secret info using print:
        print_verbose(f"{sys._getframe().f_code.co_name}(): {len(retrieved_key)} chars.")
        return True


### SECTION 18 - Send email via Gmail using SMTP


def send_smtp() -> bool:
    """Send email using SMTP protocol through port 465 (SSL) on Gmail servers.

    Global EMAIL_TO is a list of recipients [recipient@example.com,etc.]
    The sender is fixed in the .env file: EMAIL_FROM = "loadtesters@gmail.com"
    sender_password is in the
    subject is assembled in this function: subject = "Test Email"
    :body_in is assembled in this function
    :PROGRAM_NAME from global variable
    :RUNID from global variable
    "This is a test email sent from Python using Gmail SMTP."
    See https://realpython.com/python-send-email/ & https://www.youtube.com/watch?v=WZ_pUSAV5DA
    """
    password = get_api_key("gmail", EMAIL_FROM)  # loadtesters
    if not password:
        print_fail(f"{sys._getframe().f_code.co_name}(): password needed.")
        exit(9)

    recipients = EMAIL_TO  # Recipients as a list: "[ 1@example.com, 2@example.com ]"
    if recipients is None:  # Not a list
        print_error("--emailfrom does not have recipients for send_smtp().")
        return False

    # import smtplib
    body = "From send_smtp() using Gmail SMTP."
    # TODO: Add log lines captured into log database during run.
    # from email.mime.text import MIMEText
    msg = MIMEText(body)
    msg["From"] = EMAIL_FROM
    # TODO:
    msg["Subject"] = f"From {PROGRAM_NAME} for {RUNID}"

    for index, recipient in enumerate(recipients.split(",")):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(EMAIL_FROM, password)
            msg["To"] = recipient
            smtp_server.sendmail(EMAIL_FROM, recipient, msg.as_string())
            print_verbose(f"send_smtp() emailed {index + 1} to " + recipient)
    # FIXME: smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted.
    # For more information, go to\n5.7.8  https://support.google.com/mail/?p=BadCredentials
    # 98e67ed59e1d1-2f7ffa76d1csm4313179a91.32 - gsmtp')
    return True


# To parse inbound email:
# https://postmarkapp.com/blog/an-introduction-to-inbound-email-parsing-what-it-is-and-how-you-can-do-it
# https://dev.to/devteam/join-the-postmark-challenge-inbox-innovators-3000-in-prizes-497l?


def gen_qrcode(url: str, qrcode_file_path: str) -> bool:
    """Generate a QR code from a URL and save it to a file.

    See https://www.geeksforgeeks.org/python-generate-qr-code/
    See https://python.plainenglish.io/how-i-generate-qr-codes-with-python-in-under-30-seconds-77f627e8fe63
    """
    if not GEN_QR_CODE:  # Bypass
        return False

    print_verbose("gen_qrcode() url=" + url + " qrcode_file_path=" + qrcode_file_path)
    try:
        # import qrcode  with higher level of error correction
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=5,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qrcode_file_path)
        print_verbose("gen_qrcode() output to " + qrcode_file_path)
        return True
    except Exception as e:
        print_error("gen_qrcode() error: " + str(e) + " for " + url)
        return False


def main():  # SAMPLE USAGE:
    """Show sample usage."""
    do_clear_cli()
    show_print_samples()

    print_verbose(f"Started: {get_user_local_time()}, in logs: {get_log_datetime()} ")
    pgm_strt_mem_used = get_process_memory()
    print_verbose(f"Started: {pgm_strt_mem_used:.2f} MiB RAM being used.")
    pgm_strt_disk_free, pgm_strt_pct_disk_free = get_disk_free()
    print_verbose(f"Started: {pgm_strt_disk_free:.2f} GB ({pgm_strt_pct_disk_free}) disk space free.")

    print(f"is_running_locally()? {is_running_locally()} ")
    print(f"is_local_development()? {is_local_development()} ")
    # print(f"get_environment_info(): {get_environment_info()} ")

    print_module_filenames()
    get_environment_info()
    # mem_usage("start")
    # for a in list_files("./",(".py"), ("__init__")):
    #    print(a)
    #    print(get_fuid(a))
    # my_file="myutils.py"

    list_pgm_functions(__file__)
    print_dunder_vars(__file__)  # __file__ = current module name (like "myutils.py")

    get_disk_free()
    get_process_memory()
    # trace_memory_usage(func)
    show_memory_profile()
    get_all_objects_by_type()

    global_env_path = open_env_file()
    my_printer = get_str_from_env_file("MY_PRINTER")
    print(f"my_printer={my_printer}")
    update_env_file(global_env_path, "TESTING", "whatever3")

    reverse_words("A string of words")

    # Secrets:
    print_heading("RSA Key Pair Generator:")

    print(f'gen_random_alphanumeric(): "{gen_random_alphanumeric(length=12)}" (SAMPLE ONLY) ')
    # On Macos: Save keys in standard PEM format.

    # file_path = "~/keys/private_key.pem"
    # print_heading(f"1. Generating unencrypted RSA key pair (2048-bit) to \"{file_path}\"...")
    # TODO: Add folder_path = "~/keys"
    # private_pem, public_pem = generate_rsa_keypair()
    # print(f"Private key size: {len(private_pem)} bytes")
    # print(f"Public key size:  {len(public_pem)} bytes")
    # delete_all_files_in_folder(folder_path)

    # folder_path = "~/encrypted_keys"
    # print_heading(f"2. Generating encrypted RSA key pair to \"{folder_path}\"...")
    # password = "your_secure_password_here"  # Change this!
    # generate_encrypted_keypair(password, output_dir=folder_path)
    # delete_all_files_in_folder(folder_path)

    folder_path = "~/large_keys"
    print_heading(f'3. Generating large RSA key pair to "{folder_path}"...')
    generate_rsa_keypair(key_size=4096, output_dir=folder_path)
    file_path = f"{folder_path}/private_key.pem"
    private_rsa_key_clear_text = read_file_to_string(file_path)
    print_verbose(f"private_rsa_key_clear_text: {len(private_rsa_key_clear_text)} bytes")
    # DO NOT PRINT SECRETS: private_rsa_key_clear_text

    if DELETE_OUTPUT_FILE:  # -do --delout
        # Instead of: os.remove(folder_path)
        delete_all_files_in_folder(folder_path)

    show_summary()


if __name__ == "__main__":
    main()
