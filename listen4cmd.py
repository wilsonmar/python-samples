#!/usr/bin/env python3

"""listen4cmd.py here.

https://github.com/wilsonmar/python-samples/blob/main/listen4cmd.py

Infinite loop listening for known voice commands to execute, a voice user interface
like Alexa (https://wilsonmar.github.io/alexa/) but this requires no wake word.

Currently Google service is used for voice recognition to text.
This references files in the audio folder (rimshot-joke-drum.wav, jeopardy-theme-song.mp3, etc.)

Based on https://medium.com/codrift/7-python-automation-projects-you-can-build-in-less-than-2-hours-each-e00f6c98fb96
# Based on https://github.com/rlaneyjr/myutils/blob/master/saytime.py 

Usage in CLI:
    brew install portaudio  # for pyaudio on macOS
    
    git clone https://github.com/wilsonmar/python-samples --depth 1
    cd python-samples

    uv init --no-readme.  # creates pyproject.toml
    uv venv .venv --python python3.12   # for Tensorflow
    source .venv/bin/activate

    chmod +x listen4cmd.py
    ruff check listen4cmd.py  # contains Flake8, Pylint, Xenon, Radon, Black, isort, pyupgrade.
    pip install -r requirements.txt

    uv add pyaudio, requests, google-cloud-speech, speedtest-cli
    uv add discoverhue
    uv add azure-cognitiveservices-speech.  # azure package is deprecated.
    uv add python_hue_v2, BridgeFinder
    uv add SpeechRecognition, pocketsphinx, apiai, assemblyai, subprocess-tee
    # , ibm-watson, wit, etc.

    uv run listen4cmd.py
    deactivate
"""
__last_change__ = "25-09-18 v010 + speedtest assessment :listen4cmd.py"
__status__ = "pause, start, price, speed test, lights commands not working."
# See listen4cmd_scraps.py in separate repo.

from datetime import datetime, timezone
import os
from pathlib import Path
import platform
import re
import requests
import shutil
import string
#import ssl
import time
#import urllib.request

# SpeechRecognition library works with major speech recognition engines: 
# google-cloud-speech, ibm-watson, pocketsphinx, wit, apiai, assemblyai
# NOTE: (from Wit.ai)
# Supports offline file transcription (WAV, MP3, etc.)
# See https://realpython.com/python-speech-recognition/ SR 3.8.1 using Python 3.9
try:   # external libraries from pypi.com:
    import azure.cognitiveservices.speech as speechsdk
    import discoverhue   # uv add discoverhue.  # for obsoleted philips hue.
    #from dotenv import load_dotenv, find_dotenv  # uv add python-dotenv
    #import emoji         # uv add emoji  # https://emojidb.org/quote-emojis
    # pip install git+https://github.com/killjoy1221/playsound.git
    #from playsound import playsound==1.2.2   # uv add playsound --frozen # using Python 3.9
    import pyaudio  # noqa  # uv add PyAudio library to use external/Bluetooth microphone input real-time.
    from pygame import mixer   # uv add pygame
    from python_hue_v2 import Hue, BridgeFinder
    import pyttsx3     # uv add pyttsx  # for offline text to speech # adds pyobjc-framework-* modules
    import simpleaudio as sa          # uv add simpleaudio   # play .wav sound
    import speedtest                  # uv add speedtest-cli
    import speech_recognition as sr   # uv add SpeechRecognition # different names!
    from subprocess_tee import run    # uv add subprocess-tee
    import webbrowser
except Exception as e:
    print(f"Python module import failed: {e}")
    # uv run log-time-csv.py
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    print("Please activate your virtual environment:")
    print("\n  uv venv .venv\n  source .venv/bin/activate\n  uv add ___")
    exit(9)


# TODO: Run-time Parameters:
# Global variable values:
SHOW_VERBOSE = False
SHOW_DEBUG = False
SHOW_SECRETS = False

SECS_BETWEEN_TRIES = 5
global_play_menu = "Press End/Pause/Resume/End"


