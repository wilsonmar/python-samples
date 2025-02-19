#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

"""scrape-schools.py at https://github.com/wilsonmar/python-samples/blob/main/scrape-schools.py

git commit -m "v004 + all states :scrape-schools.md"

From https://www.perplexity.ai/search/python-code-to-scrape-this-url-vmdUv5PQS2asEYRmS1DjXw#0

1. In Terminal: INSTEAD OF: conda install -c conda-forge ...
    python3 -m venv venv
    source venv/bin/activate

   pip install --upgrade pip
   python3 -m pip install bs4 BeautifulSoup4
   chmod +x ./scrape-schools.py && ./scrape-schools.py    
Alternately:
    Like crawl.ai
"""

import requests
from bs4 import BeautifulSoup   # not BeautifulSoup4 which is the module name with version.
import sqlite3


PRINT_US_STATES = False
PRINT_EACH_STATE = True
SCRAPE_DISTRICTS = True
PRINT_EACH_DISTRICT = True
PRINT_DISTRICT_SUMMARY = True
PRINT_SUMMARY = True
STATES_SCRAPE_LIMIT = 3  # 0 = no limit
DISTRICTS_SCRAPE_LIMIT = 3  # 0 = no limit
STATES_DB_FILE_PATH = "/Users/johndoe/github-wilsonmar/python-samples/schools.db"
districts_initiated = 0

#### Parameters:

# From https://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/
us_states_dict = {
    'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa',
    'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland',
    'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri',
    'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina', 'ND': 'North Dakota',
    'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VA': 'Virginia', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin',
    'WV': 'West Virginia', 'WY': 'Wyoming'
}
# Does not include US Terratories! (Guam, Puerto Rico, Virgin Islands, Saipan, Marianas, 14 in all)
# Convert spaces to underscores in dictionary object: us_states_dict = us_states_dict.replace(" ", "_"
us_states_dict = {key: value.replace(" ", "_") for key, value in us_states_dict.items()}

# WARNING: Not all states are in the same time zone. Specific counties can have a differen timezone.
# From pytz timezones (you can get a look at them typing pytz.all_timezones):
state2timezone = { 'AK': 'US/Alaska', 'AL': 'US/Central', 'AR': 'US/Central', 'AS': 'US/Samoa', 'AZ': 'US/Mountain', 'CA': 'US/Pacific', 'CO': 'US/Mountain', 'CT': 'US/Eastern', 'DC': 'US/Eastern', 'DE': 'US/Eastern', 'FL': 'US/Eastern', 'GA': 'US/Eastern', 'GU': 'Pacific/Guam', 'HI': 'US/Hawaii', 'IA': 'US/Central', 'ID': 'US/Mountain', 'IL': 'US/Central', 'IN': 'US/Eastern', 'KS': 'US/Central', 'KY': 'US/Eastern', 'LA': 'US/Central', 'MA': 'US/Eastern', 'MD': 'US/Eastern', 'ME': 'US/Eastern', 'MI': 'US/Eastern', 'MN': 'US/Central', 'MO': 'US/Central', 'MP': 'Pacific/Guam', 'MS': 'US/Central', 'MT': 'US/Mountain', 'NC': 'US/Eastern', 'ND': 'US/Central', 'NE': 'US/Central', 'NH': 'US/Eastern', 'NJ': 'US/Eastern', 'NM': 'US/Mountain', 'NV': 'US/Pacific', 'NY': 'US/Eastern', 'OH': 'US/Eastern', 'OK': 'US/Central', 'OR': 'US/Pacific', 'PA': 'US/Eastern', 'PR': 'America/Puerto_Rico', 'RI': 'US/Eastern', 'SC': 'US/Eastern', 'SD': 'US/Central', 'TN': 'US/Central', 'TX': 'US/Central', 'UT': 'US/Mountain', 'VA': 'US/Eastern', 'VI': 'America/Virgin', 'VT': 'US/Eastern', 'WA': 'US/Pacific', 'WI': 'US/Central', 'WV': 'US/Eastern', 'WY': 'US/Mountain', '' : 'US/Pacific', '--': 'US/Pacific' }


def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS school_db (
            state_abbr TEXT,
            district_url TEXT,
            district_name TEXT,
            city TEXT,
            county_name TEXT
        )
    ''')


def insert_data(cursor, state_abbr, district_url, district_name, city, county_name):
    cursor.execute('''
        INSERT INTO school_db (state_abbr, district_url, district_name, city, county_name)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (state_abbr, district_url, district_name, city, county_name))


