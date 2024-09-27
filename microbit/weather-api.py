"""
# weather-api.py
# This is run on micro:bit v2 (not v1).
# Described at https://gumroad.github.io/microbit
# From https://www.perplexity.ai/search/write-in-python-microbit-v2-ca-4dlBzZsCQtaSsD3SETObJg
"""
import urequests
import network
from microbit import *

## Wi-Fi Connection
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        display.scroll("Connecting...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    display.scroll("Connected!")
    return wlan

## Weather API Call
def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = urequests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

## Main Program
ssid = "Your_WiFi_SSID"
password = "Your_WiFi_Password"
api_key = "Your_OpenWeatherMap_API_Key"
city = "London"

# Connect to Wi-Fi
wlan = connect_wifi(ssid, password)

# Get weather data
weather_data = get_weather(api_key, city)

if weather_data:
    temp = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']

    display.scroll(f"Temp: {temp}C")
    display.scroll(description)
else:
    display.scroll("Error")

# Disconnect Wi-Fi
wlan.disconnect()