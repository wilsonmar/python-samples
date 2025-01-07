#!/usr/bin/env python3

"""mondrian-gen.py at https://github.com/wilsonmar/python-samples/blob/main/mondrian-gen.py
This program provides both local programmatic and OpenAI's DALL-E Generative AI API calls
to create a PNG-format file of art in the pure abstract Neoplasticism style
initiated in 1920s by Piet Mondrian (in Amersfort, Netherlands 1872-1944).

This was created to see whether the different ways of creating horizontal and 
vertical lines of rectangular boxes filled with primary colors
compare with the intuitive beauty of manually-created works, such as
https://res.cloudinary.com/dcajqrroq/image/upload/v1736178566/mondrian.29-compnum3-268x266_hceym9.png

CURRENT STATUS: NOT WORKING for env file retrieve.
git commit -m"v005 + API vals in Keyring :mondrian-gen.py"

Based on https://www.perplexity.ai/search/write-a-python-program-to-crea-nGRjpy0dQs6xVy9jh4k.3A#0

Tested on macOS 24.1.0 using Python 3.12.7 (main, Oct  1 2024, 02:05:46) [Clang 15.0.0 (clang-1500.3.9.4)] 
flake8  E501 line too long, E222 multiple spaces after operator

# Before running this:
1. Create a Secret Key for ChatGPT API calls at https://platform.openai.com/api-keys and 
2. Open the Keyring Access.app. Click iCloud then Login. Click the add icon at the top.
3. Fill in the Item Name "OpenAI", Account Name "johndoe", Password (the API key). Click Add.
4. In Terminal:
python3 -m venv venv
source venv/bin/activate
python3 -m pip install envcloak keyring OpenAI pycairo python-dotenv Pillow psutil pytz requests shutil timeit tzlocal
   * Downloading envcloak-0.3.0-py3-none-any.whl (59 kB) See https://github.com/Veinar/envcloak
   * Downloading keyring-25.6.0-py3-none-any.whl (39 kB)
   * Downloading pycairo-1.27.0.tar.gz (661 kB)
   * Downloading pillow-11.1.0-cp312-cp312-macosx_11_0_arm64.whl (3.1 MB)
   * Downloading psutil-6.1.1-cp36-abi3-macosx_11_0_arm64.whl (248 kB)
   * shutil ???
   * Downloading tzlocal-5.2-py3-none-any.whl.metadata (7.8 kB)

5. Scan Python program using flake8, etc.
6. Edit the program to define run parameters.
7. Run this program:
chmod +x mondrian-gen.py
./mondrian-gen.py

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

"""

# pip install pycairo (https://pycairo.readthedocs.io/en/latest/)
import cairo
from datetime import datetime, timezone

from envcloak import load_encrypted_env

import pytz

import pathlib
from pathlib import Path
from dotenv import load_dotenv

 # Based on: pip3 install python-dotenv
from dotenv import load_dotenv
from openai import OpenAI
import keyring
import requests
    # urllib is a built-in module that doesn't require additional installation.
    # But the requests library is more versatile and widely used.

# import Pillow to convert SVG to PNG file format:
from PIL import Image

import os
import shutil
import platform
import random
import subprocess
import sys
import time
from timeit import default_timer as timer
import tzlocal

# Start with program name (without ".py" file extension) such as "modrian-gen":
PROGRAM_NAME = Path(__file__).stem
    # See https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    # Instead of os.path.splitext(os.path.basename(sys.argv[0]))[0]

# Obtain variables (API key, etc.) from .env file:
use_env_file = True    # -env "python-samples.env"
global ENV_FILE_PATH
ENV_FILE_PATH="python-samples.env"
global global_env_path
USER_FOLDER = ""  # args.folder (like a mount)

# Console display option defaults:
clear_cli = True
SHOW_DEBUG = True
show_trace = True
show_fail = True
show_dates_in_logs = False

show_sys_info = True
show_heading = True
show_verbose = True

# User run preferences:
keyring_service_name = "OpenAI"
keyring_account_name = "johndoe"
USE_DALLE_API = False  # if False, use programmatic Python. True = use DELL-E

# For programmatic creation code:
WIDTH, HEIGHT = 500, 500
# TODO: Vary size and format of file to generate locally:
WIDTHxHEIGHT = str(WIDTH)+"x"+str(HEIGHT)  # for "500x500"
# For ref. by generate_mondrian(), mondrian_flood_fill(), draw_mondrian()
TILE_SIZE = 10
# TODO: Vary borderWidth = 8; minDistanceBetweenLines = 50;
   # See https://github.com/unsettledgames/mondrian-generator/blob/master/mondrian_generator.pde
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

