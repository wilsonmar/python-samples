#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Please reference .pylintrc for PEP8 formatting according to https://peps.python.org/pep-0008/
# conda install black  # to reformat
# pylint: disable=line-too-long trailing-newlines
"""
This is regex-scraper.py at
https://github.com/wilsonmar/python-samples/blob/main/regex-scraper.py
to download the Survivor Library: How to surveve when the Technology Doesn't
(It's not a Library about survival. It's a library for surviors.)

Based on https://github.com/alw98/SurvivorLibraryCrawler/blob/master/LibraryCrawler.py
and A Canticle for Leibowitz.

CURRENT STATUS: WORKING!
gas "v003 shell db, downloading :regex-scraper.py"

"""

import html
import re
import time
import os
import shutil
from urllib.request import urlopen

from pathlib import Path
import datetime

# pip3 install bs4
from bs4 import BeautifulSoup
import requests

# Set the locale to the user's default settings
import locale
locale.setlocale(locale.LC_ALL, '')

DB_PATH="survivor"
DB_NAME="survivor"
# if Windows:
  # saveloc = "C:\\Users\\alw98\\Downloads\\Programming Stuff\\survivorlibrary"
# if Linux or MacOS:
BASE_FOLDER = "~"
SAVE_FOLDER = "survivorlibrary"
PAUSE_SECS=2
LIST_CATALOG=False

# PHASE A: Build a database of CATEGORIES and a link to each from the MAIN INDEX table at

# PHASE B: Build a database of files and download those files locally.
   # Accounting.csv does not contain URLs so we must scrape the HTML such as:
   # Look for words such as "Accounting" between <a href="/index.php/ and ">
   # https://www.survivorlibrary.com/index.php/Accounting

# PHASE C: Make downloaded files available offline, such as:
   # https://www.survivorlibrary.com/library/20th_century_bookkeeping_and_accounting_1922.pdf


def get_disk_usage(path):
    usage = shutil.disk_usage(path)
    total = usage.total / (1024 * 1024 * 1024)  # Convert to GB
    used = usage.used / (1024 * 1024 * 1024)    # Convert to GB
    free = usage.free / (1024 * 1024 * 1024)    # Convert to GB

    print(f">>> Disk Space Capacity: {total:.2f} GB, Used: {used:.2f} GB, Free: {free:.2f} GB")
    return 0


# PHASE A: Build a database of CATEGORIES and a link to each from the MAIN INDEX table at
   # https://www.survivorlibrary.com/index.php/main-library-index/
def establish_database(folder_path,db_name):

    # Specify the path you want to check
    path = "/"  # This checks the root directory, you can change it to any path

    # Get disk usage statistics:
    total, used, free = shutil.disk_usage(path)

    # Convert bytes to gigabytes for readability
    free_gb = free // (2**30)
    print(f">>> Free disk space: {free_gb} GB")

    print(f">>> establish_database: {db_name} within {folder_path}.")


def make_folder(base_path,add_folder):

    if base_path == "~":
        # Check if folder exists within user's home folder:
        base_path = os.path.expanduser('~')
        print(">>> ~ =",base_path)

    path = Path(base_path)
    if not path.is_dir():
        print(">>> make_folder:",path,"does not exist. Creating...")
        try:
            os.mkdir(path)
            print(f">>> make_folder: {path} created!")
        except FileExistsError:
            print(f">>> make_folder: {path} already exists!")
    try:
        modified_timestamp = os.path.getmtime(path)
        modified_date = datetime.datetime.fromtimestamp(modified_timestamp)
        print(f">>> {modified_date} {path}")
    except Exception as e:
        print(f">>> make_folder: {e}")

    path = path / add_folder
    # print(f">>> make_folder: {path} extended!")
    if not path.is_dir():
        print(">>> make_folder:",path,"does not exist. Creating...")
        try:
            os.mkdir(path)
            print(f">>> make_folder: {path} created!")
        except FileExistsError:
            print(f">>> make_folder: {path} already exists!")
            return 0
    try:
        modified_timestamp = os.path.getmtime(path)
        modified_date = datetime.datetime.fromtimestamp(modified_timestamp)
        print(f">>> {modified_date} {path}")
    except Exception as e:
        print(f">>> make_folder: {e}")
        return 0
    return path


