#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 JetBloom LLC
# SPDX-License-Identifier: MPL-2.0
"""python-samples.py within https://github.com/wilsonmar/python-samples/blob/master/python-samples/
   Explained at https://wilsonmar.github.io/python-samples
   This is sample code to provide a feature-rich base for new Python 3.9+ programs run from CLI.
   It implements advice at https://www.linkedin.com/pulse/how-shine-coding-challenges-wilson-mar-/

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
   OF ANY KIND, either express or implied. See the License for the specific
   language governing permissions and limitations under the License.
"""

# SECTION 01. Set metadata about this program

# Unlike regular comments, docstrings are available at runtime to the compiler:
__repository__ = "https://github.com/wilsonmar/python-samples"
__author__ = "Wilson Mar"
__copyright__ = "See the file LICENSE for copyright and license info"
__license__ = "See the file LICENSE for copyright and license info"
__linkedin__ = "https://linkedin.com/in/WilsonMar"
# Using semver.org format per PEP440: change on every commit:
__last_commit__ = "python-samples.py 0.3.10 aws login & 8ball with pct flag"
# login aws
# fix y = x["main"] error
# click instead of argparse
# fix call of get_ipaddr etc without request
# localization results to weather
# fix zip code
# Add 3 retries to url
# gcp_login, gcp_resc_list
# FIXME: import azure , azure_login, azure_resc_list
# aws_login, aws_resc_list


# SECTION 02: Capture pgm start date/time

# See https://wilsonmar.github.io/python-samples/#StartingTime

# Based on: pip3 install datetime
import datetime
# Based on: conda install -c conda-forge time
import time   # for time.sleep(1.5)

# For wall time of program run:
pgm_strt_datetimestamp = datetime.datetime.now()
# the most accurate difference between two times. Used by timeit.
# pgm_strt_perf_counter = time.perf_counter()

# To display date & time of program start:
pgm_strt_timestamp = time.monotonic()
# TODO: Display Z (UTC/GMT) instead of local time
pgm_strt_epoch_timestamp = time.time()
pgm_strt_local_timestamp = time.localtime()
# NOTE: Can't display the dates until formatting code is run below



# SECTION 03. Import libraries (in alphabetical order)

# See https://wilsonmar.github.io/python-samples/#Imports

# For all below, based on: https://pypi.org/project/<import name>/

# The first of several external dependencies, and will error if not installed:
# (preferrably within a conda enviornment):
# requirements.txt
# Absolute imports using "from" are explicitly recommended by PEP 8. That's because
# absolute imports are least impacted by project sharing and changes in the current location of import statements. 

# For wall time of std (standard) imports:
std_strt_datetimestamp = datetime.datetime.now()

# Python’s Standard library of built-in modules imported as
      # listed at https://docs.python.org/3/library/*.html
import base64
import cmd
import collections  # advanced data structures
import csv
import datetime
#from datetime import datetime
import decimal
import doctest   # docstrings
import hashlib
import hmac
import ipaddress
import json
import locale
import logging
import math
import os   # only on unix-like systems
            # for os.getenv(),  os.uname, os.getpid(), os.environ, os.import, os.path
import os.path
import pathlib
import platform
import pprint   # pretty print
import pwd
import random
import re       # regular expressions
import site
import sqlite3
import smtplib  # to send email
# from stat import *
import socket
import subprocess # so CLI output don't show on Terminal
import sys   # built-in     # for sys.argv[0], sys.exit(), sys.version
from sys import platform
import timeit
# import tkinter   # GUI https://pythonbasics.org/tkinter/
import unittest
import uuid
import venv
import webbrowser

# For wall time of standard imports:
std_stop_datetimestamp = datetime.datetime.now()

# For wall time of xpt imports:
xpt_strt_datetimestamp = datetime.datetime.now()

# See https://wilsonmar.github.io/python-samples.py/#PackagesInstalled

# Based on: conda install -c conda-forge azure-core
# import azure.core

# Based on: conda install -c conda-forge azure-cli-core
# https://anaconda.org/conda-forge/azure-cli-core
# from azure.cli.core import get_default_cli as azcli
import azure.cli.core
# Based on: conda install -c conda-forge azure-identity
import azure.identity
# Based on: conda install -c conda-forge azure-storage
import azure.storage.blob

# Based on: conda install -c conda-forge azure-cli-telemetry
# already installed so no need forimport azure.cli.telemetry

# for aws python
# Based on: conda install -c conda-forge boto3
import boto3

# For argparse replacement: https://click.palletsprojects.com/en/8.1.x/
# Based on: conda install -c conda-forge click
import click   # argparse replacement

# from cryptography.fernet import Fernet

# NO import _datetime  # because "datetime" doesn't work on Mac?
# conda install -c conda-forge _datetime  # doesn't work
   # FIXME: Not found: pip3 install _datetime
   # from _datetime import timedelta
# NO conda install -c conda-forge datetime NOR conda install datetime

# from dateutil import tz   # not found in conda
   # See https://bobbyhadz.com/blog/python-no-module-named-dateutil

# Based on: conda install -c conda-forge load_dotenv
from dotenv import load_dotenv
# Based on: conda install python-dotenv   # found!

# Based on: conda install -c conda-forge flask
import flask  

# See https://anaconda.org/search?q=google+cloud
# Based on: conda install google-api-python-client
# import google.api.python.client ???
# Based on: conda install -c conda-forge google-auth
import google.auth

# Based on: conda install -c conda-forge google-auth-credentials
import google.auth.credentials
# https://google-auth.readthedocs.io/en/master/reference/google.auth.transport.requests.html
# Based on: conda install -c conda-forge google-auth-transport-requests
import google.auth.transport.requests
#     https://github.com/googleapis/google-auth-library-python-oauthlib

# Based on: conda install -c conda-forge google-auth-oauthlib  # found!
# import google.auth.oauthlib       #  FIXME: No module named 'google.auth.oauthlib'

# Based on: conda install google-auth-oauthlib  # found!
import google.oauth2.credentials

# See https://github.com/googleapis/google-api-python-client/blob/main/googleapiclient/_helpers.py
# Based on: conda install -c conda-forge google-api-python-client
#import google.api.python.client   # found
# https://snyk.io/advisor/python/google-auth-oauthlib
# https://github.com/googleapis/google-auth-library-python-oauthlib

# https://snyk.io/advisor/python/google-auth-httplib2
# conda install -c conda-forge google_auth_httplib2  # NOT FOUND
# pip3 install google_auth_httplib2
# import google_auth_httplib2
   # google_auth_httplib2 = True

    # Among https://cloud.google.com/apis/docs/overview
    # Among https://cloud.google.com/python/docs/reference
    # Based on:
    # conda install google-api-python-client google-auth-httplib2 google-auth-oauthlib
    # conda install google-auth-transport-requests requests

# Based on: conda install -c conda-forge google-cloud-core
#import google.cloud.core

# pip3 install --ignore-installed google-cloud-vision

# Based on: pip3 install httplib2
import httplib2

# Based on: conda install -c conda-forge hvac
   # https://snyk.io/advisor/python/hvac  # Top 5%
   # HashiCorp Vault Python Client v23.1.2 from 
   # https://pypi.org/project/hvac/
import hvac

# Based on: pip3 install jwt
import jwt

# Based on: pip3 install jsonify  # not found in conda 
import jsonify   # use with flask
    # https://snyk.io/advisor/python/jsonify # Unable to verify the project's public source code repository.

# Based on: conda install -c conda-forge keyring
import keyring
   # import keyring.util.platform_ as keyring_platform

# NOT FOUND on: conda install -c conda-forge locale
# NOT FOUND on: pip3 install locale
# https://phrase.com/blog/posts/beginners-guide-to-locale-in-python/
# import locale  

# NOT FOUND on: conda install -c conda-forge logging
# ERROR
import logging    # see https://realpython.com/python-logging/

# Based on: conda install oauth2client
# See https://snyk.io/advisor/python/oauth2client  # Top 5%
import oauth2client
import oauth2client.client

# Based on: conda install -c conda-forge psutil
import psutil  #  psutil-5.9.5

# import pyjwt  #  pyjwt-2.7.0

# https://snyk.io/advisor/python/pytz  # Top 5%
# Based on: conda install -c conda-forge pytz
import pytz        # pytz-2021.3 for time zone handling

# regex  # regular expression 

# NOT FOUND: conda install -c conda-forge redis
# Based on: pip3 install redis
import redis

# Based on: conda install requests  # already installed
import requests

# NOT FOUND: conda install -c conda-forge shutil
# Based on: pip3 install shutil     # not found either
import shutil

# Based on: conda install -c conda-forge textblob
import textblob
#from textblob import TextBlob

import urllib.request

# Based on: pip3 install textblob   # not found

# For wall time of xpt imports:
xpt_stop_datetimestamp = datetime.datetime.now()

# https://github.com/Tinmen/pyLUID  LUID (Legible Unique ID)



# SECTION 04: Default command-line arguments parameters to shown initial menu for verbosity settings:

# Initial logic controls:
# -clear Console so output always appears at top of screen.
clear_cli = True       # -clear
use_flask = True       # -flask

show_print_samples = True
show_fail = True       # Always show
show_error = True      # Always show
show_warning = True    # -wx  Don't display warning
show_todo = True       # -td  Display TODO item for developer
show_info = True       # -qq  Display app's informational status and results for end-users
show_heading = True    # -q  Don't display step headings before attempting actions
show_verbose = True    # -v  Display technical program run conditions
show_trace = True      # -vv Display responses from API calls for debugging code
show_secrets = False   # Never show

show_config = True

use_env_file = True    # -env
# PROTIP: Global variable referenced within functions:
global ENV_FILE
ENV_FILE="python-samples.env"



# SECTION 05. Use CLI menu to control program operation

# See https://wilsonmar.github.io/python-samples/#ParseArguments

if clear_cli:
    # import os
    # QUESTION: What's the output variable?
    lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def set_cli_parms(count):
    """Present menu and parameters to control program
    """
    import click
    @click.command()
    @click.option('--count', default=1, help='Number of greetings.')
    #@click.option('--name', prompt='Your name',
    #              help='The person to greet.')
    def set_cli_parms(count):
        for x in range(count):
            click.echo(f"Hello!")
    # Test by running: ./python-examples.py --help


# SECTION 06: Define utilities for printing (in color with emojis)

# See https://wilsonmar.github.io/python-samples/#PrintColors

# QUESTION: How to pull in text_in containing {}.

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
    """ A function to put a blank line in CLI output. Used in case the technique changes throughout this code. """
    print(" ")

def print_heading(text_in):
    if show_heading:
        print('\n***', bcolors.HEADING+bcolors.UNDERLINE,f'{text_in}', bcolors.RESET)

def print_fail(text_in):  # when program should stop
    if show_fail:
        print('***', bcolors.FAIL, "FAIL:", f'{text_in}', bcolors.RESET)

def print_error(text_in):  # when a programming error is evident
    if show_fail:
        print('***', bcolors.ERROR, "ERROR:", f'{text_in}', bcolors.RESET)

def print_warning(text_in):
    if show_warning:
        print('***', bcolors.WARNING, f'{text_in}', bcolors.RESET)

def print_todo(text_in):
    if show_todo:
        print('***', bcolors.CVIOLET, "TODO:", f'{text_in}', bcolors.RESET)

def print_info(text_in):
    if show_info:
        print('***', bcolors.INFO+bcolors.BOLD, f'{text_in}', bcolors.RESET)

def print_verbose(text_in):
    if show_verbose:
        print('***', bcolors.VERBOSE, f'{text_in}', bcolors.RESET)

def print_trace(text_in):  # displayed as each object is created in pgm:
    if show_trace:
        print('***', bcolors.TRACE, f'{text_in}', bcolors.RESET)

def print_secret(secret_in):
    """ Outputs only the first few characters (like Git) with dots replacing the rest 
    """
    # See https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
    if show_secrets:  # program parameter
        print('***', bcolors.CBEIGE, "SECRET: ", f'{secret_in}', bcolors.RESET)
    else:
        # same length regardless of secret length to reduce ability to guess:
        secret_len = 32  
        if len(secret_in) >= 20:  # slice
            secret_out = secret_in[0:4] + "."*(secret_len-4)
        else:
            secret_out = secret_in[0:4] + "."*(secret_len-1)
            print('***', bcolors.CBEIGE, "SECRET: ", f'{secret_out}', bcolors.RESET)

def print_samples():
    print_heading("show_print_samples")
    print_fail("sample fail")
    print_error("sample error")
    print_warning("sample warning")
    print_todo("sample task to do")
    print_info("sample info")
    print_verbose("sample verbose")
    print_trace("sample trace")
    print_secret("1234567890123456789")

# See https://wilsonmar.github.io/python-samples/#PrintColors



# SECTION 07. Manage data storage folders and files

# See https://wilsonmar.github.io/python-samples/#FileMgmt