FILES_TO_GEN = 1     # 0 = Infinite loop while in kiosk mode.
SLEEP_SECONDS = 1.0  # between files created in a loop

DATE_OUT_Z = False  # save files with Z time (in UTC time zone now) instead of local time.
OPEN_OUTPUT_FILE = True
CLOSE_OUTPUT_FILE = True
PRINT_OUTPUT_FILE_LOG = True
PRINT_OUTPUT_COUNT = True

DELETE_OUTPUT_FILE = False  # If True, recover files from Trash
SHOW_SUMMARY_COUNTS = True

# Global Constants:
# This is the pallette of primary RBG colors:
# COLORS = [(1, 1, 1), (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 1)]
# Plus green, orange, and purple:
COLORS = [(1, 1, 1), (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 1), (0, 1, 0), (1, 0.5, 0), (0.5, 0, 0.5)]
    # See https://www.schoolofmotion.com/blog/10-tools-to-help-you-design-a-color-palette


if os.name == "nt":  # Windows operating system
    SLASH_CHAR = "\\"
    # if platform.system() == "Windows":
    print(f"*** Windows Edition: {platform.win32_edition()} Version: {platform.win32_ver()}")
else:
    SLASH_CHAR = "/"

# SAVE_PATH = os.getcwd()  # cwd=current working directory (python-examples code folder)
SAVE_PATH = os.path.expanduser("~")  # user home folder path like "/User/johndoe"
if SHOW_DEBUG:
    print(f"*** DEBUG: SAVE_PATH={SAVE_PATH}")

if USER_FOLDER == "":
    # No prefix (mount) specified:
    OUTPUT_PATH_PREFIX = SAVE_PATH + SLASH_CHAR + "Downloads"
else:
    OUTPUT_PATH_PREFIX = SAVE_PATH + SLASH_CHAR + USER_FOLDER
if SHOW_DEBUG:
    print(f"*** DEBUG: OUTPUT_PATH_PREFIX={OUTPUT_PATH_PREFIX}")

# Check to make sure folder exists:
if not os.path.isdir(OUTPUT_PATH_PREFIX):  # Confirmed a directory:
    try:
        print(f"*** WARNING: Folder {OUTPUT_PATH_PREFIX} does not exist. Creating.")
        os.mkdirs(OUTPUT_PATH_PREFIX)
    except FileExistsError:
        print(f"*** FileExistsError creating {OUTPUT_PATH_PREFIX}. Exiting.")
        exit()


def local_datetime_stamp():
    """Assemble date stamp (with a time zone offset)
    """
    # Assemble output file name onto path:
    local_time = time.localtime()
    TZ_OFFSET = time.strftime("%z", local_time)
        # returns "-0700" for MST "America/Denver"
    # SYS_TIMEZONE = tzlocal.get_localzone()
        # returns "America/Denver"
    # TZ_OFFSET = datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)
        # returns timedelta object representing the offset from UTC.
    # TZ_CODE = time.tzname[0]   # returns "MST"

    if DATE_OUT_Z:  # from user preferences
        # Add using local time zone Z (Zulu) for UTC (GMT):
        now = datetime.now(timezone.utc)
        file_date_stamp = now.strftime("%Y%m%dT%H%M%SZ")
    else:
        # Add using local time zone offset:
        now = datetime.now()
        file_date_stamp = now.strftime("%Y%m%dT%H%M%S")+TZ_OFFSET
    return file_date_stamp


# Colors
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
# Styles
BOLD = '\033[1m'
RESET = '\033[0m'

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

def get_time() -> str:
    """ Generate the current local datetime. """
    now: datetime = datetime.now()
    return f'{now:%I:%M %p (%H:%M:%S) %Y-%m-%d}'

def print_separator():
    """ Put a blank line in CLI output. Used in case the technique changes throughout this code. """
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


def do_clear_cli():
    if clear_cli:
        import os
        # Make a OS CLI command:
        lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


def display_memory():
    import os, psutil  #  psutil-5.9.5
    process = psutil.Process()
    mem=process.memory_info().rss / (1024 ** 2)  # in bytes
    # print_verbose(str(process)+" memory="+str(mem)+" MiB")
    print_verbose("memory used="+str(mem)+" MiB at "+local_datetime_stamp())


