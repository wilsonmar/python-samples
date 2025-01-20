#!/usr/bin/env python3

"""mondrian-gen.py at https://github.com/wilsonmar/python-samples/blob/main/mondrian-gen.py
This program provides both local programmatic and OpenAI's DALL-E Generative AI API calls
to create a PNG-format file of art in the pure abstract Neoplasticism style
initiated in 1920s by Piet Mondrian (in Amersfort, Netherlands 1872-1944).

This was created to see whether the different ways of creating horizontal and 
vertical lines of rectangular boxes filled with primary colors
compare with the intuitive beauty of manually-created works, such as
https://res.cloudinary.com/dcajqrroq/image/upload/v1736178566/mondrian.29-compnum3-268x266_hceym9.png

// SPDX-License-Identifier: MIT
CURRENT STATUS: WORKING but no env file retrieve.

git commit -m"v014 + parms fix :mondrian-gen.py"

Tested on macOS 24.1.0 using Python 3.12.8
flake8  E501 line too long, E222 multiple spaces after operator

# Before running this program:
1. Create a Secret Key for ChatGPT API calls at https://platform.openai.com/api-keys and 
2. Open the Keyring Access.app. Click iCloud then Login. Click the add icon at the top.
3. Fill in the Item Name "OpenAI", Account Name "johndoe", Password (the API key). Click Add.
   Create an account using your Gmail & Telegram accountat https://www.quicknode.com/signup
   Store the QuickNode API Key in the Keyring Access.app.
4. In Terminal:
# INSTEAD OF: conda install -c conda-forge ...
python3 -m venv venv
source venv/bin/activate
python3 -m pip install envcloak keyring OpenAI pycairo python-dotenv Pillow psutil qrcode requests tzlocal
python3 -m pip install web3 eth_account IPFS-Toolkit Fernet cryptography pycryptodome qiskit
   # See https://wilsonmar.github.io/quantum
python3 -m pip install --upgrade -q google-api-python-client google-auth-httplib2 google-auth-oauthlib
python3 -m pip install google-generativeai
    # Downloading google_generativeai-0.8.3-py3-none-any.whl (160 kB) and many others
5. Edit .env files to customize run parameters.
6. # USAGE: Run this program:
chmod +x mondrian-gen.py
./mondrian-gen.py -h  # for list of parameters
./mondrian-gen.py -v -vv 
7. Within VSCode install Ruff (from Astral Software), written in Rust
   to lint Python code. 
8. Run ruff check on this program (Flake8, Pylint, Xenon, Radon, Black, isort, pyupgrade, etc.)
   See https://github.com/charliermarsh/ruff

TODO: Other tools to generate art:
<a target="_blank" href="https://www.youtube.com/watch?v=Vgcr6VOwHf0">VIDEO</a>
* <a target="_blank" href="https://mondriangenerator.io/">Mondrian Generator</a> web-based tool. Allows you to adjust parameters in the left panel: Format (size), Complexity (number of blocks), Colors, Color amount.
* <a target="_blank" href="https://www.artvy.ai/ai-art-style/piet-mondrian">Artvy</a> generates based on an image you upload for style transfer.
* <a target="_blank" href="https://neural.love/ai-art-generator/1ed7da32-c7dc-6e2c-957c-7fd88793a662/mondrian-painting">Neural Love</a> generate art under a CC0 license.
* <a target="_blank" href="https://www.pcmag.com/how-to/how-to-use-dall-e-ai-art-generator">DaLL-E</a> from OpenAI's generates realistic as part of the ChatGPT Plus $20 per month paid version. 
    See https://platform.openai.com/docs/overview
* MidJourney
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


#### SECTION 1 - import internal modules (alphabetically):

# For wall time of std (standard) imports:
import datetime as dt
std_strt_datetimestamp = dt.datetime.now()

# Standard Python library modules (no need to pip install):
import argparse
from argparse import ArgumentParser
import hashlib
import io
import os
import pathlib
from pathlib import Path
import platform
import random
import re
import shutil
import socket
import subprocess
import sys
import time
import uuid

std_stop_datetimestamp = dt.datetime.now()


#### SECTION 2 - imports external modules (alphabetically) at top of file
# See https://peps.python.org/pep-0008/#imports

# For wall time of xpt imports:
xpt_strt_datetimestamp = dt.datetime.now()

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
import google.generativeai as genai
import keyring
from openai import OpenAI
# import Pillow to convert SVG to PNG file format:
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
import psutil
import pytz  # for time zone handling
import qrcode
import requests
    # urllib is a built-in module that doesn't require additional installation.
    # But the requests library is more versatile and widely used.
import timeit
import tzlocal

# For wall time of xpt imports:
xpt_stop_datetimestamp = dt.datetime.now()


#### SECTION 3 - Global date and time start timers:

# Start with program name (without ".py" file extension) such as "modrian-gen":
PROGRAM_NAME = Path(__file__).stem
    # See https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    # Instead of os.path.splitext(os.path.basename(sys.argv[0]))[0]

local_time = time.localtime()
TZ_OFFSET = time.strftime("%z", local_time)  # such as "-0700"

if os.name == "nt":  # Windows operating system:
    SLASH_CHAR = "\\"
    # if platform.system() == "Windows":
    print(f"*** Windows Edition: {platform.win32_edition()} Version: {platform.win32_ver()}")
    print("*** WARNING: This program has not been tested on Windows yet.")
else:
    SLASH_CHAR = "/"

# SAVE_PATH = os.getcwd()  # cwd=current working directory (python-examples code folder)
SAVE_PATH = os.path.expanduser("~")  # user home folder path like "/User/johndoe"
#print("*** INIT: SAVE_PATH="+SAVE_PATH)

# Based on: pip3 install datetime
#import datetime as dt
#from datetime import datetime, timezone
# For wall time of program run (using date and time together):
pgm_strt_datetimestamp = dt.datetime.now()

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


#### SECTION 4 - TASK: Customize hard-coded values that control program flow.

# These will be overridden by variables (API key, etc.) within .env file.

def set_hard_coded_defaults() -> None:

    global CLEAR_CLI
    CLEAR_CLI = True
    
    global show_todo
    show_todo = True

    global show_heading
    show_heading = True
    global show_info
    show_info = True
    global show_warning
    show_warning = True
    global show_error
    show_error = True
    global show_fail
    show_fail = True

    global PRINT_OUTPUT_FILE_LOG
    PRINT_OUTPUT_FILE_LOG = True
    global show_dates_in_logs
    show_dates_in_logs = False
    global DATE_OUT_Z
    DATE_OUT_Z = False  # save files with Z time (in UTC time zone now) instead of local time.

    global run_quiet
    run_quiet = False  # suppress show_heading, show_info, show_warning, show_error, show_fail

    global show_verbose
    show_verbose = False

    global show_trace
    show_trace = False
    global show_sys_info
    show_sys_info = False
    global show_secrets
    show_secrets = False

    global DRIVE_PATH
    DRIVE_PATH = "NODE NAME"  # as in /Volumes/YourDriveName - the default from manufacturing.
    global OUTPUT_FOLDER
    OUTPUT_FOLDER = "Desktop"  # "Desktop" or "Documents" or "Downloads" to avoid subfolder creation.

    global USE_DALLE_API
    USE_DALLE_API = False  # if False, use programmatic Python. True = use DELL-E
        # Alternatives: Adobe Firefly,https://midjourney2.com/
        # See https://nightcafe.studio/blogs/info/how-does-artbreeder-work
        # See https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Commands#webui
    global dalle_keyring_service_name
    dalle_keyring_service_name = "DALL-E"
    global dalle_keyring_account_name
    dalle_keyring_account_name = "johndoe"

    # For creation of image files:
    # Within Gemini, smaller images are scaled up to 768x768 and max. resolution is 3072x3072.
    global WIDTH
    WIDTH = 500
    global HEIGHT
    HEIGHT = 500
    # For ref. by generate_mondrian(), mondrian_flood_fill(), draw_mondrian()
    global TILE_SIZE
    TILE_SIZE = 10
    # TODO: Vary borderWidth = 8; minDistanceBetweenLines = 50;
    # See https://github.com/unsettledgames/mondrian-generator/blob/master/mondri an_generator.pde

    # For creation of text : See https://www.youtube.com/watch?v=CaxPa1FuHx4 by Aaron Dunn.
    global USE_OPENAI
    USE_OPENAI = False  # if False, use programmatic Python. True = use OpenAI
    global openai_keyring_service_name
    openai_keyring_service_name = "OpenAI"
    global openai_keyring_account_name
    openai_keyring_account_name = "johndoe"

    # For creation of text : See https://www.youtube.com/watch?v=CaxPa1FuHx4 by Aaron Dunn.
    global USE_GEMINI_API
    USE_GEMINI_API = False # Don't use unless requested by -dg parameter.
    global USE_GOOGLE_GENERATIVE_AI
    USE_GOOGLE_GENERATIVE_AI = False

    global gemini_keyring_service_name
    gemini_keyring_service_name = "Gemini5044"
    global gemini_keyring_account_name
    gemini_keyring_account_name = "ninth-matter-388922"
    global gemini_safety_settings
    gemini_safety_settings = []
    global gemini_prompt_text
    gemini_prompt_text = "A painting of a cat and a dog"
    global target_subject
    target_subject = "science"
    global target_audience
    target_audience = "teenagers in high school"
    global target_experience
    target_experience = "educational"
    global GEMINI_MODEL_ID
    GEMINI_MODEL_ID = "gemini-1.5-flash"  # "gemini-1.0-pro" or "gemini-1.5-pro" or "gemini-1.5-flash"
    global gemini_generation_config
    gemini_generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    # Based on https://www.youtube.com/watch?v=ABCqfaTjNd4
    # "Your task is to explain science in a way that teenagers can understand."
    global gemini_system_prompt
    gemini_system_prompt = "You are an expert at teaching to " + \
    target_audience + "." + \
    "Your task is to engage in conversations about " + \
    target_subject + " and answer questions in a way that " + \
    target_audience + " can understand." + \
    "Use analogies and examples that are relatable." + \
    "Use humor and make the conversation both educational and interesing." + \
    "Ask questions so that you can better understand the user and improve the " + \
    target_experience + " experience." + \
    "Suggest ways that these concepts can be related to the real world with observations and experiments."

    ### Processing controls:

    global FILES_TO_GEN
    FILES_TO_GEN = 1     # 0 = Infinite loop while in kiosk mode.
    
    global UPSCALE_IMAGE_FILE
    UPSCALE_IMAGE_FILE = False

    global ENCRYPT_FILE
    ENCRYPT_FILE = False

    global GEN_SHA256
    GEN_SHA256 = False

    global ENCRYPTION_KEY
    ENCRYPTION_KEY = None

    global USE_QISKIT  # for Quantum resistant encryption
    USE_QISKIT = False

    global GEN_NFT
    GEN_NFT = False

    global ADD_WATERMARK
    ADD_WATERMARK = False  # watermark2png()
    global WATERMARK_TEXT
    WATERMARK_TEXT = "\"Like Mondrian 2054\" Copywrite Wilson Mar 2025. All rights reserved."
    # Copyright issues: In the United States, only works created by humans can be copyrighted.
    
    global GEN_IPFS
    GEN_IPFS = False
    global UPLOAD_TO_QUICKNODE
    UPLOAD_TO_QUICKNODE = False
    global quicknode_keyring_service_name
    quicknode_keyring_service_name = "QuickNode"
    global quicknode_keyring_account_name
    quicknode_keyring_account_name = "johndoe"

    global MINT_NFT
    MINT_NFT = False
    global BLOCKCHAIN_NAME
    BLOCKCHAIN_NAME = "Ethereum"
    global NFT_MARKETPLACE
    NFT_MARKETPLACE = "Opensea"
    # global NFT_ACCOUNT_EMAIL   # from keyring
    # Email from .env file loaded by open_env_file()

    global GEN_QR_CODE
    GEN_QR_CODE = False


    ### Output controls:

    global cyphertext_file_path
    cyphertext_file_path = "path/to/your/file ???"
    global quicknode_file_path
    quicknode_file_path = "path/to/your/file ???"
    global qrcode_file_path
    qrcode_file_path = "path/to/your/qrcode/file ???"

    global decrypted_file_path
    decrypted_file_path='your_file.txt'
    global encrypted_file_path
    encrypted_file_path='your_file.txt'

    global DECRYPT_FILE
    DECRYPT_FILE = False

    global SHOW_OUTPUT_FILE
    SHOW_OUTPUT_FILE = False

    global KEEP_SHOWING
    KEEP_SHOWING = False

    global DELETE_OUTPUT_FILE
    DELETE_OUTPUT_FILE = False  # If True, recover files from Trash

    global SHOW_SUMMARY_COUNTS
    SHOW_SUMMARY_COUNTS = True

    global SLEEP_SECONDS
    SLEEP_SECONDS = 1.0  # between art created in a loop

    return


#### SECTION 8 - Read custom command line arguments

def read_cmd_args() -> None:
    """Read command line arguments and set global variables.
    See https://realpython.com/command-line-interfaces-python-argparse/
    """
    #import argparse
    #from argparse import ArgumentParser
    parser = argparse.ArgumentParser(allow_abbrev=True,description="Mondrian Generator")
    parser.add_argument("-pf", "--parmspath", help="File Path string to env specs")
    parser.add_argument("-q", "--quiet", action="store_true", help="Run without output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show each download")
    parser.add_argument("-vv", "--trace", action="store_true", help="Show trace info")

    parser.add_argument("-si", "--si", action="store_true", help="Show System Info")
    parser.add_argument("-log", "--log", action="store_true", help="Log to external file")
    parser.add_argument("-dt", "--showdates", action="store_true", help="Show dates in logs")
    parser.add_argument("-z", "--utc", action="store_true", help="Show Dates in UTC/GMT=Zulu timezone")

    parser.add_argument("-d", "--drivepath", help="Removeable USB //Volumes/DriveName to read")
    parser.add_argument("-f", "--folder", help="Folder to hold output files")

    parser.add_argument("-dg", "--gemini", action="store_true", help="Gen Gemini API text")
    parser.add_argument("-de", "--dalle", action="store_true", help="Gen Dall-E png file")

    parser.add_argument("-fg", "--filesgen", help="Files to generate integer number")
    parser.add_argument("-w", "--width", help="Width (pixel size of output file eg 500)")
    parser.add_argument("-he", "--height", help="Height (pixel size of output file eg 500)")

    parser.add_argument("-do", "--delout", action="store_true", help="Delete output file")
    parser.add_argument("-so", "--showout", action="store_true", help="Show output file")
    parser.add_argument("-ks", "--keepshow", action="store_true", help="Keep Showing output file (not kill preview)")

    parser.add_argument("-wm", "--watermark", help="Insert Watermark textin png file")
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt file")
    parser.add_argument("-key", "--key", help="Encryption key")
                       # -key --key "J64ZHFpCWFlS9zT7y5zxuQN1Gb09y7cucne_EhuWyDM="
    parser.add_argument("-256", "--hash", action="store_true", help="Gen SHA256 Hash from output file contents")
    # See https://bomonike.github.io/nft for explanation:
    #parser.add_argument("-ipfs", "--ipfs", action="store_true", help="Gen. IPFS CID")
    parser.add_argument("-qn", "--quicknode", action="store_true", help="Gen. IPFS CID in QuickNode")

    parser.add_argument("-nft", "--nft", action="store_true", help="Mint NFT")
    parser.add_argument("-qr", "--genqr", action="store_true", help="Gen QR Code image file to each URL")

    parser.add_argument("-s", "--sleepsecs", help="Sleep seconds number")
    parser.add_argument("-m", "--summary", action="store_true", help="Show summary")
    # Default -h = --help (list arguments)

    args = parser.parse_args()
    
    #### SECTION 9 - Override defaults and .env file with run-time parms:

    if args.parmspath:     # -pf
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
        global show_summary
        show_summary = False
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
    if args.si:            # -si => used by sys_info()
        global show_sys_info
        show_sys_info = True
    if args.utc:            # -z = # Dates in UTC/GMT=Zulu timezone
        global DATE_OUT_Z
        DATE_OUT_Z = True  # save files with Z time (in UTC time zone now) instead of local time.

    if args.dalle:          # -de ="Gen Dall-E png file"
        global USE_DALLE_API
        USE_DALLE_API = True  # if False, use programmatic Python. True = use DELL-E
      # USE_DALLE_API = False  # if False, use programmatic Python. True = use DELL-E
    if args.gemini:         # -ge ="Google Gemini API") see https://bomonike.github.io/google-ai
        global USE_GEMINI_API
        USE_GEMINI_API = True

    if args.folder:         # -f "Downloads" (overwrites default)
        global OUTPUT_FOLDER
        OUTPUT_FOLDER = args.folder
    if args.drivepath:      # -d "//Volumes/DriveX" # (USB removable drive without the /Volumes/ prefix)
        global DRIVE_PATH
        DRIVE_PATH = args.drivepath

    if args.filesgen:
        global FILES_TO_GEN
        FILES_TO_GEN = args.filesgen     # 0 = Infinite loop while in kiosk mode.
    if args.width:          # Width of output number (eg 500)"
        global WIDTH
        WIDTH = args.width

    if args.height:         # Height of output number (eg 500)"
        global HEIGHT
        HEIGHT = args.height

    if args.delout:  # Delete output file
        global DELETE_OUTPUT_FILE
        DELETE_OUTPUT_FILE = True   # If True, recover files from Trash

    if args.showout:
        global SHOW_OUTPUT_FILE
        SHOW_OUTPUT_FILE = True
    if args.keepshow:
        global KEEP_SHOWING
        KEEP_SHOWING = False

    if args.watermark:
        global ADD_WATERMARK
        ADD_WATERMARK = True   # used by watermark2png()
        WATERMARK_TEXT = args.watermark  # used by watermark2png()
             # "\"Like Mondrian 2054\" Copywrite Wilson Mar 2025. All rights reserved."
    if args.encrypt:
        global ENCRYPT_FILE
        ENCRYPT_FILE = True
    if args.key:               # -key --key "J64ZHFpCWFlS9zT7y5zxuQN1Gb09y7cucne_EhuWyDM="
        global ENCRYPTION_KEY
        ENCRYPTION_KEY = args.key

    if args.hash:              # "-256" ="Hash SHA256"
        global GEN_QR_CODE
        GEN_SHA256 = True
    if args.quicknode:
        global UPLOAD_TO_QUICKNODE
        UPLOAD_TO_QUICKNODE = True
    if args.nft:               # -nft --nft
        global MINT_NFT
        MINT_NFT = True
    if args.genqr:             # -qr  --genqr Gen QR code image file from URL
        global GEN_QR_CODE
        GEN_QR_CODE = True

    if args.log:               # -l
        global PRINT_OUTPUT_FILE_LOG
        PRINT_OUTPUT_FILE_LOG = True
        global LOGGER_FILE_PATH
        LOGGER_FILE_PATH = SAVE_PATH + SLASH_CHAR + os.path.basename(__file__) + '.log'
        global LOGGER_NAME
        LOGGER_NAME = os.path.basename(__file__)  # program script name.py

    if args.sleepsecs:          # -s
        global SLEEP_SECONDS
        SLEEP_SECONDS = args.sleepsecs  # between files created in a loop

    return


    #### SECTION 10 - Set Static Global working constants:

def calc_env_vars():

    global GRID_WIDTH
    GRID_WIDTH = WIDTH // TILE_SIZE

    global GRID_HEIGHT
    GRID_HEIGHT = HEIGHT // TILE_SIZE

    global WIDTHxHEIGHT
    WIDTHxHEIGHT = str(WIDTH)+"x"+str(HEIGHT)  # for "500x500"

    # TODO: For art: vary size (ratio) of file to generate locally

    return


#### SECTION 7 - printing utility globals and functions (used by other functions):

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
BLUE = '\033[34m'
# Styles:
BOLD = '\033[1m'
RESET = '\033[0m'

class bcolors:  # ANSI escape sequences:
    BOLD = '\033[1m'       # Begin bold text
    UNDERLINE = '\033[4m'  # Begin underlined text

    HEADING = '\033[90m'   # [90 gray  NOT [37 white
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
    CGRAY = '\033[90m'

    RESET = '\033[0m'   # switch back to default color

def print_separator():
    """ Put a blank line in CLI output. Used in case the technique changes throughout this code. """
    print(" ")

def print_heading(text_in):
    if show_heading:
        if show_dates_in_logs:
            print(bcolors.HEADING+bcolors.UNDERLINE, '\n***', local_datetime_stamp(), f'{text_in}', bcolors.RESET)
        else:
            print(bcolors.HEADING+bcolors.UNDERLINE,'\n***', f'{text_in}', bcolors.RESET)

def print_fail(text_in):  # when program should stop
    if show_fail:
        if show_dates_in_logs:
            print(bcolors.FAIL, '***', local_datetime_stamp(), "FAIL:", f'{text_in}', bcolors.RESET)
        else:
            print(bcolors.FAIL, '***', "FAIL:", f'{text_in}', bcolors.RESET)

def print_error(text_in):  # when a programming error is evident
    if show_fail:
        if show_dates_in_logs:
            print(bcolors.ERROR, '***', local_datetime_stamp(), "ERROR:", f'{text_in}', bcolors.RESET)
        else:
            print(bcolors.ERROR, '***', "ERROR:", f'{text_in}', bcolors.RESET)

def print_warning(text_in):
    if show_warning:
        if show_dates_in_logs:
            print(bcolors.WARNING, '***', local_datetime_stamp(), f'{text_in}', bcolors.RESET)
        else:
            print(bcolors.WARNING, '***', "WARNING:",f'{text_in}', bcolors.RESET)

def print_todo(text_in):
    if show_todo:
        if show_dates_in_logs:
            print(bcolors.CVIOLET, '***', local_datetime_stamp(), "TODO:", f'{text_in}', bcolors.RESET)
        else:
            print(bcolors.CVIOLET, '***', "TODO:", f'{text_in}', bcolors.RESET)

def print_info(text_in):
    if show_info:
        if show_dates_in_logs:
            print(bcolors.INFO+bcolors.BOLD,'***', local_datetime_stamp(), "INFO:", f'{text_in}', bcolors.RESET)
        else:
            print(bcolors.INFO+bcolors.BOLD,'***', "INFO:", f'{text_in}', bcolors.RESET)

def print_verbose(text_in):
    if show_verbose:
        if show_dates_in_logs:
            print(bcolors.VERBOSE, '***', local_datetime_stamp(), f'{text_in}', bcolors.RESET)
        else:
            print(bcolors.VERBOSE, '***', f'{text_in}', bcolors.RESET)

def print_trace(text_in):  # displayed as each object is created in pgm:
    if show_trace:
        if show_dates_in_logs:
            print(bcolors.TRACE, '***', local_datetime_stamp(), f'{text_in}', bcolors.RESET)
        else:
            print(bcolors.TRACE, '***', f'{text_in}', bcolors.RESET)

def do_clear_cli():
    if CLEAR_CLI:
        import os
        # Make a OS CLI command:
        lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def print_secret(secret_in):
    """ Outputs only the first few characters (like Git) with dots replacing the rest 
    """
    # See https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
    if show_secrets:  # program parameter
        if show_dates_in_logs:
            now_utc=datetime.now(timezone('UTC'))
            print(bcolors.CBEIGE, '*** ',now_utc,"SECRET: ", f'{secret_in}', bcolors.RESET)
        else:
            print(bcolors.CBEIGE, '***', "SECRET: ", f'{secret_in}', bcolors.RESET)
    else:
        # same length regardless of secret length to reduce ability to guess:
        secret_len = 8
        if len(secret_in) >= 8:  # slice
            secret_out = secret_in[0:4] + "."*(secret_len-4)
        else:
            secret_out = secret_in[0:4] + "."*(secret_len-1)
            if show_dates_in_logs:
                print('***', local_datetime_stamp(), bcolors.WARNING, f'{text_in}', bcolors.RESET)
            else:
                print('***', bcolors.CBEIGE, " SECRET: ", f'{secret_out}', bcolors.RESET)


#### SECTION 7 - read_env_file() to override hard-coded defaults:


def load_env_file(env_path):
    """Read .env file containing variables and values.
    See https://wilsonmar.github.io/python-samples/#envLoad
    See https://stackoverflow.com/questions/40216311/reading-in-environment-variables-from-an-environment-file
    """

    """
    openai_api_key = get_str_from_env_file('OPENAI_API_KEY')
    if openai_api_key == None:
        print_error("openai_api_key="+openai_api_key+" not in "+env_path)
    else:
        print_error("openai_api_key="+openai_api_key+" in "+env_path)
    """
    return

# See https://wilsonmar.github.io/python-samples/#envFile
def open_env_file(env_file) -> str:
    """Return a file path obtained from .env file based on the path provided
    in env_file coming in.
    """
    from pathlib import Path
    # See https://wilsonmar.github.io/python-samples#run_env
    global user_home_dir_path
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


def get_str_from_env_file(key_in) -> str:
    """Return a value of string data type from OS environment or .env file
    (using pip python-dotenv)
    """
    # FIXME:
    env_var = os.environ.get(key_in)
    print_trace("DEBUG: EXIT: key_in="+key_in+" env_var="+env_var)

    if not env_var:  # yes, defined=True, use it:
        print_warning(key_in + " not found in OS nor .env file: " + ENV_FILE_PATH)
        return None
    else:
        # PROTIP: Display only first 5 characters of a potentially secret long string:
        if len(env_var) > 5:
            print_trace(key_in + "=\"" + str(env_var[:5]) +" (remainder removed)")
        else:
            print_trace(key_in + "=\"" + str(env_var) + "\" from .env")
        return str(env_var)


def list_files_on_removable_drive(drive_path):
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


#### SECTION 11 - Utility time & date functions (which can be in a python module)

def get_time() -> str:
    """ Generate the current local datetime. """
    now: datetime = dt.datetime.now()
    return f'{now:%I:%M %p (%H:%M:%S) %Y-%m-%d}'


def local_datetime_stamp():
    """Assemble from OS clock date stamp (with a time zone offset)
    using local time zone offset above.
    """
    local_time = time.localtime()
    TZ_OFFSET = time.strftime("%z", local_time)
    # returns "-0700" for MST "America/Denver"

    if DATE_OUT_Z:  # from user preferences
        # Add using local time zone Z (Zulu) for UTC (GMT):
        now = dt.datetime.now(dt.timezone.utc)
        date_stamp = now.strftime("%Y%m%dT%H%M%SZ")
    else:
        # Add using local time zone offset:
        now = dt.datetime.now()
        date_stamp = now.strftime("%Y%m%dT%H%M%S")+TZ_OFFSET

    return date_stamp


def file_creation_datetime(path_to_file):
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
        except AttributeError as e:
            # PROTIP: Get the 
            print_error(f"{path_to_file} AttributeError {e}")
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            stat = os.stat(path_to_file)
            # like os.stat_result(st_mode=33188, st_ino=42022053, st_dev=16777232, 
            # st_nlink=1, st_uid=501, st_gid=20, st_size=4940329, st_atime=1737270005, 
            # st_mtime=1737266324, st_ctime=1737266363) 
            return stat.st_mtime   # epoch datetime modified like 1737266324



#### SECTION 12 - Utility system information functions (which can be in a python module)

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
    return

def count_files_within_path(directory) -> int:
    """Returns the number of files after looking recursively
    within a given directory"""
    # import os
    file_count = 0
    for entry in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, entry)):
            file_count += 1
    return file_count


def get_file_size_on_disk(file_path):
    """Returns integer bytes from the OS for a file path """
    try:
        file_size = os.path.getsize(file_path)
        return file_size
        # Alternately:
        # stat_result = os.stat(file_path)
        # return stat_result.st_blocks * 512  # st_blocks is in 512-byte units
    except FileNotFoundError:
        print(f"*** File path not found: {file_path}")
        return None
    except Exception as e:
        print(f"*** Error getting file size: {e}")
        return None


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
    print_trace("platform_system="+str(platform_system))

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
    
    return

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
        return


def list_macos_volumes():
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



def list_files_by_mountpoint():
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


def read_file_from_removable_drive(drive_path, file_name, content):
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


def write_file_to_removable_drive(drive_path, file_name, content):
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


def eject_drive(drive_path):
    """Safely eject removeable drive after use, where
    drive_path = '/Volumes/YourDriveName'
    """
    try:
        # import subprocess
        subprocess.run(["diskutil", "eject", drive_path], check=True)
        print(f"Successfully ejected {drive_path}")
    except subprocess.CalledProcessError:
        print(f"Failed to eject {drive_path}")



def get_from_macos_keyring(service, account):
    """Read API Key from MacOS built-in Keyring/Passwords.app
    : service ("OpenAI")
    : account ("johndoe@gmail.com")
    for password = API key value
    """
    # import keyring
    return keyring.get_password(service, account)



#### SECTION 15 - utility functions:

def define_output_path(SAVE_PATH) -> str:

    # SAVE_PATH = os.getcwd()  # cwd=current working directory.
    save_path_prefix = os.path.expanduser("~")  # user home folder path

    #if USER_FOLDER:  # blank inside, from user preferences:
    #    OUTPUT_PATH_PREFIX = save_path_prefix + SLASH_CHAR + USER_FOLDER
    #    print_trace("USER_FOLDER="+USER_FOLDER+" instead of default")
    #else:
        # No prefix (mount) specified:
    OUTPUT_PATH_PREFIX = save_path_prefix + SLASH_CHAR + SAVE_PATH
    # Confirm directory path exists:
    if not os.path.isdir(OUTPUT_PATH_PREFIX):  
        try:
            print_warning(f'*** Folder {OUTPUT_PATH_PREFIX} does not exist. Creating.')
            os.mkdirs(OUTPUT_PATH_PREFIX)
        except FileExistsError:
            print_fail(f'FileExistsError creating {OUTPUT_PATH_PREFIX}. Exiting.')
            exit(9)

    return OUTPUT_PATH_PREFIX


# def setup_logger(log_file=LOGGER_FILE_PATH, console_level=logging.INFO, file_level=logging.DEBUG):
   # See https://docs.python.org/3/library/logging.html#module-logging
# def log_event(logger, event_type, message, level='info'):


def gen_qrcode(url,png_file_path):
    """Generate a QR code from a URL and save it to a file.
    See https://www.geeksforgeeks.org/python-generate-qr-code/
    """
    #import qrcode
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(png_file_path)
    print("QR code generated as "+png_file_path)


def hash_file_sha256(filename) -> str:
    # A hash is a fixed length one way string from input data. Change of even one bit would change the hash.
    # A hash cannot be converted back to the input data (unlike encryption).
    # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python

    import hashlib
    sha256_hash = hashlib.sha256()
    # There are also md5(), sha224(), sha384(), sha512()
    BUF_SIZE = 65536
    with open(filename, "rb") as f: # read entire file as bytes
        # Read and update hash string value in blocks of 64K:
        for byte_block in iter(lambda: f.read(BUF_SIZE),b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def encrypt_symmetrically(source_file_path, cyphertext_file_path) -> str:
    """Encrypt a plaintext file to cyphertext using Fernet symmetric encryption algorithm
    after reading entire file into memory.
    Based on https://www.educative.io/answers/how-to-create-file-encryption-decryption-program-using-python
    """
    # pip install cryptography
    # from cryptography.fernet import Fernet
    
    # Generate a 32-byte random encryption key like J64ZHFpCWFlS9zT7y5zxuQN1Gb09y7cucne_EhuWyDM=
    if not ENCRYPTION_KEY:
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


def upload_to_ipfs(file_path, quicknode_api_key) -> str:
    """Upload a file to IPFS using the QuickNode API.
    See https://www.quicknode.com/docs
    See https://techieteee.hashnode.dev/how-to-build-a-decentralized-data-pipeline-with-quicknode-ipfs-and-python
    """
    # import requests, json  # (not use framework)
    # This endpoint version needs to be updated: https://www.quicknode.com/docs
    endpoint = "https://ipfs.quicknode.com/api/v0/add"
    files = {"file": open(file_path, "rb")}
    headers = {"Authorization": f"Bearer {quicknode_api_key}"}
    
    func_start_timer = time.perf_counter()
    response_obj = requests.post(endpoint, files=files, headers=headers)
    func_end_timer = time.perf_counter()
    func_duration = func_end_timer - func_start_timer

    data = json.loads(response_obj.text)
    cid = data["Hash"]

    return cid


#### SECTION 16 - custom app functions:

# Based on https://www.perplexity.ai/search/write-a-python-program-to-crea-nGRjpy0dQs6xVy9jh4k.3A#0

def generate_mondrian():
    """Create a grid and adds random horizontal and vertical lines
    based on WIDTH, HEIGHT, TILE_SIZE
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