def dir_remove(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # deletes a directory and all its contents.
        # os.remove(img_file_path)  # single file
    # Alternative: Path objects from the Python 3.4+ pathlib module also expose these instance methods:
        # pathlib.Path.unlink()  # removes a file or symbolic link.
        # pathlib.Path.rmdir()   # removes an empty directory.


def dir_tree(startpath):
    # Thanks to
    # https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print_trace('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print_trace('{}{}'.format(subindent, f))

    # TODO: Hint that this returns list data type:


def about_disk_space():
    statvfs = os.statvfs(".")
    # Convert to bytes, multiply by statvfs.f_frsize and divide for Gigabyte
    # representation:
    GB = 1000000
    disk_total = ((statvfs.f_frsize * statvfs.f_blocks) /
                  statvfs.f_frsize) / GB
    disk_free = ((statvfs.f_frsize * statvfs.f_bfree) / statvfs.f_frsize) / GB
    # disk_available = ((statvfs.f_frsize * statvfs.f_bavail ) / statvfs.f_frsize ) / GB
    disk_list = [disk_total, disk_free]
    return disk_list

    # This returns date object:


def file_creation_date(path_to_file, my_os_platform):
    """
    Get the datetime stamp that a file was created, falling back to when it was
    last modified if that isn't possible.
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
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def file_remove(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)  # deletes a directory and all its contents.

# TODO: Create, navigate to, and remove local working folders:


# SECTION 08. Get pgm run env data

# See https://wilsonmar.github.io/python-samples/#run_env

def os_platform():
    import platform # https://docs.python.org/3/library/platform.html
    platform_system = platform.system()
       # 'Linux', 'Darwin', 'Java', 'Windows'
    print_trace("platform_system="+platform_system)
    if platform_system == "Darwin":
        my_platform = "macOS"
    elif platform_system == "linux" or platform_system == "linux2":
        my_platform = "Linux"
    elif platform_system == "win32":
        my_platform = "Windows"
    else:
        print_fail("platform_system="+platform_system+" is unknown!")
        exit(1)
    return my_platform

def print_env_vars():
    """List all environment variables, one line each using pretty print (pprint)
    """
    # import os
    # import pprint
    environ_vars = os.environ
    print_heading("User's Environment variable:")
    pprint.pprint(dict(environ_vars), width = 1)

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
        '22.6': ['Next2023', 2023, '23'],
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

def os_info():
    print_heading("In os_info")
    import platform
    my_os_platform = os_platform()  # defined above.
    print_trace("my_os_platform="+my_os_platform)

    # my_os_platform=localize_blob("version")
    my_os_version = platform.release()  # platform.mac_ver()[0] can be wrong
    print_trace("my_os_version="+my_os_version)
    # Alternately:
    # my_os_version_name = macos_version_name(my_os_version)
    # print_info("my_os_version_name="+my_os_version_name)

    my_os_process = str(os.getpid())
    print_trace("my_os_process="+my_os_process)

        # print_trace("%s %s=%s" % (my_os_platform, localize_blob("version"), platform.mac_ver()[0]),end=" ")
        # print+trace("%s process ID=%s" % ( my_os_name, os.getpid() ))

        # or socket.gethostname()
    my_platform_node = platform.node()
    print_trace("my_platform_node="+my_platform_node)

    my_os_uname = str(os.uname())
    print_trace("my_os_uname="+my_os_uname)
        # MacOS version=%s 10.14.6 # posix.uname_result(sysname='Darwin',
        # nodename='NYC-192850-C02Z70CMLVDT', release='18.7.0', version='Darwin
        # Kernel Version 18.7.0: Thu Jan 23 06:52:12 PST 2020;
        # root:xnu-4903.278.25~1/RELEASE_X86_64', machine='x86_64')

    pwuid_shell = pwd.getpwuid(os.getuid()).pw_shell     # like "/bin/zsh"
    # preferred over os.getuid())[0]
    # Instead of: conda install psutil   # found
    import psutil

    # machine_uid_pw_name = psutil.Process().username()
    print_trace("pwuid_shell="+pwuid_shell)

    # Obtain machine login name:
    # This handles situation when user is in su mode.
    # See https://docs.python.org/3/library/pwd.html
    pwuid_gid = pwd.getpwuid(os.getuid()).pw_gid         # Group number datatype
    print_trace("pwuid_gid="+str(pwuid_gid)+" (process group ID number)")

    pwuid_uid = pwd.getpwuid(os.getuid()).pw_uid
    print_trace("pwuid_uid="+str(pwuid_uid)+" (process user ID number)")

    pwuid_name = pwd.getpwuid(os.getuid()).pw_name
    print_trace("pwuid_name="+pwuid_name)

    pwuid_dir = pwd.getpwuid(os.getuid()).pw_dir         # like "/Users/johndoe"
    print_trace("pwuid_dir="+pwuid_dir)
    
    from pathlib import Path
    # See https://wilsonmar.github.io/python-samples#run_env
    global user_home_dir_path
    user_home_dir_path = str(Path.home())
       # example: /users/john_doe
    print_trace("user_home_dir_path="+user_home_dir_path)
    # the . in .secrets tells Linux that it should be a hidden file.

    # Several ways to obtain:
    # See https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    # this_pgm_name = sys.argv[0]                     # = ./python-samples.py
    # this_pgm_name = os.path.basename(sys.argv[0])   # = python-samples.py
    # this_pgm_name = os.path.basename(__file__)      # = python-samples.py
    # this_pgm_path = os.path.realpath(sys.argv[0])   # = python-samples.py
    # Used by display_run_stats() at bottom:
    this_pgm_name = os.path.basename(os.path.normpath(sys.argv[0]))
    print_trace("this_pgm_name="+this_pgm_name)

    this_pgm_last_commit = __last_commit__
        # Adapted from https://www.python-course.eu/python3_formatted_output.php
    print_trace("this_pgm_last_commit="+this_pgm_last_commit)

    this_pgm_os_path = os.path.realpath(sys.argv[0])
    print_trace("this_pgm_os_path="+this_pgm_os_path)
    # Example: this_pgm_os_path=/Users/wilsonmar/github-wilsonmar/python-samples/python-samples.py

    site_packages_path = site.getsitepackages()[0]
    print_trace("site_packages_path="+site_packages_path)

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


def no_newlines(in_string):
    """ Strip new line from in_string
    """
    return ''.join(in_string.splitlines())


def python_info():
    python_version = no_newlines(sys.version)
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

    print_trace("__name__="+__name__)


    # TODO: Make this function for call before & after run:
    #    disk_list = about_disk_space()
    #    disk_space_free = disk_list[1]:,.1f / disk_list[0]:,.1f
    #    print_info(localize_blob("Disk space free")+"="+disk_space_free+" GB")
        # left-to-right order of fields are re-arranged from the function's output.


# SECTION 09. Obtain run control data from .env file (in the user's $HOME folder)

# See https://wilsonmar.github.io/python-samples/#envFile

def open_env_file(env_file) -> str:
    """
    Return a Boolean obtained from .env file based on key provided.
    """
    print_trace("env_file="+env_file)
    print_trace("user_home_dir_path="+user_home_dir_path)
    global_env_path = user_home_dir_path + "/" + env_file  # concatenate path

    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        print_error(global_env_path+" (global_env_path) not found!")
    else:
        print_info(global_env_path+" (global_env_path) readable.")

    path = pathlib.Path(global_env_path)
    # Based on: pip3 install python-dotenv
    from dotenv import load_dotenv
       # See https://www.python-engineer.com/posts/dotenv-python/
       # See https://pypi.org/project/python-dotenv/
    load_dotenv(global_env_path)  # using load_dotenv


#def last_mod_datetime(env_file) -> str:
    """
    Return a Boolean obtained from .env file based on key provided.
    """
    # Using import datetime import pathlib
    # Instead of global_env_path_time = file_creation_date(global_env_path, my_os_platform)
    # From https://www.geeksforgeeks.org/how-to-get-file-creation-and-modification-date-or-time-in-python/
#    path = pathlib.Path(global_env_path)
    
#    timestamp = path.stat().st_mtime
    #dt = _datetime.datetime.utcfromtimestamp(timestamp)
#    dt = datetime.utcfromtimestamp(timestamp)
    # Z = UTC with no time zone
#    formatted = dt.strftime('%A %d %b %Y %I:%M:%S %p Z')
#    print_verbose(global_env_path+" last modified " + formatted)
    # get creation time on windows
    # current_timestamp = path.stat().st_ctime
    # WARNING: Don't change the system's locale setting within a Python program because
    # locale is global and affects other applications.
    return True

def get_bool_from_env_file(key_in) -> bool:
    """Return a value of boolean (True/False) data type from OS environment or .env file
    (using pip python-dotenv)
    See https://how.wtf/read-environment-variables-from-file-in-python.html
    """
    env_var = os.environ.get(key_in)
    if not env_var:  # yes, defined=True, use it:
        print_warning(key_in + " not found in OS nor .env file " + ENV_FILE)
        return None
    else:
        print_trace(key_in + "=" + str(env_var) + " from .env")
        return bool(env_var)

def get_str_from_env_file(key_in) -> str:
    """Return a value of string data type from OS environment or .env file
    (using pip python-dotenv)
    """
    env_var = os.environ.get(key_in)
    if not env_var:  # yes, defined=True, use it:
        print_warning(key_in + " not found in OS nor .env file " + ENV_FILE)
        return None
    else:
        print_trace(key_in + "=\"" + str(env_var) + "\" from .env")
        return str(env_var)

def get_secret_from_env_file(key_in) -> str:
    """Return a secret value of string data type from OS environment or .env file
    (using pip python-dotenv)
    """
    env_var = os.environ.get(key_in)  # using pip python-dotenv
    if not env_var:  # yes, defined=True, use it:
        print_warning(key_in + " not found in OS nor .env file " + ENV_FILE)
        return None
    else:
        print_trace(key_in + " (secret) retrieved from .env")
        return str(env_var)

def get_int_from_env_file(key_in) -> int:
    """Return an integer number data type from OS environment or .env file
    (using pip python-dotenv)
    """
    env_var = os.environ.get(key_in)  # using pip python-dotenv
    if not env_var:  # yes, defined=True, use it:
        print_warning(key_in + " not found in OS nor .env file " + ENV_FILE)
        return None
    else:
        if str(env_var) == "False":
            print_trace(key_in + "=False=0 from .env")
            return 0
        elif str(env_var) == "True":
            print_trace(key_in + "=True=100 from .env")
            return 100
        elif int(env_var) > 100:
            print_trace(key_in + "= 100, fix of " + str(env_var) + " from .env")
            return 100
        else:
            print_trace(key_in + "=" + str(env_var) + " from .env")
            return int(env_var)

def get_float_from_env_file(key_in) -> float:
    """Return a floating-point number data type from OS environment or .env file
    (using pip python-dotenv)
    """
    env_var = os.environ.get(key_in)  # using pip python-dotenv
    if not env_var:  # yes, defined=True, use it:
        print_warning(key_in + " not found in OS nor .env file " + ENV_FILE)
        return None
    else:
        print_trace(key_in + "=" + env_var + " from .env")
        return float(env_var)


def read_env_file():
    print_heading("in read_env_file")

    global main_loop_runs_requested
    main_loop_runs_requested = get_int_from_env_file('main_loop_runs_requested')
    if not main_loop_runs_requested:
        # PROTIP: Define a data type at creation so it can contain a large number?
        main_loop_runs_requested=int(1)
        print_warning("main_loop_runs_requested="+str(main_loop_runs_requested)+" "+str(type(main_loop_runs_requested))+" from default!")

    global main_loop_pause_seconds
    main_loop_pause_seconds = get_float_from_env_file('main_loop_pause_seconds')
    if not main_loop_pause_seconds:
        # PROTIP: Define a big float data type at creation so it can contain a large number:
        main_loop_pause_seconds=float(0)   # NOT float(999)  # float(5.5)
        print_warning("main_loop_pause_seconds="+str(main_loop_pause_seconds)+" "+str(type(main_loop_pause_seconds))+" from default!")

    global main_loop_run_pct
    main_loop_run_pct = get_int_from_env_file('main_loop_run_pct')
    if not main_loop_run_pct:
        main_loop_run_pct = 100
        print_warning("main_loop_run_pct="+str(main_loop_run_pct)+" from default!")


    # NOTE: Country code can also come from IP Address lookup
                   # "US" # For use in whether to use metric
    global my_country
    my_country = get_str_from_env_file('MY_COUNTRY')
    if not my_country:
        my_country = "US"
        print_warning("my_country="+str(my_country)+" from default!")

    # CAUTION: PROTIP: LOCALE values are different on Windows than Linux/MacOS
    # "ar_EG", "ja_JP", "zh_CN", "zh_TW", "hi" (Hindi), "sv_SE" #sweden/Swedish
    global locale_from_env
    locale_from_env = get_str_from_env_file('MY_LOCALE')  # for translation
    if locale_from_env:
        my_locale = locale_from_env
        print_verbose("my_locale="+my_locale+" from system.")
    else:
        my_locale = "en_US"
        print_warning("LOCALE="+my_locale+" from default!")

    global my_encoding
    my_encoding = get_str_from_env_file('MY_ENCODING')  # "UTF-8"
    if not my_encoding:
        my_encoding = "UTF-8"
        print_warning("my_encoding="+my_encoding+" from default!")

    global my_tz_name_from_env
    my_tz_name_from_env = get_str_from_env_file('MY_TIMEZONE_NAME')
    if my_tz_name_from_env:
        my_tz_name = my_tz_name_from_env
    else:
        # Get time zone code from local operating system:
        # import datetime  # for Python 3.6+
        #my_tz_name = str(_datetime.datetime.utcnow().astimezone().tzinfo)
        # TODO: Fi _datetime
        my_tz_name="whatever"
        #my_tz_name = str(datetime.utcnow().astimezone().tzinfo)
            # _datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
            # = "MST" for U.S. Mountain Standard Time, or 'Asia/Kolkata'
        print_warning("my_tz_name="+str(my_tz_name)+" from default!")

    # "90210"  # use to lookup country, US state, long/lat, etc.
    global my_zip_code
    my_zip_code = get_str_from_env_file('MY_ZIP_CODE')
    if not my_zip_code:
        my_zip_code = "90210"   # Beverly Hills, CA, for demo usage.
        print_warning("my_zip_code="+my_zip_code+" from default!")

    global my_longitude
    my_longitude = get_str_from_env_file('MY_LONGITUDE')
    if not my_longitude:
        my_longitude = "104.322"
        print_warning("my_longitude="+my_longitude+" from default!")

    global my_latitude
    my_latitude = get_str_from_env_file('MY_LATITUDE')
    if not my_latitude:
        my_latitude = "34.123"
        print_warning("my_latitude="+my_latitude+" from default!")

    global my_currency
    my_currency = get_str_from_env_file('MY_CURRENCY')
    if not my_currency:
        my_currency = "USD"
        print_warning("my_currency="+my_currency+" from default!")

    global my_date_format
    my_date_format = get_str_from_env_file('MY_DATE_FORMAT')
    if not my_date_format:
        my_date_format = "%A %d %b %Y %I:%M:%S %p %Z %z"
        # TODO: Override default date format based on country
            # Swedish dates are like 2014-11-14 instead of 11/14/2014 in the US.
            # https://www.wikiwand.com/en/Date_format_by_country shows only 7 date style formats
            # See https://wilsonmar.github.io/python-coding/#DurationCalcs
#        if load_country_db:
#            country_info_dict=get_data_from_country_db(my_country)
#            if country_info_dict:  # TODO:
#                print_info(country_info_dict)  # "D/M/Y"
        print_warning("my_date_format="+my_date_format+" from default!")


# SECTION 10: Load .env values or hard-coded default values (in order of code)

# See https://wilsonmar.github.io/python-samples/#envLoad

# See https://stackoverflow.com/questions/40216311/reading-in-environment-variables-from-an-environment-file

    global verify_manually
    verify_manually = get_bool_from_env_file('verify_manually')
    if not verify_manually:
        verify_manually = False
        print_warning("verify_manually="+str(verify_manually)+" from default!")

# 6. Obtain run control data from .env file in the user's $HOME folder
#    to obtain the desired cloud region, zip code, and other variable specs.

    global show_en
    show_env = get_bool_from_env_file('show_env')
    if not show_env:
        show_env = True
        print_warning("show_env="+str(show_env)+" from default!")

    global show_config
    show_config = get_bool_from_env_file('show_config')
    if not show_config:
        show_config = True
        print_warning("show_config="+str(show_config)+" from default!")

    global use_flask
    use_flask = get_bool_from_env_file('use_flask')
    if not use_flask:
        use_flask = True
        print_warning("use_flask="+str(use_flask)+" from default!")

    global remove_env_line
    remove_env_line = get_bool_from_env_file('remove_env_line')
    if not remove_env_line:
        remove_env_line = True
        print_warning("remove_env_line="+str(remove_env_line)+" from default!")

    global localize_text
    localize_text = get_bool_from_env_file('localize_text')
    if not localize_text:
        localize_text = True
        print_warning("localize_text="+str(localize_text)+" from default!")

    global show_pgminfo
    show_pgminfo = get_bool_from_env_file('show_pgminfo')
    if not show_pgminfo:
        show_pgminfo = True
        print_warning("show_pgminfo="+str(show_pgminfo)+" from default!")

    global use_pytz_datetime
    use_pytz_datetime = get_bool_from_env_file('use_pytz_datetime')
    if not use_pytz_datetime:
        use_pytz_datetime = True
        print_warning("use_pytz_datetime="+str(use_pytz_datetime)+" from default!")

    global show_dates
    show_dates = get_bool_from_env_file('show_dates')
    if not show_dates:
        show_dates = True
        print_warning("show_dates="+str(show_dates)+" from default!")

    global show_logging
    show_logging = get_bool_from_env_file('show_logging')
    if not show_logging:
        show_logging = False
        print_warning("show_logging="+str(show_logging)+" from default!")


    global gen_hash
    gen_hash = get_bool_from_env_file('gen_hash')
    if not gen_hash:
        gen_hash = False
        print_warning("gen_hash="+str(gen_hash)+" from default!")

    global gen_salt
    gen_salt = get_bool_from_env_file('gen_salt')
    if not gen_salt:
        gen_salt = False
        print_warning("gen_salt="+str(gen_salt)+" from default!")

    global gen_0_to_100
    gen_0_to_100 = get_int_from_env_file('gen_0_to_100')
    if not gen_0_to_100:
        gen_0_to_100 = 0  # False
        print_warning("gen_0_to_100="+str(gen_0_to_100)+" from default!")

    global process_romans
    process_romans = get_bool_from_env_file('process_romans')
    if not process_romans:
        process_romans = False
        print_warning("process_romans="+str(process_romans)+" from default!")

    global gen_jwt
    gen_jwt = get_bool_from_env_file('gen_jwt')
    if not gen_jwt:
        gen_jwt = False
        print_warning("gen_jwt="+str(gen_jwt)+" from default!")

    global gen_lotto
    gen_lotto = get_bool_from_env_file('gen_lotto')
    if not gen_lotto:
        gen_lotto = False
        print_warning("gen_lotto="+str(gen_lotto)+" from default!")

    global gen_magic_8ball
    gen_magic_8ball = get_bool_from_env_file('gen_magic_8ball')
    if not gen_magic_8ball:
        gen_magic_8ball = False
        print_warning("gen_magic_8ball="+str(gen_magic_8ball)+" from default!")

    global gen_fibonacci
    gen_fibonacci = get_bool_from_env_file('gen_fibonacci')
    if not gen_fibonacci:
        gen_fibonacci = False
        print_warning("gen_fibonacci="+str(gen_fibonacci)+" from default!")

    global make_change
    make_change = get_bool_from_env_file('make_change')
    if not make_change:
        make_change = False
        print_warning("make_change="+str(make_change)+" from default!")

    global fill_knapsack
    fill_knapsack = get_bool_from_env_file('fill_knapsack')
    if not fill_knapsack:
        fill_knapsack = False
        print_warning("fill_knapsack="+str(fill_knapsack)+" from default!")

    global get_ipaddr
    get_ipaddr = get_bool_from_env_file('get_ipaddr')
    if not get_ipaddr:
        get_ipaddr = False
        print_warning("get_ipaddr="+str(get_ipaddr)+" from default!")
    
    global geodata_from_ipaddr
    geodata_from_ipaddr = get_bool_from_env_file('geodata_from_ipaddr')
    if not geodata_from_ipaddr:
        geodata_from_ipaddr = False
        print_warning("geodata_from_ipaddr="+str(geodata_from_ipaddr)+" from default!")

    global geodata_from_zipinfo
    geodata_from_zipinfo = get_bool_from_env_file('geodata_from_zipinfo')
    if not geodata_from_zipinfo:
        geodata_from_zipinfo = False
        print_warning("geodata_from_zipinfo="+str(geodata_from_zipinfo)+" from default!")

    global show_weather
    show_weather = get_bool_from_env_file('show_weather')
    if not show_weather:
        show_weather = False
        print_warning("show_weather="+str(show_weather)+" from default!")

    global email_weather
    email_weather = get_bool_from_env_file('email_weather')
    if not email_weather:
        email_weather = False
        print_warning("email_weather="+str(email_weather)+" from default!")

    global use_keyring
    use_keyring = get_bool_from_env_file('use_keyring')
    if not use_keyring:
        use_keyring = False
        print_warning("use_keyring="+str(use_keyring)+" from default!")


    # Python library for HashiCorp Vault:
    global use_hvault
    use_hvault = get_int_from_env_file('use_hvault')
    if not use_hvault:
        use_hvault = False
        print_warning("use_hvault="+str(use_hvault)+" from default!")

    global refresh_vault_certs
    refresh_vault_certs = get_bool_from_env_file('refresh_vault_certs')
    if not refresh_vault_certs:
        refresh_vault_certs = False
        print_warning("refresh_vault_certs="+str(refresh_vault_certs)+" from default!")


    global use_azure
    use_azure = get_bool_from_env_file('use_azure')
    if not use_azure:
        use_azure = False
        print_warning("use_azure="+str(use_azure)+" from default!")

    global login_to_azure
    login_to_azure = get_bool_from_env_file('login_to_azure')
    if not login_to_azure:
        login_to_azure = False
        print_warning("login_to_azure="+str(login_to_azure)+" from default!")

    global list_azure_resc
    list_azure_resc = get_bool_from_env_file('list_azure_resc')
    if not list_azure_resc:
        list_azure_resc = False
        print_warning("list_azure_resc="+str(list_azure_resc)+" from default!")


    global use_azure_redis
    use_azure_redis = get_bool_from_env_file('use_azure_redis')
    if not use_azure_redis:
        use_azure_redis = False
        print_warning("use_azure_redis="+str(use_azure_redis)+" from default!")


    global use_aws
    use_aws = get_bool_from_env_file('use_aws')
    if not use_aws:
        use_aws = False
        print_warning("use_aws="+str(use_aws)+" from default!")

    global show_aws_init
    show_aws_init = get_bool_from_env_file('show_aws_init')
    if not show_aws_init:
        show_aws_init = True
        print_warning("show_aws_init="+str(show_aws_init)+" from default!")
    # https://aws.amazon.com/cdk/ = Cloud Development Kit v2
    # Construct Hub to automate AWS svc provisioning
    # https://aws.amazon.com/blogs/developer/increasing-development-speed-with-cdk-watch/
    # https://github.com/aws-samples/aws-cdk-examples/tree/master/python

    global use_gcp
    use_gcp = get_bool_from_env_file('use_gcp')
    if not use_gcp:
        use_gcp = False
        print_warning("use_gcp="+str(use_gcp)+" from default!")

    global use_add_blockchain
    add_blockchain = get_bool_from_env_file('add_blockchain')
    if not add_blockchain:
        add_blockchain = False
        print_warning("add_blockchain="+str(add_blockchain)+" from default!")

    global download_imgs
    download_imgs = get_bool_from_env_file('download_imgs')
    if not download_imgs:
        download_imgs = False
        print_warning("download_imgs="+str(download_imgs)+" from default!")

    global img_set
    img_set = get_bool_from_env_file('img_set')
    if not img_set:
        img_set = False
        print_warning("img_set="+str(img_set)+" from default!")

    # TODO: Specify in argparse above?
    global img_file_name
    img_file_name = get_bool_from_env_file('img_file_name')
    if not img_file_name:
        img_file_name = "???"
        print_warning("img_file_name="+img_file_name+" from default!")

    global process_img
    process_img = get_bool_from_env_file('process_img')
    if not process_img:
        process_img = False
        print_warning("process_img="+str(process_img)+" from default!")

    global img_file_naming_method
    img_file_naming_method = get_str_from_env_file('img_file_naming_method')
    if not img_file_naming_method:
        img_file_naming_method = "uuid4time"  # or "uuid4hex" or "uuid4"
        print_warning("img_file_naming_method="+img_file_naming_method+" from default!")

    global remove_img_dir_at_beg
    remove_img_dir_at_beg = get_bool_from_env_file('remove_img_dir_at_beg')
    if not remove_img_dir_at_beg:
        remove_img_dir_at_beg = False
        print_warning("remove_img_dir_at_beg=" +
                    str(remove_img_dir_at_beg)+" from default!")

    # to clean up folder
    global remove_img_file_at_beg
    remove_img_file_at_beg = get_bool_from_env_file('remove_img_file_at_beg')
    if not remove_img_file_at_beg:
        remove_img_file_at_beg = False
        print_warning("remove_img_file_at_beg=" +
                    str(remove_img_file_at_beg)+" from default!")

    # to clean up folder
    global remove_img_dir_at_end
    remove_img_dir_at_end = get_bool_from_env_file('remove_img_dir_at_end')
    if not remove_img_dir_at_end:
        remove_img_dir_at_end = False
        print_warning("remove_img_dir_at_end=" +
                    str(remove_img_dir_at_end)+" from default!")

    # to clean up file in folder
    global remove_img_file_at_end
    remove_img_file_at_end = get_bool_from_env_file('remove_img_file_at_end')
    if not remove_img_file_at_end:
        remove_img_file_at_end = False
        print_warning("remove_img_file_at_end=" +
                    str(remove_img_file_at_end)+" from default!")

    global send_fax
    send_fax = get_bool_from_env_file('send_fax')
    if not send_fax:
        send_fax = False
        print_warning("send_fax="+str(send_fax)+" from default!")


    global send_sms
    send_sms = get_bool_from_env_file('send_sms')
    if not send_sms:
        send_sms = False
        print_warning("send_sms="+str(send_sms)+" from default!")

    global send_slack
    send_slack = get_int_from_env_file('send_slack')
    if not send_slack:
        send_slack = 0
        print_warning("send_slack="+str(send_slack)+" from default!")

    global email_via_gmail
    email_via_gmail = get_bool_from_env_file('email_via_gmail')
    if not email_via_gmail:
        email_via_gmail = False
        print_warning("email_via_gmail="+str(email_via_gmail)+" from default!")

    global verify_email
    verify_email = get_bool_from_env_file('verify_email')
    if not verify_email:
        verify_email = False
        print_warning("verify_email="+str(verify_email)+" from default!")

    global email_file_path
    email_file_path = get_str_from_env_file('email_file_path')
    if not email_file_path:
        email_file_path = ""
        print_warning("email_file_path="+str(email_file_path)+" from default!")


    # (use MD5 Hash)
    global view_gravatar
    view_gravatar = get_bool_from_env_file('view_gravatar')
    if not view_gravatar:
        view_gravatar = False
        print_warning("view_gravatar="+str(view_gravatar)+" from default!")

    global categorize_bmi
    categorize_bmi = get_bool_from_env_file('categorize_bmi')
    if not categorize_bmi:
        categorize_bmi = False
        print_warning("categorize_bmi="+str(categorize_bmi)+" from default!")

    global gen_sound_for_text
    gen_sound_for_text = get_str_from_env_file('gen_sound_for_text')
    if not gen_sound_for_text:
        gen_sound_for_text = False
        print_warning("gen_sound_for_text="+str(gen_sound_for_text)+" from default!")

    global remove_sound_file_generated
    remove_sound_file_generated = get_str_from_env_file('remove_sound_file_generated')
    if not remove_sound_file_generated:
        remove_sound_file_generated = True
        print_warning("remove_sound_file_generated=" +
                    str(remove_sound_file_generated)+" from default!")

    global cleanup_img_files
    cleanup_img_files = get_bool_from_env_file('cleanup_img_files')
    if not cleanup_img_files:
        cleanup_img_files = False
        print_warning("cleanup_img_files="+str(cleanup_img_files)+" from default!")

    global update_md_files
    update_md_files = get_bool_from_env_file('update_md_files')
    if not update_md_files:
        update_md_files = False
        print_warning("update_md_files="+str(update_md_files)+" from default!")

    global display_run_stats
    display_run_stats = get_bool_from_env_file('display_run_stats')
    if not display_run_stats:
        display_run_stats = False
        print_warning("display_run_stats="+str(display_run_stats)+" from default!")


# SECTION 11. Manage sqliteDB countryDB reference DB

# See https://wilsonmar.github.io/python-samples/#SQLLite

# CAUTION: Avoid printing api_key value and other secrets to console or logs.

# CAUTION: Leaving secrets anywhere on a laptop is dangerous. One click on a malicious website and it can be stolen.
# It's safer to use a cloud vault such as Amazon KMS, Azure, Hashicorp Vault after signing in.
# https://blog.gruntwork.io/a-comprehensive-guide-to-managing-secrets-in-your-terraform-code-1d586955ace1#bebe
# https://vault-cli.readthedocs.io/en/latest/discussions.html#why-not-vault-hvac-or-hvac-cli

def check_sqlite_header(sqlite3_db_name):

    # Check if first 100 bytes of path identifies itself as sqlite3 in header:
    # From https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
    f = open(sqlite3_db_name, "rx")
    ima = f.read(16).encode('hex')
    f.close()
    # see http://www.sqlite.org/fileformat.html#database_header magic header string
    if ima != "53514c69746520666f726d6174203300":
        return 3
    else:
        return None


def open_sqlite3_db(sqlite3_db_name):

    cwd = os.getcwd()  # Get current working directory
    print_verbose("Current working directory: {0}".format(cwd))

    import sqlite3
    try:
        # Try to see if db file exists (can be opened) in operating system:
        with open(cwd + "/" + sqlite3_db_name): pass
        # WARNING: Use SQLite rather than operating system commands to delete db.
    except IOError:
        print_verbose("Create SQLite database " + sqlite3_db_name)

    try:  # Connect to SQLite: https://zetcode.com/db/sqlitepythontutorial/
        conn = sqlite3.connect(sqlite3_db_name)
        cursor = conn.cursor()

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print_verbose("SQLite database " + sqlite3_db_name +
                      " version: " + str(record))

        # See if table can be accessed by querying the built-in sqlite_master table within every db:
        cursor.execute('''SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_name';''')
        print_verbose(check_sqlite_header(sqlite3_db_name))
        print_verbose(cursor.fetchall())

        if cursor.fetchone()[0] == 1:  # if the count is 1, then table exists:
            print_trace('Table exists.')
            return cursor  # FIXME: TypeError: 'NoneType' object is not subscriptable
        else:
            print_trace('Table does not exist.')
            # Create db if not there:
            try:
                create_country_table_query = '''CREATE TABLE Country_data (
                                        country_name TEXT NOT NULL,
                                        country_id2 INTEGER PRIMARY KEY,
                                        country_id3 INTEGER SECONDARY KEY,
                                        country_population REAL,
                                        country_area_km2 REAL,
                                        country_gdp REAL);'''
                conn.execute(create_country_table_query)
                conn.commit()
                print_trace("SQLite table Country_data created.")
                return cursor
            except sqlite3 as error:
                print_fail("SQLite database " + sqlite3_db_name+" error: " + str(error))
                return None
    except IOError as error:
        # FIXME: print_fail("SQLite database "+ sqlite3_db_name+" error: " + str(error))
        print_fail("SQLite database " + sqlite3_db_name+" error")
        return None

# TODO: def get_dtformat_from_locale():


def get_data_from_country_db(country_id):
    # Load Country SQLite in-memory database for date-time formats = load_country_db
    # TODO: Delete database if requested.
    print_heading("load_country_db")

    sqlite3_db_name = "SQLite3_country.db"
    conn = open_sqlite3_db(sqlite3_db_name)
    if load_country_db:
        try:
            cursor.execute('''SELECT name FROM sqlite_master
                WHERE type='table' AND name='table_name';''')
            if cursor.fetchone()[0] == 1:  # if the count is 1, then table exists:
                print_trace('Table exists.')
                return cursor
            else:
                print_trace('Do main table tasks.')
                # https://towardsdatascience.com/python-sqlite-tutorial-the-ultimate-guide-fdcb8d7a4f30
                # https://datagy.io/sql-beginners-tutorial/

                # TODO: Load country data from csv file
                # Alternately (Excel vis=a OpenPyXL):
                # more_users = [('00003', 'Peter', 'Parker', 'Male'), ('00004', 'Bruce', 'Wayne', 'male')]
                # cur.execute("INSERT INTO users VALUES(?, ?, ?, ?);", user)
                # conn.commit()

                # TODO: Create indexes
                # cur.execute("""SELECT *, users.fname, users.lname FROM orders LEFT JOIN users ON users.userid=orders.userid;""")
                # print_trace(cur.fetchall())

                # TODO: Lookup index 1 - 2 char country for Linux (highest priority)
                # TODO: Lookup index 2 - 3 char country for Windows (medium priority)
                # TODO: Lookup index 3 - Phone code (low priority)

                # TODO: Retrieve date_time, phone, population, land, GDP

        except IOError as error:
            print_fail("SQLite database " + sqlite3_db_name+" error: " + str(error))
            return None
        finally:
            if conn:
                conn.close()
                print_verbose("SQLite database " + sqlite3_db_name+" connection closed.")

        locale_dict = dict()
        locale_dict['en_US'] = 'D/M/Y'  # HARD-CODING FOR DEBUGGING
        return locale_dict   # {'en_US': 'D/M/Y'}


# SECTION 12. Localize/translate text to the specified locale

# See https://wilsonmar.github.io/python-samples/#Localize

# internationalization according to localization setting:
def format_epoch_datetime(date_in):
    return (time.strftime(my_date_format, time.localtime(date_in)))

# internationalization according to localization setting:


def format_number(number):
    return ("{:,}".format(number))

def set_locale():

        # TODO: Because locale package is not found:
        # Use user's default settings by setting as blank:
#        locale.setlocale(locale.LC_ALL, '')
        # Use current setting:
#        locale.setlocale(locale.LC_ALL, None)

    # TODO: if value from parsing command parameters, override value from env:
    if my_locale:  # locale_from_env:  # not empty:
        my_locale = locale_from_env
    else:  # fall back # from operating system:
        my_locale = locale.getlocale()

    if not my_locale:
        my_locale = "en_US"  # hard-coded default such as "en_US"

    try:
        locale.setlocale(locale.LC_TIME, my_locale)
    except BaseException:
        print_fail("Exception in setting OS LOCALE "+my_locale)

    # for lang in locale.locale_alias.values():  # print all locales with "UTF-8"
    #    print_trace("lang="+lang)


# Preparations for translation:
    # pip install textblob  # translates text using API calls to Google Translate.
    # python -m textblob.download_corpora
def localize_blob(byte_array_in):
    if not localize_text:
        return byte_array_in

    if type(byte_array_in) is not str:
        print_trace("byte_array_in="+byte_array_in)
        return byte_array_in
    else:
        # https://textblob.readthedocs.io/en/dev/
        from textblob import TextBlob
        blob = TextBlob(byte_array_in)
    try:
        translated = blob.translate(to=my_locale)  # such as 'de_DE'
    except BaseException:
        translated = byte_array_in
    return translated
    # https://textblob.readthedocs.io/en/dev/ can also perform natural language processing (NLP) tasks such as
    # part-of-speech tagging, noun phrase extraction, sentiment analysis,
    # classification, translation, and more.

    # TODO: PROTIP: Provide hint that data type is a time object:


def creation_date(path_to_file):
    print_trace("path_to_file type="+type(path_to_file))
    """
    Requires import platform, import os, from stat import *
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def localized_day_greeting():
    from datetime import datetime
    current_hour = datetime.now().hour
    if current_hour < 12:
        part_of_day = localize_blob('Good morning!')
    elif 12 <= current_hour < 17:
        part_of_day = localize_blob('Good afternoon!')
    else:
        part_of_day = localize_blob('Good evening!')
    return part_of_day


def verify_yes_no_manually(question, default='no'):
    # Adapted from https://gist.github.com/garrettdreyfus/8153571
    if not verify_manually:  # global
        return default
    else:
        if default is None:
            prompt = " [y/n] "
        elif default == 'yes':
            prompt = " [Y/n] "
        elif default == 'no':
            prompt = " [y/N] "
        else:
            raise ValueError(
                f'*** {localize_blob("Unknown setting")} {localize_blob("default")} \"{default}\" ')
        while True:  # Keep asking:
            try:
                resp = input(question + prompt).strip().lower()
                if default is not None and resp == '':
                    return default == 'yes'
                else:
                    return distutils.util.strtobool(
                        resp)  # QUESTION: what is this?
            except ValueError:
                print_error(localize_blob("Please respond")+'"yes" or "y" or "no" or "n"')


# if localize_text:

    # if env_locale != my_locale[0] : # 'en_US'
    #   print_error("env_locale not = "+my_locale[0])
    # print_warning("global_env_path LOCALE "+env_locale+" "+localize_blob("overrides")+" OS LOCALE "+my_locale)

    # NOTE: print_trace(f'Date: {locale.atof("32,824.23")} ')
    # File "/Users/wilsonmar/miniconda3/envs/py3k/lib/python3.8/locale.py", line 326, in atof
    # return func(delocalize(string))
    # ValueError: could not convert string to float: '32.824.23'

    # if my_encoding_from_env:  # not empty:
    #   my_encoding = my_encoding_from_env
    # else:  # fall back to hard-coded default:
    #   my_encoding = "utf-8"  # default: or "cp860" or "latin" or "ascii"


"""if show_trace:
    # Output all locales:
    # See https://docs.python.org/3/library/locale.html#locale.localeconv
    for key, value in locale.localeconv().items():
        print_trace("%s: %s" % (key, value))
"""

#  if show_dates:  # TODO: Move this to the end of the program source code!
def compare_dates():
    print_heading("show_dates using localized format:")
    my_local_time = time.localtime()

    print_trace("pgm_strt_timestamp="+str(pgm_strt_timestamp))
    print_trace("pgm_strt_epoch_timestamp=" +
                str(pgm_strt_epoch_timestamp))  # like 1685264269.421101
    time_val = time.localtime(pgm_strt_epoch_timestamp)
    print_trace("pgm_strt_epoch_timestruct=" + str(time_val))

    global my_date_format
    if my_date_format == "":  # variable contains a value:
        iso_format = '%A %Y-%b-%d %I:%M:%S %p'
        print_warning("Using default date format="+iso_format)
        my_date_format = iso_format

    # Local time with specified timezone name and offset:
    pgm_strt_epoch_time = _datetime.datetime.fromtimestamp(
        pgm_strt_epoch_timestamp)
    dt = _datetime.datetime.utcfromtimestamp(pgm_strt_epoch_timestamp)
    pgm_strt_epoch_time = dt.strftime(
        my_date_format)  # Z = UTC with no time zone
    print_trace("pgm_strt_epoch_time="+str(pgm_strt_epoch_time))

    current_local_time = time.strftime(my_date_format, my_local_time)
    # See https://www.youtube.com/watch?v=r1Iv4d6CO2Q&list=PL98qAXLA6afuh50qD2MdAj3ofYjZR_Phn&t=50s
    print_trace("current_local_time=  "+current_local_time)
    print_trace("my_local_time="+str(my_local_time))
    # Example: Friday 10 Dec 2021 11:59:25 PM MST -0600

    # username_greeting = localized_day_greeting()  # +" by pwuid_name: "+ pwuid_name
    # print_verbose(my_locale+" TZ="+str( my_tz_name ) +" "+ username_greeting)

    #    dt = _datetime.datetime.utcfromtimestamp(pgm_strt_epoch_timestamp)
    #    # NOTE: ISO 8601 and RFC 3339 '%Y-%m-%d %H:%M:%S' or '%Y-%m-%dT%H:%M:%S'
    #    iso_format = '%A %Y-%b-%d %I:%M:%S %p Z(UTC/GMT)'
    #    current_local_time=dt.strftime(iso_format)  # Z = UTC with no time zone
    #    print_trace("current_local_time="+current_local_time)

    if use_pytz_datetime:
        # import pytz
        start_UTC_time = pytz.utc   # get the standard UTC time
        datetime_utc = datetime.now(start_UTC_time)
        print_trace("pgm_strt_time_pytz= "+datetime_utc.strftime(my_date_format))

        # Example of hard-coded time zone:
        # IST = pytz.timezone('Asia/Kolkata')  # Specify a location in India:
        IST = pytz.timezone('Asia/Kolkata')  # Specify a location in India:
        datetime_utc = datetime.now(IST)   # from above
        print_trace("current time at IST= " +
                    datetime_utc.strftime(my_date_format)+" ("+str(IST)+") India")
        # print_trace(str(datetime_utc.strftime(my_date_format))+" India")

    """
    # Get a UTC tzinfo object – by calling tz.tzutc():
    # Based on: from dateutil import tz
    tz.tzutc()
    # Get offset 0 by calling the utcoffset() method with a UTC datetime object:

    # from datetime import timezone
    # import datetime
    # returns number of seconds since the epoch.
    dt = _datetime.datetime.now(timezone.utc)
    # dt = datetime.datetime.now()  # returns number of seconds since the epoch.
    # use tzinfo class to convert datetime to UTC:
    utc_time = dt.replace(tzinfo=timezone.utc)
    print_trace("utc_time="+utc_time)
    # Use the timestamp() to convert the datetime object, in UTC, to get the UTC timestamp:
    utc_timestamp = utc_time.timestamp()
    print_verbose("Epoch utc_timestamp now: "+ str(utc_timestamp))
    # Can't print+trace(utc_timestamp.strftime(my_date_format))  # AttributeError: 'float' object has no attribute 'strftime'

    import datetime
    print_trace("tz.tzutc now: "+ \
                str(tz.tzutc().utcoffset(datetime.datetime.utcnow())) )
    # datetime.timedelta(0)
    """
    
def print_wall_times():
    # All the timings together for consistency of output:
    # TODO: Write to log for longer-term analytics
    
    # For wall time of std imports:
    std_stop_datetimestamp = datetime.datetime.now()
    std_elapsed_wall_time = std_stop_datetimestamp -  std_strt_datetimestamp
    print_verbose("Wall time for import of Python standard libraries:"+ \
        str(std_elapsed_wall_time)+" (hh:mm:sec.microsecs)") 

    # For wall time of xpt imports:
    xpt_stop_datetimestamp = datetime.datetime.now()
    xpt_elapsed_wall_time = xpt_stop_datetimestamp -  xpt_strt_datetimestamp
    print_verbose("Wall time for import of Python extra    libraries:"+ \
        str(xpt_elapsed_wall_time)+" (hh:mm:sec.microsecs)") 

    pgm_stop_datetimestamp = datetime.datetime.now()
    pgm_elapsed_wall_time = pgm_stop_datetimestamp -  pgm_strt_datetimestamp
    pgm_stop_perftimestamp = time.perf_counter()
    print_verbose("Wall time for program run :"+ \
        str(pgm_elapsed_wall_time)+" (hh:mm:sec.microsecs)") 



# SECTION 13. Flask API :

def display_memory():
    import os, psutil  #  psutil-5.9.5
    process = psutil.Process()
    mem=process.memory_info().rss / (1024 ** 2)  # in bytes 
    print_verbose(str(process)+" memory="+str(mem)+" MiB")

def display_flask():

    if use_flask:
        print_heading("display_flask")

        from flask import Flask, jsonify
        app = Flask(__name__)
        songs = [
            {
                "title": "Rockstar",
                "artist": "Dababy",
                "genre": "rap",
            },
            {
                "title": "Say So",
                "artist": "Doja Cat",
                "genre": "Hiphop",
            },
            {
                "title": "Panini",
                "artist": "Lil Nas X",
                "genre": "Hiphop"
            }
        ]

        @app.route('/songs')
        def home():
            return jsonify(songs)


# SECTION 14. Generate Hash (UUID/GUID) from a file    = gen_hash

# See https://wilsonmar.github.io/python-samples/#gen_hash

def gen_hash_text(gen_hash_method, byte_array_in):
    # A hash is a fixed length one way string from input data. Change of even one bit would change the hash.
    # A hash cannot be converted back to the input data (unlike encryption).
    # import hashlib  # https://docs.python.org/3/library/hashlib.html
    # From among hashlib.algorithms_available
    if gen_hash_method == "SHA1":      # spec removed by FIPS 180-4
        m = hashlib.sha1()
    elif gen_hash_method == "SHA224":
        m = hashlib.sha224()
    elif gen_hash_method == "SHA256":
        m = hashlib.sha256()
    elif gen_hash_method == "SHA384":
        m = hashlib.sha384()
    elif gen_hash_method == "SHA512":  # (defined in archived FIPS 180-2)
        m = hashlib.sha512()
    print_todo("Use SHA3 to gen hash")
    # See https://csrc.nist.gov/Topics/Security-and-Privacy/cryptography/secure-hashing
    # See https://www.wikiwand.com/en/Cryptographic_hash_function#/Cryptographic_hash_algorithms
    # SHA224, 224 bits (28 bytes); SHA-256, 32 bytes; SHA-384, 48 bytes; and
    # SHA-512, 64 bytes.

    m.update(byte_array_in)
    if show_verbose:
        print_verbose(
            f'{gen_hash_method} {m.block_size}-bit {m.digest_size}-hexbytes {m.digest_size*2}-characters')
        # print_trace("digest={m.digest()}="+digest={m.digest()})

    return m.hexdigest()


# TODO: Merge into a single function by looking at the type of input.
def gen_hash_file(gen_hash_method, file_in):
    # A hash is a fixed length one way string from input data. Change of even one bit would change the hash.
    # A hash cannot be converted back to the input data (unlike encryption).
    # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python

    # import hashlib  # https://docs.python.org/3/library/hashlib.html
    # From among hashlib.algorithms_available:
    if gen_hash_method == "SHA1":
        m = hashlib.sha1()
    elif gen_hash_method == "SHA224":
        m = hashlib.sha224()
    elif gen_hash_method == "SHA256":
        m = hashlib.sha256()
    elif gen_hash_method == "SHA384":
        m = hashlib.sha384()
    elif gen_hash_method == "SHA512":  # (defined in FIPS 180-2)
        m = hashlib.sha512()
    # See https://www.wikiwand.com/en/Cryptographic_hash_function#/Cryptographic_hash_algorithms
    # SHA224, 224 bits (28 bytes); SHA-256, 32 bytes; SHA-384, 48 bytes; and
    # SHA-512, 64 bytes.

    # See https://death.andgravity.com/hashlib-buffer-required
    # to read files in 64kb chunks rather than sucking the life out of your
    # memory.
    BUF_SIZE = 65536
    # https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html
    with open(file_in, 'rb') as f:   # or sys.argv[1]
        for byte_block in iter(lambda: f.read(BUF_SIZE), b""):
            m.update(byte_block)
    print_verbose(
        f'{gen_hash_method} {m.block_size}-bit {m.digest_size}-hexbytes {m.digest_size*2}-characters')
        # print_trace(f'*** digest={m.digest()} ')

    return m.hexdigest()


class TestGenHash(unittest.TestCase):
    def test_gen_hash(self):

        if gen_hash:
            print_heading("gen_hash")

            # Making each image file name unique ensures that changes in the file resets cache of previous version.
            # UUID = Universally Unique Identifier, which Microsoft calls Globally Unique Identifier or GUID.
            # UUIDs are supposed to be unique in time (stamp) and space (IP address or MAC address).
            # UUIDs are always 128-bit, but can be formatted with dashes or into 32 hex bits.
            # Adapted from https://docs.python.org/3/library/uuid.html
            # CAUTION: uuid1() compromises privacy since it contains the computer’s
            # network IP address.

            # 87509061370279318 portion (sortable)
            if img_file_naming_method == "uuid4time":
                x = uuid.uuid4()
                # cbceb48b-7c97-4b46-b5f7-b55b3d09c2e4
                print_trace(f'*** uuid.uuid4()={x} ')
                print_trace(f'*** x.time={x.time} ')   # 87509061370279318
                # sorted(ss, key= lambda x: x[0].time)
                # CAUTION: Do not use the time portion by itself from
                # {uuid.uuid1().time} as it doesn't have place.

            elif img_file_naming_method == "uuid4":  # with dashes like 5ac79987-9654-4c0a-b70a-46d57cb0d4b9
                x = uuid.uuid4()
                # cbceb48b-7c97-4b46-b5f7-b55b3d09c2e4
                print_trace("uuid.uuid4()="+uuid.uuid4())

            # d42277a3bfcd4f019699d4094c457634 (not sortable)
            elif img_file_naming_method == "uuid4hex":
                x = uuid.uuid4()
                print_trace(f'uuid.uuid1() -> x.hex={x.hex} ')

            print_todo("Gen LUID to sequence UUIDs for better seek perf in memory")
            # See
            # http://coders-errand.com/hash-functions-for-smart-contracts-part-3/

# CUID (Collision Resistant Unique Identifiers) is a method of creating a unique identifier was developed by Eric Elliott
# for use in web applications to better support horizontal scaling and sequential lookup performance than UUIDs.uuid
# https://github.com/ericelliott/cuid


# SECTION 15. Sequential UUIDs

# https://github.com/tvondra/sequential-uuids
# Make UUIDs more sequential by using some sequential value as a prefix.
# Regular random UUIDs are distributed uniformly over the whole range of possible values.
# This results in poor locality when inserting data into indexes - all index leaf pages are equally likely to be hit,
# forcing the whole index into memory. With small indexes that's fine, but once the index size exceeds shared buffers (or RAM),
# the cache hit ratio quickly deteriorates.


# SECTION 16. Create URL Shortener

# https://www.freecodecamp.org/learn/back-end-development-and-apis/back-end-development-and-apis-projects/url-shortener-microservice
#

# SECTION 17. Setup logging

def show_logging():
    # Confirm manually: https://portal.azure.com/#view/Microsoft_Azure_Billing/SubscriptionsBlade
    # https://azure.github.io/azure-sdk/releases/latest/mgmt/python.html
   logger = logging.getLogger(__name__)
   print_info("logger="+str(logger))
   return False  # for now


# SECTION 18. Generate a random Salt

DEFAULT_ENTROPY = 32  # bytes in string to return, by default


def token_urlsafe(nbytes=None):
    tok = token_urlsafe(nbytes)
    # 'Drmhze6EPcv0fN_81Bj-nA'
    return base64.urlsafe_b64encode(tok).rstrip(b'=').decode('ascii')

def gen_salt():
    # “full entropy” (i.e. 128-bit uniformly random value)
    # Based on https://github.com/python/cpython/blob/3.6/Lib/secrets.py
    #     tok=token_urlsafe(16)
    # tok=token_bytes(nbytes=None)
    # 'Drmhze6EPcv0fN_81Bj-nA'
    # print_trace(f'tok{tok} ')

    from random import SystemRandom
    cryptogen = SystemRandom()
    x = [cryptogen.randrange(3) for i in range(20)]  # random ints in range(3)
    # [2, 2, 2, 2, 1, 2, 1, 2, 1, 0, 0, 1, 1, 0, 0, 2, 0, 0, 0, 0]
    print_trace(f'    {x}')

    # print_trace(f'[cryptogen.random() for i in range(3)]  # random floats in [0., 1.)')
    y = [cryptogen.random() for i in range(3)]  # random floats in [0., 1.)
    # [0.2710009745425236, 0.016722063038868695, 0.8207742461236148]
    # print_trace(f'*** {salt_size} salt={password_salt} ')
    print_info(f'    {y}')
    return y



# SECTION 19. Generate random percent of 100:

def gen_0_to_100_int() -> int:
    # see https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b311-random
    # import random  # built-in
    threshold = random.randint(0, 101)
    print_trace("in gen_0_to_100_int threshold="+str(threshold))
    return int(threshold)



# SECTION 20. Convert Roman to Decimal for use of case

# From https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s24.html
def int_to_roman(input):
    print_trace("process_romans: int_to_roman")
    # Convert a input year to a Roman numeral

    if isinstance(input, str):
        input = int(input)

    # FIXME: if not isinstance(input, type(1)):
#        raise TypeError, "expected integer, got %s" % type(input)
#    if not 0 < input < 4000:
#        raise ValueError, "Argument must be between 1 and 3999"
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = (
        'M',
        'CM',
        'D',
        'CD',
        'C',
        'XC',
        'L',
        'XL',
        'X',
        'IX',
        'V',
        'IV',
        'I')
    result = []
    for i in range(len(ints)):
        # FIXME: TypeError: unsupported operand type(s) for /: 'str' and 'int'
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)