def sys_info():
    if not show_sys_info:   # defined among CLI arguments
        return None
    print_heading("In sys_info()")

    from pathlib import Path
    # See https://wilsonmar.github.io/python-samples#run_env
    global user_home_dir_path
    user_home_dir_path = str(Path.home())
        # example: /users/john_doe
    print_trace("user_home_dir_path="+user_home_dir_path)
    # the . in .secrets tells Linux that it should be a hidden file.

    import platform # https://docs.python.org/3/library/platform.html
    platform_system = platform.system()
       # 'Linux', 'Darwin', 'Java', 'Win32'
    print_trace("platform_system="+str(platform_system))

    # my_os_platform=localize_blob("version")
    print_trace("my_os_version="+str(platform.release()))
    #           " = "+str(macos_version_name(my_os_version)))

    my_os_process = str(os.getpid())
    print_trace("my_os_process="+my_os_process)

    display_memory()

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
    print_trace("My Mac Serial Number="+my_mac_serial_number)

    # import psutil
    # TODO: pwuid_shell = pwd.getpwuid(os.getuid()).pw_shell     # like "/bin/zsh" on MacOS
    # preferred over os.getuid())[0]
    # Instead of: conda install psutil   # found
    # machine_uid_pw_name = psutil.Process().username()
    # print_trace("pwuid_shell="+pwuid_shell)

    # Obtain machine login name:
    # This handles situation when user is in su mode.
    # See https://docs.python.org/3/library/pwd.html
    # TODO: pwuid_gid = pwd.getpwuid(os.getuid()).pw_gid         # Group number datatype
    # TODO: print_trace("pwuid_gid="+str(pwuid_gid)+" (process group ID number)")

    # TODO: pwuid_uid = pwd.getpwuid(os.getuid()).pw_uid
    # TODO: print_trace("pwuid_uid="+str(pwuid_uid)+" (process user ID number)")

    # TODO: pwuid_name = pwd.getpwuid(os.getuid()).pw_name
    # TODO: print_trace("pwuid_name="+pwuid_name)

    # TODO: pwuid_dir = pwd.getpwuid(os.getuid()).pw_dir         # like "/Users/johndoe"
    # TODO: print_trace("pwuid_dir="+pwuid_dir)

    # Several ways to obtain:
    # See https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    # this_pgm_name = sys.argv[0]                     # = ./python-samples.py
    # this_pgm_name = os.path.basename(sys.argv[0])   # = python-samples.py
    # this_pgm_name = os.path.basename(__file__)      # = python-samples.py
    # this_pgm_path = os.path.realpath(sys.argv[0])   # = python-samples.py
    # Used by display_run_stats() at bottom:
    this_pgm_name = os.path.basename(os.path.normpath(sys.argv[0]))
    print_trace("this_pgm_name="+this_pgm_name)

    # TODO: this_pgm_last_commit = __last_commit__
        # Adapted from https://www.python-course.eu/python3_formatted_output.php
    #print_trace("this_pgm_last_commit="+this_pgm_last_commit)

    this_pgm_os_path = os.path.realpath(sys.argv[0])
    print_trace("this_pgm_os_path="+this_pgm_os_path)
    # Example: this_pgm_os_path=/Users/wilsonmar/github-wilsonmar/python-samples/python-samples.py

    # TODO: site_packages_path = site.getsitepackages()[0]
    # TODO: print_trace("site_packages_path="+site_packages_path)

    this_pgm_last_modified_epoch = os.path.getmtime(this_pgm_os_path)
    print_trace("this_pgm_last_modified_epoch="+str(this_pgm_last_modified_epoch))

    #this_pgm_last_modified_datetime = datetime.fromtimestamp(
    #    this_pgm_last_modified_epoch)
    #print_trace("this_pgm_last_modified_datetime=" +
    #            str(this_pgm_last_modified_datetime)+" (local time)")
        # Default like: 2021-11-20 07:59:44.412845  (with space between date & time)

    # Obtain to know whether to use new interpreter features:
    python_ver = platform.python_version()
        # 3.8.12, 3.9.16, etc.
    print_trace("python_ver="+python_ver)

    ### python_info():
    python_version = sys.version
        # 3.9.16 (main, Dec  7 2022, 10:16:11) [Clang 14.0.0 (clang-1400.0.29.202)]
        # 3.8.3 (default, Jul 2 2020, 17:30:36) [MSC v.1916 64 bit (AMD64)]
    print_trace("python_version="+python_version)

    print_trace("python_version_info="+str(sys.version_info))
        # Same as on command line: python -c "print_trace(__import__('sys').version)"
        # 2.7.16 (default, Mar 25 2021, 03:11:28)
        # [GCC 4.2.1 Compatible Apple LLVM 11.0.3 (clang-1103.0.29.20) (-macos10.15-objc-

    if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # major, minor, micro, release level, and serial: for sys.version_info.major, etc.
            # Version info sys.version_info(major=3, minor=7, micro=6,
            # releaselevel='final', serial=0)
        print_fail("Python 3.6 or higher is required for this program. Please upgrade.")
        sys.exit(1)

    venv_base_prefix = sys.base_prefix
    venv_prefix = sys.prefix
    if venv_base_prefix == venv_prefix:
        print_trace("venv at " + venv_base_prefix)
    else:
        print_fail("venv is different from venv_prefix "+venv_prefix)

    print_trace("__name__="+__name__)  # = __main__


    # TODO: Make this function for call before & after run:
    #    disk_list = about_disk_space()
    #    disk_space_free = disk_list[1]:,.1f / disk_list[0]:,.1f
    #    print_info(localize_blob("Disk space free")+"="+disk_space_free+" GB")
        # left-to-right order of fields are re-arranged from the function's output.


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

    for volume in volumes:
        print(f"Removable volume: {volume}")

        volume_path = os.path.join(volumes_path, volume)
        if os.path.ismount(volume_path):
            print(f"- {volume}")


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
        exit()

    try:
        # Write the content to the file
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File '{file_name}' has been successfully written to {drive_path}")
    except PermissionError:
        print(f"Permission denied. Unable to write to {drive_path}")
    except IOError as e:
        print(f"An error occurred while writing the file: {e}")


