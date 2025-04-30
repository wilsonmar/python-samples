#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
"""az-keyvault.py at https://github.com/wilsonmar/python-samples/blob/main/az-keyvault.py

STATUS: working on macOS Sequoia 15.3.1
No known vulnerabilities found by pip-audit -r requirements.txt
ruff check az-keyvault.py
"""

#### SECTION 01. Metadata about this program file:

__commit_date__ = "2025-04-29"
__last_commit__ = "v009 + lang rest detection :az-keyvault.py"

# Unlike regular comments in code, docstrings are available at runtime to the interpreter:
__repository__ = "https://github.com/wilsonmar/python-samples"
__author__ = "Wilson Mar"
__copyright__ = "See the file LICENSE for copyright and license info"
__license__ = "See the file LICENSE for copyright and license info"
__linkedin__ = "https://linkedin.com/in/WilsonMar"
# Using semver.org format per PEP440: change on every commit:

"""
by Wilson Mar, LICENSE: MIT
This creates the premissions needed in Azure, then 
creates a Key Vault and sets access policies.
Adds a secret, then read it.
Based on https://www.perplexity.ai/search/how-to-create-populate-and-use-Q4EyT9iYSSaVQtyUK5N31g#0

#### Before running this program:
 app.py file
Serverless function (Azure Functions)

### Prerequisites:
1. Create an .env file defining global static variables and their secret values (Account, Subscription, Tenant ID)
2. Use your email address, phone, credit card to create an account and log into Azure Portal.
3. In "Entra Admin Center" (previously Azure Active Directory) https://entra.microsoft.com/#home
4. Get a Subscription Id and Tenant Id to place in the .env file

   AIPROJECT_CONNECTION_STRING=<your-connection-string>
   See https://learn.microsoft.com/en-us/azure/ai-foundry/tutorials/copilot-sdk-create-resources?tabs=macos

5. Create a new Azure AD Enterprise application. Store the Application (client) ID in your .env file.
6. Get the app's Service Principal Id, which is similar to a user account but to access resources used by apps & services.
   See https://learn.microsoft.com/en-us/entra/architecture/service-accounts-principal
7. In CLI, get a long list of info about your account from:
   az ad sp list   # For its parms: https://learn.microsoft.com/en-us/powershell/module/microsoft.graph.applications/get-mgserviceprincipal?view=graph-powershell-1.0

    "appDisplayName": "Cortana Runtime Service",
    "appId": "81473081-50b9-469a-b9d8-303109583ecb",
    ...
       "servicePrincipalNames": [
      "81473081-50b9-469a-b9d8-303109583ecb",
      "https://cortana.ai"
    ],

?. Deploy your app with CLI command: az webapp up --runtime PYTHON:3.9 --sku B1 --logs

?. In https://entra.microsoft.com/#view/Microsoft_AAD_IAM/StartboardApplicationsMenuBlade/~/AppAppsPreview
   Click on your app in the list.
?. Under Properties, Copy the Service Principal Object ID to save the value in your .env file.
   The client_id = Application (client) ID assigned to your Azure AD app registration (service principal).
   It's required when authenticating your app or service principal programmatically.

?. Define RBAC to each Service Principal

# Add /.venv/ to .gitignore (for use by uv, instead of venv)
deactivate       # out from within venv
brew install uv  # new package manager
uv --help
uv init   # for pyproject.toml & .python-version files https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
uv lock
uv sync
uv venv  # to create an environment,
source .venv/bin/activate

uv python install 3.12
# Instead of uv pip install -r requirements.txt, uv add ...
    aiohttp   # for async features
    pathlib
    pylint 
    python-dotenv

    azure-functions
    azure-ai-contentsafety
    azure-ai-projects 
    azure-ai-inference   # instead of azure-ai-foundry
    azure-identity
    azure-keyvault-secrets
    azure-mgmt-compute
    azure-mgmt-keyvault
    azure-mgmt-network
    azure-mgmt-resource
    azure-mgmt-storage
    azure-storage-blob
    azure-ai-textanalytics==5.3.0
    click
    flask
    matplotlib   # or plotly
    numpy
    pillow
    platform   # https://docs.python.org/3/library/platform.html
    psutil  #  psutil-7.0.0
    pythonping
    pytz
    requests   # For https://microsoftlearning.github.io/AI-102-AIEngineer/Instructions/00-setup.html
    uuid
    # NOT msgraph-core           # for msgraph.core.GraphClient

source .venv/bin/activate

# Repeat this CLI command after customizing with the email you use for Azure:
uv run az-keyvault.py -v -vv -u "wmar@joliet.k12.mt.us"

PROTIP: Each function displays its own error messages. Function callers display expected responses.

REMEMBER on CLI after running uv run az-keyvault.py: deactivate

"""

#### SECTION 02: Capture pgm start date/time

# See https://bomonike.github.io/python-samples/#StartingTime
# Built-in libraries (no pip/conda install needed):
#from zoneinfo import ZoneInfo  # For Python 3.9+ https://docs.python.org/3/library/zoneinfo.html 
from datetime import datetime, timezone
import time  # for timestamp
#from time import perf_counter_ns

# To display wall clock date & time of program start:
# pgm_strt_datetimestamp = datetime.now() has been deprecated.
pgm_strt_timestamp = time.monotonic()

# TODO: Display Z (UTC/GMT) instead of local time
pgm_strt_epoch_timestamp = time.time()
pgm_strt_local_timestamp = time.localtime()
# NOTE: Can't display the dates until formatting code is run below

#### SECTION 03: Built-in Imports

# Python’s Standard library of built-in modules imported as
      # listed at https://docs.python.org/3/library/*.html
std_strt_timestamp = time.monotonic()
import argparse
import base64
# import boto3  # for aws python
from dotenv import load_dotenv   # install python-dotenv
import http.client
import json
import logging   # see https://realpython.com/python-logging/
import math
import os
import pathlib
from pathlib import Path
import platform # https://docs.python.org/3/library/platform.html
import pwd                # https://www.geeksforgeeks.org/pwd-module-in-python/
import site
import shutil     # for disk space calcs
import socket
import subprocess
import sys
import urllib.request
from urllib import request, parse, error
import uuid
std_stop_timestamp = time.monotonic()


#### SECTION 04: Import external library (from outside this program):

xpt_strt_timestamp =  time.monotonic()
try:
    import argparse
    from azure.ai.textanalytics import TextAnalyticsClient
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import ClientAuthenticationError
    import azure.functions as func
    from azure.identity import DefaultAzureCredential
    from azure.identity import ClientSecretCredential
    from azure.identity import AzureCliCredential
    from azure.keyvault.secrets import SecretClient
    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.keyvault import KeyVaultManagementClient
    from azure.mgmt.resource import SubscriptionClient
    from azure.mgmt.storage import StorageManagementClient
    # from msgraph.core import GraphClient   # doesn't work if included?
    # Microsoft Authentication Library (MSAL) for Python
    # integrates with the Microsoft identity platform. It allows you to sign in users or apps with Microsoft identities (Microsoft Entra ID, External identities, Microsoft Accounts and Azure AD B2C accounts) and obtain tokens to call Microsoft APIs such as Microsoft Graph or your own APIs registered with the Microsoft identity platform. It is built using industry standard OAuth2 and OpenID Connect protocols
    # See https://github.com/AzureAD/microsoft-authentication-library-for-python?tab=readme-ov-file
    #import click
    from pathlib import Path
    import psutil  #  psutil-5.9.5
    from pythonping import ping
    import pytz
    import requests
    import uuid
except Exception as e:
    print(f"Python module import failed: {e}")
    # pyproject.toml file exists
    print("Please activate your virtual environment:\n")
    print("    source .venv/bin/activate")
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    exit(9)
xpt_stop_timestamp =  time.monotonic()



#### SECTION 05: Print Utility Functions:

## Global variables: Colors Styles:
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
    GRAY = '\033[90m'

    RESET = '\033[0m'   # switch back to default color


def print_separator():
    """A function to put a blank line in CLI output. Used in case the technique changes throughout this code.
    """
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
            print('***', get_log_datetime(), bcolors.FAIL, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.FAIL, f'{text_in}', bcolors.RESET)

def print_error(text_in):  # when a programming error is evident
    if show_fail:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.ERROR, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.ERROR, f'{text_in}', bcolors.RESET)

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

def no_newlines(in_string):
    """Strip new line from in_string
    """
    return ''.join(in_string.splitlines())

def print_secret(in_string):
    """TODO: Display secret in shortened string.
    """
    return in_string

def print_samples():
    """Display what different type of output look like.
    """
    # See https://wilsonmar.github.io/python-samples/#PrintColors
    if not show_print_samples:
        return None
    print_heading("show_print_samples")
    print_fail("sample fail")
    print_error("sample error")
    print_warning("sample warning")
    print_todo("sample task to do")
    print_info("sample info")
    print_verbose("sample verbose")
    print_trace("sample trace")
    print_secret("1234567890123456789")
    return True



#### SECTION 06: Parameters from call arguments:
# USAGE: uv run az-keyvault.py -kv "kv-westcentralus-897e56" -s "westcentralus2504" -v -vv

parser = argparse.ArgumentParser(description="Azure Key Vault")
parser.add_argument("-q", "--quiet", action="store_true", help="Quiet")
parser.add_argument("-v", "--verbose", action="store_true", help="Show each download")
parser.add_argument("-vv", "--debug", action="store_true", help="Show debug")
parser.add_argument("-l", "--log", help="Log to external file")

parser.add_argument("-u", "--user", help="User email (for credential)")
parser.add_argument("-z", "--zip", help="6-digit Zip code (in USA)")
parser.add_argument("-sub", "--subscription", help="Subscription ID (for costing)")
parser.add_argument("-kv", "--keyvault", help="KeyVault Namo")
parser.add_argument("-st", "--storage", help="Storage Name")
parser.add_argument("-t", "--text", help="Text input (for language detection)")

# -h = --help (list arguments)
args = parser.parse_args()

show_fail = True       # Always show
show_error = True      # Always show

SHOW_QUIET = args.quiet
if SHOW_QUIET:  # -vv
    show_warning = False   # -wx  Don't display warning
    show_todo = False      # -td  Display TODO item for developer
    show_info = False      # -qq  Display app's informational status and results for end-users
else:
    show_warning = True    # -wx  Don't display warning
    show_todo = True       # -td  Display TODO item for developer
    show_info = True       # -qq  Display app's informational status and results for end-users

