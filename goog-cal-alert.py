#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "google-auth",
#   "google-auth-oauthlib",
#   "google-api-python-client ",
#   "requests",
#   "schedule",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

#### SECTION 01: Define

"""goog-cal-alert.py here.

This Python program runs continuously so Alexa loudly announces before events in Google Calendar (which has faint noise).

https://staceyoniot.com/how-to-trigger-custom-alexa-notifications-from-a-smart-home-event/

BEFORE RUNNING, on iPhone Alexa app, enable "Notify Your Echo" skill.
BEFORE RUNNING, on browser:
   1. https://www.amazon.com/Thomptronics-Notify-Me/dp/B07BB2FYFS/ref=sr_1_1?s=digital-skills&ie=UTF8&qid=1541784577&sr=1-1&keywords=notify+me
   2. Link account
BEFORE RUNNING, on Alexa device:
   3. say "Alexa, open Notify Me" and the skill will introduce itself and send your access code via email from notifymyecho.com.
BEFORE RUNNING, on Terminal:
   # cd to a folder to receive folder (such as github-wilson):
   git clone https://github.com/wilsonmar/python-samples.git --depth 1
   cd python-samples
   # uv init was run to set pyproject.toml & .python-version 
   python3 -m pip install uv.      # once only for all programs
   python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
   uv venv .venv
   source .venv/bin/activate       # on macOS & Linux
        # ./scripts/activate       # PowerShell only
        # ./scripts/activate.bat   # Windows CMD only
   # Instead of pip install:
   uv add google-auth google-auth-oauthlib google-api-python-client requests schedule
   bandit -r ./github-wilsonmar/project-samples  # Sec linter for asserts
   safety scan goog-cal-alert.py                 # Check dependencies for CVEs (now requires login via internet)
   semgrep --config=auto       # Pattern-based analysis
   ruff check goog-cal-alert.py       # Based on pyproject.toml configs

   chmod +x goog-cal-alert.py
   uv run goog-cal-alert.py
      # -v for verbose
      # -vv to trace
      # Terminal should not freeze.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__
"""

#### SECTION 02: Dundar variables for git command gxp to git add, commit, push

# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-04-03"
__commit_msg__ = "26-04-03 v016 pyproject.toml configs :goog-cal-alert.py"
__repository__ = "https://github.com/bomonike/google/blob/main/goog-cal-alert.py"
# __repository__ = "https://github.com/wilsonmar/python-samples/blob/main/goog-cal-alert.py"
__status__ = "WORKING: ruff check goog-cal-alert.py => All checks passed!"
# STATUS: Python 3.13.3 working on macOS Sequoia 15.3.1

import datetime
import requests
import schedule
import time

#from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# POLICY: Store access code in ~/python-samples.env away from GitHub repo folder.
NOTIFY_ME_ACCESS_CODE = "your-notify-me-access-code"

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar_service():
    """Get Google Calendar Service."""
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("calendar", "v3", credentials=creds)

def send_alexa_alert(message: str):
    """Send notification to Alexa via Notify Me skill."""
    response = requests.post(
        "https://api.notifymyecho.com/v1/NotifyMe",
        json={
            "notification": message,
            "accessCode": NOTIFY_ME_ACCESS_CODE
        }
    )
    print(f"Alexa notified: {message} | Status: {response.status_code}")

def check_upcoming_events():
    """Check upcoming events."""
    service = get_calendar_service()

    now = datetime.datetime.utcnow()
    five_min_later = now + datetime.timedelta(minutes=5)
    ten_min_later = now + datetime.timedelta(minutes=10)

    # Fetch events in the 5–10 minute window ahead
    events_result = service.events().list(
        calendarId="primary",
        timeMin=five_min_later.isoformat() + "Z",
        timeMax=ten_min_later.isoformat() + "Z",
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        print("No upcoming events in 5 minutes.")
        return

    for event in events:
        title = event.get("summary", "Untitled Event")
        start = event["start"].get("dateTime", event["start"].get("date"))
        
        # Format time nicely
        start_dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
        local_time = start_dt.strftime("%I:%M %p")

        message = f"Heads up! {title} starts in 5 minutes at {local_time}"
        send_alexa_alert(message)

# Run check every 5 minutes:
schedule.every(5).minutes.do(check_upcoming_events)

# POLICY: Do not use deprecatd datetime.datetime.utcnow()
now = datetime.datetime.utcnow()
print(f"Calendar monitor goog-cal-alert.py running {now} UTC...")
while True:
    """Conntinuous loop."""
    schedule.run_pending()
    time.sleep(30)