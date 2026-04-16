#!/usr/bin/env python3
# https://www.perplexity.ai/search/how-to-use-uv-to-create-the-eq-O8ocUS3VSCum2i.ARsyQGQ

"""listen4cmd.py here.

https://github.com/wilsonmar/python-samples/blob/main/listen4cmd.py

Infinite loop listening for known voice commands to execute, a voice user interface
like Alexa (https://wilsonmar.github.io/alexa/) but this requires no wake word.
Like https://wisprflow.ai

Currently Google service is used for voice recognition to text.

Pygame references files in the audio folder (rimshot-joke-drum.wav, jeopardy-theme-song.mp3, etc.)

Based on https://medium.com/codrift/7-python-automation-projects-you-can-build-in-less-than-2-hours-each-e00f6c98fb96
# Based on https://github.com/rlaneyjr/myutils/blob/master/saytime.py 

TODO: uv ///. Retry. Capture response time. Log to file.

Usage in CLI:
    brew install portaudio  # for pyaudio on macOS
    
    git clone https://github.com/wilsonmar/python-samples --depth 1
    cd python-samples

    uv init --no-readme  # creates pyproject.toml
    # Rather than editing requirements.txt, always generate it:
    uv export --no-dev --format requirements-txt > requirements.txt
    uv venv .venv   # --python python3.12   # for Tensorflow
    source .venv/bin/activate
    uv lock --check  # verify the lockfile matches pyproject.toml and dependencies are not stale.
    uv lock --upgrade   # all packages to their latest compatible versions

    chmod +x listen4cmd.py
    ruff check listen4cmd.py  # contains Flake8, Pylint, Xenon, Radon, Black, isort, pyupgrade.
    # pip install -r requirements.txt

    uv add pyaudio, requests, google-cloud-speech, speedtest-cli
    uv add discoverhue, pyperclip
    uv add azure-cognitiveservices-speech.  # azure package is deprecated.
    uv add python_hue_v2, BridgeFinder
    uv add SpeechRecognition, pocketsphinx, apiai, assemblyai, subprocess-tee
    uv add tenacity
    # , ibm-watson, wit, etc.

    uv run listen4cmd.py -v -vv -s
    deactivate
"""
__last_change__ = "25-09-18 v012 + activity monitor :listen4cmd.py"
__status__ = "pause, start, price, speed test, lights commands not working."
# See listen4cmd_scraps.py in separate repo.

from datetime import datetime, timezone
import csv
import os
#import logging  - from loguru import logger
import platform
import re
import requests
import shutil
import string
#import ssl
import time    # pytz or pendulum library
#import urllib.request
# For wall time of standard imports:
std_stop_datetimestamp = datetime.now()

# For wall time of xpt (external) imports:
xpt_strt_datetimestamp = datetime.now()
# SpeechRecognition library works with major speech recognition engines: 
# google-cloud-speech, ibm-watson, pocketsphinx, wit, apiai, assemblyai
# NOTE: (from Wit.ai)
# Supports offline file transcription (WAV, MP3, etc.)
# See https://realpython.com/python-speech-recognition/ SR 3.8.1 using Python 3.9
try:   # external libraries from pypi.com:
    import asyncio
    import azure.cognitiveservices.speech as speechsdk
    # import dashscope     # uv add dashscope # alibaba - DISABLED due to missing dependency
    import discoverhue   # uv add discoverhue.  # for obsoleted philips hue.
    #from dotenv import load_dotenv, find_dotenv  # uv add python-dotenv
    #import emoji         # uv add emoji  # https://emojidb.org/quote-emojis
    # pip install git+https://github.com/killjoy1221/playsound.git
    #from playsound import playsound==1.2.2   # uv add playsound --frozen # using Python 3.9
    import itertools
    import httpx
    from loguru import logger
    import pyaudio  # noqa  # uv add PyAudio library to use external/Bluetooth microphone input real-time.
    from pygame import mixer   # uv add pygame
    from python_hue_v2 import Hue, BridgeFinder
    import pyperclip   # uv add pyperclip  
    import pyttsx3     # uv add pyttsx  # for offline text to speech # adds pyobjc-framework-* modules
    # import simpleaudio as sa          # uv add simpleaudio   # play .wav sound - DISABLED due to segfault on Python 3.13+
    import speedtest                  # uv add speedtest-cli
    import speech_recognition as sr   # uv add SpeechRecognition # different names!
    from subprocess_tee import run    # uv add subprocess-tee
    from tenacity import retry, stop_after_attempt, wait_fixed
    import webbrowser
