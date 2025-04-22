#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
"""az-keyvault.py at https://github.com/wilsonmar/python-samples/blob/main/az-keyvault.py

STATUS: use_az_dev_acct() working on macOS Sequoia 15.3.1
"""

__last_commit__ = "v005 keyvault created :az-keyvault.py"

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

uv python install 3.12
# Instead of requirements.txt:
uv add pathlib
uv add python-dotenv
uv add azure-functions
uv add azure-identity
uv add azure-keyvault-secrets

uv add azure-mgmt-compute
uv add azure-mgmt-keyvault
uv add azure-mgmt-network
uv add azure-mgmt-resource
uv add azure-mgmt-storage
uv add azure-storage-blob
#uv add msgraph-core           # for msgraph.core.GraphClient
uv add pytz
uv add requests
# For https://microsoftlearning.github.io/AI-102-AIEngineer/Instructions/00-setup.html
uv add flask requests python-dotenv pylint matplotlib pillow
uv add numpy
uv add pythonping
uv add psutil  #  psutil-7.0.0
uv add uuid
uv add platform   # https://docs.python.org/3/library/platform.html

source .venv/bin/activate
uv run az-keyvault.py

PROTIP: Each function displays its own error messages. Function callers display expected responses.

REMEMBER on CLI after running uv run az-keyvault.py: deactivate

"""

# SECTION 01. Set metadata about this program


# SECTION 02: Capture pgm start date/time

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


import base64
from contextlib import redirect_stdout
import io
import json
import logging
import math
from typing import Dict, List, Tuple
import os
import pathlib
from pathlib import Path
import pwd                # https://www.geeksforgeeks.org/pwd-module-in-python/
import signal
import site
import subprocess
import sys
import platform
import random  # for UUID and other random number generation
from tokenize import Number


# import external library (from outside this program):
try:
    import argparse
    from azure.mgmt.resource import ResourceManagementClient
    from azure.identity import DefaultAzureCredential
    from azure.identity import ClientSecretCredential
    from azure.keyvault.secrets import SecretClient
    import azure.functions as func
    from azure.mgmt.keyvault import KeyVaultManagementClient
    from azure.mgmt.resource import ResourceManagementClient
    from azure.storage.blob import BlobServiceClient
    from azure.mgmt.storage import StorageManagementClient
    # from msgraph.core import GraphClient   # doesn't work if included?
    # Microsoft Authentication Library (MSAL) for Python
    # integrates with the Microsoft identity platform. It allows you to sign in users or apps with Microsoft identities (Microsoft Entra ID, External identities, Microsoft Accounts and Azure AD B2C accounts) and obtain tokens to call Microsoft APIs such as Microsoft Graph or your own APIs registered with the Microsoft identity platform. It is built using industry standard OAuth2 and OpenID Connect protocols
    # See https://github.com/AzureAD/microsoft-authentication-library-for-python?tab=readme-ov-file
    from dotenv import load_dotenv
    import pytz   # for aware comparisons
    import urllib.parse
    from pathlib import Path
    import platform # https://docs.python.org/3/library/platform.html
    import psutil  #  psutil-5.9.5
    from pythonping import ping
    import requests
    import uuid
except Exception as e:
    print(f"Python module import failed: {e}")
    # pyproject.toml file exists
    print(f"Please activate your virtual environment:\n")
    print("    source .venv/bin/activate")
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    exit(9)

#### Parameters from call arguments:

ENV_FILE="python-samples.env"
show_sys_info = True

DELETE_RG_AFTER = True
DELETE_KV_AFTER = True
LIST_ALL_PROVIDERS = False
DEBUG = False

# TODO: Define these as parameters:
KEYVAULT_NAME = "kv-westcentralus-897e56"  # also used as resource group name
STORAGE_ACCOUNT_NAME = "store2westcentralus"


#### Utility Functions:

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


def print_separator():
    """ Put a blank line in CLI output. Used in case the technique changes throughout this code. """
    print(" ")


## Global variables: Colors Styles:
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
CVIOLET = '\033[35m'
CBEIGE = '\033[36m'
CWHITE = '\033[37m'
GRAY = '\033[90m'

HEADING = '\033[37m'   # [37 white
FAIL = '\033[91m'      # [91 red
ERROR = '\033[91m'     # [91 red
WARNING = '\033[93m'   # [93 yellow
INFO = '\033[92m'      # [92 green
VERBOSE = '\033[95m'   # [95 purple
TRACE = '\033[96m'     # [96 blue/green
                # [94 blue (bad on black background)

BOLD = '\033[1m'       # Begin bold text
UNDERLINE = '\033[4m'  # Begin underlined text
RESET = '\033[0m'   # switch back to default color

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

# PROTIP: Global variable referenced within functions:
# values obtained from .env file can be overriden in program call arguments:
show_fail = True       # Always show
show_error = True      # Always show
show_warning = True    # -wx  Don't display warning
show_todo = True       # -td  Display TODO item for developer
show_info = True       # -qq  Display app's informational status and results for end-users
show_heading = True    # -q  Don't display step headings before attempting actions
show_verbose = True    # -v  Display technical program run conditions
show_trace = True      # -vv Display responses from API calls for debugging code
show_secrets = False   # Never show

show_dates_in_logs = False

def print_separator():
    """ A function to put a blank line in CLI output. Used in case the technique changes throughout this code. 
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
    """ Strip new line from in_string
    """
    return ''.join(in_string.splitlines())