def mondrian_flood_fill(grid, x, y, old_color, new_color):
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


def draw_mondrian(grid, filename):
    """Use the Cairo graphics library to render the grid as an image2.
    """
    print_trace("draw filename="+filename)
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = COLORS[grid[y][x]]
            ctx.set_source_rgb(*color)
            ctx.rectangle(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            ctx.fill()

    surface.write_to_png(filename)


def gen_one_file(in_seq,path_prefix):
    """Generate image and draw to a file.
    """
    func_start_timer = time.perf_counter()
    # Generate Mondrian-style art in memory:
    mondrian_grid = generate_mondrian()
    func_end_timer = time.perf_counter()
    func_duration = func_end_timer - func_start_timer

    file_date_stamp = local_datetime_stamp()
    gened_file_path = path_prefix + SLASH_CHAR +PROGRAM_NAME+"-"+file_date_stamp +"-"+str(in_seq)+".png"
    #  print_trace(f"*** DEBUG: gened_file_path = {gened_file_path}")

    # Output to a PNG file:
    draw_mondrian(mondrian_grid, gened_file_path )
    if PRINT_OUTPUT_FILE_LOG:
       file_create_datetime = file_creation_datetime(gened_file_path)
       file_bytes = get_file_size_on_disk(gened_file_path)  # type = number
       print(f"*** LOG: {gened_file_path},{file_bytes},{file_create_datetime},{func_duration:.5f}")
           # *** LOG: /Users/johndoe/Downloads/mondrian-gen-20250105T061101-0700-3.png,1912
    return gened_file_path


def gen_dalle_file(in_seq,path_prefix) -> str:

    # Pull OPENAI_API_KEY as password from macOS Keyring file (and other password manager):
    print("openai_keyring_service_name="+openai_keyring_service_name+" openai_keyring_account_name="+openai_keyring_account_name)
    import keyring
    openai_api_key = keyring.get_password(openai_keyring_service_name, openai_keyring_account_name)
    print_secret("openai_api_key="+str(openai_api_key))
    # FIXME: openai_api_key=None

    # See https://help.openai.com/en/articles/8555480-dall-e-3-api
    client = OpenAI()
    client.api_key = openai_api_key

    # TODO: User specifications parameters:
    #prompt_model="dall-e-3"
    #prompt_size="1024x1024"
    prompt_model="dall-e-2"
    prompt_size="512x512"
    prompt_text = (
        "Create an abstract painting in the style of Piet Mondrian "
        "featuring a grid of shapes between straight black lines "
        "dividing the canvas into rectangles and squares. "
        "Use the golden ratio (1:1.618) to arrange blocks. "
        "Fill 50% of shapes with primary colors - red, blue, and yellow - "
        "while leaving others white. Ensure a balanced composition with "
        "asymmetrical placement of colored blocks."
    )
    #.  size=WIDTHxHEIGHT
      # quality="hd” costs more, takes more time to generate than "standard".
      # style="vivid" or "natural" for advanced control of the generation.

    func_start_timer = time.perf_counter()
    response = client.images.generate(
        model=prompt_model,
        prompt=prompt_text,
        n=1,
        size=prompt_size
    )
    func_end_timer = time.perf_counter()
    func_duration = func_end_timer - func_start_timer
    print_trace(f"gen_dalle_file func_duration={func_duration:.5f} seconds")

    print_info("response.data[0].url"+response.data[0].url)
       # Example: https://oaidalleapiprodscus.blob.core.windows.net/private/org-4...
    response = requests.get(response.data[0].url)
    if response.status_code == 200:
        file_date_stamp = local_datetime_stamp()
        gened_file_path = path_prefix +SLASH_CHAR +PROGRAM_NAME+"-"+file_date_stamp +"-"+str(in_seq)+".png"
        watermarked_file_path = path_prefix +SLASH_CHAR +PROGRAM_NAME+"-"+file_date_stamp +"-"+str(in_seq)+".png"
        print_trace(f"*** DEBUG: gened_file_path = {gened_file_path}")
        with open(gened_file_path, 'wb') as file:
            file.write(response.content)

        if PRINT_OUTPUT_FILE_LOG:
            file_bytes = get_file_size_on_disk(gened_file_path)  # type = number
            print(f"*** LOG: {gened_file_path},{file_bytes},{file_creation_datetime(gened_file_path)},{func_duration:.5f}")

            file_bytes = get_file_size_on_disk(watermarked_file_path)  # type = number
            print(f"*** LOG: {watermarked_file_path},{file_bytes},{func_duration:.5f}")
    else:
        print_error('Download file fail with HTTP status '+response.status_code)
        return None

    return gened_file_path


def gen_gemini_text(prompt_in) -> str:
    """Call Google Gemini API to generate text
    after pasteing the GEMINI_API_KEY from https://ai.google.dev/gemini-api
    """
    # Pull gemini_api_key as password from macOS Keyring file (and other password manager):
    print("gemini_keyring_service_name="+gemini_keyring_service_name+" gemini_keyring_account_name="+gemini_keyring_account_name)
    # import keyring
    gemini_api_key = keyring.get_password(gemini_keyring_service_name, gemini_keyring_account_name)
    print_secret("gemini_api_key="+str(gemini_api_key))
    
    func_start_timer = time.perf_counter()
    # import os
    # import google.generativeai as genai
    # See https://ai.google.dev/gemini-api/docs/oauth
    genai.configure(api_key=gemini_api_key)
        # INSTEAD OF: export GEMINI_API_KEY=gemini_api_key
        # INSTEAD OF: genai.configure(api_key=os.getenv(GEMINI_API_KEY))

    # Request a specific model to create a GenerativeModel instance:
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL_ID,
        safety_settings=gemini_safety_settings,
        generation_config=gemini_generation_config,
        system_instruction=gemini_system_prompt,
    )
    func_end_timer = time.perf_counter()
    func_duration = func_end_timer - func_start_timer
    print_trace(f"gen_gemini_text func_duration={func_duration:.5f} seconds.")

    # Generate content within the response class object:
    response = model.generate_content(prompt_in)

    return response.text