def extract_categories(save_folder_path):

    # print(f">>> extract_categories: {save_folder_path}")

    # TODO: Make url a paramter-provided value?
    url = "https://www.survivorlibrary.com/index.php/main-library-index/"
    # print(">>> Starting crawler...")
    #website = urlopen(url)
    #print(">>> opened web page: " + url)

#    content = website.read().decode('utf-8')
#    categories_html_char_count=len(content)
#    print(">>> opened website contains",categories_html_char_count,"characters.")

    # Read the content of the file saved:
    # TODO: Instead read real-time using Beautiful Soup:
    with open('surivor.html', 'r') as file:
        content = file.read()

    # Define the pattern to extract text:
    pattern = r'/index.php/(.*?)">'

    # Find all matches
    matches = re.findall(pattern, content, re.DOTALL)
    # Print the results:
    category_found_count = 0
    for match in matches:
        category_found = match.strip()
        category_found_count += 1

        # Add field "Interest-Rating" field to each category in the database.
        # Add field "Download" to each category entry.
        #result=save_category(category_found)  # saved:
        #if result:  # == 0

        category_folder_path = save_folder_path / category_found  # equivalent to base_folder_path +'/'+ category_found
        # print(f">>> category_folder_path: {category_folder_path}")
        create_category_folder(category_folder_path)

        extract_files(save_folder_path,category_found)  # see local function below.

    # Summarize:
    print(" ")
    print(">>> category_found_count=",category_found_count)
    return 0


def save_category(category_found):
    #print(f">>> TODO: save category {category_found} in db.")
    return 0  # for now.


# Called from a function above:
# If the Category folder does not exist under program folder, create it:
def create_category_folder(category_folder_path):
    # print(f">>> category_folder_path: {category_folder_path}")
    # try:
        path = Path(category_folder_path)
        if not path.is_dir():
            #print(">>> Folder:",category_folder_path,"does not exist. Creating...")
            try:
                os.mkdir(path)
                print(f">>> Folder {path} created!")
            except FileExistsError:
                print(f">>> Folder {path} already exists")

        modified_timestamp = os.path.getmtime(category_folder_path)
        modified_date = datetime.datetime.fromtimestamp(modified_timestamp)
        print(f">>> {modified_date} {category_folder_path}")
        return 0

    #except Exception as e:
        # print(f">>> download_file: {e}")
        # return 0