#def read_file_from_removable_drive(drive_path, file_name, content):


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


# See https://wilsonmar.github.io/python-samples/#envFile
def open_env_file(env_file) -> str:
    """Return a file path obtained from .env file based on the path provided
    in env_file coming in.
    """
    # from pathlib import Path
    # See https://wilsonmar.github.io/python-samples#run_env

    drive_path = "Volume/DriveName"
    write_file_to_removable_drive(drive_path, env_file, content)

    # Find the user's $HOME path:
    global user_home_dir_path
    user_home_dir_path = str(Path.home())
       # example: /users/john_doe
    global_env_path = user_home_dir_path + "/" + env_file  # concatenate path

    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        print("*** global_env_path "+global_env_path+" not found!")
    else:
        print_info("*** global_env_path "+global_env_path+" is readable.")

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


def get_str_from_env_file(key_in) -> str:
    """Return a value of string data type from OS environment or .env file
    (using pip python-dotenv)
    """
    # FIXME:
    env_var = os.environ.get(key_in)
    print(f"*** DEBUG: key_in={key_in} env_var={env_var}")
    exit()
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


def get_from_macos_keyring(service, account):
    """Read API Key from MacOS built-in Keyring/Passwords.app
    : service ("OpenAI")
    : account ("johndoe@gmail.com")
    for password = API key value
    """
    # import keyring
    return keyring.get_password(service, account)


def read_env_file(env_path):
    """Read .env file containing variables and values.
    See https://wilsonmar.github.io/python-samples/#envLoad
    """
    # See https://stackoverflow.com/questions/40216311/reading-in-environment-variables-from-an-environment-file

    global openai_api_key
    openai_api_key = get_str_from_env_file('OPENAI_API_KEY')
    if openai_api_key == None:
        print_error("openai_api_key="+openai_api_key+" not in "+env_path)
    else:
        print_error("openai_api_key="+openai_api_key+" in "+env_path)

    return


def get_file_timezone(file_path):
    # Get the file's modification time
    mod_time = os.path.getmtime(file_path)

    # Convert to a datetime object
    dt = datetime.fromtimestamp(mod_time)

    # Get the system's local timezone
    local_tz = datetime.now(ZoneInfo("UTC")).astimezone().tzinfo

    # Localize the datetime object
    localized_dt = dt.replace(tzinfo=local_tz)

    return localized_dt.tzinfo