def roman_to_int(roman_str_in):
    print_trace("process_romans: roman_to_int")
    # Convert a Roman numeral to an integer

    if not isinstance(roman_str_in, type("")):
        # FIXME: TypeError: unsupported operand type(s) for /: 'str' and 'int'
        #        raise TypeError, "expected string, got %s" % type(input)
        print_error(f'Input \"{roman_str_in}\" not a string')
        return
    roman_str_in = roman_str_in.upper()
    nums = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    sum = 0
    for i in range(len(roman_str_in)):
        try:
            value = nums[roman_str_in[i]]
            # If the next place holds a larger number, this value is negative
            if i + 1 < len(roman_str_in) and nums[roman_str_in[i + 1]] > value:
                sum -= value
            else:
                sum += value
        except KeyError:
            print_fail("FIXME: raise ValueError")
            # FIXME:         raise ValueError, 'input is not a valid Roman numeral: %s' % input
    # easiest test for validity...
    if int_to_roman(sum) == roman_str_in:
        return sum

def get_cur_yyyy():
    date_object = _datetime.datetime.now()
    current_year = date_object.strftime('%Y')
    return current_year



# SECTION 21. Generate JSON Web Token          = gen_jwt

def gen_jwt():
    # import jwt
    jwt_some = "something"
    jwt_payload = "my payload"
    encoded_jwt = jwt.encode({jwt_some: jwt_payload},
                             "secret", algorithm="HS256")
    print_info(f'encoded_jwt={encoded_jwt} ')
    # A
    # eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U
    response = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    # {'some': 'payload'}
    print_trace(f'response={response} ')
    return response



