#!/usr/bin/env python3
""" roku-set.py at https://github.com/wilsonmar/python-samples/blob/main/roku.py
STATUS: NOT WORKING. Opens YouTube with hard-coded values.
"v003 + flake8 fixes :roku-set.py"

This Python program sets a Roku device on the same network to a specific Youtube video."

"""

# pip install roku  # roku-4.1.0
from roku import Roku  # v3.1 Aug 4, 2019
    # https://pypi.org/project/roku/
    # https://github.com/jcarbaugh/python-roku
import time

# GLOBALS:
# Replace with your Roku's IP address
# obtained on Roku device connected using the same SSID as your computer.
# 1. Press the Home button on your remote to access the main menu.
# 2. Navigate to Settings. 3. Select Network. 4. Choose About.
# 5. Type below the IP address displayed on Roku's screen.
roku_id_discovered = Roku.discover()
    # [<Roku: 192.168.10.163:8060>, <Roku: 192.168.1.23:80>]
print(f"roku_id discovered: {roku_id_discovered}")

ROKU_IP = '192.168.1.14'
    # TODO: Ping ROKU_IP to test if valid.

# The part after 'v=' in the YouTube URL https://www.youtube.com/watch?v=nVULVZUuJOA
YOUTUBE_ID = 'nVULVZUuJOA'

# Connect to the Roku device
try:
    roku = Roku(ROKU_IP)
except Exception as e:
    print(f"failed {e}")

# roku.apps  # returns list of apps

# Launch the YouTube app
youtube_app = roku['YouTube']
# OUTPUT: <Application: [2285] Hulu Plus v2.7.6>

youtube_app.launch()

# Wait for the app to load
time.sleep(20)

# Navigate to the search function
roku.home()
time.sleep(5)

roku.down()
roku.select()

# Enter the video ID text:
roku.literal(YOUTUBE_ID)

# Start the video
roku.right()
roku.select()
