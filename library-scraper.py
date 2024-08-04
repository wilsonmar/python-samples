#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Please reference .pylintrc for PEP8 formatting according to https://peps.python.org/pep-0008/
# conda install black  # to reformat
# pylint: disable=line-too-long trailing-newlines
"""
This is library-scraper.py at
https://github.com/wilsonmar/python-samples/blob/main/library-scraper.py
to download the Survivor Library: How to surveve when the Technology Doesn't
(It's not a Library about survival. It's a library for surviors.)

CURRENT STATUS: NOT WORKING
gas "v001 add :library-scraper.py"

Based on https://github.com/alw98/SurvivorLibraryCrawler/blob/master/LibraryCrawler.py
"""

from urllib.request import urlopen
import re
import os
import html

# pip3 install bs4
from bs4 import BeautifulSoup
import requests

# if Windows:
  # saveloc = "C:\\Users\\alw98\\Downloads\\Programming Stuff\\survivorlibrary"
# if Linux or MacOS:
saveloc = "survivorlibrary"

# PHASE A: Build a database of CATEGORIES and a link to each from the MAIN INDEX table at
   # https://www.survivorlibrary.com/index.php/main-library-index/

# PHASE B: Build a database of files and download those files locally.
   # Accounting.csv does not contain URLs so we must scrape the HTML such as:
   # Look for words such as "Accounting" between <a href="/index.php/ and ">
   # https://www.survivorlibrary.com/index.php/Accounting

# PHASE C: Make downloaded files available offline, such as:
   # https://www.survivorlibrary.com/library/20th_century_bookkeeping_and_accounting_1922.pdf

def establish_database():
    print(">>> establish_database")

def extract_categories():

    url = "https://www.survivorlibrary.com/index.php/main-library-index/"
    print(">>> Starting crawler...")

    website = urlopen(url)
    print(">>> opened website " + url)

    html = website.read().decode('utf-8')
    print(">>> read website...")

    # Read the content of the file saved:
    # TODO: Instead read real-time using Beautiful Soup:
    with open('surivor.html', 'r') as file:
        content = file.read()

    # Define the pattern to extract text:
    # TODO: Instead use Beautiful Soup:
    pattern = r'/index.php/(.*?)">'

    # Find all matches
    matches = re.findall(pattern, content, re.DOTALL)

    # Print the results:
    category_found_count = 0
    for match in matches:
        category_found = match.strip()
        category_found_count += 1
        print(category_found)

        save_category(category_found)

        extract_category(category_found)

    # Add an interesting rating field to each field in the database.

    # Summarize:
    print(" ")
    print(">>> category_found_count=",category_found_count)


# See if the Category is already in the database.
def save_category(category_found):
    print(">>> category_found to lookup=",category_found)


def extract_category(category_found):
    # Construct URL such as https://www.survivorlibrary.com/index.php/Accounting
    url="https://www.survivorlibrary.com/index.php/"+category_found
    print("url=",url)

    return

    # Loop through table to extract each line:
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')  # Adjust this if you need to target a specific table
    table_data = []

    # Find all table rows:
    rows = table.find_all('tr')

    # Iterate through rows, skipping the header:
    for row in rows[1:]:
        cells = row.find_all(['td', 'th'])
        row_data = [cell.get_text(strip=True) for cell in cells]
        table_data.append(row_data)

    # See if the Category is already in the database.

    # See if the file is already in the database.

    #    <tr id="table_7_row_0" data-row-index="0">
    #       <td style="">2013-08-08</td>
    #        <td style="">20Th Century Bookkeeping And Accounting 1922 </td>
    #        <td style="">
    #            <a href="/library/20th_century_bookkeeping_and_accounting_1922.pdf">PDF</a>
    #            23 mb
    #        </td>
    #    </tr>

    # Extract the year of publication at the end of each TITLE.
    # Extract the file size (such as "23 mb") for the LINK field.
    # Extract file url around "PDF"
    # Download the url.

    # Save the fields from each row to a database or CSV file.
    # Add an interesting rating field to the database.


#    return table_data

    # Example usage
    url = 'https://example.com/page-with-table'  # Replace with your URL
    response = requests.get(url)
    html_content = response.text

    extracted_data = extract_table_data(html_content)

    # Print the extracted data
    for row in extracted_data:
        print(row)

#### MAIN:

establish_database()

extract_categories()
   # Construct URL

exit()

#def retrieve_by_category():
    # Within "DOWNLOAD BOOKS" where there is a table by DATE, CATEGORY, TITLE, LINK to PDF.


    # Download "Last 180 Days.csv"
    # https://www.survivorlibrary.com/index.php/files-added-in-last-180-days

"""
for link in links:
	categorylink = "http://www.survivorlibrary.com" + link[0]
	category = urlopen(categorylink)
	print(">>> opened categorylink " + categorylink)
	categoryhtml = category.read().decode('utf-8')
	print(">>> read categorylink...")
	pdfs = re.findall('"((/library/)(.*?)(.pdf))', categoryhtml)
	print(">>> got pdf links")
	print(">>> make a dir for the pdfs")
	path = saveloc + "\\" + link[2]
	if not os.path.isdir(path):
		os.makedirs(path)
	print(">>> made dir")
	for pdf in pdfs:
		pdflink = "http://www.survivorlibrary.com" + pdf[0]
		pdfname = pdf[2] + pdf[3]
		fullpath = saveloc + "\\" + link[2] + "\\" + pdfname
		if not os.path.isfile(fullpath):
			print(">>> downloading " + pdfname)
			stream = requests.get(pdflink, stream = True)
			print(">>> got stream...")
			with open(fullpath, 'wb') as f:
				print(">>> opened file")
				f.write(stream.content)
			print(pdfname + " saved at " + saveloc + "\\" + pdfname)
		else:
			print(fullpath + " is already downloaded")

"""