def file_creation_datetime(path_to_file):
    """ Get the datetime stamp for a file, 
    falling back to when it was last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    WARNING: Use of epoch time means resolution is to the seconds (not microseconds)
    """
    if path_to_file is None:
        print(f"*** path_to_file="+path_to_file)
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
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = COLORS[grid[y][x]]
            ctx.set_source_rgb(*color)
            ctx.rectangle(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            ctx.fill()

    surface.write_to_png(filename)


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


# def setup_logger(log_file=LOGGER_FILE_PATH, console_level=logging.INFO, file_level=logging.DEBUG):
# def log_event(logger, event_type, message, level='info'):


def gen_one_file(in_seq,path_prefix):
    """Generate image and draw to a file.
    """
    func_start_timer = timer()
    # Generate Mondrian-style art in memory:
    mondrian_grid = generate_mondrian()
    func_end_timer = timer()
    func_duration = func_end_timer - func_start_timer
    if SHOW_DEBUG:
        print(f"*** DEBUG: func_duration={func_duration}.")

    file_date_stamp = local_datetime_stamp()
    output_file_path = path_prefix + SLASH_CHAR + file_date_stamp +"-"+str(in_seq)+".png"
    if SHOW_DEBUG:
       print(f"*** DEBUG: output_file_path = {output_file_path}")

    # Output to a PNG file:
    draw_mondrian(mondrian_grid, output_file_path )
    file_create_datetime = file_creation_datetime(output_file_path)
    file_bytes = get_file_size_on_disk(output_file_path)  # type = number
    if PRINT_OUTPUT_FILE_LOG:
        print(f"*** LOG: {output_file_path},{file_bytes},{func_duration:.5f}")
           # *** LOG: /Users/johndoe/Downloads/mondrian-gen-20250105T061101-0700-3.png,1912
    return output_file_path


def gen_dalle_file(in_seq,path_prefix):

    # Pull OPENAI_API_KEY as password from macOS Keyring file (and other password manager):
    print("keyring_service_name="+keyring_service_name+" "+keyring_account_name)
    import keyring
    openai_api_key = keyring.get_password(keyring_service_name, keyring_account_name)
    print("openai_api_key="+str(openai_api_key))
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

    func_start_timer = timer()
    response = client.images.generate(
        model=prompt_model,
        prompt=prompt_text,
        n=1,
        size=prompt_size
    )
    func_end_timer = timer()
    func_duration = func_end_timer - func_start_timer
    if SHOW_DEBUG:
        print(f"*** DEBUG: func_duration={func_duration}.")

    print(f"*** INFO: response.data[0].url={response.data[0].url}")
       # Example: https://oaidalleapiprodscus.blob.core.windows.net/private/org-4...
    response = requests.get(response.data[0].url)
    if response.status_code == 200:
        file_date_stamp = local_datetime_stamp()
        output_file_path = path_prefix + SLASH_CHAR + file_date_stamp +"-"+str(in_seq)+".png"
        if SHOW_DEBUG:
            print(f"*** DEBUG: output_file_path = {output_file_path}")
        with open(output_file_path, 'wb') as file:
            file.write(response.content)

        file_bytes = get_file_size_on_disk(output_file_path)  # type = number
        if PRINT_OUTPUT_FILE_LOG:
            print(f"*** LOG: {output_file_path},{file_bytes},{func_duration:.5f}")
    else:
        print('*** ERROR: Failed to download file')
        exit()

    return output_file_path


def show_summary(in_seq):

    if SHOW_SUMMARY_COUNTS:
        if processing_count == 1:
            print(f"*** SUMMARY: 1 file generated.")
        else:
            print(f"*** SUMMARY: {processing_count} files generated.")


if __name__ == "__main__":

    # start_time = timeit.default_timer()  # start the program-level timer.

    do_clear_cli()
    sys_info()
    # list_macos_volumes()
    # open_env_file(ENV_FILE_PATH)
    # read_env_file(ENV_FILE_PATH)  # calls print_samples()
    # eject_drive(removable_drive_path)

    processing_count = 0
    while True:
        processing_count += 1

        if USE_DALLE_API:  # Using text-to-image AI:
            output_file_path = gen_dalle_file(processing_count,OUTPUT_PATH_PREFIX)
        else:              # Programmatic:
            output_file_path = gen_one_file(processing_count,OUTPUT_PATH_PREFIX)

        if OPEN_OUTPUT_FILE:
            img = Image.open(output_file_path)
            # Display the image:
            img.show()

        if CLOSE_OUTPUT_FILE:  # if FILES_TO_GEN == 0:   # Not infinite loop:
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

        if DELETE_OUTPUT_FILE:
            os.remove(output_file_path)
            if SHOW_DEBUG:
                print(f"*** DEBUG: file {output_file_path} deleted.")

        if FILES_TO_GEN > 0:   # Not infinite loop:
            if processing_count >= FILES_TO_GEN:
                show_summary(processing_count)
                exit()


#        except KeyboardInterrupt:
#            print("*** Infinite loop manually terminated by user using control+C.")

    # END While loop.