# TODO: Specify filepath of .db file:
# TODO: Put all states into a single .db file:
def scrape_and_store(url, db_name, DISTRICTS_SCRAPE_LIMIT) -> int:
    """
    Scrape school district data from the URL and store it in a SQLite database.

    Args:
        url (str): The URL to scrape.
        db_name (str): The name of the SQLite database file.
    """
    districts_scraped_this_func = 0
    # TODO: Put fetch of URL in separate function:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {url} {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the table
    table = soup.find('table')
    if not table:
        print("Table not found on the page.")
        return None

    # Extract data from the table
    rows = table.find_all('tr')

    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print(f"scrape_and_store() Error: {e}")
        return None
    
    # TODO: Create table one time for all states:
    create_table(cursor)

    # Iterate over rows and insert data:
    # Such as https://www.greatschools.org/schools/districts/Montana/MT/"
    for row in rows[1:]:  # [1:] to Skip header row
        if DISTRICTS_SCRAPE_LIMIT > 0:
            if districts_scraped_this_func + 1 > DISTRICTS_SCRAPE_LIMIT:
               break  # out of loop
        cols = row.find_all('td')
        if len(cols) == 5:
            # FIXME: Define position to extract state_abbr & district_url
            state_abbr = cols[0].text.strip()
            district_url = cols[0].href.strip()
            district_name = cols[0].text.strip()
            city = cols[1].text.strip()
            county_name = cols[2].text.strip()
            insert_data(cursor, state_abbr, district_url, district_name, city, county_name)
            districts_scraped_this_func += 1
            if PRINT_EACH_DISTRICT:
                print(f"district \"{district_name}\" scraped.")

    try:
        # Commit changes and close connection
        conn.commit()
        conn.close()
        if PRINT_DISTRICT_SUMMARY:
            print(f"{districts_scraped_this_func} districts scraped.")
        return districts_scraped_this_func
    except sqlite3.Error as e:
        print(f"scrape_and_store() Error: {e}")
        return None


def main():
    # TODO: Test Run this program different parameters by loading different env files.
    """ Loop to generate and process artpieces.
    """
    # After set_hard_coded_defaults()
    # TODO: load_env_file("???")  # read_env_file(ENV_FILE_PATH)
    if PRINT_US_STATES:
        print("STATES_DB_FILE_PATH = ",STATES_DB_FILE_PATH)
        print("us_states_dict=",us_states_dict)

    # global states_list rather than get_states_list()
    # Loop Through States:
    states_initiated = 0
    districts_scraped = 0
    for st_abbreviation, st_name in us_states_dict.items():
        if STATES_SCRAPE_LIMIT > 0:
            if states_initiated + 1 > STATES_SCRAPE_LIMIT:
               break  # out of loop

        # URL to scrape
        url = f"https://www.greatschools.org/schools/districts/{st_name}/{st_abbreviation}/"
        if SCRAPE_DISTRICTS:
            # Run the scraper: count: districts_initiated += 1
            districts_scraped_by_func = scrape_and_store(url, STATES_DB_FILE_PATH,DISTRICTS_SCRAPE_LIMIT)
            districts_scraped = districts_scraped + districts_scraped_by_func
            # TODO: Add districts_scraped_by_func count to us_states_dict
            states_initiated += 1
            if PRINT_EACH_STATE:
                print(f"{'{:02d}'.format(states_initiated)} of {'{:02d}'.format(STATES_SCRAPE_LIMIT)}. {st_abbreviation}: {st_name}")

    if PRINT_SUMMARY:
        print(f"SUMMARY: states={states_initiated} districts={districts_initiated}")

    # END loop.

if __name__ == "__main__":
    # This is top-level code, not imported from a module.
    # See https://www.youtube.com/watch?v=NB5LGzmSiCs
    main()


