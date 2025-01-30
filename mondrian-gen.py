#!/usr/bin/env python3

"""mondrian-gen.py at https://github.com/wilsonmar/python-samples/blob/main/mondrian-gen.py
This program provides both local programmatic and Generative AI (GenAI)API calls
to create (from text prompt) a PNG image file of art in the pure abstract Neoplasticism style
initiated in 1920s by Piet Mondrian (in Amersfort, Netherlands 1872-1944).

This was created to see how the different ways of creating horizontal and 
vertical lines of rectangular boxes filled with primary colors
compare with the intuitive beauty of works manually created by Mondrian, such as
https://res.cloudinary.com/dcajqrroq/image/upload/v1736178566/mondrian.29-compnum3-268x266_hceym9.png

// SPDX-License-Identifier: MIT
CURRENT STATUS: WORKING but pgm art has too thick lines & no env file retrieve.
    ERROR: gen_one_file() draw_mondrian() failed. 

git commit -m"v021 + logging :mondrian-gen.py"

Tested on macOS 24.1.0 using Python 3.12.8

# Before running this program:
1. In Terminal: INSTEAD OF: conda install -c conda-forge ...
    python3 -m venv venv
    source venv/bin/activate

    python3 -m pip install envcloak keyring OpenAI pycairo python-dotenv Pillow psutil qrcode requests tzlocal
    python3 -m pip install web3 eth_account IPFS-Toolkit Fernet cryptography pycryptodome qiskit
    # See https://wilsonmar.github.io/quantum
    python3 -m pip install functools  # FIXME ERROR: Failed to build installable wheels for some pyproject.toml based projects (functools)
    python3 -m pip install --upgrade -q google-api-python-client google-auth-httplib2 google-auth-oauthlib
    python3 -m pip install stablediffusionapi
        import smtplib
        from email.mime.text import MIMEText
    python3 -m pip install anthropic pymongo

    # Successfully installed stablediffusionapi-0.0.5
    # Successfully installed stablediffusion_api-1.0.7 from https://stability.ai
    # See https://faun.pub/stable-diffusion-enabling-api-and-how-to-run-it-a-step-by-step-guide-7ebd63813c22
    # See https://www.datacamp.com/tutorial/how-to-use-stable-diffusion-3-api

2. Within VSCode install Ruff (from Astral Software), written in Rust
   to lint Python code. 
3. Run ruff check on this program (Flake8, Pylint, Xenon, Radon, Black, isort, pyupgrade, etc.)
   See https://github.com/charliermarsh/ruff

flake8  E501 line too long, E222 multiple spaces after operator

4. Use an internet browser to obtain API keys from cloud services: 
   1a. ChatGPT API calls at https://platform.openai.com/api-keys and 
   1b. https://platform.stability.ai/account/keys see https://www.youtube.com/watch?v=Uo9XUapKz9o&t=4s
   1c. https://www.quicknode.com/signup
   1d. https://chat.qwenlm.ai/auth?action=signup Qwen2.5-Max Max context length: 32,768 tokens, Max generation length: 8,192 tokens
5. Open the Keychain Access.app. Click login then iCloud. Click the add icon at the top.
6. Fill in the Item Name and Account Name 
   6a. Store "dalle2 as Item Name for use as --keyitem "openai"
   6b. Store "stability" as Item Name for use as --keyitem "stability"
   6c. Store QuickNode API Key & for use as --keyitem "quicknode"
   6d. Store "gmail" as Item Name for sending emails.
7. Paste the API key in the Password field. Click Add.

8. Create Edit .env files to customize run parameters.
9. Create local log database and save the password.
10. Create Mongodb database  and save the password.
11. View -h to see parameters to control how to this program runs:
    chmod +x mondrian-gen.py
    ./mondrian-gen.py -h  # for list of parameters

        usage: mondrian-gen.py [-h] [-pf PARMSPATH] [-q] [-v] [-vv] [-ss] [-ri] [-si] [-log] [-dt]
                            [-z] [-d DRIVEPATH] [-f FOLDER] [-ai AI] [-ka KEYITEM] [-ki KEYACCT]
                            [-up] [-fg FILESGEN] [-su SHORTURL] [-w WIDTH] [-he HEIGHT] [-do]
                            [-so] [-ks] [-gf] [-wm MARKTEXT] [-e] [-key KEY] [-256] [-ipfs] [-qn]
                            [-me MINTEMAIL] [-qr] [-s SLEEPSECS] [-em] [-et EMAILTO]
                            [-ef EMAILFROM] [-md MONGODB] [-m]

        Mondrian Art Generator

        options:
        -h, --help            show this help message and exit
        -pf, --parmspath PARMSPATH
                                File Path string to env specs
        -q, --quiet           Run without output
        -v, --verbose         Show what input goes into functions
        -vv, --trace          Trace info comes out of functions
        -log, --loglvl LOGLEVEL  Log to external file "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        -ss, --showsecrets    Show secrets
        -ri, --runid          Run ID (no spaces or special characters)
        -si, --si             Show System Info
        -dt, --showdates      Show dates in logs
        -z, --utc             Show Dates in UTC/GMT=Zulu timezone
        -d, --drivepath DRIVEPATH
                                Removeable USB Drive Name (after /Volumes/)
        -f, --folder FOLDER   Folder (Desktop) to hold output files
        -ai, --ai AI          AI svc: dalle2, stability, deepseek, qwen
        -ka, --keyitem KEYITEM
                                Item string in keyring
        -ki, --keyacct KEYACCT
                                Account string in keyring to get API key
        -up, --upscale        Upscale image
        -fg, --filesgen FILESGEN
                                Files to generate integer number
        -su, --shorturl SHORTURL
                                Shorten URL for less complex QR Code
        -w, --width WIDTH     Width (pixel size of output file eg 500)
        -he, --height HEIGHT  Height (pixel size of output file eg 500)
        -do, --delout         Delete output file
        -so, --showout        Show output file
        -ks, --keepshow       Keep Showing output file (not kill preview)
        -gf, --genurlfile     Gen a file to open url in browser
        -wm, --marktext MARKTEXT
                                Watermark text to insertin png file
        -e, --encrypt         Encrypt file
        -key, --key KEY       Encryption key
        -256, --hash          Gen SHA256 Hash from output file contents
        -ipfs, --ipfs         Gen. IPFS CID
        -qn, --quicknode      Gen. IPFS CID in QuickNode
        -me, --mintemail MINTEMAIL
                                Email to attribute Mint NFT
        -qr, --genqr          Gen QR Code image file to each URL
        -s, --sleepsecs SLEEPSECS
                                Sleep seconds number
        -em, --email          Email (via gmail) summary
        -et, --emailto EMAILTO
                                Recipient list of emails about results
        -ef, --emailfrom EMAILFROM
                                Sender gmail address
        -md, --mongodb MONGODB
                                "local", port "27017", or MONGODB URL
        -m, --summary         Show summary

12. Craft commands to run this program:
    ./mondrian-gen.py -v -vv 
    ./mondrian-gen.py -v -vv -q -gf
    ./mondrian-gen.py -v -vv --mintemail "johndoe@gmail.com" -q -gf -md "local" -ai "dalle2" 

Alternative API: https://niftykit.com/products/minting-api

TODO: Other articles about tools to generate art:
<a target="_blank" href="https://www.youtube.com/watch?v=Vgcr6VOwHf0">VIDEO</a>
* <a target="_blank" href="https://mondriangenerator.io/">Mondrian Generator</a> web-based tool. Allows you to adjust parameters in the left panel: Format (size), Complexity (number of blocks), Colors, Color amount.
* <a target="_blank" href="https://www.artvy.ai/ai-art-style/piet-mondrian">Artvy</a> generates based on an image you upload for style transfer.
* <a target="_blank" href="https://neural.love/ai-art-generator/1ed7da32-c7dc-6e2c-957c-7fd88793a662/mondrian-painting">Neural Love</a> generate art under a CC0 license.
* <a target="_blank" href="https://www.pcmag.com/how-to/how-to-use-dall-e-ai-art-generator">DaLL-E</a> from OpenAI's generates realistic as part of the ChatGPT Plus $20 per month paid version. 
    See https://platform.openai.com/docs/overview
* <a target="_blank" href="https://dev.to/ranjancse/systematic-modern-artwork-with-aiconfig-1ol8">AiConfig</a>
* <a target="_blank" href="https://lastmileai.dev/">LastMileAI</a>
* https://github.com/unsettledgames/mondrian-generator 

Other Mondrian artists:
* <a target="_blank" href="https://twitter.com/ArtByPietMondrian">ArtByPietMondrian</a>
* https://opensea.io/collection/mondriannft
* https://opensea.io/collection/soupxmondrian
* https://opensea.io/collection/pepemondrians
* https://opensea.io/collection/mondrian-on-polygon
"""


#### SECTION 01 - import internal modules (alphabetically):

# For wall time of std (standard) imports:
import datetime as dt
std_strt_datetimestamp = dt.datetime.now()

from doctest import run_docstring_examples
# Standard Python library modules (no need to pip install):
import argparse
from argparse import ArgumentParser
import base64
from functools import cache
import hashlib
import io
import json
import logging
import os
import pathlib
from pathlib import Path
import platform
import random
import re
import shutil
import smtplib
from email.mime.text import MIMEText
import socket
import subprocess
import sys
import time
import uuid

std_stop_datetimestamp = dt.datetime.now()


#### SECTION 02 - imports external modules (alphabetically) at top of file
# See https://peps.python.org/pep-0008/#imports

# For wall time of xpt imports:
xpt_strt_datetimestamp = dt.datetime.now()

import anthropic
import cairo  # pip install pycairo (https://pycairo.readthedocs.io/en/latest/)
#import cryptography
from Crypto.PublicKey import RSA  # from pip install pycryptodome
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from qiskit.circuit.library import QFT   # see https://docs.quantum.ibm.com/api/qiskit
#from qiskit import QuantumCircuit, execute, Aer
from dotenv import load_dotenv
from envcloak import load_encrypted_env
import ipfs_api  # https://pypi.org/project/IPFS-Toolkit/
import keyring
from openai import OpenAI
# import Pillow to convert SVG to PNG file format:
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
import psutil
import pytz  # for time zone handling
from pymongo import MongoClient
import qrcode
import requests   # used by stability.ai to operate stable diffusion API
    # NOTE: The requests library is more versatile and widely used than
    # urllib is a built-in module that doesn't require additional installation.
import timeit
import tzlocal

# For wall time of xpt imports:
xpt_stop_datetimestamp = dt.datetime.now()


#### SECTION 03 - Start Global timers:


# Based on: pip3 install datetime
#import datetime as dt
#from datetime import datetime, timezone
# For wall time of program run (using date and time together):
utc_strt_datetimestamp = dt.datetime.now(dt.timezone.utc)
pgm_strt_datetimestamp = dt.datetime.now()

local_time = time.localtime()
TZ_OFFSET = time.strftime("%z", local_time)  # such as "-0700"
# TODO: Use Decorators to capture timings. https://realpython.com/videos/timing-functions-decorators/
#import time   # std python module for time.sleep(1.5)
# To display date & time of program start:
pgm_strt_timestamp = time.monotonic()
# TODO: Display Z (UTC/GMT) instead of local time
pgm_strt_epoch_timestamp = time.time()
pgm_strt_local_timestamp = time.localtime()
# the most accurate difference between two times. Used by timeit.
# pgm_strt_perf_counter = time.perf_counter()

# For the time taken to execute a small bit of Python code:
#import timeit
#from timeit import default_timer as timer
# start_time = timeit.default_timer()  # start the program-level timer.


#### SECTION 04 - utility printing globals and functions (used by other functions):