except Exception as e:
    print(f"Python module import failed: {e}")
    print("Please activate your virtual environment:")
    print("\n  uv venv .venv\n  source .venv/bin/activate\n  uv add ___")
    exit(9)
# For wall time of xpt imports:
xpt_stop_datetimestamp = datetime.now()


# TODO: Run-time Parameters:
# Global variable values:
SHOW_VERBOSE = False
SHOW_DEBUG = False
SHOW_SECRETS = False
SHOW_STATS = False

SECS_BETWEEN_TRIES = 5

#### SECTION 4 - Meny:

global_play_menu = "Press End/Pause/Resume/End"

# user_app is at /Users/<user>/Applications/...
# sys_app  is at /Applications/...
actions_tuple = {  # as ordered key-value:
    "acronyms": ["website0", "wilsonmar.github.io/acronyms" ],
    "activity": ["sys_app", "Utilities/Activity Monitor.app" ],
    "amazon": ["website", "amazon.com" ],
    "asian": ["website", "yami.com" ],
    "aws": ["website0", "aws.amazon.com" ],
    "azure": ["website0", "portal.azure.com" ],
    "babble": ["website", "babble.com" ],
    "blog": ["website0", "wilsonmar.github.io/posts" ],
    "bomonike": ["website0", "bomonike.github.io/README" ],
    "brave": ["user_app", "Brave Browser.app" ],
    "calculator": ["sys_app", "Calculator.app" ],
    "calendar": ["website0", "calendar.google.com" ],
    "camtasia": ["sys_app", "camtasia 2023.app" ],
    "claude": ["user_app", "Claude.app" ],
    "clock": ["sys_app", "Clock.app" ],
    "costco": ["website", "costco.com" ],
    "contacts": ["website0", "contacts.google.com" ],

    "cursor": ["user_app", "Causor.app" ],
    "discord": ["sys_app", "Discord.app" ],
    "drive": ["website0", "drive.google.com" ],
    "docker": ["user_app", "Docker.app" ],
    "facebook": ["website", "facebook.com" ],
    "firefox": ["sys_app", "Firefox.app" ],
    "github": ["website", "github.com" ],
    "gmail": ["website", "gmail.com" ],
    "google": ["website", "google.com" ],
    "imdb": ["website", "imdb.com" ],
    "instagram": ["website", "instagram.com" ],
    "just watch": ["website", "justwatch.com" ],
    "linkedin": ["website", "linkedin.com" ],
    "messages": ["sys_app", "Messages.app" ],
    "quiz": ["sys_app", "Anki.app" ],
    "obs": ["user_app", "OBS.app" ],
    "perplexity": ["website", "perplexity.ai" ],
    "safari": ["sys_app", "Safari.app" ],
    "search": ["website", "startpage.com" ],
    "speed test": ["sys_app", "SpeedTest.app" ],
    "slack": ["user_app", "slack.app" ],
    "surf": ["user_app", "windsurf.app" ],
    "terminal": ["sys_app", "Utilities/Terminal.app" ],
    "virus total": ["website", "virustotal.com/gui/home/url" ],
    "voice": ["website0", "voice.google.com" ],
    "youtube": ["website", "youtube.com" ],
    "visual": ["user_app", "Visual Studio Code.app" ],
    "warp": ["user_app", "warp.app" ],
    "xcode": ["sys_app", "XCode.app" ],
}
# Firefox with no cookies: fidelity, capital one, wells fargo, proton mail, etc.

def menu():
    """Recognize these words to return information.
    
    TODO: Generate menu based on actions_tuple (above).
    """
    print("    clock, time, local, london")
    print("    lights on/off, music (jeopardy)")  # , guitar
    print("    Lookup: joke, prices (currency), quote, speed test, weather")
    print("    Apps: calculator, claude, discord, docker, messages, obs, camtasia, slack, teams")