SHOW_VERBOSE = args.verbose
if SHOW_VERBOSE:  # -vv
    SHOW_SUMMARY = True
    show_heading = True    # -q  Don't display step headings before attempting actions
    show_verbose = True    # -v  Display technical program run conditions
    show_sys_info = True
else:
    show_heading = False    # -q  Don't display step headings before attempting actions
    show_verbose = False   # -v  Display technical program run conditions
    show_sys_info = False

SHOW_DEBUG = args.debug  # print metadata before use by code during troubleshooting
if SHOW_DEBUG:  # -vv
    show_trace = True      # -vv Display responses from API calls for debugging code
else:
    show_trace = False     # -vv Display responses from API calls for debugging code

show_secrets = False   # Never show
show_dates_in_logs = False
LOG_DOWNLOADS = args.log

AZURE_ACCT_NAME = args.user
AZURE_SUBSCRIPTION_ID = args.subscription

KEYVAULT_NAME = args.keyvault  # also used as resource group name
STORAGE_ACCOUNT_NAME = args.storage

TEXT_INPUT = args.text
if not TEXT_INPUT:
    TEXT_INPUT = "The quick brown fox jumps over the lazy dog"

# if args.zip in get_longitude_latitude()


ENV_FILE="python-samples.env"

# TODO: Make these configurable
DELETE_RG_AFTER = True
DELETE_KV_AFTER = True
LIST_ALL_PROVIDERS = False

# PROTIP: Global variable referenced within functions:
# values obtained from .env file can be overriden in program call arguments:
 

#### SECTION 07: Python script control utilities:


# See https://bomonike.github.io/python-samples/#ParseArguments

def do_clear_cli():
    # import os
    # QUESTION: What's the output variable?
    lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


def set_cli_parms(count):
    """Present menu and parameters to control program
    """
    # import click
    @click.command()
    @click.option('--count', default=1, help='Number of greetings.')
    #@click.option('--name', prompt='Your name',
    #              help='The person to greet.')
    def set_cli_parms(count):
        for x in range(count):
            click.echo("Hello!")
    # Test by running: ./python-examples.py --help


def open_env_file(env_file) -> str:
    """Return a Boolean obtained from .env file based on key provided.
    """
    # from pathlib import Path
    # See https://wilsonmar.github.io/python-samples#run_env
    global user_home_dir_path
    user_home_dir_path = str(Path.home())
       # example: /users/john_doe

    global_env_path = user_home_dir_path + "/" + env_file  # concatenate path

    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        print_error(global_env_path+" (global_env_path) not found!")
    #else:
    #    print_info(global_env_path+" (global_env_path) readable.")

    path = pathlib.Path(global_env_path)
    # Based on: pip3 install python-dotenv
    # from dotenv import load_dotenv
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
    # TODO: Default ENV_FILE name:
    ENV_FILE="python-samples.env"

    env_var = os.environ.get(key_in)
    if not env_var:  # yes, defined=True, use it:
        print_warning(key_in + " not found in OS nor .env file: " + ENV_FILE)
        return None
    else:
        # PROTIP: Display only first characters of a potentially secret long string:
        if len(env_var) > 5:
            print_trace(key_in + "=\"" + str(env_var[:5]) +" (remainder removed)")
        else:
            print_trace(key_in + "=\"" + str(env_var) + "\" from .env")
        return str(env_var)


def print_env_vars():
    """List all environment variables, one line each using pretty print (pprint)
    """
    # import os
    # import pprint
    environ_vars = os.environ
    print_heading("User's Environment variable:")
    pprint.pprint(dict(environ_vars), width = 1)


#### SECTION 08: Time Utility Functions:


def get_user_local_time() -> str:
    """ 
    Returns a string formatted with datetime stamp in local timezone.
    Example: "07:17 AM (07:17:54) 2025-04-21 MDT"
    """
    now: datetime = datetime.now()
    local_tz = datetime.now(timezone.utc).astimezone().tzinfo
    return f'{now:%I:%M %p (%H:%M:%S) %Y-%m-%d} {local_tz}'


def get_log_datetime() -> str:
    """
    Returns a formatted datetime string in UTC (GMT) timezone so all logs are aligned.
    Example: 2504210416UTC for a minimal with year, month, day, hour, minute, second and timezone code.
    """
    #from datetime import datetime
    # importing timezone from pytz module
    #from pytz import timezone

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


def print_wall_times():
    """Prints All the timings together for consistency of output:
    Instead of datetime.datetime.now(), time.perf_counter(), time.monotonic()
    """
    print_heading("Wall times (hh:mm:sec.microsecs):")
    # TODO: Write to log for longer-term analytics

    # For wall time of std imports:
    std_elapsed_wall_time = std_stop_timestamp -  std_strt_timestamp
    print_verbose("for import of Python standard libraries: "+ \
        f"{std_elapsed_wall_time:.4f}")

    # For wall time of xpt imports:
    xpt_elapsed_wall_time = xpt_stop_timestamp -  xpt_strt_timestamp
    print_verbose("for import of Python extra    libraries: "+ \
        f"{xpt_elapsed_wall_time:.4f}")

    pgm_stop_timestamp =  time.monotonic()
    pgm_elapsed_wall_time = pgm_stop_timestamp -  pgm_strt_timestamp
    # pgm_stop_perftimestamp = time.perf_counter()
    print_verbose("for whole program run:                   "+ \
        f"{pgm_elapsed_wall_time:.4f}")



#### SECTION 09. Obtain program environment metadata


# See https://bomonike.github.io/python-samples/#run_env

def os_platform():
    """Return a friendly name for the operating system
    """
    #import platform # https://docs.python.org/3/library/platform.html
    platform_system = str(platform.system())
       # 'Linux', 'Darwin', 'Java', 'Windows'
    print_trace("platform_system="+str(platform_system))
    if platform_system == "Darwin":
        my_platform = "macOS"
    elif platform_system == "linux" or platform_system == "linux2":
        my_platform = "Linux"
    elif platform_system == "win32":  # includes 64-bit
        my_platform = "Windows"
    else:
        print_fail("platform_system="+platform_system+" is unknown!")
        exit(1)  # entire program
    return my_platform