# all global:
# The pallette of primary RBG colors:
# COLORS = [(1, 1, 1), (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 1)]
# Plus green, orange, and purple:
COLORS = [(1, 1, 1), (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 1), (0, 1, 0), (1, 0.5, 0), (0.5, 0, 0.5)]
    # See https://www.schoolofmotion.com/blog/10-tools-to-help-you-design-a-color-palette

# Colors:
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'   # [94 blue (bad on black background)
PURPLE = '\033[35m'
VIOLET = '\033[38m'
ORANGE = '\033[208m'

CVIOLET = '\033[35m'
CBEIGE = '\033[36m'
CWHITE = '\033[37m'
CGRAY = '\033[90m'  # secret

# Styles:
BOLD = '\033[1m'
RESET = '\033[0m'  # switch back to default color

class bcolors:  # ANSI escape sequences:
    BOLD = RED #'\033[1m'       # Begin bold text
    UNDERLINE = '\033[4m'  # Begin underlined text

    HEADING = CWHITE #'\033[90m'   # [90 gray  NOT [37 white
    INFO = GREEN # '\033[92m'      # [92 green
    VERBOSE = PURPLE # '\033[95m'   # [95 purple
    TRACE = ORANGE # '\033[96m'     # [96 blue/green
    WARNING = BLUE # '\033[93m'   # [93 yellow
    ERROR = RED # '\033[91m'     # [91 red
    FAIL = YELLOW # '\033[91m'      # [91 red

LOG_LVL = False   # If True, log to external file

def do_clear_cli() -> None:
    if CLEAR_CLI:
        import os
        # Make a OS CLI command:
        lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    return None

# TODO: Add standard log() functions
def print_separator() -> None:
    """ Put a blank line in CLI output. Used in case the technique changes throughout this code. 
    """
    print(" ")

def print_heading(text_in: str) -> None:
    """ Provide a heading to help align vertical text columns.
    """
    if show_heading:
        if show_dates_in_logs:
            out = bcolors.HEADING+bcolors.UNDERLINE, '\n***', local_datetime_stamp(), f'{text_in}', RESET
        else:
            print(bcolors.INFO +'***'+ out + RESET)
            out = bcolors.HEADING+bcolors.UNDERLINE,'\n***', f'{text_in}', RESET
        print(out)
        if LOG_LVL == "INFO":
            logging.info(out)

# "INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"
def print_fail(text_in: str) -> None:
    """ Explain a critical failure causing the program to stop.
    """
    if show_fail:
        if show_dates_in_logs:
            out = local_datetime_stamp() +" "+ text_in
        else:
            out = text_in
        print(bcolors.FAIL +'***'+ out + RESET)
        if LOG_LVL == "CRITICAL":
            logging.critical(out)

def print_error(text_in: str) -> None:  
    """ Explain to programmers about a potential programming error.
    """
    if show_fail:
        if show_dates_in_logs:
            out = local_datetime_stamp() +" "+ text_in
        else:
            out = text_in
        print(bcolors.ERROR +'***'+ out + RESET)
        if LOG_LVL == "ERROR":
            logging.error(out)

def print_warning(text_in: str) -> None:
    """ Warn the programmer about changes such as default values applied.
    """
    if show_warning:
        if show_dates_in_logs:
            out = local_datetime_stamp() +" "+ text_in
        else:
            out = text_in
        print(bcolors.WARNING +'***'+ out + RESET)
        if LOG_LVL == "WARNING":
            logging.warning(out)

def print_todo(text_in: str) -> None:
    """ Remind the programmer of a TODO item when the program is run.
    """
    if show_todo:
        if show_dates_in_logs:
            out = local_datetime_stamp() +" "+ text_in
        else:
            out = text_in
        print(bcolors.INFO +'***'+ out + RESET)
        # logging.warning(out)

def print_info(text_in: str) -> None:
    """Display information to users about what was done.
    """
    if show_info:
        if show_dates_in_logs:
            out = local_datetime_stamp() +" "+ text_in
        else:
            out = text_in
        print(bcolors.INFO+bcolors.BOLD +'***'+ out + RESET)
        if LOG_LVL == "INFO":
            logging.info(out)

def print_verbose(text_in: str) -> None:
    """Display details about inputs to each function:
    """
    if show_verbose:
        if show_dates_in_logs:
            out = local_datetime_stamp() +" "+ text_in
        else:
            out = text_in
        print(bcolors.VERBOSE +'***'+ out + RESET)
        if LOG_LVL == "INFO":
            logging.info(out)

def print_trace(text_in: str) -> None:  # displayed as each object is created in pgm:
    """To display details output from a function:
    """
    if show_trace:
        if show_dates_in_logs:
            out = local_datetime_stamp() +" "+ text_in
        else:
            out = text_in
        print(bcolors.TRACE +'***'+ out + RESET)
        if LOG_LVL == "DEBUG":
            logging.debug(out)

def print_secret(secret_in: str) -> None:
    """ Outputs only the first few characters (like Git) with dots replacing the rest 
    """
    # See https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
    if show_secrets:  # program parameter
        if show_dates_in_logs:
            now_utc=datetime.now(timezone('UTC'))
            print(bcolors.WARNING, '*** ',now_utc,"SECRET: ", secret_in, RESET)
        else:
            print(bcolors.CBEIGE, '***', "SECRET: ", secret_in, RESET)
    else:
        # same length regardless of secret length to reduce ability to guess:
        secret_len = 8
        if len(secret_in) >= 8:  # slice
            secret_out = secret_in[0:4] + "."*(secret_len-4)
        else:
            secret_out = secret_in[0:4] + "."*(secret_len-1)
            if show_dates_in_logs:
                print(bcolors.WARNING, '***', local_datetime_stamp(), f'{text_in}', RESET)
            else:
                print(bcolors.CBEIGE, '***', " SECRET: ", f'{secret_out}', RESET)
    return None


#### SECTION 05 - TASK: Customize hard-coded values that control program flow.


# Start with program name (without ".py" file extension) such as "modrian-gen":
PROGRAM_NAME = Path(__file__).stem
    # See https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    # Instead of os.path.splitext(os.path.basename(sys.argv[0]))[0]

# This check is too late because "No module named" errors appear first when not in venv.
# VSCode Python Environment Manager extension https://www.youtube.com/watch?v=1w6zUrVx4to
def is_venv_activated():
    # import sys
    return sys.prefix != sys.base_prefix
if not is_venv_activated():
    print("Please activate your virtual environment:\npython3 -m venv venv\nsource venv/bin/activate")
    exit(9)

def is_macos():
    return platform.system() == "Darwin"

if os.name == "nt":  # Windows operating system:
    SLASH_CHAR = "\\"
    # if platform.system() == "Windows":
    print_fail(f"*** Windows Edition: {platform.win32_edition()} Version: {platform.win32_ver()}")
    print_warning("*** WARNING: This program has not been tested on Windows yet.")
else:
    # print("*** os.name="+os.name)  # "posix" for macOS & Linux
    SLASH_CHAR = "/"

SAVE_CWD = os.getcwd()  # cwd=current working directory (python-examples code folder)
SAVE_PATH = os.path.expanduser("~")  # user home folder path like "/User/johndoe"
#print("*** DEBUGGING: SAVE_PATH="+SAVE_PATH)
#print("*** DEBUGGING: SAVE_CWD= "+SAVE_CWD)


# These will be overridden by variables (API key, etc.) within .env file.

#def set_hard_coded_defaults() -> None:

CLEAR_CLI = True

show_todo = True

show_heading = True
show_info = True
show_warning = True
show_error = True
show_fail = True
LOG_LVL = False

DRIVE_VOLUME = "NODE NAME"  # as in "/Volumes/NODE NAME" - the default from manufacturing.

show_dates_in_logs = False
DATE_OUT_Z = False  # save files with Z time (in UTC time zone now) instead of local time.

run_quiet = False  # suppress show_heading, show_info, show_warning, show_error, show_fail

show_verbose = False

show_trace = False
show_sys_info = False
show_secrets = False

RUNID = "R011"  # This value should have no spaces or special characters.
   # TODO: Store and increment externally each run (usign Python Generators?) into a database for tying runs to parmeters such as the PROMPT_TEXT, etc. https://www.linkedin.com/learning/learning-python-generators-17425534/

OUTPUT_FOLDER = "Desktop"  # "Desktop" or "Documents" or "Downloads" to avoid subfolder creation.
GEN_URL_FILE = False
SHORTEN_URL = False

# For creation of image files:
# PROMPT_TEXT = "A beautiful monochromatic art piece"

WIDTH_PIXELS = 500
HEIGHT_PIXELS = 500
# For ref. by generate_mondrian(), mondrian_flood_fill(), draw_mondrian()
TILE_SIZE = 10
# TODO: Vary borderWidth = 8; minDistanceBetweenLines = 50;
# See https://github.com/unsettledgames/mondrian-generator/blob/master/mondri an_generator.pde

# Alternatives for Generative AI: https://youtube.com/shorts/nHQSpxKGoms?si=K3wuarLLGmbczZHC
    # https://blog.monsterapi.ai/blogs/text-to-image-stable-diffusion-api-guide/
    # A-tier: Midjourney lacks an API (but has great models & results, easy to use)
    # A-tier: Stable Diffusion requires more technical knowledge for managing LORAs, styles, and checkpoints
        # Has flexibility with plug-ins, but can be complex to use.
        # See https://www.youtube.com/watch?v=7xc0Fs3fpCg
        # See https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Commands#webui
    # ?-tier: Anthropic https://claude.ai/new
    # B-tier: Adobe Firefly (requires subscription)
    # B-tier: NightCafe (template options)
    # C-tier: Jasper AI https://jasper.ai/ (expensive)
    # C-tier: DALL-E 2 https://openai.com/blog/dall-e-2/ (Jan 2022)
    # C-tier: Wonder 
    # D-tier: DALL-E https://openai.com/blog/dall-e/ (the original breakthrough Jan 2021)
    # D-tier: Crayon (free with watermarks, but limited) https://www.getcrayon.com/

    # Artbreeder? https://nightcafe.studio/blogs/info/how-does-artbreeder-work
    # Streamlit https://docs.streamlit.io/library/advanced-features/file-uploads
        # https://www.youtube.com/watch?v=YzvMpvXyUfs
        # https://www.youtube.com/watch?v=Wl1GtsfrskA Streamlit & Runway ML
    # Huggingface https://huggingface.co/spaces/CompVis/latent-diffusion-pytorch

# used to specify what API to use as well as keyring service name
ai_svc = None   # "dalle2", "qwen", "stability" or "deepseek", "anthropic", etc.
keyacct = None   # "johndoe@gmail.com" 
MINT_EMAIL = None  # -me --mintemail (wallet account name)
RUN_ENV = "staging"  # "prod" or staging (license)

# For creation of text : See https://www.youtube.com/watch?v=CaxPa1FuHx4 by Aaron Dunn.

gmail_api_key = None

### Processing controls:

SUMMARIZE_IMAGE = False  # For caption

KIOSK_MODE = False

FILES_TO_GEN = 1     # 0 = Infinite loop while in kiosk mode.
SLEEP_SECONDS = 1.0  # between art created in a loop

UPSCALE_IMAGE = False

ENCRYPT_FILE = False

GEN_SHA256 = False

ENCRYPTION_KEY = None

USE_QISKIT = False   # for Quantum resistant encryption

GEN_NFT = False

ADD_WATERMARK = False  # watermark2png()
WATERMARK_TEXT = "\"Like Mondrian 2054\" Copywrite Wilson Mar 2025. All rights reserved."
# Copyright issues: In the United States, only works created by humans can be copyrighted.

GEN_IPFS = False
UPLOAD_TO_QUICKNODE = False