#### Python script control and timing utilities:

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
    from dotenv import load_dotenv
       # See https://www.python-engineer.com/posts/dotenv-python/
       # See https://pypi.org/project/python-dotenv/
    load_dotenv(global_env_path)  # using load_dotenv

    # Wait until variables for print_trace are retrieved:
    #print_trace("env_file="+env_file)
    #print_trace("user_home_dir_path="+user_home_dir_path)


def print_wall_times():
    """Prints All the timings together for consistency of output:
    """
    print_heading("Wall times (hh:mm:sec.microsecs):")
    # TODO: Write to log for longer-term analytics

    # For wall time of std imports:
    std_stop_datetimestamp = datetime.datetime.now()
    std_elapsed_wall_time = std_stop_datetimestamp -  std_strt_datetimestamp
    print_verbose("for import of Python standard libraries: "+ \
        str(std_elapsed_wall_time))

    # For wall time of xpt imports:
    xpt_stop_datetimestamp = datetime.datetime.now()
    xpt_elapsed_wall_time = xpt_stop_datetimestamp -  xpt_strt_datetimestamp
    print_verbose("for import of Python extra    libraries: "+ \
        str(xpt_elapsed_wall_time))

    pgm_stop_datetimestamp = datetime.datetime.now()
    pgm_elapsed_wall_time = pgm_stop_datetimestamp -  pgm_strt_datetimestamp
    pgm_stop_perftimestamp = time.perf_counter()
    print_verbose("for whole program run: "+ \
        str(pgm_elapsed_wall_time))



# SECTION 08. Obtain program environment metadata

# See https://wilsonmar.github.io/python-samples/#run_env

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
    """ Returns the marketing name of macOS versions which are not available
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

def get_mem_used() -> str:
    # import os, psutil  #  psutil-5.9.5
    process = psutil.Process()
    mem=process.memory_info().rss / (1024 ** 2)  # in bytes
    print_trace(str(process))
    return str(mem)
    # to print_verbose("get_mem_used(): "+str(mem)+" MiB used.")

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
    #    disk_list = about_disk_space()
    #    disk_space_free = disk_list[1]:,.1f / disk_list[0]:,.1f
    #    print_info(localize_blob("Disk space free")+"="+disk_space_free+" GB")
        # left-to-right order of fields are re-arranged from the function's output.


#### Azure core utilities:

def use_az_dev_acct(az_acct_name) -> object:
    """
    Returns an Azure cloud credential object for the given account name
    for local development after CLI:
    az cloud set -n AzureCloud   // return to Public Azure.
    az login
    """
    try:
        credential = DefaultAzureCredential()
        #blob_service_client = BlobServiceClient(
        #    account_url="https://{az_acct_name}.blob.core.windows.net",
        #    credential=credential
        #)
        print_info(f"use_az_dev_acct(credential: \"{my_acct_name}\")")
        return credential
            # <azure.identity._credentials.default.DefaultAzureCredential object at 0x106be6ba0>
    except blob_service_client.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except blob_service_client.exceptions.ConnectionError as errc:
        print("Connection Error:", errc)
    except blob_service_client.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except blob_service_client.exceptions.RequestException as err:
        print("Other Error:", err)
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
    The different personas/roles in an enterprise, each with dansboards and alerts:
    A. TechOps (SREs) who establish, monitor, troubleshoot, and restore the services (CA, dashbords, alerts) that others to operate. See https://github.com/bregman-arie/sre-checklist
    B. SecOps who enable people, Web (Flask, Django, FastAPI) apps & Serverless Functios accessing secrets based on RBAC policies
    C. Managers with authority to permanently delete (purge) secrets and backups https://learn.microsoft.com/en-us/azure/key-vault/policy-reference
    D. AppDevs who request, obtain, use, rotate secrets (but not delete) access to Networks, Apps. and Functions
    E. End Users who make use of Networks, Apps. and Functions built by others
    F. DataOps to regularly backup and rotate secrets and manage log storage. Data governance
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


def register_subscriber_providers(credential, subscription_id) -> bool:
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

        print_heading(f"register_subscriber_providers() {len(all_providers)}:")
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
        print_error(f"register_subscriber_providers() ERROR: {e}")
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
    """
    try:
        tenant_id = os.environ["AZURE_TENANT_ID"]  # EntraID
        print_info(f"-tenant (AZURE_TENANT_ID from .env): \"{tenant_id}\"")
        return tenant_id
    except KeyError as e:   
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