def menu():
    """Recognize these words to return information."""
    print("    clock, time, local, london")
    print("    lights on/off, music (jeopardy)")  # , guitar
    print("    Lookup: joke, prices (currency), quote, speed test, weather")
    print("    Apps: calculator, claude, discord, docker, messages, obs, camtasia, slack, teams")


def listen_command() -> str:
    """Listen and recognize as text."""
    r = sr.Recognizer()              # listens with speech-to-text.   
    # f = sr.AudioFile(fileout)
    with sr.Microphone() as source:  # speaks  with text-to-speech.
        print("Listening... Say \"menu\" or other word(s)...")   # default wait for 5 seconds.
        try:
            audio = r.listen(source)
            if not audio:
                return None
            # command_str = speech_to_text_azure(audio).lower()   # from Microsoft, online 
               # FIXME: response: No speech could be recognized: NoMatchDetails(reason=NoMatchReason.InitialSilenceTimeout) # 'NoneType' object has no attribute 'lower'
            # Fallback to Google: _google comes with a dev. API key good for 50 queries per day.
            # print(f"DEBUGGING: command_str={command_str}")
            #if not command_str:
            command_str = r.recognize_google(audio).lower()
                    

                # Other alternatives (Not as precise as Google):
                # r.recognize_sphinx(audio).lower()    # from CMU Sphinx, offline!  uv add pocketsphinx
                # r.recognize_google()    # from Google Web Speech API, uv add google-cloud-speech
                # r.recognize_ibm()       # from IBM Speech to Text, online  uv add ibm-watson
                # r.recognize_houndify()  # from SoundHound, online  uv add ???
                # r.recognize_wit()       # from wit.ai, online  uv add wit

                # The Amazon Transcribe service is the real-time AWS speech recognition API:
                    # https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html
                    # https://github.com/aws-samples/amazon-transcribe-examples
                    # https://github.com/orgs/aws-samples/repositories?language=&q=transcribe&sort=&type=all
                    # https://reference-server.pipecat.ai/en/latest/api/pipecat.services.aws.stt.html
                    # https://docs.pipecat.ai/server/services/stt/aws
                    # https://github.com/pipecat-ai/pipecat/blob/main/examples/foundational/07m-interruptible-aws.py
                # For audio recognition through signal processing:
                # Also: https://docs.edgeimpulse.com/tutorials/end-to-end/keyword-spotting
            if SHOW_VERBOSE:
                print(f"\033[1m{command_str}\033[0m")
            return command_str
        except Exception as e:
            print(f"   {e}") # listen_command() died {e}")
            return None


def speech_to_text(text):
    """Convert text to speech object."""
    # import pyttsx3
    try:
        engine = pyttsx3.init()  # Initialize TTS engine
        engine.say(text)         # Pass the text to speak
        engine.runAndWait()      # Play the speech and wait until done
        engine.stop()
    except Exception as e:
        print(f"speech_to_text(): {e}")