"""
Create analytics for file 'school.db' created above
W I should first examine the structure of the SQLite database to understand what tables and data are available. I'll use the SQLite command line tool to explore the database.
Allow Agent Mode to automatically execute commands identified as read-only by the model Manage AI Autonomy permissions

sqlite3 school.db ".schema"
CREATE TABLE school_db (
            district_name TEXT,
            city TEXT,
            county_name TEXT
        );
        
Now that I can see the schema, I should look at the actual data in the table to understand what kind of analytics we can create. Let's see a sample of the data first.

sqlite3 school.db "SELECT * FROM school_db LIMIT 5;"
Absarokee Elementary School District|Absarokee|Stillwater County
Absarokee High School|Absarokee|Stillwater County
Alberton K-12 Schools|Alberton|Mineral County
Alder Elementary School District|Alder|Madison County
Alzada Elementary School District|Alzada|Carter County

Now I can see the data structure clearly. Let's create some meaningful analytics queries:
1. Count of schools by county
2. Count of schools by city
3. Districts that have both Elementary and High schools

I'll create these analytics using SQLite queries and format them for better readability.

echo "=== Schools per County ===" && \
sqlite3 school_db.db "SELECT county_name, COUNT(*) as school_count FROM school_db GROUP BY county_name ORDER BY school_count DESC;" && \
echo -e "\n=== Schools per City ===" && \
sqlite3 school_db.db "SELECT city, COUNT(*) as school_count FROM school_db GROUP BY city ORDER BY school_count DESC LIMIT 10;" && \
echo -e "\n=== Cities with both Elementary and High Schools ===" && \
sqlite3 school_db.db "SELECT city, GROUP_CONCAT(district_name) as schools FROM school_db WHERE district_name LIKE '%Elementary%' AND city IN (SELECT city FROM school_db WHERE district_name LIKE '%High School%') GROUP BY city LIMIT 10;"
=== Schools per County ===
Flathead County|23
Gallatin County|21
Yellowstone County|19
Missoula County|14
Fergus County|14
Lake County|13
Cascade County|13
Stillwater County|12
Roosevelt County|12
Teton County|11
Hill County|11
Blaine County|11
Richland County|10
Lewis and Clark County|10
Rosebud County|9
Park County|9
Lincoln County|9
Jefferson County|9
Carbon County|9
Big Horn County|9
Beaverhead County|9
Valley County|8
Sanders County|8
Ravalli County|8
Pondera County|8
Powell County|7
Garfield County|7
Dawson County|7
Chouteau County|7
Madison County|6
Glacier County|6
Custer County|6
Sweet Grass County|5
Silver Bow County|5
Phillips County|5
Toole County|4
Powder River County|4
Musselshell County|4
Granite County|4
Carter County|4
Wheatland County|3
Sheridan County|3
Mineral County|3
McCone County|3
Liberty County|3
Judith Basin County|3
Golden Valley County|2
Fallon County|2
Deer Lodge County|2
Wibaux County|1
Wheatland|1
Treasure County|1
Sanders|1
Prairie County|1
Petroleum County|1
Park|1
Meagher County|1
Lincoln|1
Garfield|1
Daniels County|1
Daniels|1
Custer|1
Broadwater County|1

=== Schools per City ===
Billings|10
Kalispell|9
Bozeman|7
Miles City|6
Jordan|6
Troy|5
Missoula|5
Lewistown|5
Butte|5
Sidney|4

=== Cities with both Elementary and High Schools ===
Absarokee|Absarokee Elementary School District
Anaconda|Anaconda Elementary School District
Arlee|Arlee Elementary School District
Augusta|Augusta Elementary School District
Belgrade|Belgrade Elementary School District,Pass Creek Elementary School District,Springhill Elementary School District
Belt|Belt Elementary School District
Big Timber|Big Timber Elementary School District,Mcleod Elementary School District
Bigfork|Bigfork Elementary School District,Swan River Elementary School District
Billings|Billings Elementary School District,Blue Creek Elementary School District,Canyon Creek Elementary School District,Elder Grove Elementary School District,Elysian Elementary School District,Independent Elementary School District,Morin Elementary School District,Pioneer Elementary School District,Yellowstone Academy Elementary
Boulder|Boulder Elementary School District

2. City Distribution:
   - Billings (largest city in Montana) leads with 10 schools
   - Kalispell follows with 9 schools
   - Bozeman has 7 schools
   - Miles City and Jordan each have 6 schools
   - The top 10 cities show a good distribution of schools across Montana's major population centers

3. Elementary and High School Coverage:
   - Many cities have both elementary and high schools, showing good educational coverage
   - Some cities like Billings have multiple elementary school districts (9 different elementary districts)
   - Several rural areas maintain both elementary and high school facilities
   - Some elementary districts serve multiple communities within the same area

This analysis shows that Montana's school system is well-distributed across the state, with larger population centers having more schools, while maintaining educational facilities even in rural areas. The presence of both elementary and high schools in many cities indicates good K-12 coverage across the state.

"""