BLOCKCHAIN_NAME = "solana"  # "ethereum" (Ethereum Mainnet - the most popular), "Solana (solana-mainnet), "polygon-amoy", "ethereum-sepolia", "Near", "Avalanche", "AirNFTs", Arbitrum, Optimism
MINT_EMAIL = None
# wallet = "Metamask", MATIC (Polygon's native token) or Polygon-bridged ETH
# Agents = Zapier, make.com, n8n, Agentforce
NFT_MARKETPLACE = "Opensea","MagicEden", "Rarible", "Superrare"

GEN_QR_CODE = False


### Output controls:

DELETE_OUTPUT_FILE = False  # If True, recover files from Trash

encrypted_file_path='your_file.txt'
cyphertext_file_path = "path/to/your/file ???"
DECRYPT_FILE = False
decrypted_file_path='your_file.txt'

quicknode_file_path = "path/to/your/file ???"

SHOW_OUTPUT_FILE = False
MONGODB = None

KEEP_SHOWING = False

SEND_EMAIL = False
EMAIL_FROM = "loadtesters@gmail.com"
EMAIL_TO = "[1@a.com, 2@b.com]"

SHOW_SUMMARY_COUNTS = True


#### SECTION 06 - Read custom command line (CLI)arguments

def read_cmd_args() -> None:
    """Read command line arguments and set global variables.
    See https://realpython.com/command-line-interfaces-python-argparse/
    """
    #import argparse
    #from argparse import ArgumentParser
    parser = argparse.ArgumentParser(allow_abbrev=True,description="Mondrian Art Generator")
    parser.add_argument("-pf", "--parmspath", help="File Path string to env specs")
    parser.add_argument("-q", "--quiet", action="store_true", help="Run without output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show what input goes into functions")
    parser.add_argument("-vv", "--trace", action="store_true", help="Trace info comes out of functions")
    parser.add_argument("-ss", "--showsecrets", action="store_true", help="Show secrets")

    parser.add_argument("-ri", "--runid", action="store_true", help="Run ID (no spaces or special characters)")
    parser.add_argument("-si", "--si", action="store_true", help="Show System Info")
    parser.add_argument("-l", "--loglvl", help="Level of logging to external file/cloud")
    parser.add_argument("-dt", "--showdates", action="store_true", help="Show dates in logs")
    parser.add_argument("-z", "--utc", action="store_true", help="Show Dates in UTC/GMT=Zulu timezone")

    parser.add_argument("-d", "--drivepath", help="Removeable USB Drive Name (after /Volumes/)")
    parser.add_argument("-f", "--folder", help="Folder (Desktop) to hold output files")

    parser.add_argument("-ai", "--ai", help="AI svc: dalle2, stability, deepseek, qwen")
    parser.add_argument("-ka", "--keyitem", help="Item string in keyring")
    parser.add_argument("-ki", "--keyacct", help="Account string in keyring to get API key")

    parser.add_argument("-up", "--upscale", action="store_true", help="Upscale image")
    parser.add_argument("-fg", "--filesgen", help="Files to generate integer number")
    parser.add_argument("-su", "--shorturl", help="Shorten URL for less complex QR Code")

    parser.add_argument("-w", "--width", help="Width (pixel size of output file eg 500)")
    parser.add_argument("-he", "--height", help="Height (pixel size of output file eg 500)")

    parser.add_argument("-do", "--delout", action="store_true", help="Delete output file")
    parser.add_argument("-so", "--showout", action="store_true", help="Show output file")
    parser.add_argument("-ks", "--keepshow", action="store_true", help="Keep Showing output file (not kill preview)")
    parser.add_argument("-gf", "--genurlfile", action="store_true", help="Gen a file to open url in browser")

    parser.add_argument("-wm", "--marktext", help="Watermark text to insertin png file")
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt file")
    parser.add_argument("-key", "--key", help="Encryption key")
                       # -key --key like: "J64ZHFpCWFlS9zT7y5zxuQN1Gb09y7cucne_EhuWyDM="
    parser.add_argument("-256", "--hash", action="store_true", help="Gen SHA256 Hash from output file contents")
    # See https://bomonike.github.io/nft for explanation:
    parser.add_argument("-ipfs", "--ipfs", action="store_true", help="Gen. IPFS CID")
    parser.add_argument("-qn", "--quicknode", action="store_true", help="Gen. IPFS CID in QuickNode")

    parser.add_argument("-me", "--mintemail", help="Email to attribute Mint NFT")
    parser.add_argument("-qr", "--genqr", action="store_true", help="Gen QR Code image file to each URL")

    parser.add_argument("-s", "--sleepsecs", help="Sleep seconds number")
    parser.add_argument("-em", "--email", action="store_true", help="Email (via gmail) summary ")
    parser.add_argument("-et", "--emailto", help="Recipient list of emails about results")
    parser.add_argument("-ef", "--emailfrom", help="Sender gmail address")
    parser.add_argument("-md", "--mongodb", help="\"local\",  \"27017\", or MONGODB URL")
    parser.add_argument("-m", "--summary", action="store_true", help="Show summary")
    # Default -h = --help (list arguments)

    args = parser.parse_args()


    #### SECTION 07 - Override defaults and .env file with run-time parms:

    # In sequence of workflow:

    if args.parmspath:     # -pf "/Documents/my.env"
        global SHOW_PARMSPATH
        SHOW_PARMSPATH = args.parmspath
    if args.quiet:         # -quiet
        global show_heading
        show_heading = False
        global show_info
        show_info = False
        global show_warning
        show_warning = False
        global show_error
        global show_fail
        show_fail = False
        global SHOW_SUMMARY_COUNTS
        SHOW_SUMMARY_COUNTS = False

    if args.showdates:     # -dt = "--showdates", action="store_true", help="Show dates in logs")
        global show_dates_in_logs
        show_dates_in_logs = True

    if args.verbose:       # -v
        global show_verbose
        show_verbose = True
        global SHOW_DOWNLOAD_PROGRESS
        SHOW_DOWNLOAD_PROGRESS = True
    if args.trace:
        global show_trace
        show_trace = True

    if args.loglvl:               # -l --loglvl "DEBUG", "INFO", "WARNING", "ERROR", "FAIL", "NONE"
        global LOG_LVL
        LOG_LVL = args.loglvl
    # TODO: Log to cloud API?
        global LOGGER_FILE_PATH
        LOGGER_FILE_PATH = SAVE_PATH + SLASH_CHAR + os.path.basename(__file__) + '.log'
        print("*** DEBUGGING: LOGGER_FILE_PATH="+LOGGER_FILE_PATH)
        exit()
        global LOGGER_NAME
        LOGGER_NAME = os.path.basename(__file__)  # program script name.py

    if args.showsecrets:  # -ss  --showsecrets
        global show_secrets
        show_secrets = True

    if args.runid:         # -ri --runid  "Run ID (no spaces or special characters)"
        global RUNID
        RUNID = args.runid

    if args.email:     # -em  --email
        global SEND_EMAIL
        SEND_EMAIL = True
    if args.emailfrom:     # -ef  --emailfrom "loadtesters" used by send_smtp()
        global EMAIL_FROM
        EMAIL_FROM = args.emailfrom
    if args.emailto:       # -et  --emailto Recipient list "[1@a.io, 2@b.ai]"
        global EMAIL_TO
        EMAIL_TO = args.emailto
    if args.mintemail:     # -me --mintemail
        global MINT_EMAIL
        MINT_EMAIL = args.mintemail

    if args.si:            # -si => used by sys_info()
        global show_sys_info
        show_sys_info = True
    if args.utc:           # -z = # Dates in UTC/GMT=Zulu timezone
        global DATE_OUT_Z
        DATE_OUT_Z = True  # save files with Z time (in UTC time zone now) instead of local time.

    if args.ai:            # -ai --ai "dalle2", "qwen", "stability", etc.
        global ai_svc
        ai_svc = args.ai
    if args.keyitem:       # -ki --keyitem "gmail", "quicknode"
        global keyitem
        keyitem = args.keyitem
    if args.keyacct:       # -ka --keyacct "openai"
        global keyacct
        keyacct = args.keyacct

    if args.shorturl:       # -su --shorturl
        global SHORTEN_URL
        SHORTEN_URL = args.shorturl

    if args.filesgen:       # -fg --filesgen
        global FILES_TO_GEN
        FILES_TO_GEN = args.filesgen     # 0 = Infinite loop while in kiosk mode.

    if args.drivepath:      # -d "//Volumes/DriveX" # (USB removable drive without the /Volumes/ prefix)
        global DRIVE_PATH
        DRIVE_PATH = args.drivepath
    if args.folder:         # -f "Downloads" (overwrites default "Desktop" folder)
        global OUTPUT_FOLDER
        OUTPUT_FOLDER = args.folder

    if args.width:          # Width of output number (eg 500)"
        global WIDTH_PIXELS
        WIDTH_PIXELS = args.width
    if args.height:         # Height of output number (eg 500)"
        global HEIGHT_PIXELS
        HEIGHT_PIXELS = args.height

#    if args.dalle:          # -de ="Gen Dall-E png file"
#        global USE_DALLE_API
#        USE_DALLE_API = True  # if False, use programmatic Python. True = use DELL-E
#      # USE_DALLE_API = False  # if False, use programmatic Python. True = use DELL-E
#    if args.sd:     # -sd = "STABLEDIFFUSION API")
#        global USE_STABILITY_API
#        USE_STABILITY_API = True
#        # Stable Diffusion is open-source and can be used for free

#    if args.upscale:        # -up --upscale
#        UPSCALE_IMAGE = True
    if args.marktext:          # -wm "\"Like Mondrian 2054\" Copywrite Wilson Mar 2025. ..."
        global WATERMARK_TEXT  # used by watermark2png()
        WATERMARK_TEXT = args.marktext  # used by watermark2png()

    if args.encrypt:
        global ENCRYPT_FILE
        ENCRYPT_FILE = True
    if args.key:               # -key --key "J64ZHFpCWFlS9zT7y5zxuQN1Gb09y7cucne_EhuWyDM="
        global ENCRYPTION_KEY
        ENCRYPTION_KEY = args.key
    if args.hash:              # "-256" ="Hash SHA256"
        global GEN_SHA256
        GEN_SHA256 = True
    if args.ipfs:              # -ipfs --ipfs
        global GEN_IPFS
        GEN_IPFS = True
 
    if args.quicknode:
        global UPLOAD_TO_QUICKNODE
        UPLOAD_TO_QUICKNODE = True

    if args.genqr:             # -qr  --genqr Gen QR code image file from URL
        global GEN_QR_CODE
        GEN_QR_CODE = True
    if args.genurlfile:           # -gf  --genurlfile
        global GEN_URL_FILE
        GEN_URL_FILE = True

    if args.showout:           # -so  --showout Show output file
        global SHOW_OUTPUT_FILE
        SHOW_OUTPUT_FILE = True
    if args.keepshow:          # -ks  --keepshow Keep showing output file
        global KEEP_SHOWING
        KEEP_SHOWING = False

    if args.delout:            # -de  --delout Delete output file
        global DELETE_OUTPUT_FILE
        DELETE_OUTPUT_FILE = True   # If True, recover files from Trash

    if args.mongodb:           # -md "local", "27017", "mongodb://localhost:27017"
        global MONGODB
        MONGODB = args.mongodb

    if args.sleepsecs:          # -s 1.2
        global SLEEP_SECONDS
        SLEEP_SECONDS = args.sleepsecs  # between files created in a loop

    return None


    #### SECTION 08 - Set Static Global working constants:

def calc_from_globals() -> None:
    """This is called just once at the top of __main__ to 
    assemble values within global variablessuch as 
    * OUTPUT_PATH_PREFIX for defining output file paths.
    * api keys (secrets)
    * genai prompt text
    * WIDTHxHEIGHT and TILE_SIZE
    * watermark text
    """
    if LOG_LVL:  # specified:
        if LOG_LVL == "DEBUG" or LOG_LVL == "INFO" or LOG_LVL == "WARNING" or LOG_LVL == "ERROR" or LOG_LVL == "FAIL":
            logging.basicConfig(filename=LOGGER_FILE_PATH, level=LOG_LVL)
            print_info(f"--loglvl \"{LOG_LVL}\" in calc_from_globals().")

    user_home_path = os.path.expanduser("~")  # user home folder path "/Users/johndoe"
    global OUTPUT_PATH_PREFIX
    OUTPUT_PATH_PREFIX = user_home_path+ SLASH_CHAR + OUTPUT_FOLDER
    # Create folder if it does not exist: 
    if not os.path.exists(OUTPUT_PATH_PREFIX):
        # If it doesn't exist, create the folder:
        os.makedirs(OUTPUT_PATH_PREFIX)
        print_warning(f"--folder {OUTPUT_FOLDER} created by calc_from_globals().")

    # TODO: For art: vary size (ratio) of file to generate locally

    global WIDTHxHEIGHT
    WIDTHxHEIGHT = str(WIDTH_PIXELS)+"x"+str(HEIGHT_PIXELS)  # for "500x500" or "1024x1024"

    global TILE_SIZE
    TILE_SIZE = 50

    global GRID_WIDTH
    GRID_WIDTH = WIDTH_PIXELS // TILE_SIZE

    global GRID_HEIGHT
    GRID_HEIGHT = HEIGHT_PIXELS // TILE_SIZE

#    if WATERMARK_TEXT:     # -wm "\"Like Mondrian 2054\" Copywrite Wilson Mar 2025. ..."
#        global ADD_WATERMARK
#        ADD_WATERMARK = True   # used by watermark2png()

    # Assemble prompt text:
    # See https://stability.ai/learning-hub/stable-diffusion-3-5-prompt-guide
    global PROMPT_TEXT
    PROMPT_TEXT = (
        "Create an abstract painting in the style of Piet Mondrian "
        "featuring a grid of shapes between straight black lines "
        "dividing the canvas into rectangles and squares. "
        "Use the golden ratio (1:1.618) to arrange blocks. "
        "Fill 50% of shapes with primary colors - red, blue, and yellow - "
        "while leaving others white. Ensure a balanced composition with "
        "asymmetrical placement of colored blocks."
    )
 
    return None


#### SECTION 09 - read_env_file() to override hard-coded defaults:


def load_env_file(env_path: str) -> None:
    """Read .env file containing variables and values.
    See https://wilsonmar.github.io/python-samples/#envLoad
    See https://stackoverflow.com/questions/40216311/reading-in-environment-variables-from-an-environment-file
    """

        # TODO: drivepath(ENV_FILE_PATH)
        # TODO: open_env_file(ENV_FILE_PATH)
        # TODO: read_env_file(ENV_FILE_PATH)  # calls print_samples()
        #if DRIVE_PATH:
        #    list_files_on_removable_drive(DRIVE_PATH)
        # TODO: eject_drive(removable_drive_path)

    """
    openai_api_key = get_str_from_env_file('OPENAI_API_KEY')
    if openai_api_key == None:
        print_error("openai_api_key="+openai_api_key+" not in "+env_path)
    else:
        print_error("openai_api_key="+openai_api_key+" in "+env_path)
    """
    return None


# See https://wilsonmar.github.io/python-samples/#envFile
def open_env_file(env_file: str) -> str:
    """Return a file path obtained from .env file based on the path provided
    in env_file coming in.
    """
    # See https://wilsonmar.github.io/python-samples#run_env
    global user_home_dir_path
    #from pathlib import Path
    user_home_dir_path = str(Path.home())
       # example: /users/john_doe

    global_env_path = user_home_dir_path + "/" + env_file  # concatenate path

    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        print_trace(global_env_path+" (global_env_path) not found!")
    else:
        print_info(global_env_path+" (global_env_path) readable.")

    path = pathlib.Path(global_env_path)
    # Based on: pip3 install python-dotenv
    from dotenv import load_dotenv
       # See https://www.python-engineer.com/posts/dotenv-python/
       # See https://pypi.org/project/python-dotenv/
    load_dotenv(global_env_path)  # using load_dotenv

    # Wait until variables for print_trace are retrieved:
    #print_trace("env_file="+env_file)
    #print_trace("user_home_dir_path="+user_home_dir_path)


def get_str_from_env_file(key_in: str) -> str:
    """Return a value of string data type from OS environment or .env file
    (using pip python-dotenv)
    """
    # FIXME:
    env_var = os.environ.get(key_in)
    # print_verbose("get_str_from_env_file() key_in="+key_in+" env_var="+env_var)

    if not env_var:  # yes, defined=True, use it:
        print_warning("get_str_from_env_file() key="+key_in + " not found in OS nor .env file: " + ENV_FILE_PATH)
        return None
    else:
        # PROTIP: Display only first 5 characters of a potentially secret long string:
        if len(env_var) > 5:
            print_trace(key_in + "=\"" + str(env_var[:5]) +" (remainder removed)")
        else:
            print_trace(key_in + "=\"" + str(env_var) + "\" from .env")
        return str(env_var)


def list_files_on_removable_drive(drive_path: str) -> None:
    """List all directories and files on a removable USB volumedrive.
    where drive_path = "/Volumes/YOUR_DRIVE_NAME"
    """
    #import os
    #from pathlib import Path
    drive = Path("/Volumes/" + drive_path)
    if not drive.is_mount():   # NOT mounted:
        print_warning(f'/Volumes/Drive \"{drive_path}\" not mounted (plugged in). Ignored.')
        return
    else:
        print(f'{drive_path} is --drivepath \"DRIVE_PATH\":')

    for item in drive.iterdir():
        if item.is_dir():
            print_info(f'Directory: {item.name}')
        elif item.is_file():
            print_info(f'File: {item.name}')
    return None


#### SECTION 10 - Utility time & date functions (which can be in a python module)


def get_time() -> str:
    """ Generate the current local datetime. """
    now: datetime = dt.datetime.now()
    return f'{now:%I:%M %p (%H:%M:%S) %Y-%m-%d}'


def format_datetime_stamp(datetime_stamp_obj) -> str:
    """format from OS clock date stamp (with a time zone offset)
    using local time zone offset above.
    """
    # Set in SECTION 3 above:
    # local_time = time.localtime()
    # TZ_OFFSET = time.strftime("%z", local_time)
        # returns "-0700" for MST "America/Denver"

    if DATE_OUT_Z:  # from user preferences
        # Add using local time zone Z (Zulu) for UTC (GMT):
        date_stamp = datetime_stamp_obj.strftime("%Y%m%dT%H%M%SZ")
    else:
        # Add using local time zone offset:
        date_stamp = datetime_stamp_obj.strftime("%Y%m%dT%H%M%S")+TZ_OFFSET

    return date_stamp


def local_datetime_stamp() -> str:
    """Assemble from OS clock date stamp (with a time zone offset)
    using local time zone offset above.
    """
    # local_time = time.localtime()
    # TZ_OFFSET = time.strftime("%z", local_time)
        # returns "-0700" for MST "America/Denver"

    if DATE_OUT_Z:  # from user preferences
        # Add using local time zone Z (Zulu) for UTC (GMT):
        now = dt.datetime.now(dt.timezone.utc)
    else:
        # Add using local time zone offset:
        now = dt.datetime.now()
    return format_datetime_stamp(now)


def file_creation_datetime(path_to_file: str) -> str:
    """ Get the datetime stamp for a file, 
    falling back to when it was last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    WARNING: Use of epoch time means resolution is to the seconds (not microseconds)
    """
    if path_to_file is None:
        print_trace(f"path_to_file="+path_to_file)
    # print_trace("platform.system="+platform.system())
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:  # macOS & Linux:
        from datetime import datetime as dt
        try:
            from datetime import datetime
            creation_time = os.path.getctime(path_to_file)
            # Convert the timestamp to a human-readable datetime format:
            crea_time_obj = dt.fromtimestamp(creation_time)
            # Format the datetime to a string:
            local_tz = pytz.timezone('America/Denver') 
            localized_datetime = local_tz.localize(crea_time_obj)
            formatted_timestamp = localized_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            # print_trace(f"formatted_timestamp={formatted_timestamp}") 
            # print(f"formatted_timestamp={formatted_timestamp}")
            #return stat.st_birthtime # epoch datestamp like 1696898774.0
            return formatted_timestamp+TZ_OFFSET
        except Exception as e:
            # PROTIP: Get the 
            print_error(f"{path_to_file} AttributeError {e}")
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            stat = os.stat(path_to_file)
            # like os.stat_result(st_mode=33188, st_ino=42022053, st_dev=16777232, 
            # st_nlink=1, st_uid=501, st_gid=20, st_size=4940329, st_atime=1737270005, 
            # st_mtime=1737266324, st_ctime=1737266363) 
            return stat.st_mtime   # epoch datetime modified like 1737266324


#### SECTION 11 - Utility system information functions (which can be in a python module)

def display_memory() -> None:
    #import os, psutil  #  psutil-5.9.5
    process = psutil.Process()
    mem=process.memory_info().rss / (1024 ** 2)  # in bytes
    print_verbose(str(process)+"memory used="+str(mem)+" MiB at "+local_datetime_stamp())
    return 

def display_disk_free() -> None:
    #import os, psutil  #  psutil-5.9.5
    disk = psutil.disk_usage('/')
    free_space_gb = disk.free / (1024 * 1024 * 1024)  # = 1024 * 1024 * 1024
    print_verbose(f'disk space free={free_space_gb:.2f} GB at '+local_datetime_stamp())
    return None

def count_files_within_path(directory: str) -> int:
    """Returns the number of files after looking recursively
    within a given directory"""
    # import os
    file_count = 0
    for entry in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, entry)):
            file_count += 1
    return file_count


def get_file_size_on_disk(file_path: str) -> int:
    """Returns integer bytes from the OS for a file path """
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


def is_jupyter() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type
    except NameError:
        return False  # Probably standard Python interpreter
        