def macos_version_name(release_in):
    """Returns the marketing name of macOS versions which are not available
    from the running macOS operating system.
    """
    # NOTE: Return value is a list!
    # This has to be updated every year, so perhaps put this in an external library so updated
    # gets loaded during each run.
    # Apple has a way of forcing users to upgrade, so this is used as an
    # example of coding.
    # FIXME: https://github.com/nexB/scancode-plugins/blob/main/etc/scripts/homebrew.py
    # See https://support.apple.com/en-us/HT201260 and https://www.wikiwand.com/en/MacOS_version_history
    MACOS_VERSIONS = {
        '22.7': ['Next2024', 2024, '24'],
        '22.6': ['macOS Sonoma', 2023, '23'],
        '22.5': ['macOS Ventura', 2022, '13'],
        '12.1': ['macOS Monterey', 2021, '21'],
        '11.1': ['macOS Big Sur', 2020, '20'],
        '10.15': ['macOS Catalina', 2019, '19'],
        '10.14': ['macOS Mojave', 2018, '18'],
        '10.13': ['macOS High Sierra', 2017, '17'],
        '10.12': ['macOS Sierra', 2016, '16'],
        '10.11': ['OS X El Capitan', 2015, '15'],
        '10.10': ['OS X Yosemite', 2014, '14'],
        '10.9': ['OS X Mavericks', 2013, '10.9'],
        '10.8': ['OS X Mountain Lion', 2012, '10.8'],
        '10.7': ['OS X Lion', 2011, '10.7'],
        '10.6': ['Mac OS X Snow Leopard', 2008, '10.6'],
        '10.5': ['Mac OS X Leopard', 2007, '10.5'],
        '10.4': ['Mac OS X Tiger', 2005, '10.4'],
        '10.3': ['Mac OS X Panther', 2004, '10.3'],
        '10.2': ['Mac OS X Jaguar', 2003, '10.2'],
        '10.1': ['Mac OS X Puma', 2002, '10.1'],
        '10.0': ['Mac OS X Cheetah', 2001, '10.0'],
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
    release = '.'.join(release_in.split(".")[:2])  # ['10', '15', '7']
    macos_info = MACOS_VERSIONS[release]  # lookup for ['Monterey', 2021]
    print_trace("macos_info="+str(macos_info))
    print_trace("macos_platform_release="+macos_platform_release)
    return macos_platform_release


def macos_sys_info():
    if not show_sys_info:   # defined among CLI arguments
        return None
    print_heading("macos_sys_info():")

        # or socket.gethostname()
    my_platform_node = platform.node()
    print_trace("my_platform_node = "+my_platform_node + " (machine name)")

    # print_trace("env_file = "+env_file)
    print_trace("user_home_dir_path = "+user_home_dir_path)
    # the . in .secrets tells Linux that it should be a hidden file.

    # import platform # https://docs.python.org/3/library/platform.html
    platform_system = platform.system()
       # 'Linux', 'Darwin', 'Java', 'Win32'
    print_trace("platform_system = "+str(platform_system))

    # my_os_platform=localize_blob("version")
    print_trace("my_os_version = "+str(platform.release()))
    #           " = "+str(macos_version_name(my_os_version)))

    my_os_process = str(os.getpid())
    print_trace("my_os_process = "+my_os_process)

    my_os_uname = str(os.uname())
    print_trace("my_os_uname = "+my_os_uname)
        # MacOS version=%s 10.14.6 # posix.uname_result(sysname='Darwin',
        # nodename='NYC-192850-C02Z70CMLVDT', release='18.7.0', version='Darwin
        # Kernel Version 18.7.0: Thu Jan 23 06:52:12 PST 2020;
        # root:xnu-4903.278.25~1/RELEASE_X86_64', machine='x86_64')

    # import pwd   #  https://zetcode.com/python/os-getuid/
    pwuid_shell = pwd.getpwuid(os.getuid()).pw_shell     # like "/bin/zsh" on MacOS
    # preferred over os.getuid())[0]
    # Instead of: conda install psutil   # found
    # import psutil

    # machine_uid_pw_name = psutil.Process().username()
    print_trace("pwuid_shell = "+pwuid_shell)

    # Obtain machine login name:
    # This handles situation when user is in su mode.
    # See https://docs.python.org/3/library/pwd.html
    pwuid_gid = pwd.getpwuid(os.getuid()).pw_gid         # Group number datatype
    print_trace("pwuid_gid = "+str(pwuid_gid)+" (process group ID number)")

    pwuid_uid = pwd.getpwuid(os.getuid()).pw_uid
    print_trace("pwuid_uid = "+str(pwuid_uid)+" (process user ID number)")

    pwuid_name = pwd.getpwuid(os.getuid()).pw_name
    print_trace("pwuid_name = "+pwuid_name)

    pwuid_dir = pwd.getpwuid(os.getuid()).pw_dir         # like "/Users/johndoe"
    print_trace("pwuid_dir = "+pwuid_dir)

    # Several ways to obtain:
    # See https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    # this_pgm_name = sys.argv[0]                     # = ./python-samples.py
    # this_pgm_name = os.path.basename(sys.argv[0])   # = python-samples.py
    # this_pgm_name = os.path.basename(__file__)      # = python-samples.py
    # this_pgm_path = os.path.realpath(sys.argv[0])   # = python-samples.py
    # Used by display_run_stats() at bottom:
    this_pgm_name = os.path.basename(os.path.normpath(sys.argv[0]))
    print_trace("this_pgm_name = "+this_pgm_name)

    #this_pgm_last_commit = __last_commit__
    #    # Adapted from https://www.python-course.eu/python3_formatted_output.php
    #print_trace("this_pgm_last_commit = "+this_pgm_last_commit)

    this_pgm_os_path = os.path.realpath(sys.argv[0])
    print_trace("this_pgm_os_path = "+this_pgm_os_path)
    # Example: this_pgm_os_path=/Users/wilsonmar/github-wilsonmar/python-samples/python-samples.py

    # import site
    site_packages_path = site.getsitepackages()[0]
    print_trace("site_packages_path = "+site_packages_path)

    this_pgm_last_modified_epoch = os.path.getmtime(this_pgm_os_path)
    print_trace("this_pgm_last_modified_epoch = "+str(this_pgm_last_modified_epoch))

    #this_pgm_last_modified_datetime = datetime.fromtimestamp(
    #    this_pgm_last_modified_epoch)
    #print_trace("this_pgm_last_modified_datetime=" +
    #            str(this_pgm_last_modified_datetime)+" (local time)")
        # Default like: 2021-11-20 07:59:44.412845  (with space between date & time)

    # Obtain to know whether to use new interpreter features:
    python_ver = platform.python_version()
        # 3.8.12, 3.9.16, etc.
    print_trace("python_ver = "+python_ver)

    # python_info():
    python_version = no_newlines(sys.version)
        # 3.9.16 (main, Dec  7 2022, 10:16:11) [Clang 14.0.0 (clang-1400.0.29.202)]
        # 3.8.3 (default, Jul 2 2020, 17:30:36) [MSC v.1916 64 bit (AMD64)]
    print_trace("python_version = "+python_version)

    print_trace("python_version_info = "+str(sys.version_info))
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
    print_trace("venv_base_prefix = " + venv_base_prefix)
    venv_prefix = sys.prefix
    print_trace("     venv_prefix = " + venv_prefix)
    #if venv_base_prefix != venv_prefix:
    #    print_info("venv_prefix is different from venv_base_prefix!")

    # print_trace("__name__="+__name__)  # = __main__


    # TODO: Make this function for call before & after run:
    #    disk_list = get_disk_free()
    #    disk_space_free = disk_list[1]:,.1f / disk_list[0]:,.1f
    #    print_info(localize_blob("Disk space free")+"="+disk_space_free+" GB")
        # left-to-right order of fields are re-arranged from the function's output.


def get_mem_used() -> str:
    # import os, psutil  #  psutil-5.9.5
    process = psutil.Process()
    mem=process.memory_info().rss / (1024 ** 2)  # in bytes
    print_trace(str(process))
    return str(mem)
    # to print_verbose("get_mem_used(): "+str(mem)+" MiB used.")


def get_disk_free():
    # import shutil
    # Replace '/' with your target path (e.g., 'C:\\' on Windows)
    usage = shutil.disk_usage('/')
    pct_free = ( float(usage.free) / float(usage.total) ) * 100
    gb = 1024 * 1024 * 1024
    disk_gb_free = float(usage.free) / gb
    return f"{disk_gb_free:.2f} ({pct_free:.2f}%)"


def handle_fatal_exit():
    """
    Handle fatal exit with a message first.
    """
    print_trace("handle_fatal_exit() called.")
    sys.exit(9)



#### SECTION 10. Cloud utilities:


def measure_http_latency(storage_account_name, attempts=5) -> str:
    """
    Returns the HTTP latency to a storage account within the Azure cloud.
    """
    # import requests
    # import time

    url = storage_account_name + ".blob.core.windows.net"
    latencies = []
    for _ in range(attempts):
        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            latency = (time.time() - start) * 1000  # ms
            latencies.append(latency)
        except requests.RequestException:
            # FIXME: <Error data-darkreader-white-flash-suppressor="active">
            # <Code>InvalidQueryParameterValue</Code>
            # <Message>
            # Value for one of the query parameters specified in the request URI is invalid. RequestId:3b433e32-d01e-003f-274c-b37a10000000 Time:2025-04-22T06:06:36.7748787Z
            # </Message>
            # <QueryParameterName>comp</QueryParameterName>
            # <QueryParameterValue/>
            # <Reason/>
            # </Error>
            latencies.append(None)

    valid_latencies = [l for l in latencies if l is not None]
    if valid_latencies:
        avg_latencies = sum(valid_latencies)/len(valid_latencies)
        print_info(f"HTTP latency to : avg {avg_latencies:.2f} ms")
    else:
        print_error(f"measure_http_latency(): requests failed to {url}")
        return None


#### SECTION 11. Geo utility APIs:


def get_ip_address() -> str:
    """
    Returns IP address of client running this program.
    TODO: If this is running as a web server (like Flask or Django), extract it from the request headers
    from the user making a request to your site:
    See https://www.perplexity.ai/search/python-code-to-get-client-ip-a-6au51O4RTtO_NY2pImnyrw#0
    """
    try:
        ext_ip_address = requests.get('https://api.ipify.org').text
        # import socket  (built-in)
        hostname = socket.gethostname()
        int_ip_address = socket.gethostbyname(hostname)
        print_info(f"get_ip_address(): \"{int_ip_address}\" for hostname \"{hostname}\" ")
        print_info(f"get_ip_address(): \"{ext_ip_address}\" ... ")
        return ext_ip_address
    except Exception as e:   
        print_error(f"get_ip_address(): {e}")
        return None


def get_ip_geo_coordinates(ip_address=None) -> (str, str):
    """
    Returns latitude and longitude for a given IP address by calling the DistanceMatrix API.
    # CODING EXAMPLE: Return of two variable values that travel together.
    """
    # Validate ip_address input:
    if not ip_address:
        ip_address = get_ip_address()
        print_verbose(f"get_ip_geo_coordinates(using: \"{ip_address}\" ... ")
    if not ip_address:
        print_error("get_ip_geo_coordinates() ip_address not valid/specified!")
        return None, None

    # Try getting latitude and longitude from IP address by calling the ip2geotools 
    try:  # no API key needed for limited ipapi.co free tier:
        url = f'https://ipapi.co/{ip_address}/json/'
        response = requests.get(url).json()
        latitude = response.get('latitude')
        longitude = response.get('longitude')
        print_info(f"get_ip_geo_coordinates({ip_address}): lat={latitude} & lng={longitude}")
        return latitude, longitude
    except Exception as e:   
        print_error(f"get_ip_geo_coordinates(ipapi.co call): {e}")
        return None, None


def get_geo_coordinates(zip_code) -> (float, float):
    """
    Returns latitude and longitude for a given zip code by calling the DistanceMatrix API.
    # CODING EXAMPLE: Return of two variable values that travel together.
    """
    # Validate zip_code input:
    if not zip_code:
        print_error("get_geo_coordinates() zip_code not valid/specified!")
    
        # OPTION C: Try getting latitude and longitude from IP address by calling the ip2geotools 
        latitude, longitude = get_ip_geo_coordinates("")
        print_verbose(f"get_geo_coordinates(): lat={latitude} & lng={longitude}")
        print("MAIN DEBUGGING")
        exit()
    # Instead of DISTANCEMATRIX_API_KEY = get_str_from_env_file('DISTANCEMATRIX_API_KEY')
    try:
        DISTANCEMATRIX_API_KEY = os.environ["DISTANCEMATRIX_API_KEY"]
    except KeyError:   
        print_error("get_geo_coordinates() DISTANCEMATRIX_API_KEY not specified in .env file!")
        pass

    if not DISTANCEMATRIX_API_KEY:
        print_error("get_geo_coordinates() DISTANCEMATRIX_API_KEY not specified in .env file!")
        return None, None

    # Construct the API URL: CAUTION: This is a paid API, so do not expose the API key in logs.
    url = f'https://api.distancematrix.ai/maps/api/geocode/json?address={zip_code}&key={DISTANCEMATRIX_API_KEY}' 
    print_verbose(f"get_geo_coordinates() zip: \"{zip_code}\" URL = \"{url}\" ")
    try:
        # import requests
        response = requests.get(url)
        data = response.json()    # Parse JSON response
        #print("data=",data)
        # data={'result': [{'address_components': [{'long_name': 'mountain view', 'short_name': 'mountain view', 'types': ['locality']}, {'long_name': 'ca', 'short_name': 'ca', 'types': ['state']}, {'long_name': 'usa', 'short_name': 'usa', 'types': ['country']}], 'formatted_address': 'Mountain View, CA, USA',
        # 'geometry': {'location': {'lat': 37.418918000000005, 'lng': -122.07220494999999}, 'location_type': 'APPROXIMATE',
        # 'viewport': {'northeast': {'lat': 37.418918000000005, 'lng': -122.07220494999999},
        # 'southwest': {'lat': 37.418918000000005, 'lng': -122.07220494999999}}},
        # 'place_id': '', 'plus_code': {}, 'types': ['locality', 'political']}], 'status': 'OK'}
    except Exception as e:
        print_error(f"get_geo_coordinates(\"{zip_code}\") {e}")
        return None, None

    if data['status'] == 'OK':
        # Extract latitude and longitude
        latitude = data['result'][0]['geometry']['location']['lat']
        longitude = data['result'][0]['geometry']['location']['lng']
        print_verbose(f"get_geo_coordinates(\"{zip_code}\") is at lat={latitude} & lng={longitude}")
        return latitude, longitude
    else:
        print_error(f"get_geo_coordinates(\"{zip_code}\") failed: {data}")
        return None, None


def get_longitude_latitude() -> (float, float):
    """
    Returns longitude and latitude, determined various ways:
    A. From parm --zipcode which calls the DistanceMatrix API.
    B. From .env file containing "MY_LONGITUDE" and "MY_LATITUDE" variable values
    C. From lookup based on user's IP address.
    D. From hard-coded defaults.
    """
    # NOTE: No parms -lat & -long defined.

    # OPTION A. From parm --zipcode, which calls the DistanceMatrix API.
    if args.zip:
        zip_code = args.zip   # zip_code = ' '.join(map(str, args.zip))   # convert list from parms to string.
        print_trace(f"get_longitude_latitude() -zip: \"{zip_code}\" ")
        latitude, longitude = get_geo_coordinates(zip_code)
    else:  
        # OPTION B. From .env file containing "MY_LONGITUDE" and "MY_LATITUDE" variable values
        try:
            latitude = float(os.environ["MY_LATITUDE"])
            # latitude = get_str_from_env_file('MY_LATITUDE')
            print_info(f"MY_LATITUDE = \"{latitude:.7f}\"  # (North/South) from .env being used. ")
        except KeyError:   
            latitude = 0
            pass  # do below.

        try:
            longitude = float(os.environ["MY_LONGITUDE"])
            # longitude = get_str_from_env_file('MY_LONGITUDE')
            print_info(f"MY_LONGITUDE = \"{longitude:.7f}\"  # (East/West of GMT) from .env being used. ")
        except KeyError:   
            longitude = 0
            pass  # do below.

    if not (latitude and longitude):
        ip_address = get_ip_address()
        if ip_address:
            # print_info(f"get_ip_address() = \"{ip_address}\"")
            latitude, longitude = get_ip_geo_coordinates(ip_address)
            print_verbose(f"get_longitude_latitude() latitude={str(latitude)} longitude={str(longitude)} from {ip_address}")
    
    if not (latitude and longitude):
        # OPTION D. From hard-coded default values (for demos of how other parts of this program runs)
        latitude = 34.123
        print_warning(f"get_longitude_latitude() latitude={latitude:.7f} from default!")
        longitude = -104.322
        print_warning(f"get_longitude_latitude() longitude={longitude:.7f} from default!")

    if latitude and longitude:
        # format response:
        latitude_direction = "North" if latitude >= 0 else "South"
        longitude_direction = "West" if longitude >= 0 else "East"
        print_info(f"get_longitude_latitude() latitude={latitude:.7f} {latitude_direction}, longitude={longitude:.7f} {longitude_direction}")
        return latitude, longitude
    else:
        print_error("get_longitude_latitude() failed to get values!")
        return None, None


def get_elevation(longitude, latitude, units='Meters', service='google' ) -> str:
    """
    Returns elevation in metric meters or imperial (US) feet for the given longitude and latitude
    using the USGS (US Geologic Survey's National Map's Elevation Point Query Service Digital Elevation Model (DEM) at
    https://apps.nationalmap.gov/epqs/ version 1.0.0 returning error!
    https://epqs.nationalmap.gov/v1/docs
    Alternatives: Google Earth: Provides altitude data in its desktop application.
        Third-party tools offer elevation estimates but require manual input of coordinates:
            Freemaptools.com, MapCoordinates.net, DaftLogic.com
    No retries sessions as in https://www.perplexity.ai/search/python-code-to-obtain-elevatio-mtFsgRSgQXie68kzKDrVmw
    """
    print_trace(f"get_elevation(longitude={longitude} latitude={latitude}")
    try:
        # import requests
        if service == 'freemaptools':
            # WARNING: Freemaptools' API endpoint and parameters are undocumented here
            # This is a hypothetical implementation
            url = 'https://www.freemaptools.com/ajax/elevation-service.ashx'
            params = {"lat": latitude, "lng": longitude}
            response = requests.get(url, params=params)
            elevation = response.json()['elevation']
        
        # Alternative services from search results
        elif service == 'google':
            url = 'https://maps.googleapis.com/maps/api/elevation/json'
            # https://console.cloud.google.com/google/maps-apis/credentials?hl=en&project=stoked-woods-362514
            # TODO: Get API Key from https://cloud.google.com/maps-platform => mapsplatform
            try:
                api_key = os.environ["GOOGLE_API_KEY"]
            except KeyError:   
                print_error("get_geo_cget_elevationoordinates() GOOGLE_API_KEY not specified in .env file!")
                return None
            params = {"locations": f"{latitude},{longitude}", "key": api_key}
            print_trace(f"get_elevation() params={params}")
            data = requests.get(url, params=params).json()
            print_trace(f"get_elevation() response={data}")
            elevation = data['results'][0]['elevation']
        
        elif service == 'national_map':
            url = 'https://nationalmap.gov/epqs/pqs.php'
            params = {'x': longitude, 'y': latitude, 'units': 'Meters', 'output': 'json'}
            data = requests.get(url, params=params).json()
            # FIXME: Expecting value: line 1 column 1 (char 0) 
            elevation = data['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation']

    except (requests.exceptions.RequestException, KeyError) as e:
        print_error(f"get_elevation(): ERROR {e}")
        # https://www.perplexity.ai/search/what-is-cause-of-error-expecti-K3fjy0UGQwSOivoS3YQQ9g#0
        return None

    print_info(f"get_elevation() elevation={elevation}")  # Example: 
    return elevation if elevation != -1000000 else None

# print(get_elevation(39.7392, -104.9903, service='google', api_key='YOUR_KEY'))



#### SECTION 12. Azure cloud core utilities:


def get_acct_credential() -> object:
    """
    Returns an Azure cloud credential object for the given user account name (email)
    for local development after CLI:
    az cloud set -n AzureCloud   # return to Public Azure.
    az login
    """
    if AZURE_ACCT_NAME:  # defined by parameter:
        print_info(f"-u or -user \"{AZURE_ACCT_NAME}\"  # (AZURE_ACCT_NAME) being used.")
        my_acct_name = AZURE_ACCT_NAME
        pass   # to get credential object
    else:   # see if .env file has a value:
        try:
            my_acct_name = os.environ["AZURE_ACCT_NAME"]
            print_info(f"AZURE_ACCT_NAME = \"{my_acct_name}\"  # from .env file being used.")
        except Exception:
            print_error("-u or -user in parms or AZURE_ACCT_NAME in .env not provided in get_acct_credential()")
            exit(9)

    # TODO: For Web Applications (e.g., Flask, Django) with Azure AD Authentication.
    # For Azure App Service (Web Apps) with Built-in Authentication

    try:
        # from azure.identity import AzureCliCredential
        # from azure.mgmt.resource import SubscriptionClient
        # from azure.core.exceptions import ClientAuthenticationError
        credential = AzureCliCredential()
        # credential = DefaultAzureCredential()
        print_verbose(f"get_acct_credential(): \"{str(credential)}\")")
        subscription_client = SubscriptionClient(credential)
        subscriptions = list(subscription_client.subscriptions.list())
        print_verbose("User \"{my_acct_name}\" is logged in to Azure at get_acct_credential().")
                #blob_service_client = BlobServiceClient(
        #    account_url="https://{az_acct_name}.blob.core.windows.net",
        #    credential=credential
        #)
        return credential  # as logged in to Azure.
            # <azure.identity._credentials.default.DefaultAzureCredential object at 0x106be6ba0>
    except ClientAuthenticationError:
        print_fail("Please run CLI command: 'az login' (with authentication) and select Subscription.")
        exit(9)
    except blob_service_client.exceptions.HTTPError as errh:
        print_error("get_acct_credential() HTTP Error:", errh)
    except blob_service_client.exceptions.ConnectionError as errc:
        print_error("get_acct_credential() Connection Error:", errc)
    except blob_service_client.exceptions.Timeout as errt:
        print_error("get_acct_credential() Timeout Error:", errt)
    except blob_service_client.exceptions.RequestException as err:
        print_error("get_acct_credential() Other Error:", err)
    return None


def get_user_principal_id(credential) -> str:
    """
    Returns the singed-in user's principal object ID string.
    Equivlent of CLI: az ad signed-in-user show --query id -o tsv
    """
    #from azure.identity import DefaultAzureCredential
    try:
        token = credential.get_token("https://graph.microsoft.com/.default").token
        # print_trace(f"get_user_principal_id() token: "+ token)
        print_trace(f"get_user_principal_id() token size: {len(token)}")
    except Exception as e:
        print_error(f"get_user_principal_id() token ERROR: {e}")
        return None

    try:
        # Call Microsoft Graph to get the signed-in user's details:
        # Call the /me endpoint on Microsoft Graph for the signed-in user's profile:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        # import requests
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers=headers
        )
        # Extract from the returned profile the id field (the Azure AD object ID):
        response.raise_for_status()
        user = response.json()
        user_principal_id = user.get('id')
        return user_principal_id
    except Exception as e:
        print_error(f"get_user_principal_id() ERROR: {e}")
        return None