# SECTION 22. Generate Lotto using random range    = gen_lotto_num

def gen_lotto_num():
    lotto_numbers = ""
    for x in range(5):
        # (1 more than 52 due to no 0)
        lotto_numbers = lotto_numbers + str(random.randint(1, 53)) + " "
    lotto_numbers = lotto_numbers + str(random.randint(1, 11))
    return lotto_numbers


class TestGenLotto(unittest.TestCase):
    def test_gen_lotto_num(self):

        # https://www.calottery.com/draw-games/superlotto-plus#section-content-2-3
        if gen_lotto:
            print_heading("gen_lotto")

            print_verbose(
                "Lotto America: 5 lucky numbers between 1 and 52 and 1 Star number between 1 and 10:")
            lotto_numbers = gen_lotto_num()
            # Based on https://www.lottoamerica.com/numbers/montana
            print_info(lotto_numbers)  # such as "17 45 40 34 15 4" (6 numbers)



# SECTION 23. Generate Lotto using random range    = gen_magic_8ball


def gen_magic_8ball_str() -> str:
    """This shows use of case statements to return a random number.
    """
    # Adapted from https://www.pythonforbeginners.com/code/magic-8-ball-written-in-python
    # import sys
    # import random
    while True:  # loop until Enter is pressed to quit.
        # PROTIP: Ensure Python is at least a specific version:
        if sys.version_info[1] < 10:
           #raise Exception("Python 3.10+ is needed for case code.")
           print_todo("Python 3.10+ needed for this code!")
           return None
        answer = random.randint(1, 8)  # Random number between 1 and 8
        match answer:  # Making use of Python 3.10+ to use this:
            case 1:
                answer_text=localize_blob("1. It is certain!")
            case 2:
                answer_text=localize_blob("2. Outlook good!")
            case 3:
                answer_text=localize_blob("3. You may rely on it!")
            case 4:
                answer_text=localize_blob("4. Ask again later!")
            case 5:
                answer_text=localize_blob("5. Concentrate and ask again!")
            case 6:
                answer_text=localize_blob("6. Reply hazy. try again!")
            case 7:
                answer_text=localize_blob("7. My reply is no!")
            case 8:
                answer_text=localize_blob("8. My sources say no!")
            case _:
                print_fail("gen_magic_8ball_str programming error!")
                return None
        print_verbose("gen_magic_8ball_str()=\""+answer_text+"\"")
        return answer_text
    

class TestGen8Ball(unittest.TestCase):
    def test_gen_magic_8ball(self):

        if gen_magic_8ball:
            print_heading("gen_magic_8ball")
            gen_magic_8ball_str()



# SECTION 24. Generate Fibonacci to compare recursion vs memoization locally and in Redis:

# alternative:
# https://github.com/samgh/DynamicProgrammingEbook/blob/master/python/Fibonacci.py

class Fibonacci(object):

    def fibonacci_recursive(n):
        """Calculate value of n-th Fibonacci sequence using brute-force across all - for O(n) time complexity
           This recursive approach is also called a "naive" implementation.
        """
        # if (n == 0) return 0;
        # if (n == 1) return 1;
        # if n in {0, 1, 2}:  # first 3 return values (0, 1, 2) are the same as
        # the request value.
        if n <= 3:
            return n
        # recursive means function calls itself.
        return Fibonacci.fibonacci_recursive(
            n - 1) + Fibonacci.fibonacci_recursive(n - 2)

    # Starting point in local cache:
    fibonacci_memoized_cache = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 5,
        5: 8,
        6: 13,
        7: 21,
        8: 34,
        9: 55,
        10: 89,
        11: 144,
        12: 233,
        13: 377,
        14: 610}
# 15: 987, 16: 1597, 17: 2584}

    def fibonacci_iterative(n):
        """Calculate value of n-th Fibonacci sequence using iterative approach for O(1) time complexity.
           This is considered a "bottom-up" dynamic programming.
           The memoized cache is generated.
        """
        if n in {
                0,
                1,
                2,
                3}:   # the first result values (0, 1, 2, 3) are the same as the request value.
            return n
        # Initialize cache:
        cache = list(range(n+1))
        cache[0:4] = [0, 1, 2, 3]
        for i in range(4, n+1):
            cache[i] = cache[i-1] + cache[i-2]
        # TODO: Make use of hard-coded Fibonacci.fibonacci_memoized_cache
        Fibonacci.fibonacci_memoized_cache = {i: cache[i] for i in cache}
        return cache[n]

    def fibonacci_redis_connect():
            import redis
            azure_redis_hostname = get_str_from_env_file(
                'AZURE_REDIS_HOSTNAME_FOR_FIBONACCI')

            azure_redis_port = get_str_from_env_file('AZURE_REDIS_PORT_FOR_FIBONACCI')
            azure_redis_password = get_str_from_env_file('AZURE_REDIS_ACCESS_KEY')
            reddis_connect_dict = {
                'host': azure_redis_hostname,
                'port': azure_redis_port,
                'password': azure_redis_password,
                'ssl': False}
            try:
                # Retrieve fibonacci_memoized_cache from Redis:
                # PROTIP: ** means to unpack dictionary.
                redis_fibonacci_connect = redis.StrictRedis(**reddis_connect_dict)

                # WARNING: Be off VPN for this to work:
                result = redis_fibonacci_connect.ping()
                print_trace(f'Redis Host \"{azure_redis_hostname}\" established!" ')
                return redis_fibonacci_connect
            except Exception as e:
                print_fail(e)
                print_fail("fibonacci_redis_rw failed with "+e)
                use_azure_redis = False
                return False

    # https://azure.microsoft.com/en-us/blog/view-your-azure-cache-for-redis-data-in-new-visual-studio-code-extension/
    # View your Azure Cache for Redis data in new Visual Studio Code extension

    def fibonacci_redis_rw(n):
        # see https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-python-get-started
        # BEFORE ON TERMINAL: pip3 install -U redis  # to install package https://github.com/redis/redis-py
        # Check for availability of single n in the local fibonacci_memoized_cache:
        if n in Fibonacci.fibonacci_memoized_cache.keys():
            result_number = Fibonacci.fibonacci_memoized_cache[n]
            print_trae("Local returned : " + str(result_number))
        else:  # If not, lookup from Redis:
            redis_fibonacci_connect = Fibonacci.fibonacci_redis_connect()
            if redis_fibonacci_connect:
                result = redis_fibonacci_connect.exists(n)  # single key/value.
                if result:  # found in Redis:
                    # Retrieve entire contents of Redis in fibonacci_memoized_cache (for future efficiency)
                    keys = list(redis_fibonacci_connect.scan_iter())
                    values = redis_fibonacci_connect.mget(keys)
                    cache = {k.decode("utf-8"): v.decode("utf-8")
                                      for k, v in zip(keys, values)}
                    # print_trace(f'Redis cache={cache} ')
                    # return cache
                else:  # If not in Redis, create it and add to Redis:
                    result = Fibonacci.fibonacci_recursive(n)
                    if result:  # Add to Redis:
                        true_false = redis_fibonacci_connect.set(n, result)
                        print_trace(f'redis_fibonacci_connect.set returns {true_false} ')
                    else:
                        return None
                return result

    def fibonacci_redis_delete():
        """ Delete Redis cache, one key at a time : """
        redis_fibonacci_connect = Fibonacci.fibonacci_redis_connect()
        if redis_fibonacci_connect:
            for key in redis_fibonacci_connect.scan_iter():
                Fibonacci.redis_fibonacci_connect.delete(key)
            print_trace("deleted : ")

    def fibonacci_memoized(n):
        """Calculate value of n-th Fibonacci sequence using recursive approach for O(1) time complexity.
           This is considered a "bottom-up" dynamic programming.
        """

        if n in Fibonacci.fibonacci_memoized_cache:  # Base case
            return Fibonacci.fibonacci_memoized_cache[n]

        Fibonacci.fibonacci_memoized_cache[n] = Fibonacci.fibonacci_memoized(
            n - 1) + Fibonacci.fibonacci_memoized(n - 2)

        new_num = Fibonacci.fibonacci_memoized(
            n - 1) + Fibonacci.fibonacci_memoized(n - 2)

        # FIXME: Add entry to Fibonacci.fibonacci_memoized_cache
            # see https://careerkarma.com/blog/python-add-to-dictionary/
        Fibonacci.fibonacci_memoized_cache[n] = new_num
        print_trace(Fibonacci.fibonacci_memoized_cache)

        return Fibonacci.fibonacci_memoized_cache[n]  # return whole cache?


class TestFibonacci(unittest.TestCase):
    def test_gen_fibonacci(self):

        if gen_fibonacci:
            """ Fibonacci numbers are recursive in design to generate sequence.
                But storing calculated values can reduce the time complexity to O(1).
            """
            print_heading("gen_fibonacci")

            # result = Fibonacci.fibonacci_redis_delete()
            # print_trace(f'*** {result} from delete() ')

            # https://realpython.com/fibonacci-sequence-python/
            # hard-coded value (to go with hard-coded array above)
            n = 17  # For 14, n=610

            func_start_timer = timer()
            result = Fibonacci.fibonacci_recursive(n)
            func_end_timer = timer()
            recursive_time_duration = func_end_timer - func_start_timer
            print_info(
                f'fibonacci_recursive: {n} => {result} in {timedelta(seconds=recursive_time_duration)} seconds ')

            # For my next trick, replace local array with array from Redis:
            if use_azure_redis:
                if use_azure:  # is logged in
                    redis_fibonacci = Fibonacci.fibonacci_redis_rw(n)
                    if redis_fibonacci:
                        fibonacci_memoized_cache = redis_fibonacci
                    print_trace(Fibonacci.fibonacci_memoized_cache)

            # Having the array in Redis/Kafka cache service enables several instances of
            # this program to run at the same time.

            func_start_timer = timer()
            result = Fibonacci.fibonacci_memoized(n)
            if False:  # result:
                # Add new item to array in Redis cache:
                Fibonacci.fibonacci_redis_write(n, result)
            func_end_timer = timer()
            memoized_time_duration = func_end_timer - func_start_timer
            diff_order = (recursive_time_duration / memoized_time_duration)
            if show_info:
                print_trace(
                    f'fibonacci_memoized: {n} => {result} in {timedelta(seconds=memoized_time_duration)} seconds ({"%.2f" % diff_order}X faster).')



# SECTION 25. Make change using Dynamic Programming     = make_change

# See https://wilsonmar.github.io/python-samples#make_change
# alternative:
# https://github.com/samgh/DynamicProgrammingEbook/blob/master/python/MakingChange.py

MAX_INT = 10  # the maximum number of individual bills/coins returned.

def make_change_plainly(k, C):
    # k is the amount you want back in bills/change
    # C is an array of each denomination value of the currency, such as [100,50,20,10,5,1]
    # (assuming there is an unlimited amount of each bill/coin available)
    n = len(C)  # the number of items in array C
    print_verbose(f'make_change_plainly: C="{C}" n={n} ')

    turn = 0  # steps in making change
    print_trace(f'turn={turn} k={k} to start ')
    compares = 0
    # list of individual bills/coins returned the number of different
    # denominations.
    change_returned = []
    # Mutable (can grow) with each turn to return a denomination
    while k > 0:  # Keep making change until no more
        for denom in C:  # Look thru the denominations where i=100, 50, etc....
            compares += 1
            # without float(), it won't calculate correctly.
            if float(k) >= denom:
                k = k - denom
                turn += 1  # increment
                print_verbose(f'turn={turn} k={k} after denom={denom} change ')
                # Add change made to output array [20, 10, 1, 1, 1, 1]
                change_returned.append(denom)
                break  # start a new scan of denominations
    print_trace(f'After {turn} turns, k={k} remaining ...')
    # print_verbose(f'{change_returned} ')
    return change_returned


"""
MAX_INT=10  # the maximum number of individual bills/coins returned.

def make_change_dynamically(k,C):
   dp = [0] + [MAX_INT] * k  # array to hold output change made?
    print_trace(f'dp={dp} ')

    # xrange (lazy) is no longer available?
    print_trace(f'{list(range(1, n + 1))} ')
    for i in list(range(1, n + 1)):
       for j in list(range(C[i - 1], k + 1)):
           dp[j] = min(dp[j - C[i - 1]] + 1, dp[j])
    return dp
"""


class TestMakeChange(unittest.TestCase):
    def test_make_change(self):

        if make_change:
            print_heading("make_change")

            # TODO: Add timings
            change_for = 34
            denominations = [100, 50, 20, 10, 5, 1]
            change_back = make_change_plainly(change_for, denominations)
            # print_info(f'change_for {change_for} in denominations {denominations} ')
            print_info(f'make_change: change_back=\"{change_back}\" ')
            self.assertEqual(change_back, [20, 10, 1, 1, 1, 1])


# SECTION 26. Fill knapsack  = fill_knapsack

class TestFillKnapsack(unittest.TestCase):
    def test_fill_knapsack(self):

        if fill_knapsack:
            print_heading("fill_knapsack")
            print_trace(f'fill_knapsack: ')

            def setUp(self):
                self.testcases = [
                    ([], 0, 0), ([
                        Item(
                            4, 5), Item(
                            1, 8), Item(
                            2, 4), Item(
                            3, 0), Item(
                            2, 5), Item(
                                2, 3)], 3, 13), ([
                                    Item(
                                        4, 5), Item(
                                            1, 8), Item(
                                                2, 4), Item(
                                                    3, 0), Item(
                                                        2, 5), Item(
                                                            2, 3)], 8, 20)]


# class TestShowIpAddr(unittest.TestCase):

def ipaddr_get():
    # IP Address is used for geolocation (zip & lat/long) for weather info.
    # List of geolocation APIs: https://www.formget.com/ip-to-zip-code/
    # Fastest is https://ipfind.com/ offering Developers - Free, 100 requests/day

    # First, let's see if there is an override from .env:
    my_ip_address = get_str_from_env_file('MY_IP_ADDRESS')
    if my_ip_address and len(my_ip_address) > 0:
        print_info("IP Address from .env file: " + my_ip_address)

    if not my_ip_address:
        # NOTE: This is like curl ipinfo.io (which provides additional info associated with ip address)
        from requests.auth import HTTPDigestAuth
        # print_warning("IP Address is blank in .env file.")
        # Lookup the ip address on the internet:
        url = "http://checkip.dyndns.org"
            # Alternative: https://ip-fast.com/api/ip/ is fast and not wrapped in HTML.
            # Alternative: https://api.ipify.org/?format=json

        # PROTIP: Close connection immediately to reduce man-in-the-middle attacks:
        # s = requests.session()
        # s.config['keep_alive'] = False
        # TODO: Add 3 retries to url
        request = requests.get(url, allow_redirects=False,
                               headers={'Connection': 'close'})
        # print_trace("request.text="+request.text)
        # <html><head><title>Current IP Check</title></head><body>Current IP Address: 98.97.94.96</body></html>
        clean = request.text.split(': ', 1)[1]  # split 1once, index [1]
        # [0] for first item.
        my_ip_address = clean.split('</body></html>', 1)[0]
        print_info("My external IP Address: " + my_ip_address + " from " + url)

    if not my_ip_address:
        import socket  # https://docs.python.org/3/library/socket.html
        print_verbose("IP address from socket.gethostname: " +
                    socket.gethostbyname(socket.gethostname()))  # 192.168.0.118
            # 127.0.0.1
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # FIXME: Close socket
        # s.close(fd)
        my_ip_address=s.getsockname()[0]
        print_verbose("IP address from getsockname (default route): "+my_ip_address)

    """
    # https://www.delftstack.com/howto/python/get-ip-address-python/
    from netifaces import interfaces, ifaddresses, AF_INET
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(
            ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        print_trace(' '.join(addresses))
    sys.exit()  # DEBUGGING
    """
    # either way:
    return my_ip_address


# Lookup geolocation info from IP Address
def geodata_from_ipaddr(my_ip_address):
    print_trace("geodata_from_ipaddr from ip: " + my_ip_address)
    if not my_ip_address:
       print_error("ip address not provided in call to geodata_from_ipaddr!")
       return None
    
    ip_base = find_ip_geodata(my_ip_address)
    if not ip_base:
        print_fail("ip_base not found: " + str(ip_base))
        return None
    else:
        print_trace("ip_base found: " + str(ip_base))
        # Replace global defaults:
        # FIXME: TypeError: 'NoneType' object is not subscriptable
        if ip_base["country_code"]:
            my_country = ip_base["country_code"]
        if ip_base["longitude"]:
            my_longitude = ip_base["longitude"]
        if ip_base["latitude"]:
            my_latitude = ip_base["latitude"]
        if ip_base["timezone"]:
            my_timezone = ip_base["timezone"]
        if ip_base["currency"]:
            my_currency = ip_base["currency"]

        # TODO: my_country = ip_base["country_code"]