#### SECTION 4 - Logging:

store_log = False
log_start_stop = True
if store_log:
    # Configure logging format and level:
    # Used by log_http_response_time()
    # import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

def log_http_response_time(url):
    """Log response times of http requests.

    # Example usage:
    url = 'https://api.github.com'
    response = log_http_response_time(url)
    """
    if log_start_stop:
        start_time = time.time()
        logging.info(f"Starting request to {url} at {start_time}")
    try:
        response = requests.get(url, timeout=10)
        elapsed_time = time.time() - start_time
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx and 5xx)
        logging.info(f"Received response from {url} with status code {response.status_code} in {elapsed_time:.4f} seconds")
        return response
    except requests.exceptions.RequestException as e:
        elapsed_time = time.time() - start_time
        logging.error(f"Request to {url} failed after {elapsed_time:.4f} seconds: {e}")
        return None


async def log_async_http_response_time(url):
    """Log response times of asynx requests.

    # Example usage:
    url = 'https://api.github.com'
    await log_async_http_response_time(url)

    if __name__ == "__main__":
        asyncio.run(main())

    https://launchdarkly.com/blog/why-use-logging-libraries-for-python/
    logger.remove(0)  # https://loguru.readthedocs.io/en/stable/api/logger.html#record
    logger.add(sys.stderr, format="{level} : {time} : {message}: {process}")  # <-

    logger.critical("This is a critical message.") # A severe issue that can terminate the program, like " out of memory".
    logger.error("This is an error message.") # An issue that needs your immediate attention but won't terminate the program.
    logger.debug("This is a debug message")   # Information that is helpful during debugging.
    logger.info("This is an info message.")   # Confirmation that the application is behaving as expected.
    logger.warning("This is a warning message.") # an issue that may disrupt the application in the future.

    # loguru only:
    logger.trace("This is a trace message.")  # low-level details of the program's logic flow.
    logger.success("This is a success message.") # an operation was successful.

    {"levelname": "ERROR", "name": "__main__", "message": "This is an error message", "asctime": "2023-03-28 14:04:01,930"}
    {"levelname": "CRITICAL", "name": "__main__", "message": "This is a critical message", "asctime": "2023-03-28 14:04:01,930"}
    """
    # import asyncio, httpx, logging, time
    logging.info(f"Starting async request to {url}")
    start_time = time.perf_counter()
    req_count = req_count =+ 1
    try:
        timeout_specs = httpx.Timeout(   # seconds (float):
            timeout=10.0,       # Total timeout default 
            connect=5.0,        # Timeout to establish connection setup
            read=10.0,          # Timeout waiting for receiving data
            write=5.0,          # Timeout waiting for sending data
            pool=5.0            # Timeout for acquiring connection from pool
        )
        async with httpx.AsyncClient(timeout=timeout_specs) as client:
            response = await client.get(url)

            #response.raise_for_status()
            # asyncio.wait_for enforces a hard timeout for the coroutine
            response = await asyncio.wait_for(client.get(url), timeout=12.0)
            
            elapsed_time = time.perf_counter() - start_time
            logging.info(f"Received response from {url} with status code {response.status_code} in {elapsed_time:.4f} seconds")
            return response
    except httpx.RequestError as e:
        elapsed_time = time.perf_counter() - start_time
        logging.error(f"Request {req_count} to {url} failed after {elapsed_time:.4f} seconds: {e}")
        return None
    except httpx.HTTPStatusError as e:
        elapsed_time = time.perf_counter() - start_time
        logging.error(f"HTTP error during request {req_count} to {url} after {elapsed_time:.4f} seconds: {e}")
        return None


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
            # llms = ["google", "azure", "aws", "qwen", etc.]
            # if llm_to_use == "Google":
                # command_str = speech_to_text_qwen(audio).lower() https://www.alibabacloud.com/help/en/model-studio/qwen-speech-recognition
                   # Local: https://www.perplexity.ai/search/how-to-setup-qwen-speech-recog-utUbfa_5Thaqwz7nORx3yw

                # command_str = speech_to_text_azure(audio).lower()   # from Microsoft, online 
                    # FIXME: response: No speech could be recognized: NoMatchDetails(reason=NoMatchReason.InitialSilenceTimeout) # 'NoneType' object has no attribute 'lower'
                    # Fallback to Google: _google comes with a dev. API key good for 50 queries per day.
                    # print(f"DEBUGGING: command_str={command_str}")
                    #if not command_str:
                # command_str = r.recognize_google(audio).lower()
        
                # r.recognize_google()    # from Google Web Speech API, uv add google-cloud-speech
                # Other alternatives (Not as precise as Google):
                # r.recognize_sphinx(audio).lower()    # from CMU Sphinx, offline!  uv add pocketsphinx
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