def pick_closest_region() -> str:
    """
    This identifies the Azure region/location for a given geo longitude and latitude.
    based on the ping speed and distance from each Azure region.
    TODO: More importantly, for a particular service (resource) Azure charges a different cost each region.
    WARNING: The variable name "location" is reserved by Azure for its current region name.
    PROTIP: Notice how variables are defined with float and integers hints.
    """
    # First,  use the AZURE_LOCATION parameter from CLI calls:
    # Second, use the AZURE_LOCATION variable in .env file:
    # Third,  use the geo lookup based on MY_LATITUDE (North/South) and MY_LONGITUDE (East/West of GMT)
    #try:
    #    my_location = os.environ["AZURE_LOCATION"]  # EntraID
    #    print_info(f"-location (AZURE_LOCATION from .env): \"{my_location}\"")
    #    return my_location
    #except KeyError as e:   
    #    pass  # do below.

    # TODO:
    # print_info(f"-lat \"{latitude}\"  # (North/South) from parms being used.")
    # print_info(f"-long (MY_LONGITUDE West/East of GMT) from .env): \"{longitude}\"")
    try:
        latitude = float(os.environ["MY_LATITUDE"])
        print_info(f"MY_LATITUDE = \"{latitude}\"  # (North/South) from .env being used. ")
    except KeyError as e:   
        pass  # do below.

    try:
        longitude = float(os.environ["MY_LONGITUDE"])
        print_info(f"MY_LONGITUDE = \"{longitude}\"  # (East/West of GMT) from .env being used. ")
    except KeyError as e:   
        pass  # do below.

    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
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
    # print_trace(f"pick_closest_region(): from among {len(AZURE_REGIONS.items())} regions")
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
    print_verbose(f"pick_closest_region({n}:): {closest_regions}")
    closest_region = closest_regions[0][0]  # the first region ID in the list
    print_info(f"pick_closest_region(of {len(AZURE_REGIONS.items())} in Azure:): {closest_region}")
    
    return closest_region


def create_storage_account(credential, subscription_id, resource_group_name, my_location) -> str:
    """
    Returns an Azure storage account object for the given account name
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

    if STORAGE_ACCOUNT_NAME:  # already created and specified in parameters:
        print_info(f"create_storage_account() name: \"{STORAGE_ACCOUNT_NAME}\" from parm ")
        return STORAGE_ACCOUNT_NAME
    
    # WARNING: No underlines or dashes in storage account name up to 24 characters:
    storage_account_name = f"store2{my_location}"
       # Example: STORAGE_ACCOUNT_NAME="store2westcentralus"
    try:
        # Initialize and return a StorageManagementClient to manage Azure Storage Accounts:
        storage_client = StorageManagementClient(
            credential=credential,
            subscription_id=subscription_id,
            #resource_group=resource_group,
            #storage_account_name=storage_account_name,
            #location=my_location
        )
    except Exception as e:
        print_error(f"create_storage_account() ERROR: {e}")
        return None

    # BEFORE: List all storage accounts in the subscription:
    if DEBUG:
        storage_accounts = storage_client.storage_accounts.list()
        for account in storage_accounts:
            print_verbose(f"Storage Account: {account.name}, Location: {account.location}")

    # Define storage account parameters:
    parameters = {
        "location": my_location,
        "kind": "StorageV2",
        "sku": {"name": "Standard_LRS"},
        "minimum_tls_version": "TLS1_2",
        "deleteRetentionPolicy": {
            "enabled": True,
            "days": 14  # Set between 1 and 365
        }
    }  # LRS = Locally-redundant storage
    # TODO: Set soft delete policies, 
    # For update: https://www.perplexity.ai/search/python-code-to-set-azure-stora-549_KJogQOKcFMcHvynG3w#0
    try:  # Create the storage account:
        poller = storage_client.storage_accounts.begin_create(
            resource_group_name=resource_group_name,
            account_name=storage_account_name,
            parameters=parameters
        )        
        # Wait for completion:
        account_result = poller.result()
        print_info(f"create_storage_account() name: \"{account_result.name}\" ")
        return account_result  # storage_account_name
    except Exception as e:
        print_error(f"create_storage_account() ERROR: {e}")
        return None

def ping_storage_acct(storage_account_name) -> str:
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
        print_error(f"ping_storage_acct() ERROR: {e}")
        return None
 
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


def create_get_resource_group(credential, resource_group_name, my_location, subscription_id) -> str:
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
            resource_group_name, {"location": my_location}
        )
        return rg_result
    except Exception as e:
        print_error(f"create_get_resource_group() {str(rg_result)}")
        print_error(f"create_get_resource_group() {e}")
        # FIXME: ERROR: (InvalidApiVersionParameter) The api-version '2024-01-01' is invalid. The supported versions are 2024-11-01
        return None


def delete_resource_group(credential, resource_group_name, subscription_id) -> int:
    """ Equivalent of CLI: az group delete -n PythonAzureExample-rg  --no-wait
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
    except KeyError as e:
        pass

    # With the longest region name being 18:
    keyvault_name = f"{my_location}-{uuid.uuid4().hex[:6]}"
        # keyvault_name = f"kv-{uuid.uuid4().hex[:8]}"
        # TODO: Calcuate how many characters can fit within 24 character limit.

    # Alternative: 
    # Commented out prefix takes too much room from the 24-char limit: 
    #    my_keyvault_root = os.environ["AZURE_KEYVAULT_ROOT_NAME"]
    #except KeyError as e:
    #    my_keyvault_root = "kv"
    # keyvault_name = f"{my_keyvault_root}-{my_location}-{get_log_datetime()}"
        # PROTIP: Define datestamps Timezone UTC: https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
        # EX: kv-westus-2504210416UTC  # max length: 24 characters
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