def find_ip_geodata(my_ip_address):

    ipfind_api_key = get_str_from_env_file('IPFIND_API_KEY')
    # Sample IPFIND_API_KEY="12345678-abcd-4460-a7d7-b5f6983a33c7"
    if ipfind_api_key and len(my_ip_address) > 0:
        print_verbose("Using IPFIND_API_KEY in .env file.")
    else:
        # remove key from memory others might peak at.
        # remove key from memory so others can't peak at it.
        del os.environ["IPFIND_API_KEY"]
        print_verbose(f'Please remove secret \"IPFIND_API_KEY\" from .env file.')

    print_todo("Verify ipfind_api_key in find_ip_geodata")

    # Alternative: https://httpbin.org/ip returns JSON { "origin": "98.97.111.222" }
    url = 'https://ipfind.co/?auth=' + ipfind_api_key + '&ip=' + my_ip_address
    try:
        # import urllib, json # at top of this file.
        # https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b310-urllib-urlopen
        response = urllib.request.urlopen(url)
        # See https://docs.python.org/3/howto/urllib2.html
        try:
            ip_base = json.loads(response.read())
            # example='{"my_ip_address":"98.97.111.222","country":"United States","country_code":"US","continent":"North America","continent_code":"NA","city":null,"county":null,"region":null,"region_code":null,"postal_code":null,"timezone":"America\/Chicago","owner":null,"longitude":-97.822,"latitude":37.751,"currency":"USD","languages":["en-US","es-US","haw","fr"]}'
            # As of Python version 3.7, dictionaries are ordered. In Python 3.6
            # and earlier, dictionaries are unordered.
            # print_info(f'***{bcolors.TRACE} country=\"{ip_base["timezone"]}\".')
            # "timezone":"America\/Chicago",
            # "longitude":-97.822,"latitude":37.751,
            # CAUTION: The client's true IP Address may be masked if a VPN is being used!
            # "currency":"USD",
            # "languages":["en-US","es-US","haw","fr"]}
            print_info(
                f'{localize_blob("Longitude")}: {ip_base["longitude"]} {localize_blob("Latitude")}: {ip_base["latitude"]} in {ip_base["country_code"]} {ip_base["timezone"]} {ip_base["currency"]} (VPN IP).')
            return ip_base
        except Exception:
            print_fail(f'ipfind.co {localize_blob("response not read")}.')
            return None
    except Exception:
        print_fail(f'{url} {localize_blob("not operational")}')
        return None



# SECTION 28. Obtain Zip Code to retrieve Weather info, etc

def obtain_zip_code():

    # use to lookup country, US state, long/lat, etc.
    my_zip_code_from_env = get_str_from_env_file('MY_ZIP_CODE')
    if my_zip_code_from_env:
        # Empty strings are "falsy" - considered false in a Boolean context:
        # text_msg="US Zip Code: "+ str(my_zip_code_from_env) +" obtained from file "+ str(global_env_path)
        # print_verbose(text_msg)
        return my_zip_code_from_env
    else:   # zip code NOT supplied from .env:
        ZIP_CODE_DEFAULT = "90210"  # Beverly Hills, CA, for demo usage.
        zip_code = ZIP_CODE_DEFAULT
        print_warning("MY_ZIP_CODE not specified in .env file.")
        print_warning("Default US Zip Code="+ZIP_CODE_DEFAULT)
        return zip_code

        if verify_manually:
            while True:  # keep asking in loop:
                question = localize_blob("A.Enter 5-digit Zip Code: ")
                zip_code_input = input(question)
                if not zip_code_input:  # If empty input, use default:
                    zip_code = ZIP_CODE_DEFAULT
                    return zip_code
                zip_code = zip_code_input
                # zip_code_char_count = sum(c.isdigit() for c in zip_code)
                zip_code_char_count = len(zip_code)
                # Check if zip_code is 5 digits:
                if (zip_code_char_count != 5):
                    print_warning(f'Zip Code \"{zip_code}\" should only be 5 characters.')
                    # ask for zip_code
                    if not verify_manually:
                        zip_code = ZIP_CODE_DEFAULT
                        return zip_code
                    else:  # ask manually:
                        question = localize_blob("B.Enter 5-digit Zip Code: ")
                        zip_code_input = input(question)
                        if not zip_code_input:  # If empty input, use default:
                            zip_code = ZIP_CODE_DEFAULT
                            return zip_code
                        zip_code = zip_code_input
                else:
                    return zip_code
# Test cases:
# .env "59041" processed
# .env has "590" (too small) recognizing less then 5 digits.
# .env has no zip (question), answer "90222"
# .env has no zip (question), answer "902"


class TestLookupZipinfo(unittest.TestCase):
    def test_geodata_from_zipinfo(self):

        if geodata_from_zipinfo:
            print_heading("geodata_from_zipinfo")

            zip_code = obtain_zip_code()
            zippopotam_url = "https://api.zippopotam.us/us/" + zip_code
            # TODO: Do ICMP ping on api.zippopotam.us
            print_trace(f'geodata_from_zipinfo: zippopotam_url={zippopotam_url}')
            try:
                response = requests.get(zippopotam_url, allow_redirects=False)
                x = response.json()
                print_trace(x)  # sample response:
                # {"post code": "59041", "country": "United States", "country abbreviation": "US", \
                # "places": [{"place name": "Joliet", "longitude": "-108.9922", "state": "Montana", "state abbreviation": "MT", "latitude": "45.4941"}]}
                y = x["places"]
                print_info(
                    f'geodata_from_zipinfo: {zip_code} = {y[0]["place name"]}, {y[0]["state abbreviation"]} ({y[0]["state"]}), {x["country abbreviation"]} ({x["country"]})')
                print_info(
                    f'{localize_blob("Longitude:")} {y[0]["longitude"]} {localize_blob("Latitude:")} {y[0]["latitude"]}')
                    # TODO: loop through zip_codes
            except BaseException as e:  # FIXME: Test with bad DNS name
                print_fail(f'zippopotam.us BaseException: \"{e}\".')
                exit(1)
            except ConnectionError as e:
                print_fail(f'zippopotam.us connection error \"{e}\".')
                exit(1)
            except Exception as e:  # Check on error on zip_code lookup:
                print_fail(f'zippopotam.us Exception: \"{e}\".')
                exit(1)



# SECTION 29. Retrieve Weather info using API

# TODO: degrees_from_compass_text(compass_text)

def compass_text_from_degrees(degrees):
    # adapted from https://www.campbellsci.com/blog/convert-wind-directions
    compass_sector = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
        "N"]  # 17 index values
    # graphic ![python-cardinal-point-compass-windrose-600x600-Brosen svg](https://user-images.githubusercontent.com/300046/142781379-addfa8f7-9394-4751-9ddd-65e681e4a49c.png)
    # graphic from https://www.wikiwand.com/en/Cardinal_direction
    remainder = degrees % 360  # modulo remainder of 270/360 = 196
    index = int(round(remainder / 22.5, 0) + 1)   # (17 values)
    return compass_sector[index]

def get_weather_info(zip_code_in):
    print_heading("show_weather for US zip code "+zip_code_in)

    # Commentary on this at
    # https://wilsonmar.github.io/python-samples#show_weather
    # Adapted from https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
    # From https://home.openweathermap.org/users/sign_up
    # then https://home.openweathermap.org/users/sign_in

    # Retrieve from .env file (when vault doesn't work):
    # CAUTION: subprocess.Popen used to block command from sending sensitive variable value to Terminal:
    def hide_output(command):
        result = run(command, stdout=PIPE, stderr=PIPE,
                     universal_newlines=True, shell=True)
        return result.stdout
    # openweathermap_api_key = hide_output(["get_str_from_env_file", "OPENWEATHERMAP_API_KEY"])
    
    openweathermap_api_key = get_str_from_env_file('OPENWEATHERMAP_API_KEY')
    if not openweathermap_api_key:
       print_warning("OPENWEATHERMAP_API_KEY has no default! Processing skilled")
       return
    # else:

    # After retrieval, remove OPENWEATHERMAP_API_KEY value from memory:
    del os.environ["OPENWEATHERMAP_API_KEY"]
    print_todo("Please store \"OPENWEATHERMAP_API_KEY\" in a remote Vault instead of .env file.")
    
    # See https://openweathermap.org/current for
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # TODO: Ping host to verify reachability

    # api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
    # weather_url = base_url + "appid=" + api_key + "&q=" + city_name
    weather_url = base_url + "?appid=" + openweathermap_api_key + "&zip=" + zip_code_in
    print_verbose(f'weather_url={weather_url}.')

    # TODO: Verify openweathermap_api_key

    # TODO: Format request encoding to remove spaces, etc.

    # return response object from get method of requests module:
    try:
        response = requests.get(weather_url, allow_redirects=False)
    except ConnectionError:
        print_fail(f'Connection error \"{response}\".')

    # convert json format data into json method of response object:
    # python format data
    x = response.json()
    print_trace(f'x = {response.json()}')
        # On-line JSON formatter: https://jsonformatter.curiousconcept.com/

    # x contains list of nested dictionaries.
    # x item "cod" contains the HTTP response code - "404":
    # x item "main" ???
    if x["cod"] == "404":
        print_fail(f'{x["cod"]} - U.S. Zip Code \"{my_zip_code}\" Not Found!')
        return  # break out of function.

    # store the value of "main" key in variable y:
    print_todo("FIXME: zipcode KeyError: 'main'")
    y = x["main"]
    coord = x["coord"]
    system = x["sys"]
    text_weather_location = system["country"] + " " + my_zip_code + ": " + x["name"] + " " + localize_blob(
        "Longitude") + ": " + str(coord["lon"]) + " " + localize_blob("Latitude") + ": " + str(coord["lat"])
    # no  +","+ my_us_state
    print_info("text_weather_location="+text_weather_location)
# f'*** {localize_blob("Longitude")}: {coord["lon"]}
# {localize_blob("Latitude")}: {coord["lat"]} {localize_blob("in")}
# {system["country"]} {x["name"]} {my_zip_code} ')

    # store the value of "weather" key in variable z:
    z = x["weather"]
    # store the value corresponding to the "description" key at

    # store the value corresponding to the "temp" key of y:
    current_temp_kelvin = y["temp"]
    # Text to float conversion: celsius = (temp - 32) * 5/9
    current_temp_fahrenheit = (
        float(current_temp_kelvin) * 1.8) - float(459.67)
    current_temp_celsius = (float(current_temp_kelvin)) - float(273.15)

    sunrise = time.strftime(
        my_date_format, time.localtime(
            system["sunrise"]))
    sunset = time.strftime(
        my_date_format, time.localtime(
            system["sunset"]))
    min_fahrenheit = (float(y["temp_min"]) * 1.8) - float(459.67)
    max_fahrenheit = (float(y["temp_max"]) * 1.8) - float(459.67)
    min_celsius = (float(y["temp_min"])) - float(273.15)
    max_celsius = (float(y["temp_max"])) - float(273.15)

    text_weather_min = localize_blob("Minimum temperature") + ": " + "{:.2f}".format(
        min_celsius) + "°C (" + "{:.2f}".format(min_fahrenheit) + "°F) " + localize_blob("Sunrise") + ": " + sunrise
    # print_info(f'{localize_blob("Minimum temperature")}: {"{:.2f}".format(min_celsius)}°C ({"{:.2f}".format(min_fahrenheit)}°F), {localize_blob("Sunrise")}: {sunrise} ')
    print_info(text_weather_min)

    text_weather_cur = localize_blob("Currently") + ": " + "{:.2f}".format(current_temp_celsius) + "°C (" + "{:.2f}".format(current_temp_fahrenheit) + "°F) " \
        + str(y["humidity"]) + "% " + localize_blob("humidity") + ", " + localize_blob(z[0]["description"]) + ", " + \
        localize_blob("visibility") + ": " + str(x["visibility"]) + " feet"
    # f'***{bcolors.INFO} {localize_blob("Currently")}:
    # {"{:.2f}".format(current_temp_celsius)}°C
    # ({"{:.2f}".format(current_temp_fahrenheit)}°F), {y["humidity"]}%
    # {localize_blob("humidity")},
    # {localize_blob(z[0]["description"])},
    # {localize_blob("visibility")}: {x["visibility"]}
    # feet???')
    print_info(text_weather_cur)
    # f'***{bcolors.INFO} {localize_blob("Currently")}:
    # {"{:.2f}".format(current_temp_celsius)}°C
    # ({"{:.2f}".format(current_temp_fahrenheit)}°F), {y["humidity"]}%
    # {localize_blob("humidity")},
    # {localize_blob(z[0]["description"])},
    # {localize_blob("visibility")}: {x["visibility"]}
    # feet???')

    text_weather_max = localize_blob("Maximum temperature") + ": " + "{:.2f}".format(
        max_celsius) + "°C (" + "{:.2f}".format(max_fahrenheit) + "°F) " + localize_blob("Sunset") + ": " + sunset
    # print_info(f'{localize_blob("Maximum temperature")}: {"{:.2f}".format(max_celsius)}°C ({"{:.2f}".format(max_fahrenheit)}°F),  {localize_blob("Sunset")}: {sunset} ')
    print_info(text_weather_max)

    wind = x["wind"]
    if "gust" not in wind.keys():
        # if wind["gust"] == None :
        gust = ""
    else:
        gust = localize_blob("Gusts") + ": " + \
            str(wind["gust"]) + " mph"
    text_wind = localize_blob("Wind Speed") + ": " + str(wind["speed"]) + " " + gust + " " + localize_blob(
        "from direction") + ": " + compass_text_from_degrees(wind["deg"]) + "(" + str(wind["deg"]) + "/360)"
    print_info(text_wind)
    # print_info(f'{localize_blob("Wind Speed")}: {wind["speed"]} {gust} {localize_blob("from direction")}: {compass_text_from_degrees(wind["deg"])} ({wind["deg"]}/360)')
    # FIXME: y["grnd_level"]
    grnd_level = ""
    text_pressure = localize_blob("Atmospheric pressure") + ": " + grnd_level + ":" + str(
        y["pressure"]) + " hPa (hectopascals) or millibars (mb) " + localize_blob("at ground level")
    print_info("text_pressure="+text_pressure)
    #    f'*** {localize_blob("Atmospheric pressure")}: {grnd_level} ({y["pressure"]}) hPa (hectopascals) or millibars (mb) {localize_blob("at ground level")}')
    # at Sea level: {y["sea_level"]} Ground: {y["grnd_level"]} '),
    # From a low of 1011 hPa in December and January, to a high of about 1016 in mid-summer,
    # 1013.25 hPa or millibars (mb) is the average pressure at mean sea-level (MSL) globally.
    # (101.325 kPa; 29.921 inHg; 760.00 mmHg).
    # In the International Standard Atmosphere (ISA) that is 1 atmosphere (atm).
    # In the continental US, San Diego CA has the smallest range (994.58 to 1033.86) hPa (29.37 to 30.53 inHg).
    # The boiling point of water is higher than 100 °C (212 °F) at
    # higher pressure (on mountains).

    # TODO: Save readings for historical comparisons.

    # TODO: Look up previous temp and pressure to compare whether they are rising or falling.
        # Air pressure rises and falls about 3 hP in daily cycles, regardless of weather.
        # A drop of 7 hP or more in 24 hours may indicate a tendency: high-pressure system is moving out and/or a low-pressure system is moving in.
        # Lows have a pressure of around 1,000 hPa/millibars.
        # Generally, high pressure means fair weather, and low pressure
        # means rain.

    if use_keyring:
        print_heading("use_keyring")

        # TODO: Replace these hard-coded with real values:
        key_namespace = "my-app"
        key_entry = "OPENWEATHERMAP_API_KEY"  # = cred.username
        key_text = "yackaty yack"
        print_trace(f'username/key_namespace: \"{key_entry}\" in namespace \"{key_namespace}\" ')

        store_in_keyright(key_namespace, key_entry, key_text)
        key_text_back = get_text_from_keyring(key_namespace, key_entry)
        print_trace(key_text_back)

        # TODO: remove_from_keyring(key_namespace_in, key_entry_in)

    if email_weather:
        message = text_weather_location + "\n" + text_weather_min + "\n" + \
            text_weather_cur + "\n" + text_weather_max + \
                "\n" + text_wind + "\n" + text_pressure
        to_gmail_address = get_str_from_env_file("TO_EMAIL_ADDRESS")
        subject_text = "Current weather for " + x["name"]
        # FIXME: smtplib_sendmail_gmail(to_gmail_address,subject_text, message )
        # print_trace("Emailed to ...")



# SECTION 29. Retrieve secrets from local OS Key Vault  = use_keyring

# Commentary on this at https://wilsonmar.github.io/python-samples#use_keyring
def store_in_keyright(key_namespace_in, key_entry_in, key_text_in):
    # This function is controlled by use_keyring.

    import keyring  # based on: pip install keyring
    import keyring.util.platform_ as keyring_platform

    print_trace("Keyring path="+keyring_platform.config_root())
        # /home/username/.config/python_keyring  # Might be different for you

    print_trace("Keyring="+keyring.get_keyring())
        # keyring.backends.SecretService.Keyring (priority: 5)

    keyring.set_password(key_namespace_in, key_entry_in, key_text_in)
    # print_trace("text: "+keyring.get_password(key_namespace_in, key_entry_in))


def get_text_from_keyring(key_namespace_in, key_entry_in):
    # pip install -U keyring
    import keyring
    import keyring.util.platform_ as keyring_platform

    cred = keyring.get_credential(key_namespace_in, key_entry_in)
    # CAUTION: Don't print out {cred.password}
    # print_trace(f"For username/key_namespace {cred.username} in namespace {key_namespace_in} ")
    return cred.password


# TODO: def remove_from_keyring(key_namespace_in, key_entry_in):

def rm_env_line(api_key_in, replace_str_in):
    with open(global_env_path, 'r') as f:
        x = f.read()
        # Obtain line containing value of api_key_in:
        regex_pattern = api_key_in + r'="\w*"'
        matched_line = re.findall(regex_pattern, x)[0]
        print_trace(matched_line)

        # Substitute in an entire file:
        entire_file = re.sub(matched_line, replace_str_in, x)
        print_trace(entire_file)
        # t=input()    # DEBUGGING

    with open(global_env_path, 'w+') as f:
        f.write(entire_file)

    # Read again to confirm:
    with open(global_env_path, 'r') as f:
        print_trace(f.read())



# SECTION 30. Login to Vault using Python hvac library

def vault_login():
    print_trace("In vault_login")



# SECTION 31. ???


# SECTION 32. Login to Azure

def azure_login():
    print_trace("In azure_login")
    # This Python program is invoked by python-samples.sh so that it can, 
    # before running this, in a Terminal type: "az login" which pops up in your default browser 
    # for you to Pick an Azure account. 
    # Return to the Terminal.  TODO: Service account login?

    # https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview
    # https://azuredevopslabs.com/labs/vstsextend/azurekeyvault/
    # Based on https://docs.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python

    # Based on CLI: conda install azure-identity   # found!
    from azure.identity import DefaultAzureCredential
    # Instantiate a DefaultAzureCredential object to access Azure SDK client class,
    # such as a BlobServiceClient object used to access Azure Blob Storage.
    credential = DefaultAzureCredential()
    print_trace("Got creds in azure_login")
    
    AZ_ACCOUNT = get_str_from_env_file('AZ_ACCOUNT')  # from .env file
    if not AZ_ACCOUNT:
        print_fail("No AZ_ACCOUNT in .env!")
        use_azure=False
        exit()

    # Based on CLI: conda install azure-storage-blob
    from azure.storage.blob import BlobServiceClient
    print_trace("Got creds in azure_login for "+AZ_ACCOUNT)
    blob_service_client = BlobServiceClient(
            account_url="https://"+AZ_ACCOUNT+".blob.core.windows.net",
            credential=credential)

    # pip install azure-storage-blob
    from azure.storage.blob import BlobServiceClient

    # The DefaultAzureCredential object automatically detects the authentication mechanism 
    # configured for the app and obtains the necessary tokens to authenticate the app to Azure. 
    # An application making use of more than one SDK client can use the same credential object.


def azure_info():
    # QUESTION Equivalent to: az login --use-device-code
    # Referenced by login_to_azure parameter.
    # See https://www.youtube.com/watch?v=unbzStG3IVY
    # In preview June, 2022.
    # Azure ML CLI v2 support python, R, Java, Julia, C#
    # Python SDK v2 build any workflow (simple to complex incrementally)

    # pip install -r requirements.txt

    AZ_SUBSCRIPTION_ID = get_str_from_env_file('AZ_SUBSCRIPTION_ID')
    # AZ_SUBSCRIPTION_ID exmple: "285a9b29-43df-4ebf-85b1-61bbf7929871"
    if not AZ_SUBSCRIPTION_ID:
        print_error("AZ_SUBSCRIPTION_ID not defined in .env file. No default!")
        return False
    
    # Python equivalent of "az login" CLI command.