def qwen_stt():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-Audio")

    audio_url = "https://example.com/audio.flac"
    prompt = "<|startoftranscript|><|en|><|transcribe|><|en|><|notimestamps|><|wo_itn|>"

    query = f"<audio>{audio_url}</audio>{prompt}"

    audio_info = tokenizer.process_audio(query)
    inputs = tokenizer(query, return_tensors='pt', audio_info=audio_info)

    pred = model.generate(**inputs, audio_info=audio_info)
    response = tokenizer.decode(pred.cpu()[0], skip_special_tokens=False, audio_info=audio_info)

    print(response)


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
    

# def speech_to_text_qwen(audio):
#     """Use Qwen AI Alibaba cloud in Singapore for speech-to-text."""
#     # DISABLED: dashscope dependency not installed
#     # https://www.alibabacloud.com/help/en/model-studio/qwen-speech-recognition
#     # To enable, run: uv add dashscope
#     pass


def wav_play(filepath):
    """Play a .wav file to your machine's speaker using pygame.
    
    Such as "audio/rimshot-joke-drum.wav"
    NOTE: Fixed segfault issue by replacing simpleaudio with pygame
    """
    #import os
    # os.path.isfile() checks if the file exists and is not a directory:
    if not os.path.isfile(filepath):
        print(f"FATAL: File {filepath} not found!")
        return None
    try:
        # Using pygame instead of simpleaudio to avoid segfault on Python 3.13+
        from pygame import mixer
        mixer.init()
        mixer.music.load(filepath)
        mixer.music.play()
        # Wait until playback is finished
        while mixer.music.get_busy():
            time.sleep(0.1)  # Small delay to prevent busy waiting
        mixer.quit()  # Clean up resources
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


def print_wall_times(counter):
    """Print All the timings together for consistency of output."""
    # if DISPLAY_RUN_STATS:
    print("display_run_stats():    Wall times (hh:mm:se.microsecs):")
    # TODO: Write to log for longer-term analytics

    # For wall time of std imports:
    std_stop_datetimestamp = datetime.now()
    std_elapsed_wall_time = std_stop_datetimestamp -  std_strt_datetimestamp
    print("Import of Python standard libraries: "+ \
        str(std_elapsed_wall_time))

    # For wall time of xpt imports:
    xpt_stop_datetimestamp = datetime.now()
    xpt_elapsed_wall_time = xpt_stop_datetimestamp -  xpt_strt_datetimestamp
    print("Import of Python extra    libraries: "+ \
        str(xpt_elapsed_wall_time))

    pgm_stop_datetimestamp = datetime.now()
    pgm_elapsed_wall_time = pgm_stop_datetimestamp -  pgm_strt_datetimestamp
    #pgm_stop_perftimestamp = time.perf_counter()
    print("Whole program run:                   "+ \
        str(pgm_elapsed_wall_time))



