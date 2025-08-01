#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""openweather.py at https://github.com/wilsonmar/python-samples/blob/main/openweather.py

git commit -m "v027 + apisec fix :openweather.py"

STATUS: working

by Wilson Mar, LICENSE: MIT
This program formats CLI output after parsing JSON returned from
REST API calls to openweathermp.org. Response includes
sunrise and sunset times.
This creates fuzzy value #tags to represent range value about
cloudiness, humidity, dew point comfort, pressure, wind direction, etc..

bathymetry maps determine depth from sea level at the latitude and longitude location.

Sample CLI putput running this program:
./openweather.py --zip london --verbose
openweather.org
id: 2646003    at: 07:01 AM (07:01:38) 2025-03-31 TZ: 3600
          Sunrise: 11:37 PM (23:37:41) 2025-03-30 local time
           Sunset: 12:31 PM (12:31:07) 2025-03-31
few clouds at Islington , country=GB "lat=51.5286416&lon=-0.1015987"
     Latitude:  51.5286416° North of the Equator &
     Longitude: -0.1015987° East of the Meridian at Greenwich, UK
comfortable Dew Point of 41.58°F vs. 60.87°F at 49% humidity
     Feels like 58.96°F from Wind: 8.79 mph from S (151°)
     Visibility to 10000 meters
high +15 pressure at 1028 hPa (HectoPascals = 10.28 millibars)
          vs. normal 1013.25 hPa at sea level
                     1024    hPa at ground level
                
Based on https://www.instructables.com/Get-Weather-Data-Using-Python-and-Openweather-API/
Create account at https://home.openweathermap.org/users/sign_up
⛈ subscribe to the "One Call API 3.0" with a credit card.
https://blog.apilayer.com/what-is-the-best-weather-api-for-python/
weatherstack.com/

TODO: Integrate locally collected data (rainfall, sunlight, soil moisture, etc.)
like https://www.ventusky.com/?p=45.45;-109.78;6&l=gust&w=soft
TODO: Store each day's readings to a database for trending on dashboard (such as
https://wilsonmar.github.io/dashboards/#weather-maps)
* Ambient Weather: https://ambientweather.net/dashboard/3e5ec6331a8884e1ac1d5fbd2812ba11/tiles
* Weather Underground: https://www.wunderground.com/dashboard/pws/KNJRIDGE44
* Weather Cloud: https://app.weathercloud.net/d7511690833#current
* PWS Weather: https://www.pwsweather.com/station/pws/KRUSE1
* weather.gov (free)
* sunriseandsunset.io (free)