# Called from function above:
def extract_files(folder_path,category_found):
    # Construct URL such as https://www.survivorlibrary.com/index.php/Accounting
    url="https://www.survivorlibrary.com/index.php/"+category_found
    # print(">>> files_url:",url)

    try:
        # Fetch the entire HTML page as content:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f">>> Error fetching the webpage: {e}")
    except Exception as e:
        print(f">>> Error occurred: {e}")

        # Loop through table to extract each line:
        # https://www.perplexity.ai/search/extract-separate-values-from-e-fKJ47.ivRquXBiVYC_7PMg

    html_content = response.text
    files_html_char_count=len(html_content)
    print(f">>>",files_html_char_count,"characters in",category_found,"files page.")

    # soup = BeautifulSoup(html_content, 'html.parser')
        # extracted_data = extract_table_data(html_content)
    # Unlike elements by class name in url = "http://quotes.toscrape.com"
    # quotes = soup.find_all('span', class_='text') from <span class="text" itemprop="text">“There are
    # BeautifulSoup find_all() cannot be used here because of the lack of HTML class specifications:
    #    <tr id="table_7_row_0" data-row-index="0">
    #       <td style="">2013-08-08</td>
    #        <td style="">20Th Century Bookkeeping And Accounting 1922 </td>
    #        <td style="">
    #            <a href="/library/20th_century_bookkeeping_and_accounting_1922.pdf">PDF</a>
    #            23 mb
    #        </td>
    #    </tr>

    pattern = r'<a href="/library/(.*?)">'
    # Find all matches:
    matches = re.findall(pattern, html_content, re.DOTALL)
    # print(">>> matches:",matches)

    # FIXME: Define the pattern to extract text:
    # ['20th_century_bookkeeping_and_accounting_1922.pdf', 'Accounting.zip', etc.

    file_found_count = 0
    file_download_count = 0
    for match in matches:
        file_found = match.strip()
        file_found_count += 1
        # print(">>> file_found:",file_found)

        # TODO: See if the Category is already in the database.

        # TODO: See if the file is already in the database.

        # TODO: Extract the year of publication at the end of each TITLE.
        # TODO: Extract the file size (such as "23 mb") for the LINK field.
        # TODO: Extract file url around "PDF"
        # TODO: Download the url.

        # TODO: Save the fields from each row to a database or CSV file.
        # TODO: Add an interesting rating field to the database.

        save_folder_path=folder_path / category_found
        # print(f">>> save_folder_path: {save_folder_path}")
        download_file(file_found,save_folder_path)
        file_download_count += 1

    return 0


# Called from function above:
def download_file(file_found,save_folder_path):
    # print(f">>> download_file: {file_found} to {save_folder_path}.")

    #create_category_folder(save_folder_path)
    file_path = save_folder_path / file_found   # as object
    # print(">>> file_path:",file_path)
    try:
        # Bypass if file already downloaded:
        if os.path.exists(file_path):
            file_stats = os.stat(file_path)
            file_size = file_stats.st_size
            print(f">>> {file_size} bytes in {file_path}.")

    except Exception as e:
        print(f">>> {save_folder_path} {e}")

       # https://www.survivorlibrary.com/library/20th_century_bookkeeping_and_accounting_1922.pdf
    url="https://www.survivorlibrary.com/library/"+file_found
    print(">>> download:",url)

    try:
        response = requests.get(url, stream=True)  # to download large files in chunks.
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
        else:
            print('>>> Failed to download file with',response)
            return 0
    except requests.RequestException as e:
        print(f">>> download_file Error fetching the url: {e}")
    except Exception as e:
        print(f">>> download_file {url} Error: {e}")


    # Print size of downloaded file:
    #try:
        file_size = os.path.getsizez(file_path)
        #formatted_num = f"{file_size:,}"
        # formatted_num = f"{file_size:n}"
        # FIXME: number not being formatted with commans:
        formatted_num = locale.format_string("%.2f", file_size, grouping=True)
        print(f">>> {file_path} file size: {formatted_num} bytes.")
        return 0
    # except Exception as e:
        # print(f">>> file_size of {file_path} Error: {e}")

    # Pause for seconds between downloads:
    time.sleep(PAUSE_SECS)
    print(" ")


# Your code after the pause

#### MAIN:

path = "/"  # Root directory for Unix-like systems, or "C:\\" for Windows
disk_stats = get_disk_usage(path)

establish_database(DB_PATH,DB_NAME)

extended_path=make_folder(BASE_FOLDER,SAVE_FOLDER)
# print(f">>> main: {extended_path} ")

if extended_path:
   result=extract_categories(extended_path)

    # Alternately, Download "Last 180 Days.csv" ???
    # https://www.survivorlibrary.com/index.php/files-added-in-last-180-days

if result:
   if LIST_CATALOG == True:
       print(">>> TODO: LIST_CATALOG")


    # Within "DOWNLOAD BOOKS" where there is a table by DATE, CATEGORY, TITLE, LINK to PDF.