def load_env_variable(variable_name, env_file='~/python-samples.env') -> str:
    """Retrieve a variable from a .env file in Python without the external dotenv package.
    
    USAGE: my_variable = load_env_variable('MY_VARIABLE')
    Instead of like: api_key = os.getenv("API_KEY")
    TODO: Encrypt using a key in USB (Yubikey serial number)
    TODO: Add a parm to retrieve variable from cloud store (Pulumi/Akeyless/AWS Secret Manager, etc.)
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


def clipboard_from_string(text_in: str):
    """Copy text to the operating systen clipboard."""
    # alternative: import pyperclip.  # it's cross-platform
    pyperclip.copy(text_in)
    # if is_mocOS:
        # subprocess_tee of pbcopy CLI:
        #process = subprocess.Popen(
        #    'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        #process.communicate(text.encode('utf-8'))


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


def read_verse_from_csv( csv_filepath = "listen4cmd-verses.csv"):
    """Return row from csv."""
    row_seq = 5  # week_number. for example, get the 5th row (0-indexed, so this is the 6th row)
    # import csv
    # import itertools
    with open(csv_filepath, newline='') as csvfile:
        row = next(itertools.islice(csv.reader(csvfile), row_seq, None))
        print(row)
    verse = row
    return verse

def verse_lookup():
    """Lookup by calling api."""
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
    # Ookla’s Speedtest.net puts US 7th in the world by https://tradingeconomics.com/united-states/rural-population-percent-of-total-population-wb-data.html#:~:text=Rural%20population%20(%25%20of%20total,compiled%20from%20officially%20recognized%20sources.
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

## Logging
# https://www.structlog.org/en/stable/
# https://www.matthewstrawbridge.com/content/2024/python-logging-basic-better-best/

if __name__ == "__main__":

    # uv add python-dotenv
    # Load environment variables from .env file:
    # from dotenv import load_dotenv, find_dotenv

    asyncio.run(main())   # for log_async_http_response_time(url)

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
                # TODO: 'goodbye' for machine shutdown?
                print("    Bye Bye")
                exit()

            elif 'speed' in command_str:
                results = do_speedtest()

            elif 'verse' in command_str:
                verse=verse_random()
                print(f"    {verse}...")
                speech_to_text(verse)

            elif 'lights' in command_str and 'on' in command_str:
                light_num = 1
                action = "on"
                print(f"{philips_hue_action(light_num,action)}")
            elif 'lights' in command_str and 'off' in command_str:
                light_num = 1
                action = "off"
                print(f"{philips_hue_action(light_num,action)}")

            elif 'say' in command_str and 'time' in command_str:
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

            elif 'calculator' in command_str and 'plus' in command_str:
                result = run(["open", "-a", "Calculator Plus.app"], tee=True, text=True, capture_output=True)
                print("    Opening Calculator Plus...")
                # PROTIP: compound actions need to precede single commands.

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

            #elif: 'start' 'calendar' to create a new calendar entry starting at current time.

            # End of targeted actions.
            else:  # lookups from actions tuple = { "keyword": ["function", "parm"] } :
                tar = command_str  # target element in tuple, such as "github"  
                func, parm = actions_tuple.get(tar, (None, None))
                if SHOW_STATS:
                    print("STATS: len(actions_tuple) entries in actions_tuple!")
                if func:  # found:
                    if func == "website0":
                        url = f"https://{parm}/"
                        print(f"    Opening website to {url}...")
                        webbrowser.open(url)
                    elif func == "website":
                        url = f"https://www.{parm}/"
                        print(f"    Opening website to {url}...")
                        webbrowser.open(url)
                    elif func == "user_app":
                        url = f"../../Applications/{parm}"
                        print(f"    Opening {url}...")
                        result = run(["open", url], tee=True, text=True, capture_output=True)
                    elif func == "sys_app":
                        url = f"/Applications/{parm}"
                        print(f"    Opening {url}...")
                        result = run(["open", "-a", url], tee=True, text=True, capture_output=True)
                    else:  # action not found:
                        print(f"FATAL: action {func} needs to be added in actions_tuple!")
                        exit(9)
                else:  # action not found:
                    clipboard_from_string(command_str)
                    # TODO: Send unrecognized sentences to ChatGPT?
                    print("    ? clipped: command+V")  # Command not recognized!
        
        # loop again
    except KeyboardInterrupt:
        print("\ncontrol+C exiting listen4cmd.py gracefully.")


    if SHOW_STATS:
        print_wall_times()