"""
# STEP 1 = Setup. Before running this program: Installing Required Libraries & Importing Required Libraries

# pip install yubikey-manager

# Built-in modules within the Python interpreter:
from datetime import datetime
from datetime import timedelta, timezone
import argparse
import pathlib
import math
import os

try:
    # Based on: conda install -c conda-forge load_dotenv
    from dotenv import load_dotenv
    # After: brew install miniconda
    # Based on: conda install python-dotenv   # found!
    # conda create -n py313
    # conda activate py313
    # conda install --name py313 requestsa
    import urllib.parse
    import requests
except Exception as e:
    print(f"Python module import failed: {e}")
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    print(f"Please activate your virtual environment:\n  python3 -m venv venv\n  source venv/bin/activate")
    exit(9)


#### TODO: Pull from command arguemnt:
# Constants used within functions:
VERBOSE = False  # True or False
USE_IMPERIAL_UNITS = True  # True or False

use_env_file = True    # -env "python-samples.env"
global ENV_FILE
ENV_FILE="python-samples.env"

# Colors
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
# Styles
BOLD = '\033[1m'
GRAY = '\033[90m'
RESET = '\033[0m'

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

def get_time() -> str:
    """ Generate the current local datetime. """
    now: datetime = datetime.now()
    return f'{now:%I:%M %p (%H:%M:%S) %Y-%m-%d}'

def print_separator():
    """ Put a blank line in CLI output. Used in case the technique changes throughout this code. """
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
            print('***', get_log_datetime(), bcolors.FAIL, "FAIL:", f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.FAIL, "FAIL:", f'{text_in}', bcolors.RESET)

def print_error(text_in):  # when a programming error is evident
    if show_fail:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.ERROR, "ERROR:", f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.ERROR, "ERROR:", f'{text_in}', bcolors.RESET)

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

# See https://wilsonmar.github.io/python-samples/#envFile

def open_env_file(env_file) -> str:
    """Return a Boolean obtained from .env file based on key provided.
    """
    from pathlib import Path
    # See https://wilsonmar.github.io/python-samples#run_env
    global user_home_dir_path
    user_home_dir_path = str(Path.home())
       # example: /users/john_doe

    global_env_path = user_home_dir_path + "/" + env_file  # concatenate path

    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        print(global_env_path+" (global_env_path) not found!")
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


def check_yubikey_serial() -> None:
    """Stop processing unless the Yubikey serioal is found in the .env file.
    """
    my_yubikey_serial = get_str_from_env_file('YUBIKEY_SERIAL')
    #print("my_yubikey_serial="+my_yubikey_serial)
    if not my_yubikey_serial:  # not in env file:
        print_warning(">>> No YUBIKEY_SERIAL specified in .env file!")
        exit(9)
    else:
        # https://developers.yubico.com/yubikey-manager/Scripting.html
        from ykman.device import list_all_devices
        from yubikit.core.smartcard import SmartCardConnection
        from yubikit.piv import PivSession
        # Iterate through all connected Yubikey devices:
        for device, info in list_all_devices():   # using ykman module:
            #print(f" Yubikey inserted={info.serial}")
            # Check if the device serial number is your YubiKey:
            try:
                if my_yubikey_serial == info.serial:
                    print(f">>> YubiKey serial not match with env file! Continuing...")
                else:
                    print(f">>> YubiKey serial is not the one connected. Exiting...")
                #    exit(9)
            except Exception as e:
                print(f">>> Error using city: {city_input} in {e}")
                #exit(9)
            else:
                print(f">>> YubiKey not inserted!")
    return


def find_yubikey_by_serial(target_serial):
    """
    Check if a connected YubiKey matches the desired serial number.

    Args:
        target_serial (int): The serial number to match.

    Returns:
        bool: True if the YubiKey with the target serial is found, False otherwise.
    """
    for device, info in list_all_devices():
        if info.serial == target_serial:
            print(f"YubiKey found with serial number: {info.serial}")
            return True
    print("No YubiKey with the specified serial number was found.")
    return False


def other():


    if info.version >= (5, 0, 0):  # The info object provides details about the YubiKey
        print(f"version={info.version} serial={info.serial}")
    else:
        print("ha")

    if info.version >= (5, 0, 0):  # The info object provides details about the YubiKey
        print(f"version={info.version} serial={info.serial}")
        if my_yubikey_serial == info.serial:
            print_info(f">>> YubiKey serial not match with env file! Continuing...")
        else:
            print_fatal(f">>> YubiKey serial is not the one connected. Exiting...")
            exit(9)

def read_env_file():
    """Read .env file containing variables and values.
    See https://wilsonmar.github.io/python-samples/#envLoad
    """
    # See https://stackoverflow.com/questions/40216311/reading-in-environment-variables-from-an-environment-file

    # Joliet, MT at "45° 29' 5.028'' N-108° 58' 20.244'' W

    global my_latitude
    my_latitude = get_str_from_env_file('MY_LATITUDE')
    if my_latitude == None:
        my_latitude = "34.123"
        print_warning(">>> my_latitude="+my_latitude+" from default!")

    global my_longitude
    my_longitude = get_str_from_env_file('MY_LONGITUDE')
    if my_longitude == None:
        my_longitude = "104.322"
        print_warning(">>> my_longitude="+my_longitude+" from default!")

    global my_zip_code
    my_zip_code = get_str_from_env_file('MY_ZIP_CODE')
    if my_zip_code == None:
        my_zip_code = "59041"
        print_warning(">>> my_zip_code="+my_zip_code+" from default!")

    # More precise Longitude & Latitude in .env overrides zip code:
    global apispec
    apispec="lat=" + my_latitude +"&lon=" + my_longitude

    return

def get_str_from_env_file(key_in) -> str:
    """Return a value of string data type from OS environment or .env file
    (using pip python-dotenv)
    """
    env_var = os.environ.get(key_in)
    if not env_var:  # yes, defined=True, use it:
        print_warning(key_in + " not found in OS nor .env file: " + ENV_FILE)
        return None
    else:
        # PROTIP: Display only first 15 characters of a potentially secret long string:
        if len(env_var) > 10:
            print_trace(key_in + "=\"" + str(env_var[:10]) +" (remainder removed)")
        else:
            print_trace(key_in + "=\"" + str(env_var) + "\" from .env")
        return str(env_var)



def get_coordinates(zip_code, api_key):
    # Construct the API URL
    url = f'https://api.distancematrix.ai/maps/api/geocode/json?address={zip_code}&key={api_key}'

    try:
        # import requests
        response = requests.get(url)
        data = response.json()    # Parse JSON response
        #print("data=",data)
        # data={'result': [{'address_components': [{'long_name': 'mountain view', 'short_name': 'mountain view', 'types': ['locality']}, {'long_name': 'ca', 'short_name': 'ca', 'types': ['state']}, {'long_name': 'usa', 'short_name': 'usa', 'types': ['country']}], 'formatted_address': 'Mountain View, CA, USA',
        # 'geometry': {'location': {'lat': 37.418918000000005, 'lng': -122.07220494999999}, 'location_type': 'APPROXIMATE',
        # 'viewport': {'northeast': {'lat': 37.418918000000005, 'lng': -122.07220494999999},
        # 'southwest': {'lat': 37.418918000000005, 'lng': -122.07220494999999}}},
        # 'place_id': '', 'plus_code': {}, 'types': ['locality', 'political']}], 'status': 'OK'}
    except Exception as e:
        print(f">>> get_coordinates of {zip_code} in {e}")
        exit(9)  # TODO: Handle retry?

    if data['status'] == 'OK':
        # Extract latitude and longitude
        latitude = data['result'][0]['geometry']['location']['lat']
        longitude = data['result'][0]['geometry']['location']['lng']
        # print(f">>> get_coordinates of {zip_code} is at lat={latitude} & lng={longitude}")
        return latitude, longitude
    else:
        return None, None


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

def kelvin2celcius(temp_k):
    return float(temp_k) - 273.15

def celcius2fahrenheit(temp_c):
    return (temp_c * 9/5) + 32

def kelvin2fahrenheit(temp_k):
    temp_c = kelvin2celcius(temp_k)
    return celcius2fahrenheit(temp_c)

def meters2feet(meters):
    return meters * 3.28084

def kph2mph(kph):
    return kph * 3.28084


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
        "N",
        "?"]  # 17 index values
    # graphic ![python-cardinal-point-compass-windrose-600x600-Brosen svg](https://user-images.githubusercontent.com/300046/142781379-addfa8f7-9394-4751-9ddd-65e681e4a49c.png)
    # graphic from https://www.wikiwand.com/en/Cardinal_direction
    remainder = degrees % 360  # modulo remainder of 270/360 = 196
    index = int(round(remainder / 22.5, 0) + 1)   # (17 values)
    return compass_sector[index]

def dew_desc_f(dew_point_f):
    # Dew Point is the temperature at which air becomes 100% saturated with water vapor
    # (at a given pressure) causing condensation to occur (at 60F=muggy, 70F=humid)
    # https://www.weather.gov/arx/why_dewpoint_vs_humidity
    if dew_point_f >= 70:
        return RED+"muggy"+RESET
    elif dew_point_f >= 65:
        return RED+"sticky"+RESET
    else:
        return GREEN+"comfortable"+RESET


def pressure_desc(pressure):
    # Above 1022.689 hPa at sea level for clear skies and calm weather.
    # pressure rarely exceeds 1050 hPa at sea level.
    if pressure > 1022.689:
        return RED+"high"+RESET
    elif pressure < 1010:
        # pressure below 1010 hPa is often considered Low, associated with unsettled weather conditions.
        return BLUE+"low"+RESET
    else:
        # Normal pressure is between 1009.144 hPa and 1022.689 hPa:
        return GREEN+"normal"+RESET


def cloud_text(cloud_desc):
    # Fuzzy names
    # https://openweathermap.org/history
    if cloud_desc == "clear sky":
        return BLUE+cloud_desc+RESET
    elif cloud_desc == "few clouds":
        return BLUE+cloud_desc+RESET
    elif cloud_desc == "scattered clouds":
        return BLUE+cloud_desc+RESET
    elif cloud_desc == "mist":
        return BLUE+cloud_desc+RESET
    elif cloud_desc == "broken clouds":
        return BLUE+cloud_desc+RESET

    elif cloud_desc == "shower rain":
        return YELLOW+cloud_desc+RESET
    elif cloud_desc == "rain":
        return YELLOW+cloud_desc+RESET
    elif cloud_desc == "light snow":
        return YELLOW+cloud_desc+RESET

    elif cloud_desc == "thunderstorm":
        return RED+cloud_desc+RESET
    elif cloud_desc == "snow":
        return RED+cloud_desc+RESET
    else:
        cloud_desc == "Unknown"
        return GRAY+cloud_desc+RESET

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

###############

if __name__ == "__main__":

    # PROTIP: Global variable referenced within functions:
    # values obtained from .env file can be overriden in program call arguments:
    show_fail = True       # Always show
    show_error = False      # Always show
    show_warning = False    # -wx  Don't display warning
    show_todo = False       # -td  Display TODO item for developer
    show_info = False       # -qq  Display app's informational status and results for end-users
    show_heading = False    # -q  Don't display step headings before attempting actions
    show_verbose = False    # -v  Display technical program run conditions
    show_trace = False      # -vv Display responses from API calls for debugging code
    show_secrets = False   # Never show

    show_sys_info = False
    show_config = False   # not used?

    global show_dates_in_logs
    show_dates_in_logs = False

    open_env_file(ENV_FILE)
    read_env_file()  # calls print_samples()
    #check_yubikey_serial()

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity")  # on/off flag
    parser.add_argument(
        "-z", "--zip",
        type=str,
        nargs="+",
        help="6-digit US Zip Code"
    )
    args = parser.parse_args()

    if args.verbose:
        VERBOSE = True  # True or False

    if args.zip:
        zip_code = ' '.join(map(str, args.zip))   # convert list from parms to string.
        if zip_code.isdigit() and len(zip_code) == 5:
            my_zip_code = zip_code

        DISTANCEMATRIX_API_KEY = get_str_from_env_file('DISTANCEMATRIX_API_KEY')
        if not DISTANCEMATRIX_API_KEY:
            print("DISTANCEMATRIX_API_KEY not specified in .env file!")
            if my_longitude and my_latitude:  # from .env file:
                apispec="lat=" + my_latitude +"&lon=" + my_longitude
            else:
                apispec=f"zip={zip_code}"
        else:
            latitude, longitude = get_coordinates(zip_code, DISTANCEMATRIX_API_KEY)
            if longitude and latitude:  # from .env file:
                my_latitude = f"{latitude:.7f}"
                my_longitude = f"{longitude:.7f}"

    latitude_direction = "North of" if float(my_latitude) >= 0 else "South of"
    longitude_direction = "West of" if float(my_longitude) >= 0 else "East of"
    # print(f'--zip {zip_code} is at Latitude {my_latitude}, Longitude {my_longitude}')
    apispec="lat=" + my_latitude +"&lon=" + my_longitude

    openweathermap_api_key = get_str_from_env_file('OPENWEATHERMAP_API_KEY')
    if not openweathermap_api_key:
       print("OPENWEATHERMAP_API_KEY has no default! Processing killed")

    # https://api.openweathermap.org/data/2.5/weather?lat=40.7128&lon=-74.0060&appid={API key}
    #url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=" + apikey + "&units=metric.format(city)"
    url = "http://api.openweathermap.org/data/2.5/weather?"+apispec+"&appid="+openweathermap_api_key
    #city_input = "q=Billings" # instead of input("Enter City:")
    #city_encoded = urllib.parse.quote(city_input)
    if VERBOSE:
        print(f">>> url={url}")

    #if VERBOSE:
    #   print(">>> url=",url)  # contains APIKEY
    # data= {'coord': {'lon': -108.975, 'lat': 45.4869}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 302.63, 'feels_like': 301.72, 'temp_min': 299.05, 'temp_max': 302.63, 'pressure': 1009, 'humidity': 34, 'sea_level': 1009, 'grnd_level': 879}, 'visibility': 10000, 'wind': {'speed': 3.28, 'deg': 121, 'gust': 4.99}, 'clouds': {'all': 0}, 'dt': 1727569281, 'sys': {'type': 2, 'id': 2006447, 'country': 'US', 'sunrise': 1727529056, 'sunset': 1727571699}, 'timezone': -21600, 'id': 5661766, 'name': 'Laurel', 'cod': 200}
    try:
        res = requests.get(url)
        data = res.json()
    except Exception as e:
        "data= {'cod': '404', 'message': 'city not found'}"
        print(f">>> Error using city: {city_input} in {e}")
        exit(9)

    current_datetime = datetime.now()

    if VERBOSE:
        print(">>> returned data=",data)

    # Extract individual elements:
    lon = data['coord']['lon']
    lat = data['coord']['lat']
    try:
        cloud_desc = data['weather'][0]['description']
    except:
        cloud_desc = ""
    icon_code = data['weather'][0]['icon']  # '01n'
    wind_kph = data['wind']['speed']
    wind_deg = data['wind']['deg']
    wind_gust_kph = 0
    try:
        wind_gust_kph = data['wind']['gust']
    except:
        wind_gust_kph = 0
    else:
        wind_gust_kph = 0
    temp_k = data['main']['temp']
    temp_k_min = data['main']['temp_min']
    temp_k_max = data['main']['temp_max']
    feels_like_k = data['main']['feels_like']
    humidity = data['main']['humidity']
    sea_level_hpa = data['main']['sea_level']
    grnd_level_hpa = data['main']['grnd_level']
    visibility = data['visibility']
    call_dt = data['dt']
    pressure = data['main']['pressure']
    # 'sys': {'country': 'UA', 'sunrise': 1727497180, 'sunrise': 1727539818},
    try:
        country_text = ", country=" + data['sys']['country']
    except:
        country_text = ""
    sunrise_epoch = data['sys']['sunrise']
    sunset_epoch = data['sys']['sunset']
    timezone = data['timezone']

    call_id = data['id']  # 5661766
    cod = data['cod']  # 200
    try:
        station_name = data['name']  # "Bigfork"
    except Exception as e:
        # print(f">>> Error getting: name in {e}")
        station_name = ""


    #### Calculations from response:

    STRFTIME_FORMAT="%I:%M %p (%H:%M:%S) %Y-%m-%d"

    tz_offset = timedelta(seconds = timezone)  # = "-1 day, 18:00:00"
    #tz = timezone(tz_offset)
    # FIXME: TypeError: 'int' object is not callable
    #tz_name = datetime.now(tz).strftime('%Z')
    # print({tz_name})  # "UTC-0600"

    formatted_datetime=current_datetime.strftime(STRFTIME_FORMAT)

    sunrise_date_time = datetime.fromtimestamp(sunrise_epoch)
    sunrise_formatted = sunrise_date_time.strftime(STRFTIME_FORMAT)

    sunset_date_time = datetime.fromtimestamp(sunset_epoch)
    sunset_formatted = sunset_date_time.strftime(STRFTIME_FORMAT)

    call_date_time = datetime.fromtimestamp(call_dt)
    call_formatted = call_date_time.strftime(STRFTIME_FORMAT)

    cloud_text = cloud_text(cloud_desc)

    temp_c = kelvin2celcius(temp_k)
    feels_like_f = f" Feels like {kelvin2fahrenheit(feels_like_k):.2f}°F"

    # Dew point provides a more consistent and
    # easily interpretable measure of how humid it actually feels outside.
    dew_point_c = get_dew_point_c(temp_c, humidity)
    dew_point_f = celcius2fahrenheit(dew_point_c)
    dew_comfort = dew_desc_f(dew_point_f)


    #### Print:

    print(f"openweather.org")
    print(f"id: {call_id}    at: {formatted_datetime} TZ: {timezone}")
    print(f"          Sunrise: {GREEN}{sunrise_formatted}{RESET} local time")
    print(f"           Sunset: {sunset_formatted}")

    print(f"{cloud_text} at ",end="")
    if not station_name == None:
        print(f"{station_name} {country_text}",end="")
    print(f" {GRAY}\"{apispec}\"{RESET}")
    if latitude_direction:
        print(f"     Latitude:  {my_latitude}° {latitude_direction} the Equator &")
    if longitude_direction:
        print(f"     Longitude: {my_longitude}° {longitude_direction} the Meridian at Greenwich, UK")

    if USE_IMPERIAL_UNITS:
        temp_f = celcius2fahrenheit(temp_c)
        dew_point_c
        print(f"{dew_comfort} Dew Point of {dew_point_f:.2f}°F",end="")
        print(f" vs. {BOLD}{temp_f:.2f}°F{RESET} at {humidity}% humidity")
    else:
        print(f"{dew_comfort} Dew Point of {BOLD}{dew_point_c:.2f}°C{RESET}",end="")
        print(f" vs. {BOLD}{temp_c:.2f}°C{RESET} at {humidity}% Humidity")

    # Don't display min & max temperature if the are bogus:
    if temp_k_min != temp_k_max:
        temp_c_min = float(temp_k_min) - 273.15
        temp_c_max = float(temp_k_max) - 273.15
        if temp_c_min == temp_c_max:
            if USE_IMPERIAL_UNITS:
                temp_f_min = celcius2fahrenheit(temp_c_min)
                temp_f_max = celcius2fahrenheit(temp_c_max)
                print(f"    Temp. Minimum: {temp_f_min:.2f}°F,",end="")
                print(f" Maximum: {temp_f_max:.2f}°F")
            else:
                print(f"    Temp. Minimum: {temp_c_min:.2f}°C,",end="")
                print(f" Maximum: {temp_c_max:.2f}°C")


    print(f"    {feels_like_f} from",end="")
    # Convert wind direction to names (such as NWW):
    wind_dir = compass_text_from_degrees(wind_deg)
    if USE_IMPERIAL_UNITS:
        wind_mph = kph2mph(wind_kph)
        print(f" Wind: {wind_mph:.2f} mph from {wind_dir} ({wind_deg}°)",end="")
    else:
        print(f" Wind: {wind_kph:.2f} kph from {wind_dir} ({wind_deg}°)",end="")
    # See illustration at https://res.cloudinary.com/dcajqrroq/image/upload/v1727494071/compass-800x800_hvwmtu.webp
    if wind_gust_kph > 0:
        if USE_IMPERIAL_UNITS:
            wind_gust_mph = kph2mph(wind_gust_kph)
            print(f" with gusts: {wind_gust_mph:.2f} mph",end="")
        else:
            print(f" with gusts: {wind_gust_kph:.2f} kph",end="")

    print(f"\n     Visibility to {visibility} meters")


    # sea_level returned is a normalized value that allows for comparison between different locations, regardless of their actual elevation.
    # The average sea-level pressure is 1013.25 mb/hPA (Hectopascal).
    # One millibar is equivalent to 100 Pa (Pascals).
    # The SI Atmosphere (atm) average air pressure at sea level
    # of 101,325 pascals (Pa) or 1013.25 hPa (hectopascals).
    # See https://blog.mensor.com/blog/adjusting-barometric-pressure-readings-for-aviation-and-meteorology
    # See https://cumulus.hosiene.co.uk/viewtopic.php?t=8286
    # Example usage of the adjustment functions:
    sea_level_pressure = calculate_sea_level_pressure( \
        pressure, sea_level_hpa, temp_c)
    sea_millibars = pressure / 100
    pressure_diff = sea_level_pressure - pressure

    altitude_to_adjust = sea_level_hpa  # meters
    adjusted_pressure = adjust_pressure_for_altitude \
        (sea_level_hpa, altitude_to_adjust, temp_c)

    diff_hpa = sea_level_hpa - 1013
    if diff_hpa > 0:
        plus_hpa = "+"
    else:
        plus_hpa = ""
    #### Format & display each element:
    pressure_desc = pressure_desc(pressure)
    print(f"{RED}{pressure_desc} {plus_hpa}{diff_hpa}{RESET} pressure at {sea_level_hpa} hPa {GRAY}(HectoPascals = {sea_millibars} millibars){RESET}")
    print(f"          {GRAY}vs. normal 1013.25 hPa at sea level{RESET}")
    print(f"                     {grnd_level_hpa}    hPa at ground level")
    # Pressure changes with altitude, decreasing by about 12 hPa for every 100 meters of elevation.

    #print(f"is {pressure_diff:.2f} \
    #      hPa from adjusted average \
    #      {sea_level_pressure:.2f} hPa")
    # print(f"      vs. {sea_level_hpa} hPa at sea level.")
    # print(f"{hectopascals:.2f} hPa above sea level average of 1013.25 hPA")
    # What is normal for your location's altitude
    # Python code: https://www.perplexity.ai/search/how-adjust-normal-hectopascals-SuInNLlARxadL9GbY.NmBA
    # print(f"      vs. {adjusted_pressure:.2f} hPa normally for local elevation.")