def azure_blob_actions():
    print_trace("In azure_blob_actions")

    # "eastus"  # aka LOCATION using the service.
    az_region_from_env = get_str_from_env_file('AZURE_REGION')
    if az_region_from_env:
        azure_region = az_region_from_env
    else:
        azure_region = "eastus"

    AZ_SUBSCRIPTION_ID = get_str_from_env_file('AZ_SUBSCRIPTION_ID')  # from .env file
    if not AZ_SUBSCRIPTION_ID:
        print_fail("No AZ_SUBSCRIPTION_ID.")
        use_azure=False
        # break

    azure_region = get_str_from_env_file('AZURE_REGION')  # from .env file
    if not azure_region:
        print_fail("No AZURE_REGION.")
        exit

    # ON A CLI TERMINAL:
    # pip install -U azure-keyvault-secrets
    # az account list --output table
    # az account set --subscription ...
    # az group create --name KeyVault-PythonQS-rg --location eastus
    # az keyvault create --name howdy-from-azure-eastus --resource-group KeyVault-PythonQS-rg
    # az keyvault set-policy --name howdy-from-azure-eastus --upn {email} --secret-permissions delete get list set
    # Message: Resource group 'devwow' could not be found.

    # Defined at top of this file:
    # import os
    # from azure.keyvault.secrets import SecretClient
    # from azure.identity import DefaultAzureCredential

    azure_keyVaultName = get_str_from_env_file('AZ_KEY_VAULT_NAME')  # from .env file
    if not azure_keyVaultName:
        print_fail("No AZ_KEY_VAULT_NAME.")
        exit

    KVUri = f"https://{azure_keyVaultName}.vault.azure.net"
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        print_trace(
            f'Using Azure secret Key Vault \"{azure_keyVaultName}\" in {azure_region} region.')
    except Exception:
        print_fail(f'Azure Key Vault {azure_keyVaultName} auth failed!')
        # don't exit. Using .env file failure.

    # TODO: Encrypt/hash secret in transit and at rest!
    result = set_azure_secret_from_env("OPENWEATHERMAP_API_KEY")
        # OPENWEATHERMAP_API_KEY="12345678901234567890123456789012"
    if not result:
        exit

    # retrieved_secret = retrieve_azure_secret("OPENWEATHERMAP_API_KEY")
    # print_trace("Secret retrieved: " + str(retrieved_secret) )  # please avoid printing out secret values.
    # TODO: Unencrypt/rehash secretValue?

    x = input("Press Enter to continue")  # DEBUGGING

    # set_azure_secret_from_env("IPFIND_API_KEY")
    # retrieve_azure_secret("IPFIND_API_KEY")
        # IPFIND_API_KEY="12345678-abcd-4460-a7d7-b5f6983a33c7"

    if show_logging:
        print_heading("show_logging")
        show_logging()


def azure_see():
    # See https://www.youtube.com/watch?v=YAg6khewJiU
    # How to use Python SDK for Azure Automation by vrchinnarathod@gmail.com
    # https://www.linkedin.com/in/rekhu-chinnarathod-58b3a860/
    # which uses https://github.com/RekhuGopal/PythonHacks/tree/main/AzureAutomationWithPython
    # https://github.com/RekhuGopal/PythonHacks/blob/main/AzureAutomationWithPython/provision_rg.py

    # Requires: pip install azure.identity # (2021.10.8) Azure Active Directory identity library
    # 1.13.0 https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python
    # https://pypi.org/project/azure-identity/
    # from azure.identity import DefaultAzureCredential

    # See https://azuresdkdocs.blob.core.windows.net/$web/python/azure-storage-blob/12.1.0/index.html
    resource_client = ResourceManagementClient(credential, subscription_id)
    RESOURCE_GROUP_NAME = "PythonAzureExample-Storage-rg"
    LOCATION = "centralus"
    return

"""
    az login --use-device-code
    python provision_rg.py

    # https://github.com/RekhuGopal/PythonHacks/blob/main/AzureAutomationWithPython/requirements.txt
    # contains:
    azure-mgmt-resource
    azure-mgmt-storage
    azure-identity
    """
    # Based on: import os, random
    # from azure.identity import AzureCliCredential
    
    #    from azure.mgmt.resource import ResourceManagementClient
    #    from azure.mgmt.storage import StorageManagementClient

    # from azure.common.credentials import ServicePrincipalCredentials

    # https://pypi.python.org/pypi/azure-keyvault-secrets
    # from azure.keyvault.secrets import SecretClient

    # azure-mgmt-storage
    # https://pypi.python.org/pypi/azure-mgmt-storage
    # azure-mgmt-compute
    # https://pypi.python.org/pypi/azure-mgmt-compute) : Management of Virtual Machines, etc.

    # from azure.mgmt.resource import ResourceManagementClient
    # https://pypi.python.org/pypi/azure-mgmt-resource

    #from azure.storage.blob import BlobServiceClient   #
    # https://pypi.python.org/pypi/azure-storage-blob



# SECTION 33. In Azure, list resources for specific SubscriptionID

def az_cliz(args_str):
    args = args_str.split()
    cli = get_default_cli()
    cli.invoke(args)
    if cli.result.result:
        return cli.result.result
    elif cli.result.error:
        raise cli.result.error
    return True



# SECTION 34. Retrieve secrets from Azure Key Vault

# Commentary on this at https://wilsonmar.github.io/python-samples#use_azure

def set_azure_secret_from_env(secretName):
    # TODO: Get from user prompt?
    # secretName  = input("Input a name for your secret > ")
    # secretValue = input("Input a value for your secret > ")

    secretValue = get_str_from_env_file(secretName)  # from .env file
    if not secretValue:
        print_fail("No " + secretName + " in .env")
        return None
    try:
        client.set_secret(secretName, secretValue)
        print_verbose("Secret " + secretName + " saved.")
        print_info("Please store in a Vault instead of .env file.")
    except Exception:
        # FIXME:
        print_fail(f'client.set.secret of \"{secretName}\" failed.')
        return None

    # python3 wants to use your confidential
    # information stored in "VS Code Azure" in your
    # keychain
    # See https://github.com/microsoft/vscode-azurefunctions/issues/1759


def retrieve_azure_secret(secretName):
    try:
        retrieved_secret = client.get_secret(secretName)
        # Don't print secrets: f'*** Secret \"{secretName}\" = \"{retrieved_secret.value}\".')
        return retrieved_secret
    except Exception:
        print_fail(f'client.get.secret name of \"{secretName}\" failed!')


def delete_azure_secret(secretName):
    try:
        poller = client.begin_delete_secret(secretName)
        deleted_secret = poller.result()
        print_trace(f'Secret \"{secretName}\" deleted.')
    except Exception:
        print_fail(f'delete.secret of \"{secretName}\" failed.')
        exit(1)



# SECTION 35. Retrieve secrets from AWS KMS  = use_aws

# Commentary on this at https://wilsonmar.github.io/python-samples#use_aws
# https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview 
# https://github.com/saginadir/python3-boto3-upload
# https://www.learnaws.org/2021/02/20/aws-kms-boto3-guide/
# https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/secrets-manager.html
# https://docs.aws.amazon.com/kms/latest/developerguide/
# https://docs.aws.amazon.com/code-samples/latest/catalog/python-kms-encrypt_decrypt_file.py.html
# https://cloudacademy.com/course/get-started-with-aws-cloudhsm/what-is-cloudhsm/

# In the Terminal running this program:
# Must first install : pip install boto3 -U
# Use the "cryptopgraphy" package to encrypt and decrypt data.
# Paste definitions of AWS keys to authenticate.

""" Boto3 has two ways to access objects within AWS services (such as kms):
    * boto3.client('kms') provide a low-level interface to all AWS service operations.
    Client whose methods map close to 1:1 with service APIs.
    Clients are generated from a JSON service definition file.

    * boto3.resources('kms') represent an object-oriented interface to AWS to provide
    a higher-level abstraction than the raw, low-level calls made by service clients.
"""


def create_aws_cmk(description="aws_cmk_description"):  # FIXME
    """Creates KMS Customer Master Keys (CMKs).
    AWS KMS supports two types of CMKs, using a Description to differentiate between them:
    1. By default, KMS creates a symmetric CMK 256-bit key. It never leaves AWS KMS unencrypted.
    2. Asymmetric CMKs are where AWS KMS generates a key pair. The private key never leaves AWS KMS unencrypted.
    """

    print_verbose("aws_boto3_version="+str(boto3.__version__))  # example: 1.26.155

    kms_client = boto3.client("kms")
    response = kms_client.create_key(Description=aws_cmk_description)

    # Return the key ID and ARN:
    return response["KeyMetadata"]["KeyId"], response["KeyMetadata"]["Arn"]
    # RESPONSE: ('c98e65ee-95a5-409e-8f25-6f6732578798',
    # 'arn:aws:kms:us-west-2:xxxx:key/c98e65ee-95a5-409e-8f25-6f6732578798')


def retrieve_aws_cmk(aws_cmk_description):
    """Retrieve an existing KMS CMK based on its description"""

    # Retrieve a list of existing CMKs
    # If more than 100 keys exist, retrieve and process them in batches
    kms_client = boto3.client("kms")
    response = kms_client.list_keys()

    for cmk in response["Keys"]:
        key_info = kms_client.describe_key(KeyId=cmk["KeyArn"])
        if key_info["KeyMetadata"]["Description"] == description:
            return cmk["KeyId"], cmk["KeyArn"]

    # No matching CMK found
    return None, None


def create_aws_data_key(cmk_id, key_spec="AES_256"):
    """Generate a data key to use when encrypting and decrypting data,
    so this returns both the encrypted CiphertextBlob as well as Plaintext of the key.
    A data key is a unique symmetric data key used to encrypt data outside of AWS KMS.
    AWS returns both an encrypted and a plaintext version of the data key.
    AWS recommends the following pattern to use the data key to encrypt data outside of AWS KMS:
    - Use the GenerateDataKey operation to get a data key.
    - Use the plaintext data key (in the Plaintext field of the response) to encrypt your data outside of AWS KMS. Then erase the plaintext data key from memory.
    - Store the encrypted data key (in the CiphertextBlob field of the response) with the encrypted data.
    """

    # Create data key:
    kms_client = boto3.client("kms")
    response = kms_client.generate_aws_data_key(KeyId=cmk_id, KeySpec=key_spec)

    # Return the encrypted and plaintext data key
    return response["CiphertextBlob"], base64.b64encode(response["Plaintext"])


def delete_aws_data_key(cmk_id):
    print_trace("delete_aws_data_key(cmk_id)="+delete_aws_data_key(cmk_id))


def decrypt_aws_data_key(data_key_encrypted):
    """Decrypt an encrypted data key"""

    # Decrypt the data key
    kms_client = boto3.client("kms")
    response = kms_client.decrypt(CiphertextBlob=data_key_encrypted)

    # Return plaintext base64-encoded binary data key:
    return base64.b64encode((response["Plaintext"]))


NUM_BYTES_FOR_LEN = 4


def encrypt_aws_file(filename, cmk_id):
    """Encrypt JSON data using an AWS KMS CMK
    Client-side, encrypt data using the generated data key along with the cryptography package in Python.
    Store the encrypted data key along with your encrypted data since that will be used to decrypt the data in the future.
    """

    with open(filename, "rb") as file:
        file_contents = file.read()

    data_key_encrypted, data_key_plaintext = create_aws_data_key(cmk_id)
    if data_key_encrypted is None:
        return None

    # try: Encrypt the data:
    f = Fernet(data_key_plaintext)
    file_contents_encrypted = f.encrypt(file_contents)

    # Write the encrypted data key and encrypted file contents together:
    with open(filename + '.encrypted', 'wb') as file_encrypted:
        file_encrypted.write(
            len(data_key_encrypted).to_bytes(
                NUM_BYTES_FOR_LEN,
                byteorder='big'))
        file_encrypted.write(data_key_encrypted)
        file_encrypted.write(file_contents_encrypted)


def decrypt_aws_file(filename):
    """Decrypt a file encrypted by encrypt_aws_file()"""

    # Read the encrypted file into memory
    with open(filename + ".encrypted", "rb") as file:
        file_contents = file.read()

    # The first NUM_BYTES_FOR_LEN tells us the length of the encrypted data key
    # Bytes after that represent the encrypted file data
    data_key_encrypted_len = int.from_bytes(file_contents[:NUM_BYTES_FOR_LEN],
                                            byteorder="big") \
        + NUM_BYTES_FOR_LEN
    data_key_encrypted = file_contents[NUM_BYTES_FOR_LEN:data_key_encrypted_len]

    # Decrypt the data key before using it
    data_key_plaintext = decrypt_aws_data_key(data_key_encrypted)
    if data_key_plaintext is None:
        return False

    # Decrypt the rest of the file:
    f = Fernet(data_key_plaintext)
    file_contents_decrypted = f.decrypt(file_contents[data_key_encrypted_len:])

    # Write the decrypted file contents
    with open(filename + '.decrypted', 'wb') as file_decrypted:
        file_decrypted.write(file_contents_decrypted)


# The AWS Toolkit uses the AWS Serverless Application Model (AWS SAM) to
# create and manage AWS resources such as AWS Lambda Functions.
# It provides shorthand syntax to express functions, APIs, databases, and more in a declarative way.
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html
# https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

def login_aws():
    # See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
    AWS_ACCESS_KEY_ID = get_secret_from_env_file('AWS_ACCESS_KEY_ID')
    if not AWS_ACCESS_KEY_ID:
        print_fail("AWS_ACCESS_KEY_ID not in .env")
        return None

    AWS_SECRET_ACCESS_KEY = get_secret_from_env_file('AWS_SECRET_ACCESS_KEY')
    if not AWS_SECRET_ACCESS_KEY:
        print_fail("AWS_SECRET_ACCESS_KEY not in .env")
        return None

    # import boto3
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    print_verbose("login_aws(): "+str(session))
    return session

def use_aws():
    print_heading("In use_aws")
    login_aws()

def get_aws_s3():
    aws_region_from_env = get_str_from_env_file('AWS_REGION')   # "us-east-1"
    # PROTIP: Count number of characters in string:
    if len(s.encode('utf-8')) > 0: 
        aws_region = aws_region_from_env
    else:
        # "Friends don't let friends use AWS us-east-1 in production"
        aws_region = "us-east-1"
        print_warning("aws_region="+aws_region+" from default!")

    s3 = session.resource('s3')

    # Retrieve from .env file:
    aws_cmk_description = get_str_from_env_file('AWS_CMK_DESCRIPTION')
    if not aws_cmk_description:
        print_fail("AWS_CMK_DESCRIPTION not in .env")
        exit(1)
    else:
        print_verbose(f'Creating AWS CMK with Description:\"{aws_cmk_description}\" ')

    # https://hands-on.cloud/working-with-kms-in-python-using-boto3/

    # create_aws_cmk(description=aws_cmk_description)

    # retrieve_aws_cmk(aws_cmk_description)
    # RESPONSE: ('c98e65ee-95a5-409e-8f25-6f6732578798',
    # 'arn:aws:kms:us-west-2:xxx:key/c98e65ee-95a5-409e-8f25-6f6732578798')
    # enable_aws_cmk()
    # disable_aws_cmk()
    # list_aws_cmk()

    # create_aws_data_key(cmk_id, key_spec="AES_256")
    # schedule_key_deletion()
    # option to specify a PendingDeletion period of 7-30 days.
    # cancel_key_deletion()

    # encrypt_aws_data_key(data_key_encrypted)
    # decrypt_aws_data_key(data_key_encrypted)

    # encrypt_aws_file(filename, cmk_id)
    # decrypt_aws_file(filename)
    #    cat test_file.decrypted
    # hello, world
    # this file will be encrypted



# SECTION 36. Login and use GCP   = use_gcp

# Commentary on this is at:
    # https://wilsonmar.github.io/python-samples#use_gcp
    # https://wilsonmar.github.io/gcp

# TODO: Deadline-dependent Timeout = https://googleapis.dev/python/google-api-core/latest/timeout.html

# https://developers.google.com/apis-explorer/

# Adapted from:
    # https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets
    # https://developers.google.com/docs/api/quickstart/python

def gcp_login():
    print_trace("In gcp_login")
    """Get credentials for GCP
    """
    # When running in a local development environment, such as a development workstation, 
    # user credentials associated with your Google (Gmail or Workspace) Account.
    # See https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to
    # In a Terminal app, run my gcpinfo.sh to invoke "gcloud auth application-default login"
    # which on Linux, macOS creates: $HOME/.config/gcloud/application_default_credentials.json
    # which uses the file path exported into environment variable GOOGLE_APPLICATION_CREDENTIALS,
    # such as ""/Users/johndoe/johndoe-svc-2112140232.json" created on 2021-12-14.
    # See https://medium.com/@lyle-okoth/github-oauth-using-python-and-flask-a385876540af

    gcp_creds = get_str_from_env_file('GOOGLE_APPLICATION_CREDENTIALS')
    if not gcp_creds:
        GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/application_default_credentials.json"
        print_warning("Default json contents are in GOOGLE_APPLICATION_CREDENTIALS environment var!")
        # The json file contains a "client_id", "client_secret", "quota_project_id", "refresh_token", type: "authorized_user" which Google ADC (Application Default Credentials) uses.
        # Acquire a Google-signed OpenID Connect (OIDC) ID token to access Cloud Run, Cloud Function, Identity-Aware Proxy API Gateway.
        # The target service is the service or application that the ID token authenticates to.
        # Quota project "ninth-matter-388922" was added to ADC which can be used by Google client libraries for billing and quota.
    # storage_client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)

    GCP_PROJECT_ID = get_str_from_env_file('GCP_PROJECT_ID')
    if not GCP_PROJECT_ID:
        print_warning("GCP_PROJECT_ID="+GCP_PROJECT_ID+" has no default!")

    GCP_PROJECT_NAME = get_str_from_env_file('GCP_PROJECT_NAME')
    if not GCP_PROJECT_NAME:
        print_warning("GCP_PROJECT_NAME="+GCP_PROJECT_NAME+" has no default!")

    GCP_PROJECT_NUM = get_str_from_env_file('GCP_PROJECT_NUM')
    if not GCP_PROJECT_NUM:
        print_warning("GCP_PROJECT_NUM="+GCP_PROJECT_NUM+" has no default!")

    # See https://readthedocs.org/projects/google-auth/downloads/pdf/latest/
    # Based on : pip3 install google.cloud.storage    # in requirements.txt
        #  Downloading google_cloud-0.34.0-py2.py3-none-any.whl (1.8 kB)
    from google.cloud import storage  
        # google.cloud-0.34.0 ImportError: cannot import name 'storage' from 'google.cloud' (unknown location)

    # creds, GCP_PROJECT_ID = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    creds = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    auth_req = google.auth.transport.requests.Request()
    print_trace("auth_req="+str(auth_req))
    creds.refresh(auth_req)    # refresh token
    token_str = (creds.token)    # print token
    print_trace("token_str="+str(token_str))
    print_info(creds.expiry)
    
    # Create credentials from the access token:
    #credentials = google.oauth2.credentials.Credentials(access_token)
    #service = googleapiclient.discovery.build('iam', 'v1', credentials=credentials) 
    return token_str, GCP_PROJECT_ID

def gcp_buckets_list():
    print_trace("In gcp_buckets_list")

    # And https://github.com/googleapis/google-auth-library-python/blob/HEAD/samples/cloud-client/snippets/authenticate_implicit_with_adc.py

    # This snippet demonstrates how to list buckets.
    # *NOTE*: Replace the client created below with the client required for your application.
    # Note that the credentials are not specified when constructing the client.
    # Hence, the client library will look for credentials using ADC.
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")

# Global static variables:
READONLY_SCOPE  = ['https://www.googleapis.com/auth/documents.readonly']
READWRITE_SCOPE = ['https://www.googleapis.com/auth/documents.readwrite']  # ???

def gcp_doc_info():
    gcp_doc_id = get_str_from_env_file('GCP_DOCUMENT_ID')
    if not gcp_doc_id:
        print_warning("gcp_doc_id has no default!")
        return None
    
    gcp_doc_title(READONLY_SCOPE, gcp_doc_id)

def gcp_doc_title(scope_in, document_id_in):
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    From https://github.com/googleworkspace/python-samples/blob/main/docs/quickstart/quickstart.py
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scope_in)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scope_in)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('docs', 'v1', credentials=creds)
        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=document_id_in).execute()
        print_info("The title of the document is: "+format(document.get('title')) )
    except HttpError as err:
        print_error(err)


def create_gcp_secret(gcp_project_id_in, secret_id):
    """
    Create a new secret with the given name. A secret is a logical wrapper
    around a collection of secret versions. Secret versions hold the actual
    secret material.
    """
    from google.cloud import secretmanager

    # Create the Secret Manager client:
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent project:
    parent = f"projects/{gcp_project_id_in}"

    # Build a dict of settings for the secret:
    secret = {'replication': {'automatic': {}}}

    # Create the secret:
    response = client.create_secret(
        secret_id=secret_id,
        parent=parent,
        secret=secret)
    # request={
    #    "parent": parent,
    #    "secret_id": secret_id,
    #    "secret": {"replication": {"automatic": {}}},
    # }

    print_verbose(f'Created GCP secret response.name: {response.name}')
    return response.name