# def job roles permissions RBAC:
    """
    The different personas/roles in an enterprise, each with job-relevant dashboards and alerts:
    A. TechOps (SREs) who establish, troubleshoot, and restore the services (CA, dashbords, alerts) that others to operate. See https://github.com/bregman-arie/sre-checklist
    B. SecOps who enable people, Web (Flask, Django, FastAPI) apps & Serverless Functios accessing secrets based on RBAC policies
    C. Managers with authority to permanently delete (purge) secrets and backups https://learn.microsoft.com/en-us/azure/key-vault/policy-reference
    D. AppDevs who request, obtain, use, rotate secrets (but not delete) access to Networks, Apps. and Functions
    E. End Users who make use of Networks, Apps. and Functions built by others
    F. DataOps to regularly backup and rotate secrets, manage log storage. Data governance. Migrate data.
    """


def use_app_credential(tenant_id, client_id, client_secret) -> object:
    """
    Returns a credential object after app registration
    no need for CLI az login.
    """
    try:
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        return credential
    except Exception as e:
        print(f"use_app_credential() ERROR: {e}")
        return None


def get_azure_subscription_id(credential) -> str:
    """
    Returns subscription ID string from credential object.
    Equivalent of CLI to list: az account show --query id --output tsv
    Portal: https://portal.azure.com/#@jetbloom.com/resource/subscriptions/15e19a4e-ca95-4101-8e5f-8b289cbf602b/overview
    """
    if AZURE_SUBSCRIPTION_ID:  # defined by parameter:
        print_info(f"-sub or -subscription \"{AZURE_SUBSCRIPTION_ID}\"  # (AZURE_SUBSCRIPTION_ID) being used.")
        return AZURE_SUBSCRIPTION_ID
    else:   # see if .env file has a value:
        print_trace(f"get_azure_subscription_id( \"{str(credential)}\" ")
        try:
            subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
            print_info(f"AZURE_SUBSCRIPTION_ID = \"{subscription_id}\"  # from .env file being used.")
            return subscription_id
        except Exception:
            print_fail("-sub or -subscription / AZURE_SUBSCRIPTION_ID in .env not defined for get_azure_subscription_id()")
            pass  # to below to get a subscription_id
        finally:
            pass

    # Authenticate using Azure CLI credentials
    # credential = AzureCliCredential()  <- from function input.

    # Initialize the SubscriptionClient:
    # from azure.identity import AzureCliCredential
    # from azure.mgmt.resource import SubscriptionClient
    subscription_client = SubscriptionClient(credential)

    # List all subscriptions and print their IDs and display names
    for subscription in subscription_client.subscriptions.list():
        print(f"Subscription Name: {subscription.display_name}, ID: {subscription.subscription_id}")
    # PROTIP: Pick the first one to use:
    subscription_id = subscription.subscription_id
    print_info(f"get_azure_subscription_id(): \"{subscription_id}\" ")
    return subscription_id 