def sys_info() -> None:
    """Obtain and display system info:
    OS, RunEnv, AppP Program, Memory, Disk spaceCPU.
    """
    if not show_sys_info:   # defined among CLI arguments
        return None

    print_trace("local_datetime_stamp="+local_datetime_stamp())

    #from pathlib import Path
    # See https://wilsonmar.github.io/python-samples#run_env
    global user_home_dir_path
    user_home_dir_path = str(Path.home())
        # example: /users/john_doe
    print_trace("user_home_dir_path="+user_home_dir_path)
    # the . in .secrets tells Linux that it should be a hidden file.

    this_pgm_name = os.path.basename(os.path.normpath(sys.argv[0]))
    print_trace("this_pgm_name="+this_pgm_name)

    this_pgm_os_path = os.path.realpath(sys.argv[0])
    print_trace("this_pgm_os_path="+this_pgm_os_path)
    # Example: this_pgm_os_path=/Users/wilsonmar/github-wilsonmar/python-samples/python-samples.py

    using_jupyter = is_jupyter()
    #import os
    jupyter_parent_pid = 'JPY_PARENT_PID' in os.environ
    print_trace("Jupyter? "+str(is_jupyter)+" JPY_PARENT_PID="+str(jupyter_parent_pid))

    #last_modified_epoch = os.path.getmtime(this_pgm_os_path)
    # FEATURE: Convert unix epoch time (from 1970) to human-readable datetime:
    #import datetime as dt
    #last_modified_datetime = dt.fromtimestamp(last_modified_epoch)
        # Default like: 2021-11-20 07:59:44.412845  (with space between date & time)
    #print_trace("program_created_datetime=" + str(last_modified_datetime) +
    #    TZ_OFFSET + " = unix epoch="+str(last_modified_epoch))

    #import platform # https://docs.python.org/3/library/platform.html
    platform_system = platform.system()
       # 'Linux', 'Darwin', 'Java', 'Win32'
    print_trace("platform_system="+str(platform_system)+" (Darwin = macOS)")

    # my_os_platform=localize_blob("version")
    print_trace("my_os_version="+str(platform.release()))
    #           " = "+str(macos_version_name(my_os_version)))

    my_os_process = str(os.getpid())
    print_trace("my_os_process="+my_os_process)

        # or socket.gethostname()
    my_platform_node = platform.node()
    print_trace("my_platform_node="+my_platform_node)

    my_os_uname = str(os.uname())
    print_trace("my_os_uname="+my_os_uname)
        # MacOS version=%s 10.14.6 # posix.uname_result(sysname='Darwin',
        # nodename='NYC-192850-C02Z70CMLVDT', release='18.7.0', version='Darwin
        # Kernel Version 18.7.0: Thu Jan 23 06:52:12 PST 2020;
        # root:xnu-4903.278.25~1/RELEASE_X86_64', machine='x86_64')

    # Permissions?
    cmd = "ioreg -c IOPlatformExpertDevice -d 2 | awk -F\\\" '/IOPlatformSerialNumber/{print $(NF-1)}'"
    my_mac_serial_number = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
       # Alternative: ioreg -c IOPlatformExpertDevice -d 2 | awk -F\\\" '/IOPlatformSerialNumber/{print $(NF-1)}'
    print_trace("my_mac_serial_number="+my_mac_serial_number)
       # Example: DFJXAJ09M1

    #import uuid
    mac = uuid.getnode()
    #import re
    mac_address = ':'.join(re.findall('..', '%012x' % mac))
    print_trace("mac_address=" + mac_address)

    #import socket
    hostname = socket.gethostname()
    # sudo: Allow Python to find devices on local networks?
    ip_addresses_list = socket.gethostbyname_ex(hostname)[2]
    ip_addresses_str = ', '.join(map(str, ip_addresses_list))
    print_trace("hostname="+hostname+" ip_addresses="+ip_addresses_str)
    # for ip in ip_addresses: print(ip)

    display_disk_free()
    display_memory()
    # list_disk_space_by_device()
    
    return None


def list_disk_space_by_device() -> None:
    """ List each physical drive (storage device hardware), such as an internal hard disk drive (HDD) or solid-state drive (SSD)
    """
    print_heading("Logical Disk Device Partitions (sdiskpart):\n"+
        "/mountpoint Drive           /device        fstype  opts (options)\n"+
        "   Total size:    Used:       Free: ")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(partition.mountpoint.ljust(28) +
            partition.device.ljust(15) +
            partition.fstype.ljust(8) +
            partition.opts)
        if partition.mountpoint.startswith('/Volumes/'):
            # Check if the volume is removable
            cmd = f"diskutil info {partition.device}"
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            if "Removable Media: Yes" in output:
                removable_volumes.append(partition.mountpoint)
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print("   "+f"{usage.total / (1024 * 1024 * 1024):.2f} GB".rjust(10) +
                f"{usage.used / (1024 * 1024 * 1024):.2f} GB".rjust(12) +
                f"{usage.free / (1024 * 1024 * 1024):.2f} GB".rjust(12) )
        except PermissionError:
            print_error("Permission denied to access usage information")

        print()
        return None


def list_macos_volumes() -> None:
    """ Like Bash CLI: diskutil list
    STATUS: NOT WORKING
    volumes_path = '/Volumes'
    volumes = os.listdir(volumes_path)
    """
    print("*** Drive Volumes:")
    removable_volumes = []
    import psutil
    partitions = psutil.disk_partitions(all=True)

    for partition in partitions:
        if partition.mountpoint.startswith('/Volumes/'):
            # Check if the volume is removable
            cmd = f"diskutil info {partition.device}"
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            if "Removable Media: Yes" in output:
                removable_volumes.append(partition.mountpoint)

    for volume in removable_volumes:
        print(f"Removable volume: {volume}")

        volume_path = os.path.join(volumes_path, volume)
        if os.path.ismount(volume_path):
            print(f"- {volume}")
    return None


def list_files_by_mountpoint() -> None:
    """ List files within get all disk partitions
    """
    #import os
    #import psutil
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
    """TODO: Read content (text) from a file_name on a removable drive on macOS. 
    Example: -d "/Volumes/DriveName"
    """
    write_file_to_removable_drive(drive_path, env_file, content)

    # Find the user's $HOME path:
    global user_home_dir_path
    user_home_dir_path = str(Path.home())
       # example: /users/john_doe
    global_env_path = user_home_dir_path + "/" + env_file  # concatenate path

    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        print_error("global_env_path "+global_env_path+" not found!")
    else:
        print_info("global_env_path "+global_env_path+" is readable.")

    path = pathlib.Path(global_env_path)
    # Based on: pip3 install python-dotenv
    # from dotenv import load_dotenv
       # See https://www.python-engineer.com/posts/dotenv-python/
       # See https://pypi.org/project/python-dotenv/
    load_dotenv(global_env_path)  # using load_dotenv

    # Wait until variables for print_trace are retrieved:
    #print_trace("env_file="+env_file)
    #print_trace("user_home_dir_path="+user_home_dir_path)

    # After pip install envcload
    # from envcloak import load_encrypted_env
    load_encrypted_env('.env.enc', key_file='mykey.key').to_os_env()
        # Now os.environ contains the decrypted variables

    return global_env_path


def write_file_to_removable_drive(drive_path: str, file_name: str, content: str) -> None:
    """
    Write content (text) to a file_name on a removable drive on macOS.
    :param drive_path: The path to the removable drive
    See https://www.kingston.com/en/blog/personal-storage/using-usb-drive-on-mac
    """
    # Verify that the drive is mounted and the path exists:
    if not os.path.exists(drive_path):
        # mount point = drive_path = '/Volumes/YourDriveName'
        print(f"Drive path {drive_path} not found. Please check if it's properly connected.")
        raise FileNotFoundError(f"The drive path {drive_path} does not exist.")
        # Perhaps permission error?
        list_macos_volumes()
        exit(9)

    try:
        # Write the content to the file
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File '{file_name}' has been successfully written to {drive_path}")
    except PermissionError:
        print(f"Permission denied. Unable to write to {drive_path}")
    except IOError as e:
        print(f"An error occurred while writing the file: {e}")


def eject_drive(drive_path: str) -> None:
    """Safely eject removeable drive after use, where
    drive_path = '/Volumes/YourDriveName'
    """
    try:
        # import subprocess
        subprocess.run(["diskutil", "eject", drive_path], check=True)
        print(f"Successfully ejected {drive_path}")
    except subprocess.CalledProcessError:
        print(f"Failed to eject {drive_path}")
    return None


#### SECTION 12 - utility cryptopgraphic functions:


def hash_file_sha256(filename: str) -> str:
    # A hash is a fixed length one way string from input data. Change of even one bit would change the hash.
    # A hash cannot be converted back to the input data (unlike encryption).
    # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python

    #import hashlib
    sha256_hash = hashlib.sha256()
    # There are also md5(), sha224(), sha384(), sha512()
    BUF_SIZE = 65536
    with open(filename, "rb") as f: # read entire file as bytes
        # Read and update hash string value in blocks of 64K:
        for byte_block in iter(lambda: f.read(BUF_SIZE),b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def encrypt_symmetrically(source_file_path: str, cyphertext_file_path: str) -> str:
    """Encrypt a plaintext file to cyphertext using Fernet symmetric encryption algorithm
    after reading entire file into memory.
    Based on https://www.educative.io/answers/how-to-create-file-encryption-decryption-program-using-python
    """
    # pip install cryptography
    # from cryptography.fernet import Fernet
    
    # Generate a 32-byte random encryption key like J64ZHFpCWFlS9zT7y5zxuQN1Gb09y7cucne_EhuWyDM=
    if not ENCRYPTION_KEY:   # global variable
        ENCRYPTION_KEY = Fernet.generate_key()
    # Create a Fernet object instance from the encryption key:
    fernet_obj = Fernet(ENCRYPTION_KEY)

    # Read file contents:
    with open(source_file_path, 'rb') as file:
        file_contents = file.read()
    # WARNING: Measure file size because file.read() reads the wholefile into memory.
    file_bytes = len(file_contents)

    # Encrypt file contents:
    encrypted_contents = fernet_obj.encrypt(file_contents)
    with open(cyphertext_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_contents)
    # Measure encrypted file size:
    encrypted_file_bytes = len(encrypted_file)
    
    # import io
    key_out = io.BytesIO()
    # WARNING: For better security, we do not output the key out to a file.
    # with open('filekey.key', 'wb') as key_file:
    #    key_out.write(key)

    print_info("From ", file_bytes, "bytes to ", encrypted_file_bytes, "bytes.")

    return key_out


# FIXME:
# @functools.cache  # See https://www.datacamp.com/tutorial/python-cache-introduction
def get_openai_parms(app_id: str, account_name: str) -> str:
    api_key = get_api_key(app_id, account_name)
    return api_key


def shorten_url(long_url: str) -> str:
    base_url = 'http://tinyurl.com/api-create.php?url='
    response = requests.get(base_url + long_url)
    print_trace(f"shorten_url() {response.text}")
    return response.text


def save_url_to_file(filepath: str, url: str) -> None:
    """ Create a shareable file that, when clicked, opens a window in the default browser,
    showing the web page at the URL specified in the file.
    filepath = "/Users/johndoe/Desktop/whatever/example.url"
    url such as "https://www.example.com"
    USAGE: save_url_to_file(url, filename) 
    """
    print_verbose("save_url_to_file() filepath="+filepath+", url="+url)
    content = "[InternetShortcut]\nURL="+url
    try:
        with open(filepath, "w") as file:
            file.write(content)
        return True
    except Exception as e:
        print_error("save_url_to_file() "+filepath+" exception: "+str(e))
        return False


def get_api_key(app_id: str, account_name: str) -> str:
    """Get API key from macOS Keyring file or .env file (depending on what's available)
    referencing global variables keyring_service_name & keyring_account_name
    USAGE: api_key = get_api_key("anthropic","johndoe")
    """
    print_verbose("get_api_key() app_id="+app_id+", account_name="+account_name)

    if is_macos():
        # Pull sd_api_key as password from macOS Keyring file (and other password manager):
        try:
            #import keyring
            api_key = keyring.get_password(app_id,account_name)
            if api_key:
                print_trace("get_api_key() len(api_key)="+str(len(api_key)))
                return api_key
            else:
                # FIXME: sd_api_key=None
                print_fail("get_api_key() api_key=None")
                return None
        except Exception as e:
            print_error("get_api_key() str({e})")
            return None
    #else: Windows, Linux, etc.

    return None


#### SECTION 13 - utility output functions:


# def setup_logger(log_file=LOGGER_FILE_PATH, console_level=logging.INFO, file_level=logging.DEBUG):
   # See https://docs.python.org/3/library/logging.html#module-logging
# def log_event(logger, event_type, message, level='info'):

def set_output_file_path(i: int, api_id: str, filetype: str) -> str:
    """Generate the full file path for the generated image like this:
    /Users/johndoe/Desktop/mondrian-gen-20250119T192300-0700-1-openai-qr.png
    Using :SLASH_CHAR ("/") from global variable depending on OS platform
    OUTPUT_PATH_PREFIX contains:
        /Users/johndoe = from os.path.expanduser("~")
        /Desktop :OUTPUT_FOLDER =  from global variable
    /mondrian-gen :PROGRAM_NAME =  from global variable
    -Test001 :RUNID = from global variable

    -20250119T192300 :datetime_stamp generated by this function
    -0700  :TZ_OFFSET global variable included in datetime_stamp

    -1  :i = incrementor from argument
    -dalle2 or -pgm (if local programmatic code) :api_id = from argument 
    -art or -qr  :filetype = from argument
    .png
    """
    print_verbose("set_output_file_path() api_id="+api_id+" i="+str(i)+" of "+str(FILES_TO_GEN))
    # WARNING: NOT from input file date's own timestamp:
    # OUTPUT_PATH_PREFIX set by calc_from_globals()
    print_verbose("set_output_file_path() OUTPUT_PATH_PREFIX="+OUTPUT_PATH_PREFIX)

    datetime_stamp = local_datetime_stamp()
    full_file_path = OUTPUT_PATH_PREFIX+SLASH_CHAR+PROGRAM_NAME \
        +"-"+RUNID+"-"+datetime_stamp+"-"+str(i)+"-"+api_id+"-"+filetype
    print_trace("set_output_file_path()="+full_file_path+" len="+str(len(full_file_path)))
    # /Users/johndoe/Desktop/mondrian-gen-t1-20250126T210748-0700-
    # /Users/johndoe/Desktop/mondrian-gen-t1-20250126T210748-0700-1-dalle2-art.png-dalle2-qr.png
    return full_file_path


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
    password = get_api_key("gmail",EMAIL_FROM)  # loadtesters
    if not password:
        print_fail("send_smtp() does not have password needed.")
        return False

    recipients = EMAIL_TO  # Recipients as a list: "[ 1@example.com, 2@example.com ]"
    if recipients is None:   # Not a list
        print_fail("--emailfrom does not have recipients for send_smtp().")
        return False
    
    #import smtplib
    #from email.mime.text import MIMEText
    body = f"From send_smtp() using Gmail SMTP."
        # TODO: Add log lines captured into log database during run.
    msg = MIMEText(body)
    msg['From'] = EMAIL_FROM
    msg['Subject'] = f"From {PROGRAM_NAME} for {RUNID}"

    for index, recipient in enumerate(recipients.split(",")):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(EMAIL_FROM, password)
            msg['To'] = recipient
            smtp_server.sendmail(EMAIL_FROM, recipient, msg.as_string())
            print_verbose(f"send_smtp() emailed {index + 1} to "+recipient)
    # FIXME: smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted. 
    # For more information, go to\n5.7.8  https://support.google.com/mail/?p=BadCredentials 
    # 98e67ed59e1d1-2f7ffa76d1csm4313179a91.32 - gsmtp')
    return True


def gen_qrcode(url: str,qrcode_file_path: str) -> bool:
    """Generate a QR code from a URL and save it to a file.
    See https://www.geeksforgeeks.org/python-generate-qr-code/
    See https://python.plainenglish.io/how-i-generate-qr-codes-with-python-in-under-30-seconds-77f627e8fe63
    """
    if not GEN_QR_CODE:  # Bypass
        return False

    print_verbose("gen_qrcode() url="+url+" qrcode_file_path="+qrcode_file_path)
    try:
        #import qrcode  with higher level of error correction
        qr = qrcode.QRCode(version=2, 
            error_correction=qrcode.constants.ERROR_CORRECT_H, 
            box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qrcode_file_path)
        print_verbose("gen_qrcode() output to "+qrcode_file_path)
        return True
    except Exception as e:
        print_error("gen_qrcode() error: "+str(e)+" for "+url)
        return False


# Test if a variable is None:
def is_none(variable):
    return variable is None

def is_only_numbers(variable):
    return str(variable).isdigit()

def insert_mongodb(doc_in: object) -> str:
    """Call MongoDB to store a document into a collection into aNoSQL database
    """
    print_verbose("insert_mongodb() str(document)="+str(doc_in)) # str(len(doc_in)))
    
    # from pymongo import MongoClient
    # client = MongoClient('localhost', 27017)
    # Connect to MongoDB (assuming it's running on localhost):
    if is_none(MONGODB):
        return None
    elif MONGODB == "local":
        MONGODB_URL = f"mongodb://localhost:27017/"
    elif is_only_numbers(MONGODB):
        MONGODB_URL = f"mongodb://localhost:{MONGODB}/"
    else:
        MONGODB_URL = MONGODB  # host URL pecified in parm.
 
    MONGODB_NAME = "mondrian"
    # Define a NoSQL collection (like a table in relational databases):
    MONGODB_COLLECTION = "runs"
 
    client = MongoClient(MONGODB_URL)
    db = client[MONGODB_NAME]
    collection = db[MONGODB_COLLECTION]

    # Create a document to insert:
    #doc_in = {
    #    "interests": ["programming", "data science", "machine learning"],
    #    ...
    #}
    try:
        # Insert the document into the collection:
        result = collection.insert_one(doc_in)
        print(f"Inserted document ID: {result.inserted_id}")
        print_trace("insert_mongodb() collection \""+MONGODB_COLLECTION+\
            "\" inserted_id="+result.inserted_id)
        return result.inserted_id

    except Exception as e:
        print_error(f"insert_mongodb() Exception: {e}")
        return False


def upload_to_ipfs(file_path: str) -> str:
    """Upload a file to IPFS using QuickNode or TatumAPI.
    See https://www.quicknode.com/docs
    See https://docs.tatum.io/reference/storeipfs
    See https://techieteee.hashnode.dev/how-to-build-a-decentralized-data-pipeline-with-quicknode-ipfs-and-python
    """
    # import requests, json  # (not use framework)
    # This endpoint version needs to be updated: https://www.quicknode.com/docs

    # global quicknode_api_key
    quicknode_api_key = get_api_key("quicknode", "johndoe")
    print_verbose("-fromitem quicknode api_key length="+len(str(quicknode_api_key)))

    endpoint = "https://ipfs.quicknode.com/api/v0/add"
    files = {"file": open(file_path, "rb")}
    headers = {"Authorization": f"Bearer {quicknode_api_key}"}
    
    func_start_timer = time.perf_counter()
    response_obj = requests.post(endpoint, files=files, headers=headers)
    func_end_timer = time.perf_counter()
    func_duration = func_end_timer - func_start_timer

    data = json.loads(response_obj.text)
    cid = data["Hash"]

    print_trace("upload_to_ipfs() ="+cid)

    return cid


#### SECTION 14 - custom programmatic app functions:


# Based on https://www.perplexity.ai/search/write-a-python-program-to-crea-nGRjpy0dQs6xVy9jh4k.3A#0

def generate_mondrian() -> list:
    """Called by Create a grid and adds random horizontal and vertical lines
    based on WIDTH_PIXELS, HEIGHT_PIXELS, TILE_SIZE
    """
    # Initialize grid:
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Generate lines
    # TODO: Use golden ratios
    for _ in range(random.randint(6, 15)):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        direction = random.choice(['horizontal', 'vertical'])

        if direction == 'horizontal':
            for i in range(GRID_WIDTH):
                grid[y][i] = 1
        else:
            for i in range(GRID_HEIGHT):
                grid[i][x] = 1

    # Fill areas with primary colors selected randomly, using a flood fill algorithm:
    for _ in range(random.randint(3, 8)):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        color = random.randint(2, 4)
        mondrian_flood_fill(grid, x, y, 0, color)

    return grid


def mondrian_flood_fill(grid, x: int, y: int, old_color: int, new_color: int) -> None:
    """Fill grid with colors:
    """
    if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
        return
    if grid[y][x] != old_color:
        return

    grid[y][x] = new_color
    # Call recursively:
    mondrian_flood_fill(grid, x+1, y, old_color, new_color)
    mondrian_flood_fill(grid, x-1, y, old_color, new_color)
    mondrian_flood_fill(grid, x, y+1, old_color, new_color)
    mondrian_flood_fill(grid, x, y-1, old_color, new_color)
    return None


def draw_mondrian(grid: list, filename: str) -> None:
    """Use the Cairo graphics library to render the grid as an image2.
    This references global variables WIDTH_PIXELS, HEIGHT_PIXELS.
    """
    print_trace("draw_mondrian() grid="+str(grid)+"\nfilename="+filename)
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH_PIXELS, HEIGHT_PIXELS)
    ctx = cairo.Context(surface)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = COLORS[grid[y][x]]
            ctx.set_source_rgb(*color)
            ctx.rectangle(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            ctx.fill()

    surface.write_to_png(filename)
    return


def gen_one_file(file_path: str) -> bool:
    """Generate image and draw to a file.
    """
    func_start_timer = time.perf_counter()
    # Generate Mondrian-style art in memory:
    mondrian_grid = generate_mondrian()
    func_end_timer = time.perf_counter()
    func_duration = func_end_timer - func_start_timer

    result = draw_mondrian(mondrian_grid, file_path )
    if not result:
        print_error("gen_one_file() draw_mondrian() failed.")
        return False
    else:
        print_trace(f"gen_one_file() func_duration={func_duration:.5f} seconds")
        return True


#### SECTION 15 - DALL-E Generative AI API functions:


def gen_dalle2_file(gened_file_path: str) -> str:
    """Generate image using DALL-E Generative AI API calls to OpenAI servers.
    """
    #openai_engine_id = get_openai_engine_id(openai_api_key)
    openai_engine_id="dall-e-2"   #prompt_model="dall-e-2" # for 500x500 FREE
    # openai_engine_id="dall-e-3" #prompt_model="dall-e-3" # for 1024x1024 licen$ed
    WIDTHxHEIGHT = "500x500"
    # TODO: Use global variable: See https://beta.dreamstudio.ai/prompt-guide
    #.  size=WIDTHxHEIGHT = "512x512"
      # quality="hd” costs more, takes more time to generate than "standard".
       # or "vivid" for advanced control of the generation.
    print_verbose("gen_dalle2_file() model="+openai_engine_id+\
        " WIDTHxHEIGHT="+WIDTHxHEIGHT+\
        " len(PROMPT_TEXT)="+str(len(PROMPT_TEXT)))

    openai_api_key = get_api_key("openai","johndoe")
    if openai_api_key:
        print_trace("gen_dalle2_file() len(openai_api_key)="+str(len(openai_api_key)))
    else:
        print_error("gen_dalle2_file() does not have openai_api_key.")
        return None

    func_start_timer = time.perf_counter()
    # See https://help.openai.com/en/articles/8555480-dall-e-3-api
    # See https://platform.openai.com/docs/guides/images?context=python
    client = OpenAI()
    client.api_key = openai_api_key
    response = client.images.generate(
        model=openai_engine_id,
        prompt=PROMPT_TEXT,
        n=1,
        style="natural",
        quality="standard",
        size=WIDTHxHEIGHT
    )
    print_info("response.data[0].url"+response.data[0].url)
       # Example: https://oaidalleapiprodscus.blob.core.windows.net/private/org-4...
    response = requests.get(response.data[0].url)
    if response.status_code == 200:
        with open(gened_file_path, 'wb') as file:
            file.write(response.content)

        func_end_timer = time.perf_counter()
        func_duration = func_end_timer - func_start_timer
        print_trace(f"gen_dalle2_file() func_duration={func_duration:.5f} seconds")

        if LOG_LVL:
            file_bytes = get_file_size_on_disk(gened_file_path)  # type = number
            print(f"*** LOG: {gened_file_path},{file_bytes},{file_creation_datetime(gened_file_path)},{func_duration:.5f}")
        else:
            file_bytes = get_file_size_on_disk(watermarked_file_path)  # type = number
            print(f"*** LOG: {watermarked_file_path},{file_bytes},{func_duration:.5f}")
    else:
        print_error('gen_dalle2_file() fail with HTTP status '+response.status_code)
        return None

    return gened_file_path


def gen_qwen_file(gened_file_path: str) -> str:
    """Generate image using Qwen Generative AI API calls to Alibaba servers in China.
    Released 01/25/2025.See https://www.youtube.com/watch?v=he9xAr_CKMQ
    """
    qwen_engine_id="qwen-max-2025-01-25"
    # qwen_engine_id="dall-e-3" #prompt_model="dall-e-3" # for 1024x1024 licen$ed
    WIDTHxHEIGHT = "500x500"
    print_verbose("gen_qwen_file() model="+qwen_engine_id+\
        " WIDTHxHEIGHT="+WIDTHxHEIGHT+\
        " len(PROMPT_TEXT)="+str(len(PROMPT_TEXT)))

    qwen_api_key = get_api_key("qwen","johndoe")
    if qwen_api_key:
        print_trace("gen_qwen_file() len(qwen_api_key)="+str(len(qwen_api_key)))
    else:
        print_error("gen_qwen_file() does not have qwen_api_key.")
        return None

    func_start_timer = time.perf_counter()
    # See https://help.qwen.com/en/articles/8555480-dall-e-3-api
    # See https://platform.qwen.com/docs/guides/images?context=python
    client = qwen()
    client.api_key = qwen_api_key
    response = client.chat.completions.create(
        model=qwen_engine_id,
        messages=[
            {"role": "system", "content": 'You are a helpful assistant.'},
            {"role": "user", "content": PROMPT_TEXT}
        ]
    )
    print_info("gen_qwen_file() url="+response.data[0].url)
       # Example: https://oaiqwenapiprodscus.blob.core.windows.net/private/org-4...
    # print(completion.choices[0].message.content)
    response = requests.get(response.data[0].url)
    if response.status_code == 200:
        with open(gened_file_path, 'wb') as file:
            file.write(response.content)

        func_end_timer = time.perf_counter()
        func_duration = func_end_timer - func_start_timer
        print_trace(f"gen_qwen_file() func_duration={func_duration:.5f} seconds")

        if LOG_LVL:
            file_bytes = get_file_size_on_disk(gened_file_path)  # type = number
            print(f"*** LOG: {gened_file_path},{file_bytes},{file_creation_datetime(gened_file_path)},{func_duration:.5f}")

            file_bytes = get_file_size_on_disk(watermarked_file_path)  # type = number
            print(f"*** LOG: {watermarked_file_path},{file_bytes},{func_duration:.5f}")
    else:
        print_error('Download file fail with HTTP status '+response.status_code)
        return None

    return gened_file_path


def get_stability_engine_id(api_key: str) -> str:
    """Return the id to the Stability AI model/engine id for using Stable Diffusion.
    """
    stability_engine_id = "stable-diffusion-xl-1024-v1-0"
    # stability_engine_id = "stable-diffusion-v1-6"

    if not stability_engine_id:  # global variable
        # import os, requests, config
        url = f"https://api.stability.ai/v1/engines/list"
        response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
        print_verbose("get_stability_engine_id() response.text="+response.text)
            # [{'description': 'Stability-AI Stable Diffusion XL v1.0', \
            #   'id': 'stable-diffusion-xl-1024-v1-0', 'name': 'Stable Diffusion XL v1.0', \
            #   'type': 'PICTURE'}, \
            #  {'description': 'Stability-AI Stable Diffusion v1.6', \
            #   'id': 'stable-diffusion-v1-6', 'name': 'Stable Diffusion v1.6', \
            #   'type': 'PICTURE'}] 
    
    # TODO: Pick an engine to use based on some heuristic.
    # FIXME: Extract 'id' values using a list comprehension
    #id_values = [item['id'] for item in response.text)]
    #print_info("get_stability_engine_id() ids="+str(id_values))

    return stability_engine_id


def gen_stablediffusion_file(prompt: str) -> str:
    """Based on global variables PROMPT_TEXT, WIDTH_PIXELS and HEIGHT_PIXELS,
    generate an image using Stable Diffusion API calls to Stability AI servers.
    # Stable Diffusion shines at precise control and customization, or specific artistic directions
    # for professional use cases like painting or illustration.
    # It generates realistic images, like those captured by a camera or painted by a professional artist.
    # Read about Limitations at https://en.wikipedia.org/wiki/Stable_Diffusion
    # See https://stable-diffusion-art.com/beginners-guide/
    # https://python.plainenglish.io/how-to-use-new-stable-diffusion-xl-api-from-stability-ai-b6f9b0bf0b91?gi=6b0b27ee1929
    # https://faun.pub/stable-diffusion-enabling-api-and-how-to-run-it-a-step-by-step-guide-7ebd63813c22?gi=c86ebdc74d67
    # https://python.plainenglish.io/how-to-use-new-stable-diffusion-xl-api-from-stability-ai-b6f9b0bf0b91?gi=6b0b27ee1929
    # https://platform.stability.ai/rest-api#tag/v1engines/operation/listEngines
    """
    # stability_engine_id = get_stability_engine_id(stability_api_key)
    stability_engine_id = "stable-diffusion-xl-1024-v1-0"
    # stability_engine_id = "stable-diffusion-v1-6

    # Hard coded to ensure HEIGHT is a multiple of 64:
    # if HEIGHT_PIXELS % 64 != 0:
    # Allowed dimensions for stability_engine_id = "stable-diffusion-xl-1024-v1-0" are:
    # 1024x1024, 1152x896, 1216x832, 1344x768, 1536x640, 640x1536, 768x1344, 832x1216, 896x1152
       # https://picsum.photos/896/1152
    HEIGHT_PIXELS = 1024
    WIDTH_PIXELS = 1024

    print_verbose("gen_stablediffusion_file() WIDTH="+str(WIDTH_PIXELS)+\
        " HEIGHT="+str(HEIGHT_PIXELS)+ \
        " len(PROMPT_TEXT)="+str(len(PROMPT_TEXT)))

    stability_api_key = get_api_key("stability","johndoe")
    
    url = "https://api.stability.ai/v1/generation/" + stability_engine_id + "/text-to-image"    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {stability_api_key}"
    }
    
    # prompt = "A serene landscape with mountains and a lake at sunset"
    payload = {
        "text_prompts": [{"text": PROMPT_TEXT}],
        "cfg_scale": 7,
        "clip_guidance_preset": 'FAST_BLUE',
        "height": HEIGHT_PIXELS,
        "width": WIDTH_PIXELS,
        "samples": 1,
        "steps": 30,
    }
    # Experiment is needed to get the best "steps" value for denoising.
    # More than 50 steps may be needed for more complex prompts and landscape images.
    
    func_start_timer = time.perf_counter()
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        #image_data = base64.b64decode(data["artifacts"][0]["base64"])
        #image = Image.open(io.BytesIO(image_data))
        #image.save("generated_image.png")
        for i, image in enumerate(data["artifacts"]):
            file_path = set_output_file_path(i,"stability","art.png")
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(image["base64"]))
        print("gen_stability_image() Image generated successfully!")
    else:
        print(f"gen_stability_image() Error: {response.status_code}")
        # FIXME: Error: 400 {"id":"e5628c21ac5e7b24231b95df44ce8f45","message":"height and width must be specified in increments of 64","name":"invalid_height_or_width"}
        print(response.text)
        return False

    func_end_timer = time.perf_counter()
    func_duration = func_end_timer - func_start_timer
    print_trace(f"gen_stability_image() func_duration={func_duration:.5f} seconds")

    return False


