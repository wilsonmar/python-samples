#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openweather.py
by Wilson Mar
LICENSE: MIT
Based on https://www.instructables.com/Get-Weather-Data-Using-Python-and-Openweather-API/
Create account at https://home.openweathermap.org/users/sign_up
⛈ subscribe to the "One Call API 3.0" with a credit card.
and get the API key. 
https://blog.apilayer.com/what-is-the-best-weather-api-for-python/
"""
import requests

# TODO: Obtain input values from arguments
VERBOSE = False #True
city = "Joliet" # instead of input("Enter City:")
apikey="f18fbdf35e9a32c34a26c1d1719f12e8" # ??? from https://openweathermap.org/api"

#url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=" + apikey + "&units=metric.format(city)"
url = "http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=" + apikey
if VERBOSE:
   print(">>> url=",url)
res = requests.get(url)
data = res.json()

if VERBOSE:
   print(">>> data=",data)

humidity = data['main']['humidity']
pressure = data['main']['pressure']
wind = data['wind']['speed']
description = data['weather'][0]['description']
temp = data['main']['temp']

print('Temperature:',temp,'°C')
print('Wind:',wind)
print('Pressure: ',pressure)
print('Humidity: ',humidity)
print('Description:',description)