def register_subscription_providers(credential, subscription_id) -> bool:
    """
    Ensure providers are registered for the Subscription ID provided,
    which requires getting the long (300+) list of providers
    """
    #uv add azure-identity
    #uv add azure-mgmt-resource
    #from azure.identity import DefaultAzureCredential
    #from azure.mgmt.resource import ResourceManagementClient

    # WARNING: Only register providers you need to maintain least-privilege security:
    required_providers = [
        "Microsoft.BotService",
        "Microsoft.Web",
        "Microsoft.ManagedIdentity",
        "Microsoft.Search",
        "Microsoft.Storage",
        "Microsoft.CognitiveServices",
        "Microsoft.AlertsManagement",
        "microsoft.insights",
        "Microsoft.KeyVault",
        "Microsoft.ContainerInstance"
    ]  # there are many others.

    try:
        # Obtain the management object for resources:
        resource_client = ResourceManagementClient(credential, subscription_id)

        # It's said that there is no lookup of
        # Get all providers and their registration states:
        all_providers = {provider.namespace: provider.registration_state for provider in resource_client.providers.list()}

        print_heading(f"register_subscription_providers() {len(all_providers)}:")
        for provider in required_providers:
            reg_state = all_providers.get(provider, None)
            if reg_state != "Registered":  # Register providers if not registered:
                rg_result = resource_client.providers.register(provider)
                print_trace(f"   \"{provider}\" being registered: {rg_result}")
                    # NOTE: If a provider is in the “Registering” state, you don’t need to wait for all regions to complete—resource creation can proceed as soon as the region you need is ready.
            else:
                print_trace(f"   \"{provider}\" already registered.")
        return True

    except Exception as e:
        print_error(f"register_subscription_providers() ERROR: {e}")
        return False


# def use_interactive_credential() -> object:
# """ For Interactive/OAuth Login	Web apps, user logins	Yes (browser)
# """


def get_tenant_id() -> str:
    """
    Get Azure Tenant ID from .env or by making a subprocess call of CLI from within Python:
            az account show --query tenantId -o tsv
    The Tenant ID uniquely identifies the Microsoft Entra (formerly Azure AD) directory you use.
    Obtain from Portal at: https://portal.azure.com/#view/Microsoft_AAD_IAM/TenantProperties.ReactView
    Organization ID at https://portal.azure.com/#view/Microsoft_AAD_IAM/DirectorySwitchBlade/subtitle/
    """
    try:
        tenant_id = os.environ["AZURE_TENANT_ID"]  # EntraID
        print_info(f"-tenant (AZURE_TENANT_ID from .env): \"{tenant_id}\"")
        return tenant_id
    except KeyError:   
        # import subprocess
        #     az    account    show    --query    tenantId    -o    tsv
        tenant_id = subprocess.check_output(
            ["az", "account", "show", "--query", "tenantId", "-o", "tsv"]
        ).decode().strip()
        if tenant_id:
            print_info(f"get_tenant_id(): \"{tenant_id}\"")
            return tenant_id


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # import math

    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371  # Radius of earth in kilometers
    return c * r   

def closest_az_region(latitude: float, longitude: float) -> str:
    """
    This identifies the Azure region/location for a given geo longitude and latitude.
    based on the ping speed and distance from each Azure region.
    TODO: More importantly, for a particular service (resource) Azure charges a different cost each region.
    WARNING: The variable name "location" is reserved by Azure for its current region name.
    PROTIP: Notice how variables are defined with float and integers hints.
    """
    # CODING EXAMPLE: Ensure valid inputs into function:
    if not (-90 <= float(latitude) <= 90) or not (-180 <= float(longitude) <= 180):
        print("Error: Invalid coordinates. Latitude must be between -90 and 90, and longitude between -180 and 180.")
        return

    # please write python code to show regions of azure as a dictionary named AZURE_REGIONS with region name, latitude, longitude, with location with. Sort by region name.
    AZURE_REGIONS = {
        "australiasoutheast": (-37.814, 144.963),   # Melbourne
        "australiacentral": (-35.282, 149.128),     # Canberra
        "australiacentral2": (-35.282, 149.128),    # Canberra
        "southafricawest": (-33.925, 18.423),       # Cape Town
        "australiaeast": (-33.865, 151.209),        # Sydney
        "southafricanorth": (-25.731, 28.218),      # Johannesburg
        "brazilsouth": (-23.55, -46.633),           # Sao Paulo
        "southeastasia": (1.283, 103.833),          # Singapore
        "southindia": (13.0827, 80.2707),           # Chennai
        "centralindia": (18.5204, 73.8567),         # Pune
        "jioindiacentral": (18.5204, 73.8567),      # Pune
        "westindia": (19.076, 72.8777),             # Mumbai
        "jioindiawest": (19.076, 72.8777),          # Mumbai
        "eastasia": (22.267, 114.188),              # Hong Kong
        "uaecentral": (24.466, 54.366),             # Abu Dhabi
        "uaenorth": (25.096, 55.174),               # Dubai
        "qatarcentral": (25.2854, 51.531),          # Doha
        "southcentralus": (29.4167, -98.5),         # Texas
        "isrealcentral": (31.046, 34.851),          # Jerusalem
        "chinaeast": (31.2304, 121.4737),           # Shanghai
        "chinaeast2": (31.2304, 121.4737),          # Shanghai
        "israelnorth": (32.0853, 34.7818),          # Tel Aviv
        "westus3": (33.448, -112.074),              # Arizona
        "japanwest": (34.6939, 135.5022),           # Osaka
        "koreasouth": (35.1796, 129.0756),          # Busan
        "japaneast": (35.68, 139.77),               # Tokyo
        "eastus2": (36.6681, -78.3889),             # Virginia, US
        "eastus": (37.3719, -79.8164),              # Virginia, US
        "koreacentral": (37.5665, 126.9780),        # Seoul
        "westus": (37.783, -122.417),               # California
        "chinanorth": (39.9042, 116.4074),          # Beijing
        "chinanorth2": (39.9042, 116.4074),         # Beijing
        "westcentralus": (40.89, -110.234),         # Wyoming
        "centralus": (41.5908, -93.6208),           # Iowa
        "northcentralus": (43.653, -92.332),        # Illinois
        "canadacentral": (43.653, -79.383),         # Toronto
        "francesouth": (43.7102, 7.2620),           # Marseille
        "italynorth": (45.4642, 9.19),              # Milan
        "switzerlandwest": (46.204, 6.143),         # Geneva
        "francecentral": (46.3772, 2.373),          # Paris
        "canadaeast": (46.817, -71.217),            # Quebec City
        "westus2": (47.233, -119.852),              # Washington
        "switzerlandnorth": (47.451, 8.564),        # Zurich
        "germanywestcentral": (50.11, 8.682),       # Frankfurt
        "uksouth": (51.5074, -0.1278),              # London
        "polandcentral": (52.2297, 21.0122),        # Warsaw
        "westeurope": (52.3667, 4.9),               # Amsterdam, Netherlands
        "ukwest": (52.4796, -1.9036),               # Cardiff
        "northeurope": (53.3478, -6.2597),          # Dublin, Ireland
        "germanynorth": (53.55, 10.0),              # Hamburg
        "swedencentral": (59.329, 18.068),          # Stockholm
        "norwayeast": (59.913, 10.752),             # Oslo
        "norwaywest": (60.391, 5.322),              # Bergen
    }  # This needs to be updated occassionally.
    # print_trace(f"closest_az_region(): from among {len(AZURE_REGIONS.items())} regions")
        # Equivalent of CLI: az account list-locations --output table --query "length([])" 
        # Equivalent of CLI: az account list-locations --query "[?contains(regionalDisplayName, '(US)')]" -o table
        # Equivalent of CLI: az account list-locations -o table --query "[?contains(regionalDisplayName, '(US)')]|sort_by(@, &name)[]|length(@)"
            # Remove "|length(@)"

    # TODO: Identify the longest region name (germanywestcentral) and announce its number of characters (18)
        # for use in keyvault name which must be no longer than 24 characters long.

    num_regions = 1
    distances = []
    for region, (region_lat, region_lon) in AZURE_REGIONS.items():
        distance = haversine_distance(latitude, longitude, region_lat, region_lon)
        distances.append((region, distance))
    
    # Sort by distance and return the n closest:
    n:int = 3
    closest_regions = sorted(distances, key=lambda x: x[1])[:n]
    print_verbose(f"closest_az_region({n}:): {closest_regions}")
    closest_region = closest_regions[0][0]  # the first region ID in the list
    print_info(f"closest_az_region(of {len(AZURE_REGIONS.items())} in Azure:): \"{closest_region}\" ")
    
    return closest_region


def obtain_storage_object(credential, subscription_id) -> object:
    """
    Returns an Azure storage client object for the given credential and subscription ID.
    At Portal: https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts
    Equivalent CLI: az cloud set -n AzureCloud   // return to Public Azure.
    # TODO: allowed_copy_scope = "MicrosoftEntraID" to prevent data exfiltration from untrusted sources.
        See https://www.perplexity.ai/search/python-code-to-set-azure-stora-549_KJogQOKcFMcHvynG3w#0
    # TODO: PrivateLink endpoints
    """
    #from azure.identity import DefaultAzureCredential
    #from azure.mgmt.storage import StorageManagementClient
    #from azure.storage.blob import BlobServiceClient
    #import os

    try:
        # Initialize and return a StorageManagementClient to manage Azure Storage Accounts:
        storage_client = StorageManagementClient(
            credential=credential,
            subscription_id=subscription_id,
            # api_version="2024-01-01" 
            #resource_group=resource_group,
            #storage_account_name=storage_account_name,
            #location=my_location
        )
        print_verbose(f"obtain_storage_object(): {storage_client}")
        return storage_client
    except Exception as e:
        print_error(f"obtain_storage_object(): {e}")
        return None



