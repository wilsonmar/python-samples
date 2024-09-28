#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gas "v006 VERBOSE False :openweather.py"
by Wilson Mar
LICENSE: MIT
Based on https://www.instructables.com/Get-Weather-Data-Using-Python-and-Openweather-API/
Create account at https://home.openweathermap.org/users/sign_up
⛈ subscribe to the "One Call API 3.0" with a credit card.
and get the API key. 
https://blog.apilayer.com/what-is-the-best-weather-api-for-python/
"""
from datetime import datetime
import urllib.parse
import requests
import math

def get_frost_point_c(t_air_c, dew_point_c):
    """Compute the frost point in degrees Celsius
    :param t_air_c: current ambient temperature in degrees Celsius
    :type t_air_c: float
    :param dew_point_c: current dew point in degrees Celsius
    :type dew_point_c: float
    :return: the frost point in degrees Celsius
    :rtype: float
    """
    dew_point_k = 273.15 + dew_point_c
    t_air_k = 273.15 + t_air_c
    frost_point_k = dew_point_k - t_air_k + 2671.02 / ((2954.61 / t_air_k) + 2.193665 * math.log(t_air_k) - 13.3448)
    return frost_point_k - 273.15

# Online: https://www.omnicalculator.com/physics/dew-point
# from https://en.wikipedia.org/wiki/Dew_point#Calculating_the_dew_point
def get_dew_point_c(t_air_c, rel_humidity):
    """Compute the dew point in degrees Celsius
    :param t_air_c: current ambient temperature in degrees Celsius
    :type t_air_c: float
    :param rel_humidity: relative humidity in %
    :type rel_humidity: float
    :return: the dew point in degrees Celsius
    :rtype: float
    """
    A = 17.27
    B = 237.7
    alpha = ((A * t_air_c) / (B + t_air_c)) + math.log(rel_humidity/100.0)
    return (B * alpha) / (A - alpha)

def calculate_sea_level_pressure(station_pressure, altitude, temperature):
    """
    Calculate sea level pressure from station pressure.
    
    :param station_pressure: Measured pressure at the station (hPa)
    :param altitude: Altitude of the station (meters)
    :param temperature: Temperature at the station (Celsius)
    :return: Calculated sea level pressure (hPa)
    """
    # Constants
    GRAVITY = 9.80665  # m/s^2
    R = 287.05  # Gas constant for dry air, J/(kg*K)

    # Convert temperature to Kelvin
    T = temperature + 273.15

    # Calculate sea level pressure
    sea_level_pressure = station_pressure * math.exp((GRAVITY * altitude) / (R * T))

    return round(sea_level_pressure, 2)

# Function to adjust pressure for altitude (reverse calculation)
def adjust_pressure_for_altitude(sea_level_pressure, altitude, temperature):
    """
    Adjust sea level pressure for a specific altitude.
    
    :param sea_level_pressure: Sea level pressure (hPa)
    :param altitude: Altitude to adjust for (meters)
    :param temperature: Temperature at the altitude (Celsius)
    :return: Adjusted pressure for the given altitude (hPa)
    """
    # Constants
    GRAVITY = 9.80665  # m/s^2
    R = 287.05  # Gas constant for dry air, J/(kg*K)

    # Convert temperature to Kelvin
    T = temperature + 273.15

    # Calculate adjusted pressure
    adjusted_pressure = sea_level_pressure * math.exp(-(GRAVITY * altitude) / (R * T))

    return round(adjusted_pressure, 2)

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


#### TODO: Obtain input values from arguments
VERBOSE = False  # True or False
USE_IMPERIAL_UNITS = True  # True or False
city_input = "Billings" # instead of input("Enter City:")
city_encoded = urllib.parse.quote(city_input)
apikey="10c5aa3e8279618cfe92220849af5352" # ??? from https://openweathermap.org/api"

#url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=" + apikey + "&units=metric.format(city)"
url = "http://api.openweathermap.org/data/2.5/weather?q="+city_encoded+"&appid=" + apikey

if VERBOSE:
   print(">>> url=",url)
   # data= {'coord': {'lon': 23.886, 'lat': 48.1792}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 296.48, 'feels_like': 296.28, 'temp_min': 296.48, 'temp_max': 296.48, 'pressure': 1012, 'humidity': 54, 'sea_level': 1012, 'grnd_level': 938}, 'visibility': 10000, 'wind': {'speed': 2.43, 'deg': 235, 'gust': 6.41}, 'clouds': {'all': 75}, 'dt': 1727441174, 'sys': {'country': 'UA', 'sunrise': 1727410696, 'sunset': 1727453543}, 'timezone': 10800, 'id': 709516, 'name': 'Dubove', 'cod': 200}
try:
    res = requests.get(url)
    data = res.json()
except Exception as e:
    "data= {'cod': '404', 'message': 'city not found'}"
    print(f">>> Error using city: {city_input} in {e}")
    exit()

current_datetime = datetime.now()

if VERBOSE:
    print(">>> data=",data)


# Extract individual elements:
lon = data['coord']['lon']
lat = data['coord']['lat']
try:
    station_name = data['sys']['name']
except Exception as e:
    print(f">>> Error getting: name in {e}")
    station_name = ""
    # exit()
else:
    station_name = ""

description = data['weather'][0]['description']
icon_code = data['weather'][0]['icon']  # '01n'
# 'sys': {'country': 'UA', 'sunrise': 1727497180, 'sunrise': 1727539818},
country = data['sys']['country']
sunrise_epoch = data['sys']['sunrise']
sunset_epoch = data['sys']['sunset']
wind_kph = data['wind']['speed']
wind_deg = data['wind']['deg']
wind_gust_kph = 0
try:
    wind_gust_kph = data['wind']['gust']
except:
    wind_gust_kph = 0
else:
    wind_gust_kph = 0
feels_like = data['main']['feels_like']
temp_k = data['main']['temp']
humidity = data['main']['humidity']
sea_level_m = data['main']['sea_level']
grnd_level_m = data['main']['grnd_level']
pressure = data['main']['pressure']


#### Icon for GUI (not CLI):
# icon_code =
   # "01d" or "01n": Clear sky (day or night)
   # "02d" or "02n": Few clouds
   # "03d" or "03n": Scattered clouds
   # "04d" or "04n": Broken clouds
   # "09d" or "09n": Shower rain
   # "10d" or "10n": Rain
   # "11d" or "11n": Thunderstorm
   # "13d" or "13n": Snow
   # "50d" or "50n": Mist
# const iconCode = weatherData.weather[0].icon;
# const iconUrl = `https://openweathermap.org/img/wn/${icon_Code}@2x.png`;
# document.getElementById('weather-icon').src = iconUrl;


#### Calculations:
STRFTIME_FORMAT="%I:%M %p (%H:%M:%S) %Y-%m-%d"
formatted_datetime=current_datetime.strftime(STRFTIME_FORMAT)
sunrise_date_time = datetime.fromtimestamp(sunrise_epoch)
sunrise_formatted = sunrise_date_time.strftime(STRFTIME_FORMAT)
sunset_date_time = datetime.fromtimestamp(sunset_epoch)
sunset_formatted = sunset_date_time.strftime(STRFTIME_FORMAT)

temp_c = float(temp_k) - 273.15
# Dew point provides a more consistent and
# easily interpretable measure of how humid it actually feels outside.
dew_point_c = get_dew_point_c(temp_c, humidity)
dew_point_f = (dew_point_c * 9/5) + 32
# Dew Point is the temperature at which air becomes
# 100% saturated with water vapor (at 60F=muggy, 70F=humid)
# causing condensation to occur.
if dew_point_f > 60:
    dew_comfort = "muggy"
elif dew_point_f > 70:
    dew_comfort = "humid"
else:
    dew_comfort = "mild"

# TODO: More categories of comfort, localized?
if pressure > 60:
    pressure_desc = "falling"
elif pressure > 70:
    pressure_desc = "rising"
else:
    pressure_desc = "steady"


#### Print:

print(f"openweather.org at {formatted_datetime} reports")  # cloud, rain
print(f"          Sunrise: {sunrise_formatted}")
print(f"          Sunset:  {sunset_formatted}")
print(f"{description} at {city_input}",end="")
print(f" country={country}",end="")
if station_name == "":
    print("")
else:
    print(f" ({station_name})")

if USE_IMPERIAL_UNITS:
    sea_level_f = sea_level_m * 3.28084
    print(f"    Elevation: {sea_level_f:.2f} feet",end="")
    grnd_level_f = grnd_level_m
    print(f" (Ground_level: {grnd_level_f} feet)")
else:
    print(f"    Elevation: {sea_level_m:.2f} meters",end="")
    print(f" (Ground_level: {grnd_level_m} meters)")

print(f"    Latitude:  {lat} from the Equator &")
print(f"    Longitude: {lon} from the Meridian at Greenwich, UK")
# Not print if same: print('Feels like: ',feels_like)

if USE_IMPERIAL_UNITS:
   temp_f = (temp_c * 9/5) + 32
   print(f"{temp_f:.2f}°F",end="")
   print(f" with {dew_comfort} Humidity: {humidity}%",end="")
   print(f" for Dew Point: {dew_point_f:.2f}°F")
else:
   print(f"At a {dew_comfort} {temp_c:.2f}°C",end="")
   print(f" with Humidity: {humidity}%",end="")
   print(f" for Dew Point: {dew_point_c:.2f}°C")

# Convert wind direction to names (such as NWW):
wind_dir = compass_text_from_degrees(wind_deg)
if USE_IMPERIAL_UNITS:
    wind_mph=wind_kph * 0.621371
    print(f"Wind: {wind_mph:.2f} mph from {wind_dir} ({wind_deg}°)",end="")
else:
    print(f"Wind: {wind_kph:.2f} kph from {wind_dir} ({wind_deg}°)",end="")
# See illustration at https://res.cloudinary.com/dcajqrroq/image/upload/v1727494071/compass-800x800_hvwmtu.webp
if wind_gust_kph == 0:
    print("")
else:
    if USE_IMPERIAL_UNITS:
        wind_gust_mph = wind_gust_kph * 0.621371
        print(f" with gusts: {wind_gust_mph:.2f} mph")
    else:
        print(f" with gusts: {wind_gust_kph:.2f} kph")

# The average sea-level pressure is 1013.25 mb/hPA (Hectopascal).
# One millibar is equivalent to 100 Pa (Pascals).
# The SI Atmosphere (atm) average air pressure at sea level
# of 101,325 pascals (Pa) or 1013.25 hPa (hectopascals).
# See https://blog.mensor.com/blog/adjusting-barometric-pressure-readings-for-aviation-and-meteorology
# See https://cumulus.hosiene.co.uk/viewtopic.php?t=8286
# Example usage of the adjustment functions:
sea_level_pressure = calculate_sea_level_pressure( \
    pressure, sea_level_m, temp_c)
pressure_diff = sea_level_pressure - pressure

altitude_to_adjust = sea_level_m  # meters
adjusted_pressure = adjust_pressure_for_altitude \
    (sea_level_pressure, altitude_to_adjust, temp_c)

# Format & display each element:

print(f"Pressure:",end="")
#print(f" {pressure_desc} at")
print(f" {pressure} hPa (Hectopascals, aka millibars)")

#print(f"is {pressure_diff:.2f} \
#      hPa from adjusted average \
#      {sea_level_pressure:.2f} hPa")
print(f"      vs. {sea_level_pressure} hPa adjusted to sea level.")
# print(f"{hectopascals:.2f} hPa above sea level average of 1013.25 hPA")
# What is normal for your location's altitude
# Python code: https://www.perplexity.ai/search/how-adjust-normal-hectopascals-SuInNLlARxadL9GbY.NmBA
print(f"      vs. 1013.25 hPa unadjusted normally at sea level.")
# print(f"      vs. {adjusted_pressure:.2f} hPa normally for local elevation.")

# Normal pressure is between 1009.144 hPa and 1022.689 hPa.
# Above 1022.689 hPa at sea level for clear skies and calm weather.
# rarely exceeds 1050 hPa at sea level.
# Pressure changes with altitude, decreasing by about 12 hPa for every 100 meters of elevation.
# pressure below 1010 hPa is often considered Low, associated with unsettled weather conditions.
