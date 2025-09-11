#!/usr/bin/env python3

"""wttr-weather.py here.

https://github.com/wilsonmar/python-samples/blob/main/weather/wttr-weather.py

This code crafts a URL to wattr.in to respond with a 3-day weather forecast text in CLI console.

See full-screen output layout at:
https://www.geeksforgeeks.org/python/how-to-extract-weather-data-from-google-in-python/

To run this, in Terminal CLI:
    uv pip install requests
    chmod +x wttr-weather.py
    ruff check wttr-weather.py
    uv run wttr-weather.py -v -vv
"""
__last_change__ = "25-09-09 v005 + timeout & escape quote() :wttr-weather.py"

# Importing the requests module
import requests
from urllib.parse import quote

# Globals TODO: From params:
my_city_name = "Joliet,MT"

# Percent escape spaces to %20, commas to %2C, and special chars for use in a URL:
citydata_formatted = quote(my_city_name)

# Passing the city name to the URL to get weather data
# NOTE: format() to HTTP. '?u' for US Fareinheit. 
# what's %7B%7D
# FIXME: https://bandit.readthedocs.io/en/1.8.6/plugins/b113_request_without_timeout.html
url = 'https://wttr.in/'+citydata_formatted+'?u'
print("wttr-weather.py of URL:", url)
res = requests.get(url)

# Printing the schematic weather details of the city
print(res.text)