def create_storage_account(credential, subscription_id, resource_group_name, new_location) -> str:
    """
    Returns an Azure storage account object for the given account name
    At Portal: https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts
    Equivalent CLI: az cloud set -n AzureCloud   // return to Public Azure.
    az storage account create --name mystorageacct --resource-group mygroup --location eastus --sku Standard_LRS --kind StorageV2 --api-version 2024-08-01
    # TODO: allowed_copy_scope = "MicrosoftEntraID" to prevent data exfiltration from untrusted sources.
        See https://www.perplexity.ai/search/python-code-to-set-azure-stora-549_KJogQOKcFMcHvynG3w#0
    # TODO: PrivateLink endpoints
    """
    #from azure.identity import DefaultAzureCredential
    #from azure.mgmt.storage import StorageManagementClient
    #from azure.storage.blob import BlobServiceClient
    #import os

    # Fetch current account properties
    storage_client = obtain_storage_object(credential, subscription_id)
    if not storage_client:
        print_error("create_storage_account(): obtain_storage_object() failed to fetch storage_client! ")
        exit(9)
    else:  # redundant
        print_trace(f"create_storage_account(): {storage_client}")

    if STORAGE_ACCOUNT_NAME:  # defined by parameter:
        print_info(f"--storage \"{STORAGE_ACCOUNT_NAME}\"  # (STORAGE_ACCOUNT_NAME) from parms being used.")
        return STORAGE_ACCOUNT_NAME
    try:
        storage_account_name = os.environ["STORAGE_ACCOUNT_NAME"]
        print_info(f"STORAGE_ACCOUNT_NAME = \"{STORAGE_ACCOUNT_NAME}\"  # from .env file being used.")
        return storage_account_name
    except KeyError:
        pass

    # WARNING: No underlines or dashes in storage account name up to 24 characters:
    fts = datetime.fromtimestamp(time.time(), tz=timezone.utc)
    date_str = fts.strftime("%y%m")  # EX: "...-250419" no year, minute, UTC %y%m%d%H%M%Z https://strftime.org
    # Max. my_location is "germanywestcentral" of 19 characters + 5 (yymm of 2504) = 24 characters (the max):
    storage_account_name = f"{my_location}{date_str}"  # no dashes/underlines
       # Example: STORAGE_ACCOUNT_NAME="germanywestcentral-2504"
    # Alternative: STORAGE_ACCOUNT_NAME = f"pythonazurestorage{random.randint(1,100000):05}"
    print_info(f"create_storage_account() considering name: \"{storage_account_name}\" ")

    try:
        # Fetch current storage account properties:
        account_props = storage_client.storage_accounts.get_properties(resource_group_name, storage_account_name)
        print_verbose(f"create_storage_account() properties: {account_props}")
    except Exception as e:
        print_verbose(f"create_storage_account(): {e}")
        pass  # to create storage account below
    else:  # if storage account already exists:
        # List all storage accounts in the subscription for credential:
        storage_accounts = storage_client.storage_accounts.list()
        for account in storage_accounts:
            print_verbose(f"Storage Account: {account.name}, Location: {account.location}")
        return storage_account_name

    # CAUTION: API version needs update occassionally:
    # See https://learn.microsoft.com/en-us/python/api/azure-mgmt-storage/azure.mgmt.storage.storagemanagementclient?view=azure-python
    parameters = {
        "location": new_location,
        "kind": "StorageV2",
        "api_version": "2024-01-01",
        "sku": {"name": "Standard_LRS"},
        "minimum_tls_version": "TLS1_2",
        "deleteRetentionPolicy": {
            "enabled": True,
            "days": 14  # Set between 1 and 365
        }
    }  # LRS = Locally-redundant storage
    # TODO: Set soft delete policies, 
    # For update: https://www.perplexity.ai/search/python-code-to-set-azure-stora-549_KJogQOKcFMcHvynG3w#0
    # https://learn.microsoft.com/en-us/rest/api/storagerp/storage-accounts/create?view=rest-storagerp-2024-01-01&tabs=HTTP
    try:  # Create the storage account:
        poller = storage_client.storage_accounts.begin_create(
            resource_group_name=resource_group_name,
            account_name=storage_account_name,
            api_version="2024-01-01",
            parameters=parameters
        )
        # Wait for completion:
        account_result = poller.result()
        print_info(f"create_storage_account(\"{account_result.name}\") created!")
        return account_result  # storage_account_name
    except Exception as e:
        print_error(f"create_storage_account(): {e}")
        # FIXME: api_version="2024-03-01" -> API version 2024-03-01 does not have operation group 'storage_accounts' 
        # See https://www.perplexity.ai/search/azure-api-version-2024-03-01-d-7aatmHRXQ32L0PF3zaraxg#0
        return None


def ping_az_storage_acct(storage_account_name) -> str:
    """
    CAUTION: This is not currently used due to "Destination Host Unreachable" error.
    Returns the ping utility latency to a storage account within the Azure cloud.
    """
    ping_host = storage_account_name + ".blob.core.windows.net"
    try:
        # from pythonping import ping
        response = ping(ping_host, count=5, timeout=2)
        response_text = f"Min-Avg-Max Latency: {response.rtt_min_ms:.2f}-{response.rtt_avg_ms:.2f}-{response.rtt_max_ms:.2f} ms"
        response_text =+ f"  Packet loss: {response.packet_loss * 100:.0f}%"
        return response_text
    except Exception as e:  # such as "Destination Host Unreachable"
        print_error(f"ping_az_storage_acct() ERROR: {e}")
        return None
 

# def create_storage_blob():
#     See https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-delete-python

# def delete_storage_blob():
#     """
#     A blob that was soft deleted due to the delete_retention_policy.
#     See https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-delete-python
#     See https://learn.microsoft.com/en-us/rest/api/storageservices/delete-blob
#     """
#     # from azure.identity import DefaultAzureCredential
      # from azure.storage.blob import BlobServiceClient
      # First, delete all snapshots under the storageaccount:
      # undelete_storage_blob():

# def access_storage_blob():


# TODO: set the principal with the appropriate level of permissions (typically Directory.Read.All for these operations).


def get_func_principal_id(credential, app_id, tenant_id) -> object:
    """
    TODO: Get userId by decoding function's X-MS-CLIENT-PRINCIPAL header. Sometimes, properties like userPrincipalName or name might not be present, 
    depending on the identity provider or user type (like guest users). 
    In such a case, check the userDetails property, which often contains the user's email or username.
    # Extract the user's email from the claims using:  user_email = client_principal.get('userDetails')
    based on https://learn.microsoft.com/en-us/answers/questions/2243286/azure-function-app-using-python-how-to-get-the-pri
    """
    app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
    return app


# @app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve the X-MS-CLIENT-PRINCIPAL header
    client_principal_header = req.headers.get('X-MS-CLIENT-PRINCIPAL')
    logging.info(f"X-MS-CLIENT-PRINCIPAL header: {client_principal_header}")
    user_name = None

    if client_principal_header:
        try:
            # Decode the Base64-encoded header
            decoded_header = base64.b64decode(client_principal_header).decode('utf-8')
            logging.info(f"Decoded X-MS-CLIENT-PRINCIPAL: {decoded_header}")
            client_principal = json.loads(decoded_header)

            # Log the entire client principal for debugging
            logging.info(f"Client Principal: {client_principal}")

            # Extract the user's name from the claims
            user_name = client_principal.get('userPrincipalName') or client_principal.get('name')
        except Exception as e:
            logging.error(f"Error decoding client principal: {e}")

    if user_name:
        return func.HttpResponse(f"Hello, {user_name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. However, no authenticated user information was found.",
            status_code=200
        )


def create_get_resource_group(credential, resource_group_name, new_location, subscription_id) -> str:
    """
    Create Resource Group if the resource_group_name is not already defined.
    Return json object such as {'additional_properties': {}, 'id': '/subscriptions/15e19a4e-ca95-4101-8e5f-8b289cbf602b/resourceGroups/az-keyvault-for-python-250413', 'name': 'az-keyvault-for-python-250413', 'type': 'Microsoft.Resources/resourceGroups', 'properties': <azure.mgmt.resource.resources.v2024_11_01.models._models_py3.ResourceGroupProperties object at 0x1075ec1a0>, 'location': 'westus', 'managed_by': None, 'tags': None}
    Equivalent to CLI: az group create -n "myResourceGroup" -l "useast2"
        --tags "department=tech" "environment=test"
    Equivalent of Portal: https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups.ReactView
    See https://learn.microsoft.com/en-us/azure/developer/python/sdk/examples/azure-sdk-example-resource-group?tabs=cmd
    """
    #uv add azure-mgmt-resource
    #uv add azure-identity
    #from azure.identity import DefaultAzureCredential
    #from azure.mgmt.resource import ResourceManagementClient

    # WARNING: Only register providers you need to maintain least-privilege security:
    required_providers = [
        "Microsoft.BotService",
        "Microsoft.Web",
        "Microsoft.ManagedIdentity",
        "Microsoft.Search",
        "Microsoft.Storage",
        "Microsoft.CognitiveServices",
        "Microsoft.AlertsManagement",
        "microsoft.insights",
        "Microsoft.KeyVault",
        "Microsoft.ContainerInstance"
    ]
    try:
        # Obtain the management object for resources:
        resource_client = ResourceManagementClient(credential, subscription_id)

        # Get all providers and their registration states:
        all_providers = {provider.namespace: provider.registration_state for provider in resource_client.providers.list()}
        # print(f"create_get_resource_group() all_providers: {all_providers}")
        # TODO: List resource groups like https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups.ReactView

        # Provision the resource group:
        rg_result = resource_client.resource_groups.create_or_update(
            resource_group_name, {"location": new_location}
        )
        print_info(f"create_get_resource_group() new resource_group_name: \"{resource_group_name}\"")
        return rg_result
    except Exception as e:
        print_error(f"create_get_resource_group() {str(rg_result)}")
        print_error(f"create_get_resource_group() {e}")
        # FIXME: ERROR: (InvalidApiVersionParameter) The api-version '2024-01-01' is invalid. The supported versions are 2024-11-01
        return None