def add_watermark2png(input_image, output_image, watermark_text) -> None:
    # See https://www.geeksforgeeks.org/python-pillow-creating-a-watermark/
    # Alt: cv2 (OpenCV), Filetools (China), pythonwatermark
         # see https://www.youtube.com/watch?v=Yu8z0Lg53zk

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

    return


def mint_nft(file_path_in, blockchain_name, file_path_out):
    # TODO: mint_nft - see https://bomonike.github.io/nft
    # marketplace = "OpenSea", "MagicEden", "Rarible", "Superrare"
    # blockchain_name = "Ethereum", "Solana", "Polygon", "AirNFTs", "NEAR"
    # wallet = "Metamask", MATIC (Polygon's native token) or Polygon-bridged ETH
    print_trace("Mint NFT from: "+file_path_in+" to "+blockchain_name)
    print_trace("Minted NFT at: "+file_path_out)


#### SECTION 15 - End-of-Run summary functions:


def print_wall_times():
    """Prints All the timings together for consistency of output:
    """
    #print_heading("Wall times (hh:mm:sec.microsecs):")

    # For wall time of std imports:
    std_elapsed_wall_time = std_stop_datetimestamp -  std_strt_datetimestamp
    print_verbose("for import of Python standard libraries: "+ \
        str(std_elapsed_wall_time))

    # For wall time of xpt imports:
    xpt_elapsed_wall_time = xpt_stop_datetimestamp -  xpt_strt_datetimestamp
    print_verbose("for import of Python extra    libraries: "+ \
        str(xpt_elapsed_wall_time))

    pgm_stop_datetimestamp = dt.datetime.now()
    pgm_elapsed_wall_time = pgm_stop_datetimestamp -  pgm_strt_datetimestamp
    print_verbose("for whole program run: "+ \
        str(pgm_elapsed_wall_time))  # like 0:00:00.317434 Days:Hours:Mins:Secs.

    pgm_stop_perftimestamp = time.perf_counter()
    # print(str(pgm_stop_perftimestamp)+" seconds.microseconds perf time.")