def speech_to_text_azure(audio) -> str | None:
    """Use Microsoft cloud service for speech-to-text.
    
    Using import of https://pypi.python.org/pypi/SpeechRecognition/
    NOTE: "Bing" branding in BING_KEY is no longer used by Microsoft.
    1. Try Fast Transcription on Microsoft's demo web page: https://ai.azure.com/explore/models/aiservices/Azure-AI-Speech/version/1/registry/azureml-cogsvc/tryout?flight=SpeechBuild2025#fasttranscription
    2. See https://learn.microsoft.com/en-us/azure/ai-services/speech-service/index-speech-to-text
    3. Get an Azure account & Subscription: https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/#pricing
    4. Create Speech Service within AI Foundary at: https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/SpeechServices
    5. Crate Resource such as "speech-to-text-250918" for your Region (such as West Central US)
    6. Name such as "listen4cmd".
    7. Select "Standard S0" for 5 audio hours/month free: https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/#pricing
    8. In the resource's Resource Management menu, "Click here to manage keys" or "Keys and Endpoint" menu:
    9. Click icon to KEY1 and paste in .env file securely outside your GitHub repo:
        SPEECH_KEY="1234..." (Not shown here to avoid getting flagged by secret scans of code.)
    10. This program constructs the ENDPOINT from AZURE_REGION:
        ENDPOINT="https://westcentralus.api.cognitive.microsoft.com"  # (your region)
    11. Make a Calendar entry to Regenerate keys on a schedule according to your corporate security policies.
    """
    az_region = load_env_variable("AZURE_REGION")
    az_speech_endpoint = f"https://{az_region}.api.cognitive.microsoft.com"

    az_speech_key = load_env_variable("SPEECH_KEY")
    if not az_speech_key:
        print("FATAL: Azure SPEECH_KEY not found within .env file.")
        return None

    try:
        # import azure.cognitiveservices.speech as speechsdk
        speech_config = speechsdk.SpeechConfig(subscription=az_speech_key, \
            endpoint=az_speech_endpoint)
        #Instead of:
        #speech_config = speechsdk.SpeechConfig(subscription=os.environ.get(az_speech_key), \
        #    endpoint=os.environ.get(az_speech_endpoint))
        speech_config.speech_recognition_language="en-US"   # default.

        # import azure.cognitiveservices.speech as speechsdk
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # print("DOTHIS: Speak into your microphone:")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return speech_recognition_result.text
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("Speech not recognized. Please try again.")
                #  'NoneType' object has no attribute 'lower'
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("ERROR: Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("ERROR: details: {}".format(cancellation_details.error_details))
                #print("ERROR: Did you set the speech resource key and endpoint values?")
        return None
    except sr.UnknownValueError: 
        print("FATAL: speech_to_text_azure(): UnknownValueError.")
        return None
    except sr.RequestError as e:
        print(f"FATAL: speech_to_text_azure(): {e}")
        return None
    

def wav_play(filepath):
    """Play a .wav file to your machine's speaker.
    
    Such as "audio/rimshot-joke-drum.wav"
    """
    #import os
    # os.path.isfile() checks if the file exists and is not a directory:
    if not os.path.isfile(filepath):
        print(f"FATAL: File {filepath} not found!")
        return None
    try:
        # import simpleaudio as sa          # uv add simpleaudio   # play .wav sound
        wave_object = sa.WaveObject.from_wave_file(filepath)
        play_object = wave_object.play()
        play_object.wait_done()  # Wait until playback is finished
    except Exception as e:
        print(f"wav_play(): {e}")

def mp3_play_pygame(filepath="audio/jeopardy-theme-song.mp3",volume_in="7"):
    """Play mp3 audio file using pygame."""
    # Referencing global_play_menu
    try: 
        #from pygame import mixer
        mixer.init()
        mixer.music.load(filepath)

        if float(volume_in) > 10:
            volume_to_1 = float(volume_in) / 100
        elif float(volume_in) > 1:
            volume_to_1 = float(volume_in) / 10
        else:
            volume_to_1 = float(volume_in)
        mixer.music.set_volume(volume_to_1)

        mixer.music.play()

        # PROTIP: Keep the program running while sound plays:
        while mixer.music.get_busy():
            user_input = input(" ")
            if user_input == 'p':
                mixer.music.pause()	
                print(f"music Paused.... {global_play_menu}")
            elif user_input == 'r':
                mixer.music.unpause()
                print(f"music Resumed.... {global_play_menu}")
            elif user_input == 'e' or user_input == 's':
                mixer.music.stop()
                print("music Stopped/Ended.")
                return
            pass
    except Exception as e:
        print(f"mp3_pygame(): {e}")


## Time Utility functions:

def day_of_week(local_time_obj) -> str:
    """Return day of week name from number."""
    # str(days[local_time_obj.weekday()])  # Monday=0 ... Sunday=6
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return str(days[local_time_obj.weekday()])


def timestamp_local() -> str:
    """Generate a timestamp straing containing the local time with AM/PM & Time zone code."""
    # import pytz
    # now = datetime.now(tz)  # adds time zone.

    # from datetime import datetime
    local_time_obj = datetime.now().astimezone()
    local_timestamp = local_time_obj.strftime("%Y-%m-%d_%I:%M:%S %p %Z%z")  # local timestamp with AM/PM & Time zone codes
    enhanced = str(local_timestamp) +" "+ day_of_week(local_time_obj)
    return enhanced


def timestamp_utc() -> str:
    """Generate a timestamp straing containing the UTC "Z" time with no AM/PM & Time zone code."""
    # import time
    timestamp = time.time()   # UTC epoch time.
    # from datetime import datetime, timezone
    # Get the current UTC time as a timezone-aware datetime object
    now_utc = datetime.now(timezone.utc)
    # Format the UTC timestamp as a string, e.g., ISO 8601 format
    timestamp = now_utc.strftime('%Y-%m-%dT%H:%M:%SZ') +' '+ day_of_week(now_utc)
    return timestamp


def load_env_variable(variable_name, env_file='~/python-samples.env') -> str:
    """Retrieve a variable from a .env file in Python without the external dotenv package.
    
    USAGE: my_variable = load_env_variable('MY_VARIABLE')
    Instead of like: api_key = os.getenv("API_KEY")
    """
    home_path_env = os.path.expanduser('~')+"/python-samples.env"
    # Check for env_file:
    env_path = Path(home_path_env)
    if SHOW_VERBOSE:
        print(f"VERBOSE: env_path={env_path}")
    if env_path.is_file() and env_path.exists():
        if SHOW_DEBUG:
            print("DEBUG: .env file is accessible")
    else:
        print(f"ERROR: .env file {env_path} is not accessible")
        return None

    with open(env_path) as file:
        # FIXME: FileNotFoundError: [Errno 2] No such file or directory: 'Users/johndoe/python-samples.env'
        for line in file:
            # Strip whitespace and ignore comments or empty lines:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            
            # Split the line into key and value:
            key_value = line.split('=', 1)
            if len(key_value) != 2:
                continue
            
            key, value = key_value
            if key.strip() == variable_name:
                return value.strip().strip('\"').strip('\'')
    return None


def ninja_api(topic) -> str:
    """Return after call for a (singular) topic of choice."""
    if topic == "quote":
        url = "https://api.api-ninjas.com/v1/quotes"
    elif topic == "joke":
        url = "https://api.api-ninjas.com/v1/jokes"
    elif topic == "gold":
        url = "https://api.api-ninjas.com/v1/goldprice"
    else:
        print(f"Unknown topic: {topic}")
        return None

    api_ninjas = load_env_variable("API_NINJAS")
    if not api_ninjas:
        print("FATAL: API_NINJAS environment variable not set")
        return None
    if SHOW_SECRETS:
        print(f"SECRETS: API_NINJAS={api_ninjas}")
    headers = { "X-Api-Key": f"{api_ninjas}" }
    api_ninjas = None
    params = ""  # {"category": "success"}
    
    try:
        # verify=True to not bypass TLS CA certificate bundle issue - to make production-worthy.
        response = requests.get(url, headers=headers, params=params, verify=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return None


def exchangerates():
    """Get exchange rate prices."""
    # https://www.exchangerate-api.com/docs/python-currency-api

    exchange_rates_api = load_env_variable("EXCHANGE_RATES_API") # load_env_variable('')
    if not exchange_rates_api:
        print("FATAL: EXCHANGE_RATES_API environment variable not set")
        return None
    if SHOW_SECRETS:
        print(f"SECRETS: EXCHANGE_RATES_API={exchange_rates_api}")

    # For USD as the base currency: ISO 4217 Three Letter Currency Codes 
    # Rate limiting once per hour:
    url = f"https://v6.exchangerate-api.com/v6/{exchange_rates_api}/latest/USD"
    exchange_rates_api = None
    # TODO: Add TTL
    # WARNING: Added verify=False to bypass TLS CA certificate bundle issue. Not recommended for production.
    response = requests.get(url, verify=False)
    data = response.json()
    usd_eur = data["conversion_rates"]["EUR"]
    usd_jpy = data["conversion_rates"]["JPY"]
    usd_gbp = data["conversion_rates"]["GBP"]
    print(f"1 USD= {usd_eur} EUR (Euros), {usd_jpy} JPY (Yen), {usd_gbp} GBP (Pounds)")


def get_random_kjv_verse():
    """Return random English KJV Bible verse."""
    #url = "https://bible-api.com/data/random/KJV"
    url = "https://bible-api.com/John+3:16?translation=kjv"
    # WARNING: Added verify=False to bypass TLS CA certificate bundle issue. Not recommended for production.
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        data = response.json()
        verse_text = data['text']  # verse text content
        reference = data['reference']  # verse reference like "John 3:16"
        return f"{verse_text} — {reference}"
    else:
        return None


def human_readable_speed(nbytes):
    """Return formatted speed metric."""
    suffixes = ['bps', 'Kbps', 'Mbps', 'Gbps', 'Tbps']
    i = 0
    while nbytes >= 1000 and i < len(suffixes) - 1:
        nbytes /= 1000.0
        i += 1
    return f"{nbytes:.2f} {suffixes[i]}"


def do_speedtest() -> str | None:
    """Measure internet speed."""
    print("\N{antenna with bars} Measuring wifi/internet download speed, upload speed, and ping...")
    try:
        # import speedtest   # uv add speedtest-cli
        st = speedtest.Speedtest()
    except Exception as e:
        print(f"FATAL: do_speedtest(): {e}")
        return None
    
    download_speed = st.download()
    upload_speed = st.upload()
    ping = st.results.ping

    # PROTIP: Use Regex to recognize and extract number from within string:
    # import re
    download_numbers = re.findall(r'\d+', download_speed)
    upload_numbers = re.findall(r'\d+', upload_speed)
    if download_numbers:
        download_number = int(download_numbers[0])  # Use first found number
        upload_number = int(upload_numbers[0])  # Use first found number
        if download_number >= 300:
            assessment = " (fibre)"
        if download_number >= 100 and upload_number > 20:
            assessment = " (broadband)"
        if download_number < 25:
            assessment = " slow!"
        else:
            assessment = " middling"
    # In July 2025, the average U.S. household gets about 285 Mbps download and 48 Mbps upload.
    # Ookla’s Speedtest.net makes US 7th in the world by https://tradingeconomics.com/united-states/rural-population-percent-of-total-population-wb-data.html#:~:text=Rural%20population%20(%25%20of%20total,compiled%20from%20officially%20recognized%20sources.
    # T-Mobile is the fastest mobile provider in the 1st half of 2024 at 206 Mbps.
    # Where did the US Broadband Equity, Access and Deployment Program (BEAD) that provided $42.45 billion in state broadband grants?
    # A 100 Mbps plan allows one to four users to be online at the same time streaming or working from home.
    response=f"    Download Speed:{assessment} {human_readable_speed(download_speed)}, Upload Speed: {human_readable_speed(upload_speed)}, Ping: {ping} ms"
    # speech_to_text(results)
    print(f"    {response}")
    return response


def philips_hue_hub_ip() -> (str, str):
    """Identify Philips Hue hub IP address."""
    # https://developers.meethue.com/develop/application-design-guidance/hue-bridge-discovery/
    # import discoverhue

    # Find all Hue bridges on the local network:
    found_bridges = discoverhue.find_bridges()
    if not found_bridges:
        print("philips_hue_hub_ip() found no Philips Hue bridges on the network.")
        return None, None
    else:
        for bridge_id, ip in found_bridges.items():
        # such as "191.168.2.3" in Hue app, Settings icon, Bridges, Bridge Settings, IP-address
            if SHOW_SECRETS:
                print(f"SECRET: philips_hue_hub_ip(): Bridge ID {bridge_id} at IP {ip}")
        # TODO: Add or update entry in .env file if it's not there.
        return bridge_id, ip


def philips_hue_action(light_num, action):
    """Turn Philips Hue lights on or off via Philips Hue Bridge API v2."""
    # https://github.com/zzstoatzz/phue?tab=readme-ov-file

    # WARNING: In 2025 Philips made several changes to the API.
    # See https://developers.meethue.com/forum/t/signaling-not-working-for-older-lights/7092
    # https://developers.meethue.com
    # Among the helper libraries at https://developers.meethue.com/develop/tools-and-sdks/

    # https://pypi.org/project/python-hue-v2/ was Released: Jan 30, 2025 by Yichen Zhao
    # from https://developers.meethue.com/develop/hue-api-v2/api-reference/

    # Python library adafruit_hue helper module provide easier interaction.

    # Python library https://pypi.org/project/HueBLE/ by github.com/flip-dots/ 
    # was written by as CS degree student in Manchester, UK.
    # It leverages the Bleak Bluetooth library to directly interact with 
    # MAC addresss on Philips Hue bulbs, without a bridge or ZigBee dongle.

    # File phue.py was created when Hue was created in 2012 at
    # https://github.com/studioimaginaire/phue and is not even in PiPy.
    # It leverages the Bridge Bluetooth library to directly interact with the IP address.
    # of the Philips Hue bridge controlling Philips-branded bulbs.
    # See Derrick Sherrill's https://www.youtube.com/watch?v=kSruoqDTYt0
        # https://www.linkedin.com/in/derricksherrill/

    # from python_hue_v2 import Hue, BridgeFinder  # uv add python_hue_v2
    bridge_id, bridge_ip = philips_hue_hub_ip()
    if not bridge_ip:   # returned:
        print("FATAL: Bridge IP not found. Aborting.")
        return None
    
    finder = BridgeFinder()
    time.sleep(1)  # Give time for search
    # Get server by Hue's mDNS:
    host_name = finder.get_bridge_server_lists()[0]  # Here we use first Hue Bridge
    # such as "0012345678c0.local" in Hue app, Settings icon, Bridges, Bridge Settings, ID field
    if SHOW_VERBOSE:
        print(f"host_name={host_name}")

    # Retrieve app_key from .env file variable = 
    app_key = load_env_variable("PHILIPS_HUE_APP_KEY") # load_env_variable('')
    if not app_key:
        print("FATAL: PHILIPS_HUE_APP_KEY environment variable not set")
        return None
    if SHOW_SECRETS:
        print(f"SECRETS: PHILIPS_HUE_APP_KEY={app_key}")

    print("DO THIS: Press the Hue button quickly now:")
    # (this only needs to be run a single time)
    hue = Hue(host_name)
    app_key = hue.bridge.connect() # you can get app_key and storage on disk
    if not app_key:
        print("FATAL: No app key. Aborting.")
        return None
    else:
        if SHOW_SECRETS:
            print(f"SECRET: app_key={app_key} TODO: Insert in .env.")
    
    # from python_hue_v2 import Hue
    hue = Hue(bridge_ip, app_key)
    app_key = None
    try:
        lights = hue.lights   # FIXME: lights object exception?
        print(f"lights={lights}")
        for light in lights:  # cycle through lights:
            print(f"light={light}, light_num={int(light_num)} from parm.")
            if action == "on":
                print(light_num.on)
                light_num.on = True
                light_num.brightness = 80.0
            elif action == "off":
                light_num.on = False
            else:
                print(f"FATAL: action {action} unknown.")
                return None
    except Exception as e:
        print(f"philips_hue_action(): {e}")
        # FIXME: philips_hue_action(): HTTPSConnectionPool(host='http', port=443): Max retries exceeded with url: /192.168.1.2:80//clip/v2/resource/light (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x102322120>: Failed to resolve 'http' ([Errno 8] nodename nor servname provided, or not known)"))
        return None


def say_string(text, voice=None, rate=None):
    """Use macOS 'say' command to speak text aloud.
    
    Args:
        text (str): The text to speak
        voice (str, optional): The voice to use (e.g., 'Alex', 'Samantha')
        rate (int, optional): Speech rate (words per minute)
    """
    command = ['say']
    
    if voice:  # other than value = None:
        command.extend(['-v', voice])
    
    if rate:
        command.extend(['-r', str(rate)])
    
    command.append(text)
    os.system(' '.join(command))


def organize_downloads():
    """Command to organize downloads folder."""
    folder = '/Users/you/Downloads'
    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        if os.path.isfile(filepath):
            ext = os.path.splitext(file)[1].lower()
            category = 'Images' if ext in ['.jpg', '.png'] else 'Docs'
            target = os.path.join(folder, category)
            os.makedirs(target, exist_ok=True)
            shutil.move(filepath, os.path.join(target, file))

# TODO: def more commands to process!

if __name__ == "__main__":

    # uv add python-dotenv
    # Load environment variables from .env file:
    # from dotenv import load_dotenv, find_dotenv

    if SHOW_VERBOSE:
        print(f"speech_recognition __version__ = {sr.__version__}")

    try:
        while True:    # Infinite loop:
            loops_count =+ 1
            command_str = listen_command()
            if command_str is None:
                print(f"Sleeping {SECS_BETWEEN_TRIES} seconds...")
                time.sleep(SECS_BETWEEN_TRIES)
                continue  # loop again

                # TODO: Allow commands to be typed in while listening.

            print(f"\033[1m{command_str}\033[0m")
            if 'menu' in command_str:
                menu()

            elif 'exit' in command_str or 'abort' in command_str or 'stop' in command_str:
                print("    Bye Bye")
                exit()

            elif 'speed' in command_str:
                # from playsound import playsound
                results = do_speedtest()

            elif 'bible' in command_str:
                # TODO: Random KJV Bible verse:
                text=get_random_kjv_verse()
                print(f"{text}")
                speech_to_text(text)

            elif 'lights' in command_str and 'on' in command_str:
                light_num = 1
                action = "on"
                print(f"{philips_hue_action(light_num,action)}")
            elif 'lights' in command_str and 'off' in command_str:
                light_num = 1
                action = "off"
                print(f"{philips_hue_action(light_num,action)}")

            elif 'time' in command_str:
                # Run another Python script (e.g. "saytime.py") with arguments
                result = run(["python", "saytime.py"], tee=True, text=True, capture_output=True)
                # "Twenty five past five is the local time"    
            elif 'local' in command_str and 'time' in command_str:
                print(f"   {timestamp_local()}")
            elif 'london' in command_str or 'UTC' in command_str:
                print(f"   {timestamp_utc()}")                  

            elif 'weather' in command_str:
                # From among https://github.com/public-apis/public-apis
                # Run another Python script (e.g. "other_script.py") with arguments
                result = run(["python", "openweather.py", "-v"], tee=True, text=True, capture_output=True)
                # Output is printed live and also captured in result.stdout:
                print("Captured output:", result.stdout)

            elif 'discord' in command_str:
                result = run(["open", "-a", "Discord"], tee=True, text=True, capture_output=True)
                print("    Opening Discord...")
            elif 'messages' in command_str:
                result = run(["open", "-a", "Messages"], tee=True, text=True, capture_output=True)
                print("    Opening Messages...")

            elif 'calculator' in command_str and 'plus' in command_str:
                result = run(["open", "-a", "Calculator Plus.app"], tee=True, text=True, capture_output=True)
                print("    Opening Calculator Plus...")
                # PROTIP: compound actions need to precede single commands.
            elif 'calculator' in command_str:
                result = run(["open", "-a", "Calculator.app"], tee=True, text=True, capture_output=True)
                print("    Opening Calculator...")
            elif 'camtasia' in command_str:
                result = run(["open", "-a", "Camtasia 2023.app"], tee=True, text=True, capture_output=True)
                print("    Opening Camtasia...")
            elif 'clock' in command_str:
                result = run(["open", "-a", "Clock.app"], tee=True, text=True, capture_output=True)
                print("    Opening Clock...")

            elif 'claude' in command_str:
                result = run(["open", "../../Applications/Claude.app"], tee=True, text=True, capture_output=True)
                print("    Opening Claude...")
            elif 'cursor' in command_str:
                result = run(["open", "../../Applications/Cursor.app"], tee=True, text=True, capture_output=True)
                print("    Opening Cursor...")
            elif 'docker' in command_str:    # say "dock er"
                result = run(["open", "../../Applications/Docker.app"], tee=True, text=True, capture_output=True)
                print("    Opening Docker...")
            elif 'slack' in command_str:
                result = run(["open", "../../Applications/Slack.app"], tee=True, text=True, capture_output=True)
                print("    Opening Slack...")
            elif 'obs' in command_str:   # pronounce each letter.
                result = run(["open", "../../Applications/OBS.app"], tee=True, text=True, capture_output=True)
                print("    Opening OBS...")
                # NOTE: Apps in "/Applications" not accessible from / due to security permissions.

            elif 'prices' in command_str or 'rates' in command_str:
                #FIXME: OSError: Could not find a suitable TLS CA certificate bundle, invalid path: /path/to/my.crt
                data = ninja_api("gold")
                # exchangerates()
                # TODO: https://www.commodities-api.com/register?path=blog
                # https://api.api-ninjas.com/v1/goldprice
                # Gold, Silver, USD-Euro, USD-UK, Bitcoin, Etherium, US stablecoins.
                print(f"    {data}")

            elif 'quote' in command_str:
                # Google has difficulty understanding this word.
                # https://api-ninjas.com/api/quotes
                # Returns one of 100 random quotes for free users. 200,000 quotes for premium users.
                data = ninja_api("quote")
                if SHOW_VERBOSE:
                    print(f"VERBOSE: Quote API returned: {data}")
                
                # Check if data is valid and not empty
                if data and isinstance(data, list) and len(data) > 0:
                    for s in range(len(data)):
                        quote_item = data[s]
                        # Ensure the quote item has all required fields
                        if all(key in quote_item for key in ['category', 'quote', 'author']):
                            text = f"    \033[4m{quote_item['category']}\033[0m: \u201C{quote_item['quote']}\u201D \u2014{quote_item['author']}"
                            print(f"{text}")
                            speech_to_text(text)
                        else:
                            print(f"Quote item missing required fields: {quote_item}")
                else:
                    print("No quotes available or invalid API response")
            
            elif 'facebook' in command_str:
                #import webbrowser
                url = "https://www.facebook.com"
                webbrowser.open(url)

            elif 'joke' in command_str:
                # https://api-ninjas.com/api/jokes
                # import emoji         # uv add emoji
                data = ninja_api("joke")
                if SHOW_VERBOSE:
                    print(f"Joke API returned: {data}")
                
                # Check if data is valid and not empty
                if data and isinstance(data, list) and len(data) > 0:
                    for s in range(len(data)):
                        joke_item = data[s]
                        # Ensure the joke item has the required 'joke' field
                        if 'joke' in joke_item:
                            # Unicode emoji name with \N: https://github.com/carpedm20/emoji/blob/master/emoji/unicode_codes/emoji.json
                            print("Joking...")
                            text = f"{joke_item['joke']}"
                            print(f"\N{grinning face}  {text}")
                            speech_to_text(text)
                            wav_play("audio/rimshot-joke-drum.wav")
                        else:
                            print(f"Joke item missing 'joke' field: {joke_item}")
                else:
                    print("No jokes available or invalid API response")

            #elif 'log' in command_str:
                # log show --predicate 'subsystem == "com.apple.speech"' --last 1h

            #elif 'organize' in command_str and 'downloads' in command_str:
            #    organize_downloads()
            #    print(".   DONE: Files sorted by voice command.")


            elif 'music' in command_str or 'jeopardy' in command_str or 'song' in command_str:
                if any(char.isdigit() for char in command_str):
                    # Ignoring possibility that several numbers can be in command:
                    numbers = [int(command_str) for command_str in string.split() if command_str.isdigit()]
                    if numbers:
                        volume = numbers[0]  # First found number
                    print(f"play volume set to {volume}")
                else:
                    volume = "0.7"

                print(f"    Playing Jeopardy song (33 seconds)... {global_play_menu}")
                mp3_play_pygame("audio/jeopardy-theme-song.mp3",volume)


            #elif 'guitar'
            #    print(".   Playing guitar.")
            #    guitar_play()


            elif 'settings' in command_str or 'system' in command_str:
                # import platform
                if platform.system().lower() == 'darwin':  # is macOS:
                    # AppleScript command to open System Preferences (Settings)
                    applescript = 'tell application "System Preferences" to activate'
                    # Execute the AppleScript command as CLI call:
                    run(['osascript', '-e', applescript])

            else:
                # TODO: Send unrecognized sentences to ChatGPT.
                print("    ?")  # Command not recognized!
        
        # loop again
    except KeyboardInterrupt:
        print("\ncontrol+C exiting listen4cmd.py gracefully.")