def delete_resource_group(credential, resource_group_name, subscription_id) -> int:
    """Equivalent of CLI: az group delete -n PythonAzureExample-rg  --no-wait
    """
    try:
        resource_client = ResourceManagementClient(credential, subscription_id)
        if not resource_client:
            print(f"Cannot find ResourceManagementClient to delete_resource_group({resource_group_name})!")
            return False
        rp_result = resource_client.resource_groups.begin_delete(resource_group_name)
            # EX: <azure.core.polling._poller.LROPoller object at 0x1055f1550>
        # if DEBUG: print(f"delete_resource_group({resource_group_name}) for {rp_result}")
        return True
    except Exception as e:
        print(f"delete_resource_group() ERROR: {e}")
        return False


def create_content_safety_policy(credential, subscription_id, resource_group_name, keyvault_name) -> bool:
    """
    CAUTION: Before running this function, manual steps need to be taken in the GUI Portal to obtain the CONTENT_SAFETY_KEY and ENDPOINT:
    https://microsoftlearning.github.io/mslearn-ai-services/Instructions/Exercises/05-implement-content-safety.html
    """
    # pip install azure-ai-contentsafety
    # Set endpoint and key as environment variables for security:
    # export/setx CONTENT_SAFETY_KEY "YOUR_CONTENT_SAFETY_KEY"
    # export/setx CONTENT_SAFETY_ENDPOINT "YOUR_CONTENT_SAFETY_ENDPOINT"

    # import os
    # from azure.ai.contentsafety import ContentSafetyClient
    # from azure.core.credentials import AzureKeyCredential
    # from azure.core.exceptions import HttpResponseError
    # from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory



def define_keyvault_name(my_location) -> str:
    """
    Come up with a globally unique keyvault name that's 24 characters long.
    """
    if KEYVAULT_NAME:  # defined by parameter:
        print_info(f"-kv \"{KEYVAULT_NAME}\"  # (AZURE_KEYVAULT_NAME) being used.")
        return KEYVAULT_NAME
    # else see if .env file has a value:
    try:
        keyvault_name = os.environ["AZURE_KEYVAULT_NAME"]  # EntraID
        print_info(f"AZURE_KEYVAULT_NAME = \"{keyvault_name}\"  # from .env file being used.")
        return keyvault_name
    except KeyError:
        pass

    # TODO: Calcuate how many characters can fit within 24 character limit.
    # With the longest region name being 18, such as "westcentralus-fa5bdb":
    keyvault_name = f"{my_location}-{uuid.uuid4().hex[:6]}"
        # So no room for prefix "kv-" as in
    #    my_keyvault_root = os.environ["AZURE_KEYVAULT_ROOT_NAME"]
    #except KeyError as e:
    #    my_keyvault_root = "kv"
    # Also no room for both: "{my_keyvault_root}-{my_location}-{get_log_datetime()}"
        # PROTIP: Define datestamps Timezone UTC: https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
    return keyvault_name


def check_keyvault(credential, keyvault_name, vault_url) -> int:
    """Check if a Key Vault exists
    Return True if found, False if not.
    See https://learn.microsoft.com/en-us/python/api/overview/azure/keyvault-secrets-readme?view=azure-python
    """
    #from azure.identity import DefaultAzureCredential
    #from azure.keyvault.secrets import SecretClient
    #from azure.core.exceptions import HttpResponseError
    #import sys
    
    client = SecretClient(vault_url=vault_url, credential=credential)
        # Expected: "<azure.keyvault.secrets._client.SecretClient object at 0x106fc42f0>")
    if not client:
        print_fail(f"check_keyvault(client) failed to obtain client: \"{client}\")")
        exit(9)
    secrets = client.list_properties_of_secrets()
        # Expected: <iterator object azure.core.paging.ItemPaged at 0x106911550>
    if not secrets:
        print_fail(f"check_keyvault(client) failed to obtain secrets: \"{secrets}\") ...")
        exit(9)

    try:
        for secret in secrets:
            # CAUTION: Avoid printing out {secret.name} values in logs:
            print_verbose(f"check_keyvault(\"{keyvault_name}\" exists with secrets.")
            return True
        else:
            print_info(f"check_keyvault({keyvault_name}) Vault exists but contains no secrets.")
            return True
    except Exception as e:
        print_fail(f"Key Vault not recognized in check_keyvault({keyvault_name}): {e}")
        # This is expected if the Key Vault does not exist.
        return False  # KeyVault not found, so create it!


def create_keyvault(credential, subscription_id, resource_group, keyvault_name, location, tenant_id, user_principal_id) -> object:
    """
    # 1. Ensure the credential is for a service principal with Key Vault Contributor or Contributor RBAC role assignments.
    # Equivalent to CLI: az keyvault create --name "{$keyvault_name}" -g "${resc_group}" --enable-rbac-authorization 
    # 2. Create the Key Vault using azure-mgmt-keyvault
    Alternative is https://registry.terraform.io/modules/Azure/avm-res-keyvault-vault/azurerm/latest
    Based on https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Labfiles/02-ai-services-security/Python/keyvault_client/keyvault-client.py
    """
    resource_client = ResourceManagementClient(credential, subscription_id)
    if not resource_client:
        print(f"Cannot find ResourceManagementClient to create_keyvault({keyvault_name})!")
        return None
    
    # Create a KeyVault management client:
    keyvault_client = KeyVaultManagementClient(credential, subscription_id)
    if not keyvault_client:
        print(f"Cannot find KeyVaultManagementClient to create_keyvault({keyvault_name})!")
        return None

    # CAUTION: Replace <service-principal-object-id> with your SP’s object ID.
    keyvault_client.vaults.begin_create_or_update(
        resource_group,
        keyvault_name,
        {
            "location": location,
            "properties": {
                "tenant_id": tenant_id,
                "sku": {"name": "standard", "family": "A"},
                "access_policies": [{
                    "tenant_id": tenant_id,
                    "object_id": user_principal_id,
                    "permissions": {"secrets": ["all"], "keys": ["all"]}
                }]
            }
        }
    ).result()
    # TODO: CAUTION: set permissions to least privilege.


def delete_keyvault(credential, keyvault_name, vault_url) -> bool:
    """ Equivalent to CLI: az keyvault delete --name "{$keyvault_name}" 
    """
    # from azure.keyvault.secrets import SecretClient
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())  
        if secret_client:
            secret_client.delete_secret(keyvault_name)
        return True
    except Exception as e:
        print(f"delete_keyvault() ERROR: {e}")
        return False


def populate_keyvault_secret(credential, keyvault_name, secret_name, secret_value) -> bool:
    """ Equivalent to az keyvault secret set --name "{$secret_name}" --value "{$secret_value}" --vault-name "{$keyvault_name}" 
    """
    # from azure.keyvault.secrets import SecretClient
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())    
        if secret_client:
            rp_secret = secret_client.set_secret(secret_name, secret_value)
        return True
    except Exception as e:
       print(f"populate_keyvault_secret() ERROR: {e}")
           # <urllib3.connection.HTTPSConnection object at 0x1054a5a90>: Failed to resolve 'az-keyvault-2504190459utc.vault.azure.net' ([Errno 8] nodename nor servname provided, or not known)
       return False


def get_keyvault_secret(credential, keyvault_name, secret_name) -> object:
    """ Equivalent to CLI: az keyvault secret show --name "{$secret_name}" --vault-name "{$keyvault_name}" 
    """
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
        if secret_client:
            rp_secret = secret_client.get_secret(secret_name)
            if rp_secret:
                return rp_secret
        return None
    except Exception as e:
       print(f"get_keyvault_secret() ERROR: {e}")
       return None


def delete_keyvault_secret(credential, keyvault_name, secret_name) -> bool:
    """ Equivalent to CLI: az keyvault secret delete --name "{$secret_name}" --vault-name "{$keyvault_name}" 
    """
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
        if secret_client:
            rp_secret = secret_client.delete_secret(secret_name)
            if rp_secret:
                print_info(f"delete_keyvault_secret(\"{secret_name}\") done!")
                return True
        print_error(f"delete_keyvault_secret() {secret_client} failed!")
        return False
    except Exception as e:
       print_error(f"delete_keyvault_secret() ERROR: {e}")
       return False


def get_ai_svc_globals() -> bool:
    """ Load Configuration from environment variables in .env file
    See https://microsoftlearning.github.io/mslearn-ai-services/Instructions/Exercises/01-use-azure-ai-services.html
    Manually follow https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Labfiles/01-use-azure-ai-services/Python/sdk-client/sdk-client.py
    1. Use the Edge browser to htps://portal.azure.com and sign in using the Microsoft account associated with your Azure subscription.
    2. In the top search bar, search for "Azure AI services" at https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/AIServices
    3. Select the blue "Azure AI services multi-service account" at https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne to create a new resource:
       1. Subscription: Your Azure subscription
       2. Resource group: Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)
       3. Region: Choose any available region
       4. Name: Enter a unique name (such as "ai-instance-250429a") up to 64 chars with dashes.
       5. Pricing tier: "Standard S0"
       6. Select the required checkboxes 
       7. Click "Create" and "Create" to create the resource for "Your deployment is complete".
       8. Click "Go to resource" then click the "Azure AI services multi-service account" name at
       https://portal.azure.com/#@jetbloom.com/resource/subscriptions/15e19a4e-ca95-4101-8e5f-8b289cbf602b/resourceGroups/westcentralus-42ad1a/providers/Microsoft.CognitiveServices/accounts/ai-instance-250429a/overview
       9. Copy the Endpoint to copy and paste in your .env file:
       AI_SERVICE_ENDPOINT="https://ai-instance-250429a.cognitiveservices.azure.com/"
       10. Click "Click here to manage keys", "Show Keys", "KEY 1" to copy and paste in your .env file:
       AI_SERVICE_KEY="12345..." KEY2 can also be used.
       11. Copy the Location and (for example) paste into AZURE_LOCATION="centralus"
    """
    global ai_svc_resc
    global ai_endpoint
    global ai_key
    # TODO: ai_svc_name from parms.
    try:
        # Get Configuration Settings:
        load_dotenv()   #from dotenv import load_dotenv

        # TODO: retrieve based on ai_svc_name in

        #import os
        ai_svc_resc = os.getenv('AI_SERVICE_RESOURCE')
        # These are associated with the resource:
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        print_info(f"get_ai_svc_globals() ai_svc_resc: \"{ai_svc_resc}\" endpoint: \"{ai_endpoint}\" ")
            # CAUTION: Don't display secure ai_key.
        return True

    except Exception as e:
       print_error(f"get_ai_svc_globals() ERROR: {e}")
       return False


