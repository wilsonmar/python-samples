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

CURRENT STATUS: NOT WORKING
gas "v002 rename library-scraper.py to :regex-scraper.py"

Based on https://github.com/alw98/SurvivorLibraryCrawler/blob/master/LibraryCrawler.py
and A Canticle for Leibowitz.
"""

from urllib.request import urlopen
import re
import os
import html

from pathlib import Path
import datetime

# pip3 install bs4
from bs4 import BeautifulSoup
import requests

# Set the locale to the user's default settings
import locale
locale.setlocale(locale.LC_ALL, '')

# if Windows:
  # saveloc = "C:\\Users\\alw98\\Downloads\\Programming Stuff\\survivorlibrary"
# if Linux or MacOS:
SAVE_FOLDER = ".survivorlibrary"
DB_FOLDER="survivor"

# PHASE A: Build a database of CATEGORIES and a link to each from the MAIN INDEX table at
   # https://www.survivorlibrary.com/index.php/main-library-index/

# PHASE B: Build a database of files and download those files locally.
   # Accounting.csv does not contain URLs so we must scrape the HTML such as:
   # Look for words such as "Accounting" between <a href="/index.php/ and ">
   # https://www.survivorlibrary.com/index.php/Accounting

# PHASE C: Make downloaded files available offline, such as:
   # https://www.survivorlibrary.com/library/20th_century_bookkeeping_and_accounting_1922.pdf


def establish_library(save_folder):
    # print(">>> establish_library: save_folder:",save_folder)

    # Check if folder exists within user's home folder:
    home_directory = os.path.expanduser('~')
    # print(">>> home_directory:",home_directory)

    folder_path=home_directory+"/"+save_folder
    print(">>> save_folder_path:",folder_path)

    try:
        path = Path(folder_path)
        if not path.is_dir():
            print(">>> Folder:",folder_path,"does not exist. Creating...")
            try:
                os.mkdir(path)
                print(f">>> Folder {path} created!")
            except FileExistsError:
                print(f">>> Folder {path} already exists")

        modified_timestamp = os.path.getmtime(folder_path)
        modified_date = datetime.datetime.fromtimestamp(modified_timestamp)
        print(f">>> Folder: {folder_path} last modified: {modified_date}")
        return folder_path

    except Exception as e:
        print(f">>> download_file: {e}")
        return 0


def establish_database(db_folder):
    print(">>> TODO: establish_database:",db_folder)


def extract_categories():

    url = "https://www.survivorlibrary.com/index.php/main-library-index/"
    # print(">>> Starting crawler...")

    website = urlopen(url)
    print(">>> opened web page: " + url)

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

        # print(" ")
        # print(">>> category_found:",category_found)

        save_category(category_found)

        extract_files(category_found)  # see local function below.

    # Add field "Interest-Rating" field to each category in the database.
    # Add field "Download" to each category entry.

    # Summarize:
    print(" ")
    print(">>> category_found_count=",category_found_count)


# See if the Category is already in the database.
def save_category(category_found):
    print(">>> TODO: {category_found} to save in db:",category_found)


def extract_files(category_found):
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
        print(f">>>Error occurred: {e}")

        # Loop through table to extract each line:
        # https://www.perplexity.ai/search/extract-separate-values-from-e-fKJ47.ivRquXBiVYC_7PMg

    html_content = response.text

    files_html_char_count=len(html_content)
    print(">>>",category_found,"files page contains",files_html_char_count,"characters.")

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

    # FIXME: Define the pattern to extract text:
    pattern = r'<a href="/library/(.*?)">'
    # Find all matches:
    matches = re.findall(pattern, html_content, re.DOTALL)
    # print(">>> matches:",matches)
        # ['20th_century_bookkeeping_and_accounting_1922.pdf', 'Accounting.zip', etc.

    file_found_count = 0
    file_download_count = 0
    for match in matches:
        file_found = match.strip()
        file_found_count += 1
        # print(">>> file_found:",file_found)

        # See if the Category is already in the database.

        # See if the file is already in the database.

        # Extract the year of publication at the end of each TITLE.
        # Extract the file size (such as "23 mb") for the LINK field.
        # Extract file url around "PDF"
        # Download the url.

        # Save the fields from each row to a database or CSV file.
        # Add an interesting rating field to the database.

        download_file(file_found)
        file_download_count += 1

        exit()


def download_file(file_found):
    print(">>> download_file:",file_found)

    try:
        file_path=save_folder_path+"/"+file_found
        # Bypass if file already downloaded:
        if os.path.exists(file_path):
            file_stats = os.stat(file_path)
            file_size = file_stats.st_size
            print(f">>> Existing {file_path} contains {file_size} bytes.")
            return
        else:
            print(">>>",file_path,"does not exist. So download:")

    except Exception as e:
        print(f">>> {save_folder_path} {e}")

       # https://www.survivorlibrary.com/library/20th_century_bookkeeping_and_accounting_1922.pdf
    url="https://www.survivorlibrary.com/library/"+file_found
    print(">>> download_file:",url)

    try:
       #response = requests.get(url)
       response = requests.get(url, stream=True)  # to download large files in chunks.
    except requests.RequestException as e:
        print(f">>> download_file Error fetching the url: {e}")
    except Exception as e:
        print(f">>> download_file Error occurred: {e}")

    # Print size of downloaded file:
    try:
        file_size = os.path.getsize(file_path)
        #formatted_num = f"{file_size:,}"
        # formatted_num = f"{file_size:n}"
        formatted_num = locale.format_string("%.2f", file_size, grouping=True)
        print(f">>> {file_path} file size: {formatted_num} bytes.")
    except Exception as e:
        print(f">>> download_file: {e}")



#### MAIN:

save_folder_path=establish_library(SAVE_FOLDER)
print(f">>> main: {save_folder_path} ")
# establish_database(DB_FOLDER)

extract_categories()
   # Construct URL


#def retrieve_by_category():
    # Within "DOWNLOAD BOOKS" where there is a table by DATE, CATEGORY, TITLE, LINK to PDF.

    # Download "Last 180 Days.csv"
    # https://www.survivorlibrary.com/index.php/files-added-in-last-180-days