def add_gcp_secret_version(gcp_project_id_in, secret_id, payload):
    """
    Add a new secret version to the given secret with the provided payload.
    """

    # from google.cloud import secretmanager

    # Create the Secret Manager client:
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent secret.
    parent = f"projects/{gcp_project_id_in}/secrets/{secret_id}"

    # Convert the string payload into a bytes. This step can be omitted if you
    # pass in bytes instead of a str for the payload argument.
    payload = payload.encode('UTF-8')

    # Add the secret version.
    response = client.add_secret_version(
        parent=parent, payload={'data': payload})

    print_verbose(f'Added GCP secret version: {response.name}')
    return response.name


def access_gcp_secret_version(
        gcp_project_id_in,
        secret_id,
        version_id="latest"):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Create the Secret Manager client:
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{gcp_project_id_in}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)
  # response = client.access_secret_version(request={"name": name})

    respone_payload = response.payload.data.decode('UTF-8')
    print_verbose(f'Added GCP secret version: {respone_payload}')
    return respone_payload


def hash_gcp_secret(secret_value):
    return hashlib.sha224(bytes(secret_value, "utf-8")).hexdigest()


def list_gcp_secrets(gcp_project_id_in):
    """
    List all secrets in the given project.
    """

    # from google.cloud import secretmanager
    # Create the Secret Manager client:
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent project:
    parent = f"projects/{gcp_project_id_in}"

    for secret in client.list_secrets(request={"parent": parent}):
        print_trace("Found secret: {}".format(secret.name))


# Based on https://cloud.google.com/secret-manager/docs/managing-secrets
# TODO: Getting details about a secret, Managing access to secrets,
# TODO: Updating a secret, Deleting a secret

def grace_use_gcp():
    print_trace("In use_gcp")
    
    # https://cloud.google.com/docs/authentication/external/set-up-adc
    # Adapted from https://codelabs.developers.google.com/codelabs/secret-manager-python#5
    # pip install -U google-cloud-secret-manager
    # from google.cloud import secretmanager  #
    # https://cloud.google.com/secret-manager/docs/reference/libraries
    # CAUTION: On FreeBSD and Mac OS X, putenv() setting environ may cause memory leaks. https://docs.python.org/2/library/os.html#os.environ

    gcp_project_id = get_str_from_env_file('GCP_PROJECT_ID')
    if not gcp_project_id:
        print_error("GCP_PROJECT_ID not defined in .env. No default!")
        return False


    print_todo("Make my_secret_key and value variables")
    my_secret_key = "secret123a"  # format: [[a-zA-Z_0-9]+]
    my_secret_value = "can't tell you"
    result = create_gcp_secret(gcp_project_id, my_secret_key)
        # TODO hide RESPONSE: Created secret: projects/<PROJECT_NUM>/secrets/my_secret_key
    if result:
        # Each payload value of a secret key is a different version:
        result = add_gcp_secret_version(gcp_project_id, my_secret_key, my_secret_value)

    if result:
        # Add secret version:
        result = add_gcp_secret_version(gcp_project_id, my_secret_key, my_secret_key)
        # google.api_core.exceptions.AlreadyExists: 409 Secret [projects/1070308975221/secrets/secret123] already exists.
        # projects/<PROJECT_NUM>/secrets/my_secret_key/versions/2

    if result:
        result = hash_gcp_secret(access_secret_version(my_secret_key))
        # Example: 83f8a4edb555cde4271029354395c9f4b7d79706ffa90c746e021d11

    if result:
        # Since previous call did not specify a version, the latest value is retrieved:
        result = hash_gcp_secret(access_secret_version(my_secret_key, version_id=2))

    if result:
        # You should see the same output as the last command.
        # Call the function again, but this time specifying the first version:
        result = hash_gcp_secret(access_secret_version(my_secret_key, version_id=1))
        # You should see a different hash this time, indicating a different output:

    if show_verbose:
        list_gcp_secrets(gcp_project_id)

    # return ???



# SECTION 37: Log into AWS using Pythong Boto3 library

# See https://wilsonmar.github.io/python-samples#HashicorpVault


def do_use_hvault():
    if use_hvault == 0:
        print_trace("do_use_hvault() skipped: use_hvault="+str(use_hvault))
        return False
    print_trace("in do_use_hvault()")
    
    global VAULT_URL
    VAULT_URL = get_str_from_env_file('VAULT_URL')
    if not VAULT_URL:
        VAULT_URL = 'http://127.0.0.1:8200'  # -vaulturl "http://127.0.0.1:8200"
        print_warning("VAULT_URL="+VAULT_URL+" from default!")

    global VAULT_TOKEN
    VAULT_TOKEN = get_str_from_env_file('VAULT_TOKEN')
    if not VAULT_TOKEN:
        VAULT_TOKEN = 'dev-only-token'
        print_warning("VAULT_TOKEN="+VAULT_TOKEN+" from default!")

    global VAULT_USER
    VAULT_USER = get_str_from_env_file('VAULT_USER')
    if not VAULT_USER:
        VAULT_USER = 'default_user'
        print_warning("VAULT_USER="+VAULT_USER+" from default!")

    global HVAULT_LEASE_DURATION
    HVAULT_LEASE_DURATION = get_str_from_env_file('HVAULT_LEASE_DURATION')
    if not HVAULT_LEASE_DURATION:
        # Global static values (according to Security policies):
        HVAULT_LEASE_DURATION = '1h'
        print_warning("HVAULT_LEASE_DURATION="+HVAULT_LEASE_DURATION+" from default!")

    client = auth_hvault()
    if not client:
        print_error("client "+client)
        return False
    secret = get_hvault_secret()
    if not secret:
        print_error("client "+client)
        return False
    # hvault_secret_path
    # write_hvault_secret(hvault_secret_path):
    return True

def auth_hvault():
    print_trace("in auth_hvault()")

    # Equiv to vault login -method=userpass username=webapp password=webapp-password

    # Leveraging the Vault Agent Template feature
    # From https://developer.hashicorp.com/vault/tutorials/vault-agent/agent-read-secrets
    

    # From https://github.com/jakefurlong/vault/blob/main/read.py
    # import os    # built-in
    # import hvac  # https://github.com/hvac/hvac = Python client
    client = hvac.Client(url=VAULT_URL)
    if not client.is_authenticated():
        print_error(f"{VAULT_URL} NOT authenticated as Hashicorp Vault client!")
        return False
    return client

def get_hvault_secret():
    print_trace("in get_hvault_secret()")
    # Equiv to vault kv get external-apis/socials/twitter
    # {"api_key"=>"MQfS4XAJXYE3SxTna6Yzrw", "api_secret_key"=>"uXZ4VHykCrYKP64wSQ72SRM10WZwirnXq5rmyiLnVk"}

    # import hvac
    # import json
    client = hvac.Client(url=VAULT_URL)
    read_response = client.secrets.kv.v2.read_secret_version(path='hello')
    print(json.dumps(read_response, indent=4, sort_keys=True))
    if not read_response:
        return False
    return True

def retrieve_hvault_secret():
    # Adapted from
    # https://fakrul.wordpress.com/2020/06/06/python-script-credentials-stored-in-hashicorp-vault/
    client = hvac.Client(VAULT_URL)
    read_response = client.secrets.kv.read_secret_version(path='meraki')

    url = 'https://api.meraki.com/api/v0/organizations/{}/inventory'.format(
        ORG_ID)
    MERAKI_API_KEY = 'X-Cisco-Meraki-API-Key'
    ORG_ID = '123456'  # TODO: Replace this hard coding.
    MERAKI_API_VALUE = read_response['data']['data']['MERAKI_API_VALUE']
    response = requests.get(
        url=url,
        headers={
            MERAKI_API_KEY: MERAKI_API_VALUE,
            'Content-type': 'application/json'})

    switch_list = response.json()
    switch_serial = []
    for i in switch_list:
        if i['model'][:2] in ('MS') and i['networkId'] is not None:
            switch_serial.append(i['serial'])

    print_trace("switch_serial="+switch_serial)

def write_hvault_secret(hvault_secret_path):

    client = hvac.Client(
        url=os.environ['VAULT_URL'],
        token=os.environ['VAULT_TOKEN'],
        cert=(client_cert_path, client_key_path),
        verify=server_cert_path
    )

    client.write(
        hvault_secret_path,
        type='pythons',
        lease=HVAULT_LEASE_DURATION)

    if client.is_authenticated():
        print_trace(client.read(hvault_secret_path))
        # {u'lease_id': u'', u'warnings': None, u'wrap_info': None, u'auth': None, u'lease_duration': 3600, u'request_id': u'c383e53e-43da-d491-6c20-b0f5f7e4a33a', u'data': {u'type': u'pythons', u'lease': u'1h'}, u'renewable': False}



# SECTION 39: Write secret to HashiCorp Vault per https://github.com/hashicorp/vault-examples/blob/main/examples/_quick-start/python/example.py



# SECTION 40: Refresh certs crated by HashiCorp Vault

def refresh_vault_certs():
    # if refresh_vault_certs:

    # Authentication
    client = hvac.Client(
        url='http://127.0.0.1:8200',
        token='dev-only-token',
    )
    # Write a secret:
    create_response = client.secrets.kv.v2.create_or_update_secret(
        path='my-secret-password',
        # secret=dict(password='Hashi123'),
    )

    print_trace('Secret written successfully.')

    # Reading a secret
    read_response = client.secrets.kv.read_secret_version(
        path='my-secret-password')

    password = read_response['data']['data']['password']

    if password != 'Hashi123':
        sys.exit('unexpected password')

    print_trace('Access granted!')



# SECTION 41. Create/Reuse folder for img app to put files:

def img_download():
    print_heading("In img_download")
    
    # Sets :
    img_directory = get_str_from_env_file('img_directory')
    if not img_directory:
        img_directory = "Images"
        print_warning("img_directory="+img_directory+" from default!")

    if img_set == "small_ico":
        img_url = "http://google.com/favicon.ico"
        img_file_name = "google.ico"

    elif img_set == "big_mp4":
        # Big 7,376,089' byte mp4 file:
        img_url = 'https://aspb1.cdn.asset.aparat.com/aparat-video/a5e07b7f62ffaad0c104763c23d7393215613675-360p.mp4?wmsAuthSign=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IjUzMGU0Mzc3ZjRlZjVlYWU0OTFkMzdiOTZkODgwNGQ2IiwiZXhwIjoxNjExMzMzMDQxLCJpc3MiOiJTYWJhIElkZWEgR1NJRyJ9.FjMi_dkdLCUkt25dfGqPLcehpaC32dBBUNDC9cLNiu0'
        img_file_name = "play.mp4"

    elif img_set == "zen_txt":   # Used by paragraphs.py:
        img_url = "https://www.pythontutorial.net/wp-content/uploads/2020/10/the-zen-of-python.txt"
        img_file_name = "the-zen-of-python.txt"

    elif img_set == "lorem_5":
        # Website that obtain "Lorem Ipsum" placeholder text commonly used for
        # previewing layouts and visual mockups.
        img_url = "https://baconipsum.com/api/?type=meat-and-filler&sentences=3&start-with-lorem=1&format=text"
        img_file_name = "Lorem_ipson_5.txt"

        # type: all-meat for meat only or meat-and-filler for meat mixed with miscellaneous ‘lorem ipsum’ filler.
        # paras: optional number of paragraphs, defaults to 5. Blank line in between paragraphs
        # sentences: number of sentences (this overrides paragraphs)
        # start-with-lorem: optional pass 1 to start the first paragraph with ‘Bacon ipsum dolor sit amet’.
        # format: ‘json’ (default), ‘text’, or ‘html’

    # TODO: QR Code Generator https://www.qrcode-monkey.com/qr-code-api-with-logo/ for url to mobile authenticator app (Google) for MFA
        # import pyqrcode - https://github.com/mindninjaX/Python-Projects-for-Beginners/blob/master/QR%20code%20generator/QR%20code%20generator.py
    # TODO: Generate photo of people who don't exist.

    else:
        print_fail(f'img_set \"{img_set}\" not recognized in coding!')
        exit(1)

    img_project_root = get_str_from_env_file(
        'IMG_PROJECT_ROOT')  # $HOME (or ~) folder
    # FIXME: If it's blank, use hard-coded default

    # under user's $HOME (or ~) folder
    img_project_folder = get_str_from_env_file('IMG_PROJECT_FOLDER')
    # FIXME: If it's blank, use hard-coded default

    # Convert "$HOME" or "~" (tilde) in IMG_PROJECT_PATH to "/Users/wilsonmar":
    if "$HOME" in img_project_root:
        img_project_root = Path.home()
    elif "~" in img_project_root:
        img_project_root = expanduser("~")
    img_project_path = str(img_project_root) + "/" + img_project_folder
        # macOS "$HOME/Projects" or on Windows: D:\\Projects
    print_verbose(f'{localize_blob("Path")}: \"{img_project_path}\" ')

    from os import path
    if path.exists(img_project_path):
        formatted_epoch_datetime = format_epoch_datetime(
            os.path.getmtime(img_project_path))
        print_verbose(
            f'{localize_blob("Directory")} \"{img_directory}\" {localize_blob("created")} {formatted_epoch_datetime}')
        # FIXME: dir_tree( img_project_path )  # List first 10 folders
        # TODO: Get file creation dates, is platform-dependent, differing even
        # between the three big OSes.

        if remove_img_dir_at_beg:
            if verify_manually:  # Since this is dangerous, request manual confirmation:
                Join = input(
                    'Delete a folder used by several other programs?\n')
                if Join.lower() == 'yes' or Join.lower() == 'y':
                    dir_remove(img_project_path)
            else:
                dir_remove(img_project_path)

    try:
        # Create recursively, per
        # https://www.geeksforgeeks.org/create-a-directory-in-python/
        os.makedirs(img_project_path, exist_ok=True)
        # Alternative: os.mkdir(img_parent_path)
        os.chdir(img_project_path)  # change to directory.
    except OSError as error:
        print_fail(
            f'{localize_blob("Directory path")} \"{img_file_name}\" {localize_blob("cannot be created")}.')
        # print_fail(f'{localize_blob("Present Working Directory")}: \"{os.getcwd()}\" ')



# SECTION 42. Download img application files  = download_imgs

# Commentary on this at
# https://wilsonmar.github.io/python-samples#download_imgs

def img_download():
    print_heading("In img_download")

    # STEP: Get current path of the script being run:
    img_parent_path = pathlib.Path(
        __file__).parent.resolve()  # for Python 3 (not 2)
    # NOTE: The special variable _file_ contains the path to the current file.
    print_verbose("Script executing at path: '% s' " % img_parent_path)
    # img_parent_path=os.path.dirname(os.path.abspath(__file__))  # for Python 2 & 3
    # print_verbose("Script executing at path: '% s' " % img_parent_path )

    # STEP: TODO: Create a Projects folder (to not clutter the source code
    # repository)

    # STEP: Show target directory path for download:

    img_project_path = os.path.join(img_parent_path, img_directory)

    print_verbose("Downloading to directory: '% s' " % img_project_path)
    if path.exists(img_directory):
        formatted_epoch_datetime = format_epoch_datetime(
            os.path.getmtime(img_project_path))
        print_trace(
            f'{localize_blob("Directory")} \"{img_directory}\" {localize_blob("created")} {formatted_epoch_datetime}')
        dir_tree(img_project_path)
        # NOTE: Getting file creation dates, is platform-dependent, differing
        # even between the three big OSes.
        if remove_img_dir_at_beg:
            dir_remove(img_project_path)
    try:
        # Create recursively, per
        # https://www.geeksforgeeks.org/create-a-directory-in-python/
        os.makedirs(img_project_path, exist_ok=True)
        # os.mkdir(img_parent_path)
    except OSError as error:
        print_fail(f'Directory path \"{img_file_name}\" cannot be created.')

    # STEP: Show present working directory:
    # About Context Manager:
    # https://stackoverflow.com/questions/6194499/pushd-through-os-system
    os.chdir(img_project_path)
    # if show_verbose:
    #    print (f'*** {localize_blob("Present Working Directory")}: \"{os.getcwd()}\" ')

    # STEP: Download file from URL:

    img_file_path = os.path.join(img_project_path, img_file_name)
    print_verbose("Downloading to file path: '% s' " % img_file_path)
    if path.exists(img_file_path) and os.access(img_file_path, os.R_OK):
        if remove_img_file_at_beg:
            print_verbose(f'{localize_blob("File being removed")}: {img_file_path} ')
            file_remove(img_file_path)
        else:
            print_verbose(f'No downloading as file can be accessed.')
    else:
        print_verbose("Downloading from url: '% s' " % img_url)
        # Begin perf_counter_ns()  # the nanosecond version of perf_counter().
        tic = time.perf_counter()

        # urllib.urlretrieve(img_url, img_file_path)  # alternative.
        file_requested = requests.get(img_url, allow_redirects=True)
        headers = requests.head(img_url, allow_redirects=True).headers
        print_trace("content_type: '% s' " % headers.get('content-type'))
        open(img_file_name, 'wb').write(file_requested.content)
        # NOTE: perf_counter_ns() is the nanosecond version of perf_counter().

    # STEP: Show file size if file confirmed to exist:

    if path.exists(img_file_path):
        toc = time.perf_counter()
        # FIXME: took = toc - tic:0.4f seconds
        print_verbose(
            f'Download of {format_number( os.path.getsize(img_file_path))}-byte {img_file_name} ')
            # On Win32: https://stackoverflow.com/questions/12521525/reading-metadata-with-python
            # print_verbose(os.stat(img_file_path).st_creator)
    else:
        print_fail(f'File {img_file_name} not readable.')
        # no exit()



# SECTION 43. Manipulate image (OpenCV OCR extract)    = process_img

"""
# if process_img:
# Based on https://www.geeksforgeeks.org/python-read-blob-object-in-python-using-wand-library/

# import required libraries
from __future__ import print_function

# import Image from wand.image module
from wand.image import Image

# open image using file handling
with open('koala.jpeg') as f:

    # get blob from image file
    image_blob = f.read()

# read image using wand from blob file
with Image(blob = image_binary) as img:

    # get height of image
    print_trace("img.height="+img.height)

    # get width of image
    print_trace("img.width="+img.width)
"""


# SECTION ??. Send image files via fax        = send_fax

# https://www.codeproject.com/Articles/5362374/Fax-REST-API-Quick-Start-Guide



# SECTION ??. Send SMS text to mobile devices = send_sms

def sms_from_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    sms_phone_from = get_str_from_env_file('sms_phone_from')
    if not sms_phone_from:
        print_fail("sms_phone_from not in .env")
        return None

    sms_phone_to = get_str_from_env_file('sms_phone_to')
    if not sms_phone_to:
        print_fail("sms_phone_to not in .env")
        return None

    SMS_ACCT_SID = get_secret_from_env_file('SMS_ACCT_SID')
    if not SMS_ACCT_SID:
        print_fail("SMS_ACCT_SID not in .env")
        return None

    SMS_AUTH_TOKEN = get_secret_from_env_file('SMS_AUTH_TOKEN')
    if not SMS_AUTH_TOKEN:
        print_fail("SMS_AUTH_TOKEN not in .env")
        return None

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print_info("SMS via Twillo \""+pubsub_message+"\" from "+sms_phone_from+" to "+sms_phone_to)

    #import base64
    #import os
    #import twillo
    from twillo.rest import Client
    client = Client(SMS_ACCT_SID, SMS_AUTH_TOKEN)
    message = client.messages.create(
                              body='Message from twillo pubsub : ' +pubsub_message,
                              from_=sms_phone_from,
                              to=sms_phone_to
                                    )
    return message.sid



# SECTION 44. Send message to Slack           = send_slack_msgs

# Described at https://wilsonmar.github.io/python-samples/#send_slack_msgs
# But to avoid adding yet another dependency that may become a vulnerability:
# we send Slack message - https://keestalkstech.com/2019/10/simple-python-code-to-send-message-to-slack-channel-without-packages/
#   https://api.slack.com/methods/chat.postMessage

def do_send_slack():
    if send_slack == 0:
       return None
    threshold = gen_0_to_100_int()
    if send_slack < threshold:
        print_warning("do_send_slack "+str(send_slack)+" < threshold "+str(threshold)+" so not executed.")
    else:
        SLACK_APP1_OAUTH_TOKEN = get_secret_from_env_file('SLACK_APP1_OAUTH_TOKEN')
        if not SLACK_APP1_OAUTH_TOKEN:
            print_fail("SLACK_APP1_OAUTH_TOKEN not in .env")
            return None

        SLACK_CHANNEL = get_str_from_env_file('SLACK_CHANNEL')
        if not SLACK_CHANNEL:
            print_fail("SLACK_CHANNEL not in .env")
            return None

        slack_text_to_send = get_str_from_env_file('slack_text_to_send')
        if not slack_text_to_send:
            print_fail("slack_text_to_send not in .env")
            return None

        # Based on: conda install slackclient 
        # See https://www.youtube.com/watch?v=DyzNPAuGtcU
        import slack
        client = slack.WebClient(SLACK_APP1_OAUTH_TOKEN)
        client.chat_postMessage(channel=SLACK_CHANNEL,text=slack_text_to_send)
        print_verbose("\""+slack_text_to_send+"\" sent to channel "+SLACK_CHANNEL)