def input_az_ai_language() -> str:
    """ Returns language code.
    See https://microsoftlearning.github.io/mslearn-ai-services/Instructions/Exercises/01-use-azure-ai-services.html
    Referencing https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Labfiles/01-use-azure-ai-services/Python/sdk-client/sdk-client.py
    """
    # TODO: Get language from parameters instead of user input:
    try:
        # Get user input (until they enter "quit")
        userText =''
        while userText.lower() != 'quit':
            userText = input('\nEnter some text ("quit" to stop)\n')
            if userText.lower() != 'quit':
                language = GetLanguage(userText)
                print_info(f"input_az_ai_language()() Language: {language}")
        return language
    except Exception as e:
        print_error(f"input_az_ai_language() ERROR: {e}")
            # ERROR: name 'GetLanguage' is not defined 
        return None


# Alternative: get_az_ai_textanalytics_rest_client() based on rest-client.py
def get_az_ai_textanalytics_sdk_client() -> object:
    """ Create client using global endpoint and key
    See https://microsoftlearning.github.io/mslearn-ai-services/Instructions/Exercises/01-use-azure-ai-services.html
    Referencing https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Labfiles/01-use-azure-ai-services/Python/sdk-client/sdk-client.py
    """
    get_ai_svc_globals()  # retrieves ai_endpoint, ai_key, ai_svc_resc
    try:
        #from azure.ai.textanalytics import TextAnalyticsClient
        #from azure.core.credentials import AzureKeyCredential
        credential = AzureKeyCredential(ai_key)
        client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
        print_verbose(f"get_az_ai_textanalytics_sdk_client() client: \"{client}\" ")
        return client
    except Exception as e:
       print_error(f"get_az_ai_textanalytics_sdk_client() ERROR: {e}")
       return None


def detect_language_using_az_ai_sdk_client(ai_svc_name,text_in) -> str:
    """
    Docs:    https://learn.microsoft.com/en-us/azure/ai-services/translator/
    Pricing: https://azure.microsoft.com/en-us/pricing/details/cognitive-services/translator/
    """
    client = get_az_ai_textanalytics_sdk_client()
    try:
        # Call the service to get the detected language:
        detectedLanguage = client.detect_language(documents = [text_in])[0]
        print_info(f"detect_language_using_az_ai_sdk_client({len(text_in)} chars) lang: \"{detectedLanguage.primary_language.name}\" " )
        return detectedLanguage.primary_language.name
            # Example: "English"
    except Exception as e:
        print_error(f"detect_language_using_az_ai_sdk_client() ERROR: {e}")
            # ERROR: No connection adapters were found for '/:analyze-text???/language&api-version=2023-04-01' 
        return None


def detect_language_using_az_ai_rest_client( text_in) -> str:
    """ Returns language name (such as "English") with confidence score using REST API call.
    Docs:    https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Labfiles/01-use-azure-ai-services/Python/rest-client/rest-client.py
    Pricing: https://azure.microsoft.com/en-us/pricing/details/cognitive-services/translator/
    """
    client = get_az_ai_textanalytics_sdk_client()
    try:
        get_ai_svc_globals()  # retrieves ai_endpoint, ai_key, ai_svc_resc

        # Construct the JSON request body (a collection of documents, each with an ID and text)
        jsonBody = {
            "documents":[
                {"id": 1,
                 "text": text_in}
            ]
        }  # TODO: target_languages???

        # Let's take a look at the JSON we'll send to the service
        print(json.dumps(jsonBody, indent=2))

        # Make an HTTP request to the REST interface:
        #import http.client, base64, json, urllib
        #from urllib import request, parse, error        
        uri = ai_endpoint.rstrip('/').replace('https://', '')
        conn = http.client.HTTPSConnection(uri)

        # Add the authentication key to the request header
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': ai_key
        }

        # Use the Text Analytics language API
        conn.request("POST", "/text/analytics/v3.1/languages?", str(jsonBody).encode('utf-8'), headers)

        # Send the request
        response = conn.getresponse()
        data = response.read().decode("UTF-8")

        # If the call was successful, get the response
        if response.status == 200:
            # Display the JSON response in full (just so we can see it)
            results = json.loads(data)
            print_trace(json.dumps(results, indent=1))
                # Extract the detected language name for each document:
                    #    {
                    #    "documents": [
                    #        {
                    #        "id": "1",
                    #        "warnings": [],
                    #        "detectedLanguage": {
                    #            "name": "English",
                    #            "iso6391Name": "en",
                    #            "confidenceScore": 0.79
            for document in results["documents"]:
                # TODO: Parse language name such as "English" in a list:
                print_info(f"detect_language_using_az_ai_rest_client(): Language: \"{document["detectedLanguage"]["name"]}\" iso6391Name: \"{document["detectedLanguage"]["iso6391Name"]}\" Confidence: \"{document["detectedLanguage"]["confidenceScore"]}\" ")
        else:
            # Something went wrong, write the whole response:
            print_error(f"detect_language_using_az_ai_rest_client() {response.status} ERROR: {data}")

        conn.close()

    except Exception as e:
        print_error(f"detect_language_using_az_ai_rest_client() ERROR: {e}")
        return None


# def translate_text_using_az_ai_rest_client(TEXT_INPUT, ai_languages):


# https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Instructions/Exercises/05-implement-content-safety.md


#### SECTION 13. Main control loop:


if __name__ == "__main__":

    #### STAGE 1 - Show starting environment:

    print_info(f"Started: {get_user_local_time()}, in logs: {get_log_datetime()} ")
    print_info(f"Started: {get_mem_used()} MiB RAM being used.")
    print_info(f"Started: {get_disk_free()} GB disk space free.")

    #### STAGE 2 - Load environment variables, Azure Account:


    open_env_file(ENV_FILE)
    macos_sys_info()


    #### STAGE 3 - Load Azure environment variables, Azure Account:


    my_credential = get_acct_credential()
    my_user_principal_id = get_user_principal_id(my_credential)
    my_subscription_id = get_azure_subscription_id(my_credential)
    register_subscription_providers(my_credential, my_subscription_id)
    my_tenant_id = get_tenant_id()
    longitude, latitude = get_longitude_latitude() # from parms or .env file calling get_geo_coordinates()
    my_location = closest_az_region(longitude, latitude)
    #get_elevation(longitude, latitude)  # has error


    #### STAGE 4 - Azure AI


    # get_ai_svc_globals()
    # ai_language = detect_language_using_az_ai_sdk_client(TEXT_INPUT)
    ai_language = detect_language_using_az_ai_rest_client(TEXT_INPUT)
    exit()

    # CAUTION: This costs money:
    #ai_languages = ["fr","zn"]   # French & Simplified Chinese
    #translated_text = translate_text_using_az_ai_rest_client(TEXT_INPUT, ai_languages)
    #print_info(f"translated_text: \"{translated_text}\"")


    #### STAGE 5 - Azure Key Vault at a location:


    if KEYVAULT_NAME:
        my_resource_group = KEYVAULT_NAME
        my_keyvault_name = KEYVAULT_NAME
    else:
        my_keyvault_name = define_keyvault_name(my_location)
        my_resource_group = create_get_resource_group(my_credential, my_keyvault_name, my_location, my_subscription_id)
        # TODO: Add tags to resource group.
    vault_url = f"https://{my_keyvault_name}.vault.azure.net"
    rc = check_keyvault(my_credential, my_keyvault_name, vault_url)
    if rc is True: 
        print_verbose(f"Key Vault \"{my_keyvault_name}\" already exists.")
    if rc is False:  # False (does not exist), so create it:
        create_keyvault(my_credential, my_subscription_id, my_resource_group, my_keyvault_name, my_location, my_tenant_id, my_user_principal_id)

    # my_storage_account_name = create_storage_account(my_credential, my_subscription_id, my_resource_group, my_location)
    # ping_az_storage_acct(my_storage_account_name)
    # measure_http_latency(my_storage_account_name, attempts=5)
    exit()

    print_wall_times()
    print("DEBUGGING EXIT")
    exit()

    #### List Azure Key Vaults:
    # Equivalent of Portal: List Key Vaults: https://portal.azure.com/#browse/Microsoft.KeyVault%2Fvaults
    # TODO: List costs like https://portal.azure.com/#view/HubsExtension/BrowseCosts.ReactView
    # PRICING: STANDARD SKU: $0.03 per 10,000 app restart operation, plus $3 for cert renewal, PLUS $1/HSM/month.
        # See https://www.perplexity.ai/search/what-is-the-cost-of-running-a-Fr6DTbKQSWKzpdSGv6qyiw
    
    #### STAGE 6 - Azure Resource Group for Azure Key Vault at a location:

    #my_principal_id = os.environ["AZURE_KEYVAULT_PRINCIPAL_ID"]

    # Before: Register an app in Azure and create a client secret.
    my_app_id = os.environ["AZURE_APP_ID"]
    my_client_id = os.environ["AZURE_CLIENT_ID"]
    my_client_secret = os.environ["AZURE_CLIENT_SECRET"]
    #my_principal_id = get_app_principal_id(my_credential, my_app_id, my_tenant_id)
    if not my_principal_id:
        print(f"get_app_principal_id() failed with JSON: \"{my_principal_id}\" ")
        exit(9)
    # Alternative: Using Azure Function App Headers (For Authenticated Users) using Easy Auth and returns the signed-in user's principal ID.
    exit()

 

    #### Add secrets to Azure Key Vault:

    my_secret_name = os.environ["MY_SECRET_NAME"]
    my_secret_value = os.environ["MY_SECRET_PLAINTEXT"]

    rp_result = populate_keyvault_secret(my_credential, my_keyvault_name, my_secret_name, my_secret_value)

    # TODO: List secrets in Key Vault

    rp_result = get_keyvault_secret(my_credential, my_keyvault_name, my_secret_name)
    
    # delete_keyvault_secret(my_credential, my_keyvault_name, my_secret_name)

    #### Retrieve secrets from Azure Key Vault:

    
    #### Rotate secrets in Azure Key Vault:

    
    #### -D to delete Key Vault created above.

    if DELETE_KV_AFTER:
        rp_result = delete_keyvault(my_credential, my_keyvault_name, vault_url)

    #### -D to delete Resource Group for Key Vault created above.

    if DELETE_RG_AFTER:
        rp_result = delete_resource_group(my_credential, my_keyvault_name, my_subscription_id)



    #### Azure Key Vault allows you to more securely store and manage SSL/TLS certificates.


# END