def gen_claude_file(prompt: str) -> str:
    """Call Anthropic API to generate an image.
    : PROMPT_TEXT  from global variables
    : WIDTHxHEIGHT from global variables
    generate an image using Anthropic API calls to Anthropic servers.
    See https://docs.anthropic.com/en/docs/build-with-claude/vision
    (Claude can also run within Amazon Bedrock and Google Vertex AI)
    """
    global claude_api_key
    if not claude_api_key:
        claude_api_key = get_api_key("anthropic","johndoe")

    # import anthropic
    try:
        client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=claude_api_key,
        )
        client.models.list(limit=20)  # QUESTION: What is the limit?
            # See https://docs.anthropic.com/en/docs/build-with-claude/models
        global claude_engine_id
        if not claude_engine_id:
            claude_engine_id = "claude-3-5-sonnet-20240620"
    except Exception as e:
        # PROTIP: Get the 
        print_error(f"gen_claude_file() {e}")

    # QUESTION: What are max_tokens and size?
    try:
        image_obj = client.images.create(
            model=claude_engine_id,
            prompt=PROMPT_TEXT,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "Hello, Claude"}
            ],
            size=WIDTHxHEIGHT
        )
        out_url = image_obj.url
    except Exception as e:
        # PROTIP: Get the 
        print_error(f"gen_claude_file() {e}")
        out_url = None

    print_verbose("gen_claude_file() url="+image_obj.url)
    return out_url


#### SECTION 16 - Post-generation processing


def add_watermark2png(input_image: str, output_image: str, watermark_text: str) -> str:
    """Add watermark to PNG image.
    """
    # See https://www.geeksforgeeks.org/python-pillow-creating-a-watermark/
    # Alt: cv2 (OpenCV), Filetools (China), pythonwatermark
         # see https://www.youtube.com/watch?v=Yu8z0Lg53zk

    print_verbose("add_watermark2png() input_image=\n"+input_image+ \
        " output_image=\n"+output_image+"\nwatermark_text="+watermark_text)

    try:
        # from PIL import Image, ImageDraw, ImageFont
        # Open the original image
        image = Image.open(input_image)

        # Create a copy of the image
        watermarked = image.copy()

        # Create a draw object
        draw = ImageDraw.Draw(watermarked)

        # Choose a font and size
        font = ImageFont.truetype("Arial.ttf", 36)

        # Get image size
        width, height = image.size

        # Calculate text size FIXME: AttributeError: 'ImageDraw' object has no attribute 'textsize'
        text_width, text_height = draw.textsize(watermark_text, font)

        # Calculate text position (bottom right corner)
        margin = 10
        x = width - text_width - margin
        y = height - text_height - margin

        # Add the watermark text
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

        # Save the watermarked image
        watermarked.save(output_image, "PNG")

    except Exception as e:
        print_error(f"add_watermark2png() {e}")
        out_url = None

    return out_url


def mint_nft(file_path_in: str, desc: str, env: str, email: str, chain: str) -> str:
    # See https://bomonike.github.io/nft
    # See https://docs.crossmint.com/api-reference/minting/nfts/mint-nft
    url = f"https://{env}.crossmint.com/api/2022-06-09/collections/default/nfts"
    api_key = get_api_key("crossmint","prod-ntfs")  # In Cloud Keychain
        # See https://www.crossmint.com/console/projects/apiKeys
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key
    }
    recipient_address = f"email:{email}:{chain}"
    payload = {
        "recipient": recipient_address,
        "metadata": {
            "name": "Crossmint Test NFT",
            "image": file_path_in,
            "description": desc
        }
    }
    print_verbose("mint_nft() env="+env+", chain="+chain+", desc="+desc)
    try:
        func_start_timer = time.perf_counter()
        #import requests, json
        response = requests.post(url, headers=headers, json=payload)
            # FIXME: Error: 403 Client Error: Forbidden for url: https://staging.crossmint.com/api/2022-06-09/collections/default/nfts 

        response.raise_for_status() # Raises an HTTPError for bad responses
        print(response.json())
            # {
            #     "actionId": "6410b5a7-f6f8-4776-9480-13ef83389808",
            #     "onChain": {
            #         "status": "pending",
            #         "chain": "solana"
            #     },
            #     "id": "6410b5a7-f6f8-4776-9480-13ef83389808"
            # }
        # From the response Extract the CID to the NFT
        # Parse the JSON string into a Python dictionary
        data = json.loads(response.json())        
        id_value = data["id"]  # Extract the "id" value.

        func_end_timer = time.perf_counter()
        func_duration = func_end_timer - func_start_timer
        print_trace(f"mint_nft() CID="+id_value+" func_duration={func_duration:.5f} seconds")
        return id_value
    except requests.exceptions.RequestException as err:
        print_error(f"mint_nft() Error: {err}")
        return None


#### SECTION 17 - End-of-Run summary functions:


def print_wall_times() -> None:
    """Prints All the timings together for consistency of output:
    """
    #print_heading("Wall times (hh:mm:sec.microsecs):")

    # For wall time of std imports:
    std_elapsed_wall_time = std_stop_datetimestamp -  std_strt_datetimestamp
    print_verbose("for import of Python standard libraries: "+ \
        str(std_elapsed_wall_time))

    # For wall time of xpt imports:
    xpt_elapsed_wall_time = xpt_stop_datetimestamp -  xpt_strt_datetimestamp
    print_verbose("for import of Python external libraries: "+ \
        str(xpt_elapsed_wall_time))

    pgm_stop_datetimestamp = dt.datetime.now()
    pgm_elapsed_wall_time = pgm_stop_datetimestamp -  pgm_strt_datetimestamp
    print_verbose("for whole program run: "+ \
        str(pgm_elapsed_wall_time))  # like 0:00:00.317434 Days:Hours:Mins:Secs.

    pgm_stop_perftimestamp = time.perf_counter()
    # print(str(pgm_stop_perftimestamp)+" seconds.microseconds perf time.")

    return


def log_file_gened() -> None:
    """TODO: LOG_LVL()
    """
    # Output to a PNG file:
    if LOG_LVL:
        file_create_stamp = file_creation_datetime(gened_file_path)
        file_bytes = get_file_size_on_disk(gened_file_path)  # type = number
        print(f"*** LOG: {gened_file_path},{file_bytes},{file_create_datetime},{func_duration:.5f}")
            # /Users/johndoe/Downloads/mondrian-gen-20250105T061101-0700-3.png,1912


def show_summary(in_seq: int) -> None:
    """Print summary count of files processed and the time to do them.
    """
    if SHOW_SUMMARY_COUNTS:
        pgm_stop_datetimestamp = dt.datetime.now()
        pgm_elapsed_wall_time = pgm_stop_datetimestamp - pgm_strt_datetimestamp

        if in_seq == 1:
            print_info(f"SUMMARY: 1 artpiece gen'd"
                f" during {str(pgm_elapsed_wall_time)} Days:Hours:Mins.Secs.")
                    # like  0:00:00.989131
        else:
            print_info(f"SUMMARY: {in_seq} artpieces gen'd"
                f" during {str(pgm_elapsed_wall_time)} Days:Hours:Mins.Secs")

    # TODO: Write wall times to log for longer-term analytics
    return None


#### SECTION 18 - Main calling function:

if __name__ == "__main__":
# TODO: Test Run this program different parameters by loading different env files.
    """
    Referencing global variables: stability_api_key
    """
    # After set_hard_coded_defaults()
    # TODO: load_env_file("???")  # read_env_file(ENV_FILE_PATH)
    read_cmd_args()  # override command line parameters at run time.
    calc_from_globals()
    sys_info()

    artpiece_num = 0
    while True:  # loop forever
        artpiece_num += 1
        artpiece_start_timer = time.perf_counter()

        # Generate text-to-image using only one method at a time (for easier post-processing):
        if ai_svc == "dalle2":    # Using text-to-image OpenAI's DALL-E service:
            gened_file_path = set_output_file_path(artpiece_num,"dalle2","art.png")
            result = gen_dalle2_file(gened_file_path)
        elif ai_svc == "qwen":
            gened_file_path = set_output_file_path(artpiece_num,"qwen","art.png")
            result = gen_qwen_file(gened_file_path)
        elif ai_svc == "stability":
            gened_file_path = set_output_file_path(artpiece_num,"stab","art.png")
            result = gen_stablediffusion_file(gened_file_path)
        elif ai_svc == "anthropic":
            gened_file_path = set_output_file_path(artpiece_num,"stab","art.png")
            result = gen_claude_file(gened_file_path)
        # TODO: Add "sora"
        # TODO: Add DeepSeek 384x384 Janus from HuggingFace "janus" # https://api-docs.deepseek.com
        # TODO: Add https://chat.qwenlm.ai/ "qwenlm" https://www.youtube.com/watch?v=he9xAr_CKMQ
        else: # use local programmatic code:
            ai_svc = "pgm"
            gened_file_path = set_output_file_path(artpiece_num,ai_svc,"art.png")
            result = gen_one_file(gened_file_path)

        if SHOW_OUTPUT_FILE:   # --showout
            img = Image.open(gened_file_path)
            img.show() # Display the image:

        if GEN_URL_FILE: # -wm --watermark
            gened_file_path = set_output_file_path(artpiece_num,ai_svc,"art.png")
            result = gen_one_file(gened_file_path)
            if not result:
                print_error("gen_one_file() failed.")
                gened_file_path = None
                continue

        if KEEP_SHOWING:  # -ks--keepshow if FILES_TO_GEN == 0:   # Not infinite loop:
            # For running in kiosk mode where images appear and disappear:
            time.sleep(SLEEP_SECONDS)  # give user some time to appreciate the art.

            # Alternative A: Kill Preview.app window just opened:
            subprocess.run(['killall', 'Preview'])
            # osascript -e 'tell application "Preview" to close window 1'
            apple_script = '''
            tell application "Preview"
                close (every window whose name is not "")
            end tell
            '''
            subprocess.run(['osascript', '-e', apple_script])
            # NOTE: On first execution, access needs to be granted to control “Preview.app”.
            # Alternative B: close all windows (if can't differentiate specific window):
            # This doesn't work:
            # subprocess.run(['killall', 'Preview'])
            # Alternative C: use UI automation pyautogui or pyobjc to control Preview app.
            # See https://stackoverflow.com/questions/16928021/mac-python-close-window

        if DELETE_OUTPUT_FILE and gened_file_path:  # -del --delete
            os.remove(gened_file_path)
            print_info(f"File {gened_file_path} deleted.")
        else:
            # Upscale image using https://topazai.com (paid)
            #if UPSCALE_IMAGE:
            #    upscaled_file_path=upscale_image_file(gened_file_path)

            watermarked_file_path = None
            if ADD_WATERMARK and gened_file_path:  # -wm --watermark
                wmatermarked_file_path = set_output_file_path(artpiece_num,ai_svc,"wmd.png")
                result = add_watermark2png(gened_file_path, wmatermarked_file_path, WATERMARK_TEXT)

            #TODO: watermarked_file_found = read_watermark(watermarked_file_path)
            #TODO: create_thumbnail_png()
            #TODO: Resize mockups for different canvas sizes using free XnConvert @ xnview.com

            if ENCRYPT_FILE and watermarked_file_path:  # -e --encrypt  (password protect file)
                symmetric_key_str = encrypt_symmetrically(watermarked_file_path,cyphertext_file_path)
                print_trace("Encrypted file: "+cyphertext_file_path+" size: "+\
                    str(get_file_size_on_disk(cyphertext_file_path)))
                #TODO: test decrypt_symmetrically(cyphertext_file_path,plaintext_file_path,symmetric_key_str) 

            cyphertext_file_path = None
            if UPLOAD_TO_QUICKNODE and cyphertext_file_path:  # -qn --quicknode
                quicknode_cid_url = upload_to_ipfs(cyphertext_file_path)
                print_trace("QuickNode IPFS CID:", quicknode_cid_url)
                # see https://marketplace.quicknode.com/add-on/nft-mint-api-testnet
    
            # TODO: Define smart contract Collection (Solidity code) using OpenZeppelin https://docs.openzeppelin.com/contracts/4.4.1/
            # TODO: Have ready an address with its privatekey with native assets. Required to pay for the minting.
            # If a Minter address was added to the Collection SmartContract, 
            # Tatum pays on your behalf. Your account will be charged accordingly.

           # Pinata https://medium.com/pinata/how-to-programmatically-mint-an-nft-8e0c9a78b9c3
           # https://app.pinata.cloud/auth/signin "pinata-stage" bbfe025bc28d813106be

            if MINT_EMAIL:
                # Create a non-fungible token (NFT) on a blockchain using the ERC721 standard
                # https://ethereum.org/en/developers/docs/standards/tokens/erc-721/
                # https://www.youtube.com/watch?v=Q2MvYR8qFtU
                # TODO: Add Crossmint https://docs.crossmint.com/minting/quickstart
                # RUN_ENV & IMG_DESC, MINT_EMAIL, BLOCKCHAIN_NAME from globals above.
                IMG_DESC = "Mondrian 2025 "+ai_svc+" "+RUNID  # -id --imagedesc
                cid = mint_nft(quicknode_cid_url, IMG_DESC, RUN_ENV, MINT_EMAIL, BLOCKCHAIN_NAME)
                # TODO: Create url from CID
                if GEN_URL_FILE:  # -gf --genurlfile
                    url_file_path = set_output_file_path(artpiece_num, ai_svc,"cid.url")
                    save_url_to_file(quicknode_cid_url, url_file_path)

            if SHORTEN_URL and quicknode_cid_url:  # -su --shorturl
                shortened_url = shorten_url(quicknode_cid_url)

            if GEN_URL_FILE and shortened_url:  # -gu --genurlfile
                url_file_path = set_output_file_path(artpiece_num,ai_svc,"qn.url")
                save_url_to_file(shortened_url, url_file_path)

            if GEN_QR_CODE and shortened_url:  # -qr --qrcode  (from shortened_url):
                # Create QR code image file from URL:
                qrcode_file_path = set_output_file_path(artpiece_num,ai_svc,"qr.png")
                gen_qrcode(shortened_url,shortened_url)

            # TODO: printify.com t-shirts on demand https://www.youtube.com/watch?v=TygDUR38wuM
            # TODO: API to Etsy using TaskMagic https://www.youtube.com/watch?v=1sZ5VPlThKQ
                # See I Tried Selling AI Art https://www.youtube.com/watch?v=GXPQ-fg507o
            # TODO: API to frameiteasy.com https://documenter.getpostman.com/view/7462304/Tz5s3bQB 
            # TODO: API to Facebook Marketplace https://apify.com/shmlkv/facebook-marketplace/api
            # TODO: API to artbreeder.com https://documenter.getpostman.com/view/7462304/Tz5s3bQB

            if MONGODB:  # -md --mongodb "27017" or "mongodb://localhost:27017/"
                hash_str = hash_file_sha256(gened_file_path) # from step above
                print_trace("main() SHA256 hash "+str(len(hash_str))+" char=\""+hash_str+"\"")

                # Insert document into mongodb NoSQL database and return an index number:
                mongodb_client = MongoClient(MONGODB)
                artpiece_end_timer = time.perf_counter()
                artpiece_duration = artpiece_end_timer - artpiece_start_timer
                print_trace(f"main() artpiece_num={artpiece_num} artpiece_duration={artpiece_duration:.5f} seconds")
                document = {
                    "SHA256": hash_str,
                    "key": RUNID, # T0011
                    "pgm": PROGRAM_NAME,
                    "start": format_datetime_stamp(pgm_strt_datetimestamp),
                    "ai_svc": ai_svc,
                    "artpiece_file": gened_file_path,
                    "watermarked_file": watermarked_file_path,
                    "cyphertext_file": cyphertext_file_path,
                    "quicknode_cid_url": quicknode_cid_url,
                    "qrcode_file": qrcode_file_path,
                    "shortened_url": shortened_url,
                    #"interests": ["???", "data science", "machine learning"]
                    "secs": artpiece_duration
                }
                mongodb_index = insert_mongodb(document)
                print_trace(f"main() RUNID={RUNID} -> mongodb_index={mongodb_index}")

        if FILES_TO_GEN > 0:   
            if artpiece_num >= FILES_TO_GEN:
                # No more files to generate.Infinite loop needs to end:
                print_wall_times()
                if SEND_EMAIL:
                    send_smtp()            
                show_summary(artpiece_num)
                exit()  # graceful exit from infinite loop.

#        except KeyboardInterrupt:
#            # Gracefully handle manual interruption:
#            print("*** Infinite loop manually terminated by user using control+C.")

    # END While loop.