def post_message_to_slack(text, blocks=None):

    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': SLACK_APP1_OAUTH_TOKEN,
        'channel': slack_channel,
        'text': text,
        'icon_emoji': slack_icon_emoji,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()
    del os.environ["SLACK_APP1_OAUTH_TOKEN"]  # remove


def post_file_to_slack(text, file_name, file_bytes, file_type=None, title=None):
    return requests.post(
        'https://slack.com/api/files.upload',
        {
            'token': SLACK_APP1_OAUTH_TOKEN,
            'filename': file_name,
            'channels': slack_channel,
            'filetype': file_type,
            'initial_comment': text,
            'title': title
        },
        files={'file': file_bytes}).json()

    # image = "https://images.unsplash.com/photo-1495954484750-af469f2f9be5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
    # response = urllib.request.urlopen(image)
    # data = response.read()
    # post_file_to_slack('Amazing day at the beach. Check out this photo.', 'DayAtTheBeach.jpg', data)


class TestSendSlack(unittest.TestCase):
    def test_send_slack(self):
        if send_slack:
            print_heading("send_slack")

            SLACK_APP1_OAUTH_TOKEN = get_secret_from_env_file('SLACK_APP1_OAUTH_TOKEN')
            if not SLACK_APP1_OAUTH_TOKEN:
                print_error("SLACK_APP1_OAUTH_TOKEN not retrieved")
                return None
            
            slack_user_name = get_str_from_env_file('SLACK_USER_NAME')   # 'Double Images Monitor'
            slack_channel = get_str_from_env_file('SLACK_CHANNEL')     # #my-channel'
            slack_icon_url = get_str_from_env_file('SLACK_ICON_URL')
            slack_icon_emoji = get_str_from_env_file('SLACK_ICON_EMOJI')  # ':see_no_evil:'
            slack_text = get_str_from_env_file('SLACK_TEXT')

            double_images_count = 0
            products_count = 0
            bucket_name = 0
            file_name = "my.txt"

            slack_info = 'There are *{}* double images detected for *{}* products. Please check the <https://{}.s3-eu-west-1.amazonaws.com/{}|Double Images Monitor>.'.format(
                double_images_count, products_count, bucket_name, file_name)

            # post_message_to_slack(slack_info)
            # post_file_to_slack( 'Check out my text file!', 'Hello.txt', 'Hello World!')

            # PROTIP: When Slack returns a request as invalid, it returns an HTTP 200 with a JSON error message:
            # {'ok': False, 'error': 'invalid_blocks_format'}



# SECTION 45. Send email thru Gmail         = email_via_gmail

# Inspired by
# https://www.101daysofdevops.com/courses/101-days-of-devops/lessons/day-14/

def verify_email_address(to_email_address):
    if verify_email:
        # First, get API from https://mailboxlayer.com/product
        verify_email_api = get_str_from_env_file('MAILBOXLAYER_API')
        del os.environ["MAILBOXLAYER_API"]
        # https://apilayer.net/api/check?access_key = YOUR_ACCESS_KEY & email = support@apilayer.com
        url = "http://apilayer.net/api/check?access_key=" + verify_email_api + \
            "&email=" + to_email_address + \
            "&smtp=1&format=1"  # format=1 for JSON response
        print_trace(url)
        result = requests.get(url, allow_redirects=False)
        print_trace(result)
        if result:
            return True
        else:
            return False


def smtplib_sendmail_gmail(to_email_address, subject_in, body_in):
    # subject_in = "hello"
    # body_in = "testing ... "
    # "loadtesters@gmail.com" # Authenticate to google (use a separate gmail account just for this)
    from_gmail_address = get_str_from_env_file('THOWAWAY_GMAIL_ADDRESS')
    from_gmail_password = get_str_from_env_file('THOWAWAY_GMAIL_PASSWORD')  # a secret

    print_trace(f'send_self_gmail : from_gmail_address={from_gmail_address} ')
    message = f'Subject: {subject_in}\n\n {body_in}'
    if True:  # try:
        import smtplib
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()  # start TLS to encrypt traffic

        response = s.login(from_gmail_address, from_gmail_password)
            # Response expected = (235, '2.7.0 Accepted')
        del os.environ["THOWAWAY_GMAIL_ADDRESS"]
        del os.environ["THOWAWAY_GMAIL_PASSWORD"]  # remove
        text_msg = "Gmail login response=" + str(response)
        print_trace(text_msg)

        ok_to_email = verify_email_address(to_email_address)
        if not ok_to_email:
            print_fail("Not OK to email.")
        else:
            try:
                result = s.sendmail(from_gmail_address, to_email_address, message)
                         # FROM addr, TO addr, message
                # To avoid this error response: Allow less secure apps: ON - see https://support.google.com/accounts/answer/6010255
                # smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted. Learn more at\n
                # 5.7.8  https://support.google.com/mail/?p=BadCredentials
                # nm13sm5582986pjb.56 - gsmtp')
                print_trace("result="+result)  # RESPONSE: <Response [200]>
            except Exception as e:
                print_fail("sendmail() error "+e)
                s.quit()

    # FIXME: ResourceWarning: Enable tracemalloc to get the object allocation traceback

    # TODO: For attachments, see
    # https://github.com/Mohamed-S-Helal/Auto-gmail-draft-pdf-attatching/blob/main/gmailAPI.py


class TestSendEmail(unittest.TestCase):
    def test_email_via_gmail(self):
        if email_via_gmail:
            print_heading("email_via_gmail")

            to_gmail_address = get_str_from_env_file(
                'TO_EMAIL_ADDRESS')  # static not a secret
            subject_text = "Hello from " + this_pgm_name  # Customize this!
            if True:  # TODO: for loop through email addresses and text in file:

                # Optionally, add datestamp to email body:
                trans_datetime = str(_datetime.datetime.fromtimestamp(
                    time.time()))  # Default: 2021-11-20 07:59:44.412845
                body_text = "Please call me. It's now " + trans_datetime

                print_heading(f'email_via_gmail : {trans_datetime}')

                smtplib_sendmail_gmail(to_gmail_address, subject_text, body_text)

                # Loop to get next for



# SECTION 46. Calculate Hash and View Gravatar on Web Browser   = view_gravatar

def get_gravatar_url(email, size, default, rating):
    # Commentary of this is at https://wilsonmar.github.io/python-samples#view_gravatar
    hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    url = "https://secure.gravatar.com/avatar/"

    # Validate size up to 2048px, rating G,PG,R,X per https://en.gravatar.com/site/implement/images/
    # PROTIP: Check if a data type is numeric before doing arithmetic using it.
    if not isinstance(size, int):   # if ( type(size) != "<class 'int'>" ):
        size = int(size)
    if (size > 2048):
        print_fail("Parameter size cannot be more than 2048px. Set to 100.")
        size = 100
    rating = rating.upper()
    if rating not in {"G", "PG", "R", "X"}:
        print_fail('Rating " + rating_in + " not recognized. Set to "G". ')
        rating = "G"

    url_string = url + hash + "&size=" + \
        str(size) + "&d=" + default + "&r=" + rating
    return url_string


class TestViewGravatar(unittest.TestCase):
    def test_view_gravatar(self):

        if view_gravatar:
            print_heading("view_gravatar")

            # TODO: Alternately, obtain from user parameter specification:
            some_email = get_str_from_env_file('MY_EMAIL')  # "johnsmith@example.com"
            print_verbose(some_email)
            some_email_gravatar = ""

            if not some_email_gravatar:
                url_string = get_gravatar_url(
                    some_email, size="100", default='identicon', rating='G')
                print_info(url_string)
                # Save gravatar_url associated with email so it won't have to be created again:
                some_email_gravatar = url_string

            import webbrowser
            print_verbose("Opening web browser to view gravatar image of " + some_email)
            webbrowser.open(some_email_gravatar, new=2)
                # new=2 opens the url in a new tab. Default new=0 opens in an existing browser window.
                # See https://docs.python.org/2/library/webbrowser.html#webbrowser.open



# SECTION 47. Generate BMI  = categorize_bmi

# NOTE: There is some controversy about the value of the BMI calculation.
# So BMI calculations here are done as a technical challenge, not a medical tool.

class TestGemBMI(unittest.TestCase):
    def test_categorize_bmi(self):

        print_todo("Bring work code out of TestGemBMI class")

        if categorize_bmi:
            print_heading("categorize_bmi")

            # WARNING: Hard-coded values:
            # TODO: Get values from argparse of program invocation parameters.

            # PROTIP: Variables containing measurements should be named with
            # the unit.

            # Based on https://www.babbel.com/en/magazine/metric-system
            # and
            # https://www.nist.gov/blogs/taking-measure/busting-myths-about-metric-system
            # US, Myanmar (MM), Liberia (LR) are only countries not using
            # metric:
            if my_country in ("US", "MM", "LR"):
                # NOTE: Liberia and Myanmar already started the process of
                # “metrication.”
                if my_country == "MM":
                    country_name = "for Myanmar (formerly Burma)"
                elif my_country == "LR":
                    country_name = "for Liberia"
                else:
                    country_name = ""
                text_to_print = "Using US(English) system of measurement " + \
                    country_name
                print_verbose(text_to_print)
                height_inches = 67   # 5 foot * 12 = 60 inches
                weight_pounds = 203  # = BMI 31
                print_warning("Using hard-coded input values.")

                # TODO: Convert: 1 kilogram = 2.20462 pounds. cm = 2.54 *
                # inches.
                # input("Enter your height in cm: "))
                height_cm = float(height_inches * 2.54)
                # input("Enter your weight in kg: "))
                weight_kg = float(weight_pounds * 0.453592)
            else:  # all other countries:
                print_verbose("Using metric (International System of Units):")
                height_cm = 170
                weight_kg = 92
                print_warning("Using hard-coded input values.")

                height_inches = float(height_cm / 2.54)
                weight_pounds = float(weight_kg / 0.453592)

            # Show input in both metric and English:
            print_trace(f'height_inches={height_inches} weight_pounds={weight_pounds} ')
            print_trace(f'height_cm={height_cm} weight_kg={weight_kg} ')

            # TODO: PROTIP: Check if cm or kg based on range of valid values:
            # BMI tables at https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmi_tbl2.htm
            # Has height from 58 (91 pounds) to 76 inches for BMI up to 54 (at
            # 443 pounds)

            # PROTIP: Format the number immediately if there is no use for full floating point.
            # https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmicalc.htm
            # https://www.cdc.gov/healthyweight/assessing/bmi/Index.html
            # https://en.wikipedia.org/wiki/Body_mass_index

            # if height_inches > 0:
            # BMI = ( weight_pounds / height_inches / height_inches ) * 703  #
            # BMI = Body Mass Index
            if height_cm > 0:  # https://www.cdc.gov/nccdphp/dnpao/growthcharts/training/bmiage/page5_1.html
                BMI = (weight_kg / height_cm / height_cm) * 10000
            if BMI < 16:
                print_error("Categorize_bmi ERROR: BMI of "+BMI+" lower than 16.")
            elif BMI > 40:
                print_error("Categorize BMI of "+BMI+" higher than 40.")
            BMI = round(int(BMI), 1)  # BMI = Body Mass Index

            # PROTIP: Ensure that the full spectrum of values are covered in if
            # statements.
            if BMI == 0:
                category_text = 'ERROR'
            elif BMI <= 18.4:
                category_text = '(< 18.4) = ' + localize_blob('Underweight')
            elif BMI <= 24.9:
                category_text = '(18.5 to 24.9) = ' + \
                    localize_blob('Healthy')
            elif BMI <= 29.9:
                category_text = '(25 to 29.9) = ' + localize_blob('Overweight')
            elif BMI <= 34.9:
                category_text = '(30 to 34.9) = ' + \
                    localize_blob('Moderately Obese (class 1)')
            elif BMI <= 39.9:
                category_text = '(35 to 39.9) = ' + \
                    localize_blob('Severely Obese (class 2)')
            else:
                category_text = '(40 or above) = ' + \
                    localize_blob('Morbidly Obese (class 3)')

            text_to_show = "BMI " + str(BMI) + " " + category_text
            print_info(text_to_show)

            # TODO: Calculate weight loss/gain to ideal BMI of 21.7 based on height (discounting all other factors).
            # 138 = 21.7 / 703 = 0.030867709815078  # http://www.moneychimp.com/diversions/bmi.htm
            # ideal_pounds = ( 21.7 / 703 / weight_pounds ) * height_inches
            # print_trace(f'Ideal weight at BMI 21.7 = {ideal_pounds} pounds.')



# SECTION 48. Play text to sound:

# See https://cloud.google.com/text-to-speech/docs/quickstart-protocol

def gen_sound_for_text(text_to_say):
    print_trace("in gen_sound_for_text")

    my_accent = get_str_from_env_file('MY_ACCENT')
    if not my_accent:
        my_accent = "en"  # or "en" "uk" "fr" (for English with French accent)
        print_warning("my_accent="+my_accent+" from default!")

    if not text_to_say:
        text_to_say = get_str_from_env_file('TEXT_TO_SAY')
        if not text_to_say:
            text_to_say = "hello world!"
            print_warning("text_to_say="+text_to_say+" from default!")

    # Based on: conda install -c conda-forge gtts
    # import gtts
    from gtts import gTTS
    # Also installs  requests  2.31.0-pyhd8ed1ab_0 --> 2.28.2-pyhd8ed1ab_1

    s = gTTS(text=text_to_say, lang=my_accent)

    speech_file_name = get_str_from_env_file('SPEECH_FILE_NAME')
    if not speech_file_name:
        speech_file_name = "speech.mp3"
    s.save(speech_file_name)  # generate mp3 file.

    # Alternate 1:
    # On a Mac, double-clicking on the mp3 file by default invokes Apple Music app:
       # so NO: os.system(f'start {speech_file_name}')

    # Alternate 2:  # pip install -U playsound
    import playsound
    playsound.playsound(speech_file_name, True)

    # Alternate 3:  # pip install -U pyttsx3
    # import pyttsx3
    # engine = pyttsx3.init()allte
    # engine.say

    # Alternate 4:
    # from playsound import playsound  # pip install -upgrade playsound
    # playsound(speech_file_name)

    # Remove file:
    if remove_sound_file_generated:
        os.remove(speech_file_name)


# SECTION 49. Open a new Google Sheet online (instead of Excel spread sheet)
# SECTION 50. Retrieve a GitHub repo
# SECTION 51. Navigate into a path to the retrieved github repo (folder _posts)
# SECTION 52. Cycle through files in a folder.
# SECTION 53. Open each .md file
# SECTION 54.   Cycle through lines to identify github image URL
# SECTION 55.   Extract img alt name and ensure it has a file type png/jpg
# SECTION 56.   Retrieve image file from GitHub
# SECTION 57.   Save image file in Google Drive folder
# SECTION 58.   Correct alt text in image html.
# SECTION 59.   In md file change image URL and img alt text
# SECTION 60. Save Google Sheet entry
# SECTION 61. Update (add and commit) changed md files (in folder _posts). Push to github.
# SECTION 62. Remove (clean-up) folder/files created   = cleanup_img_files

def img_files_cleanup():
    print_trace("for cleanup_img_files")
    # Remove files and folders to conserve disk space and avoid extraneous
    # files:

    if remove_img_dir_at_end:
        print_heading("remove_img_dir_at_end")
        if verify_manually:  # Since this is dangerous, request manual confirmation:
            Join = input('Delete a folder used by several other programs?\n')
            if Join.lower() == 'yes' or Join.lower() == 'y':
                dir_remove(img_project_path)
        else:
            dir_remove(img_project_path)

    if remove_img_file_at_end:
        print_verbose(
        f'{localize_blob("File")} \"{img_file_path}\" {localize_blob("being removed")} ')
        file_remove(img_file_path)

    print_verbose(f'After this run: {img_project_path} ')
    dir_tree(img_project_path)



# SECTION 99. Display run stats at end of program       = display_run_stats

class TestDisplayRunStats(unittest.TestCase):
    def test_display_run_stats(self):

        if display_run_stats:
            print_heading("display_run_stats")
            # Compare for run duration: time.clock() deprecated in 3.3
            stop_run_time = time.monotonic()
            stop_epoch_time = time.time()
            stop_datetime = _datetime.datetime.fromtimestamp(stop_epoch_time)  # Default: 2021-11-20 07:59:44.412845
            # print_info(f'{localize_blob("Ended")} {stop_run_time.strftime(my_date_format)} ')
            # print_info(f'{localize_blob("Ended")} {stop_datetime.strftime(my_date_format)} ')

            run_time_duration = stop_run_time - start_run_time
            print_trace("type(run_time_duration))  # <class 'datetime.timedelta")
            print_trace(f'{this_pgm_name} done in {round( run_time_duration, 2 )} seconds clock time. ')


#################################################################

# Execute a script by itself, and import objects from the script as though it were a regular module:
if __name__ == "__main__":
    print_heading("In main: initialization")
    os_info()
    if show_print_samples:
        print_samples
    #set_cli_parms()
    if use_env_file:
        open_env_file(ENV_FILE)
        read_env_file()

    print_heading("main_loop_runs_requested="+str(main_loop_runs_requested))
    main_loop_runs_started=int(1)
    while True:  # loop indefinitely (for stress testing), pausing in-between:
        print_trace("In main loop "+str(main_loop_runs_started))
        # display_memory()
        # display_run_stats()
        #print_env_vars()

        #gen_magic_8ball_str()
        # do_send_slack()  # FIXME: not working

        do_use_hvault()
        exit()

#       geodata_from_ipaddr(my_ip_address)

        login_aws()

        if use_azure == True:
            print_heading("use_azure")
            if login_to_azure == True:
                print_heading("login_to_azure")
                
                # azure_login()
                # is_logged_in=azure_login()  # returns JSON of TenantID, (subscription) id
                # azure_info()
                    # azure_resc()
                # azure_blob_???
                
                if list_azure_resc == True:
                    # See https://www.youtube.com/watch?v=we1pcMRQwD8 by Michael Levan of CBTNuggets.com
                    # See https://stackoverflow.com/questions/51546073/how-to-run-azure-cli-commands-using-python
                    from azure.cli.core import get_default_cli as azcli
                    # Run a CLI az command constructed as a Python struct:
                    # Replace 'Dev2' with your resource:
                    azcli().invoke(['vm', 'list', '-g', 'Dev2'])
        
        if use_gcp == True:
            print_heading("use_gcp")
            gcp_login()
            # gcp_doc_title(READONLY_SCOPE,DOCUMENT_ID)
    
            gcp_buckets_list()

        if use_aws == True:
            print_heading("use_aws")

        if process_romans == True:
            print_heading("process_romans")
            # Verify online at # https://www.calculatorsoup.com/calculators/conversions/roman-numeral-converter.php

            current_year = get_cur_yyyy()
            # Get roman numerals from today's year:
            mylist = [current_year, "xx"]
            my_number = mylist[0]
            my_roman = int_to_roman(my_number)   # my_roman = "MMXXIII" = 2023
            print_trace("current_year="+current_year)

            my_roman_num = current_year
            ob1 = int_to_roman(my_roman_num)
            print_info(f'process_romans: int_to_roman: {my_number} ==> {my_roman} ')

            ob1 = roman_to_int(my_roman)
            # my_number = ob1.romanToInt(my_roman)
            print_info(f'process_romans: roman_to_int: {my_roman} => {my_number} ')

        if show_weather == True:
            my_zip_code = obtain_zip_code()
            get_weather_info(my_zip_code)

        if gen_0_to_100 == True:
            print_heading("gen_0_to_100 - 5 Random numbers between 1 and 100:")
            gen_0_to_100(5)

        if gen_salt == True:
            print_heading("gen_salt")
            gen_salt()

        if gen_jwt == True:
            print_heading("gen_jwt")
            gen_jwt()

        if update_md_files == True:
            print_heading("update_md_files")

        if download_imgs == True:
            img_download()

        if cleanup_img_files == True:
           img_files_cleanup()

        # if flask:  display_flask()

        # unittest.main()
        # Automatically invokes all functions within classes which inherits (unittest.TestCase):
        # Example: class TestMakeChange(unittest.TestCase):
        # The setup() is run, then all functions starting with "test_".
        
        #if show_dates == True:
        #    compare_dates()

        main_loop_runs_started += 1
        # PROTIP: Multiple conditions logic:
        if (( main_loop_runs_requested >= main_loop_runs_started ) \
            or ( main_loop_runs_requested == 0 )):  # still more runs to do:
            if main_loop_pause_seconds>=float(999):
                x = input("Press Enter to continue or control+C to cancel run.")
            elif main_loop_pause_seconds>float(0):
                # PROTIP: Pause set seconds of time delay to do nothing:
                print_trace("Sleeping "+str(main_loop_pause_seconds)+" seconds.")
                # import time
                time.sleep(main_loop_pause_seconds)
            # TODO: main_loop_run_pct=100 
            # break
        else:
            print_trace("Exiting main: Thank you for visiting!")
            break  # out of while True

        if gen_sound_for_text == True:
            gen_sound_for_text("Bye bye!")

    # while True
    
    print_wall_times()
    
# END