def show_summary(in_seq):
    """Print summary count of files processed and the time to do them.
    """
    if SHOW_SUMMARY_COUNTS:
        pgm_stop_datetimestamp = dt.datetime.now()
        pgm_elapsed_wall_time = pgm_stop_datetimestamp - pgm_strt_datetimestamp

        if artpieces_processed_count == 1:
            print_info(f"SUMMARY: 1 artpiece gen'd"
                f" during {str(pgm_elapsed_wall_time)} Days:Hours:Mins:Secs.")
        else:
            print_info(f"SUMMARY: {artpieces_processed_count} artpieces gen'd"
                f" during {str(pgm_elapsed_wall_time)} Days:Hours:Mins:Secs")

    # TODO: Write wall times to log for longer-term analytics


#### SECTION 16 - Main calling function:

if __name__ == "__main__":
# TODO: Run this program different parameters by loading different env files.

    set_hard_coded_defaults()
    #load_env_file("???")  # read_env_file(ENV_FILE_PATH)
    # TODO: drivepath(ENV_FILE_PATH)
    # TODO: open_env_file(ENV_FILE_PATH)
    # TODO: read_env_file(ENV_FILE_PATH)  # calls print_samples()
    #if DRIVE_PATH:
    #    list_files_on_removable_drive(DRIVE_PATH)
    # TODO: eject_drive(removable_drive_path)
    read_cmd_args()  # from command line parameters at run time.
    calc_env_vars()
    sys_info()

    OUTPUT_PATH_PREFIX = define_output_path(OUTPUT_FOLDER)
    
    WATERMARKED_PATH_PREFIX = OUTPUT_PATH_PREFIX # + "-wm-"

    artpieces_processed_count = 0
    while True:
        artpieces_processed_count += 1
        
        if USE_GEMINI_API:  # Using text-to-text OpenAI Gemini service:
            hash_str = hash_file_sha256(gened_file_path) # from step above
            print_trace(str(len(hash_str))+" char SHA256 hash:"+hash_str)

        if USE_DALLE_API:  #     Using text-to-image OpenAI DALL-E service:
            gened_file_path = gen_dalle_file(artpieces_processed_count,OUTPUT_PATH_PREFIX)
        else:              # Programmatic:
            gened_file_path = gen_one_file(artpieces_processed_count,OUTPUT_PATH_PREFIX)
        # TODO: if gened_file_path is None:  # if DALL-E fails

        if SHOW_OUTPUT_FILE:   # --showout
            img = Image.open(gened_file_path)
            # Display the image:
            img.show()

        if GEN_SHA256:  # -256 --hash
            hash_str = hash_file_sha256(gened_file_path) # from step above
            print_trace(str(len(hash_str))+" char SHA256 hash:"+hash_str)

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

        if DELETE_OUTPUT_FILE:  # -del --delete
            os.remove(gened_file_path)
            print_info(f"File {gened_file_path} deleted.")
        else:
            # TODO: Upscale image using https://topazai.com (paid)
            #if UPSCALE_IMAGE_FILE:
            #    upscaled_file_path=upscale_image_file(gened_file_path)

            if ADD_WATERMARK:  # -wm --watermark
                print_info(f"File {WATERMARKED_PATH_PREFIX}")
                if USE_DALLE_API:  # Using text-to-image OpenAI DALL-E service:
                    watermarked_file_path = gen_dalle_file(artpieces_processed_count,WATERMARKED_PATH_PREFIX)
                else:              # Programmatic:
                    watermarked_file_path = gen_one_file(artpieces_processed_count,WATERMARKED_PATH_PREFIX)
                add_watermark2png(gened_file_path, watermarked_file_path, WATERMARK_TEXT)
            else:
                watermarked_file_path=gened_file_path
            #TODO: watermarked_file_found = read_watermark(watermarked_file_path)

            #TODO: create_thumbnail_png()
            #TODO: Resize mockups for different canvas sizes using free XnConvert @ xnview.com

            if ENCRYPT_FILE:  # -e --encrypt  (password protect file)
                symmetric_key_str = encrypt_symmetrically(gened_file_path,cyphertext_file_path)
                print_trace("Encrypted file: "+cyphertext_file_path+" size: "+\
                    str(get_file_size_on_disk(cyphertext_file_path)))
                #TODO: test decrypt_symmetrically(cyphertext_file_path,plaintext_file_path,symmetric_key_str) 
            else:
                cyphertext_file_path=watermarked_file_path

            if MINT_NFT:
               # Create a non-fungible token (NFT) on a blockchain using the ERC721 standard
               # https://ethereum.org/en/developers/docs/standards/tokens/erc-721/
               # https://www.youtube.com/watch?v=Q2MvYR8qFtU
               mint_nftcyphertext_file_path = mint_nft(cyphertext_file_path,BLOCKCHAIN_NAME)

            if UPLOAD_TO_QUICKNODE:  # -qn --quicknode
                quicknode_cid = upload_to_ipfs(encrypted_file_path,
                    quicknode_keyring_service_name,
                    quicknode_keyring_account_name)
                print_trace("QuickNode IPFS CID:", quicknode_cid)
            
            if GEN_QR_CODE:
               # Create QR code image file from URL:
               gen_qrcode(url,qrcode_file_path)


            # TODO: printify.com t-shirts on demand https://www.youtube.com/watch?v=TygDUR38wuM
            # TODO: API to Etsy using TaskMagic https://www.youtube.com/watch?v=1sZ5VPlThKQ
                # See I Tried Selling AI Art https://www.youtube.com/watch?v=GXPQ-fg507o
            # TODO: API to frameiteasy.com https://documenter.getpostman.com/view/7462304/Tz5s3bQB 
            # TODO: API to Facebook Marketplace https://apify.com/shmlkv/facebook-marketplace/api
            # TODO: API to artbreeder.com https://documenter.getpostman.com/view/7462304/Tz5s3bQB

        if FILES_TO_GEN > 0:   # No more files to generate.Infinite loop needs to end:
            if artpieces_processed_count >= FILES_TO_GEN:
                show_summary(artpieces_processed_count)
                print_wall_times()
                exit()  # graceful exit from infinite loop.

#        except KeyboardInterrupt:
#            # Gracefully handle manual interruption:
#            print("*** Infinite loop manually terminated by user using control+C.")

    # END While loop.