def populate_keyvault_secret(credential, keyvault_name, secret_name, secret_value) -> object:
    """ Equivalent to az keyvault secret set --name "{$secret_name}" --value "{$secret_value}" --vault-name "{$keyvault_name}" 
    """
    # from azure.keyvault.secrets import SecretClient
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())    
        if secret_client:
            rp_secret = secret_client.set_secret(secret_name, secret_value)
        return rp_secret
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
        return rp_secret
    except Exception as e:
       print(f"get_keyvault_secret() ERROR: {e}")
       return False


def delete_keyvault_secret(credential, keyvault_name, secret_name) -> object:
    """ Equivalent to CLI: az keyvault secret delete --name "{$secret_name}" --vault-name "{$keyvault_name}" 
    """
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
        rp_secret = secret_client.delete_secret(secret_name)
        return rp_secret
    except Exception as e:
       print(f"delete_keyvault_secret() ERROR: {e}")
       return False


if __name__ == "__main__":

    #### STAGE 1 - Show starting environment:

    print_info(f"Started: {get_user_local_time()}, in logs: {get_log_datetime()} ")
    print_info(f"Started: {get_mem_used()} MiB being used.")

    #### STAGE 2 - Load environment variables, Azure Account:

    open_env_file(ENV_FILE)
    macos_sys_info()

    #### STAGE 3 - Load Azure environment variables, Azure Account:

    # TODO: Fill in values from parms, .env:
    my_acct_name = os.environ["AZURE_ACCT_NAME"]
    my_credential=use_az_dev_acct(my_acct_name)
    
    # if AZURE_USER_PRINCIPAL_ID:
    #    my_user_principal_id = os.environ["AZURE_USER_PRINCIPAL_ID"]
    my_user_principal_id = get_user_principal_id(my_credential)
    print_info(f"get_user_principal_id(): {my_user_principal_id} ...")

    # Equivalent of CLI to list: az account show --query id --output tsv
    my_subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
        # Equivalent of CLI: az account show --query tenantId --output tsv
        # https://portal.azure.com/#@jetbloom.com/resource/subscriptions/15e19a4e-ca95-4101-8e5f-8b289cbf602b/overview
    register_subscriber_providers(my_credential, my_subscription_id)
    
    #### STAGE 4 - Azure Tenant ID from making a subprocess call of CLI from within Python:

    my_tenant_id = get_tenant_id()

    #### STAGE 5 - Azure Resource Group for Azure Key Vault at a location:
    
    my_location = pick_closest_region()
    if KEYVAULT_NAME:
        my_resource_group = KEYVAULT_NAME
        my_keyvault_name = KEYVAULT_NAME
    else:
        my_keyvault_name = define_keyvault_name(my_location)
        my_resource_group = create_get_resource_group(my_credential, my_keyvault_name, my_location, my_subscription_id)
        # TODO: Add tags to resource group.
    my_storage_account_name = create_storage_account(my_credential, my_subscription_id, my_resource_group, my_location)
    # ping_storage_acct(my_storage_account_name)
    # measure_http_latency(my_storage_account_name, attempts=5)

    vault_url = f"https://{my_keyvault_name}.vault.azure.net"
    rc = check_keyvault(my_credential, my_keyvault_name, vault_url)
    if rc is True: 
        print_verbose(f"Key Vault \"{my_keyvault_name}\" already exists.")
    if rc is False:  # False (does not exist), so create it:
        create_keyvault(my_credential, my_subscription_id, my_resource_group, my_keyvault_name, my_location, my_tenant_id, my_user_principal_id)

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