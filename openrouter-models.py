#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   #psycopg2",
#   "requests",
#   "tenacity",
# ]
# ///
#   "openrouter",
#   "typing",
# NOTE: Specific versions are defined in pyproject.toml for project.
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

#### SECTION 01: Define

"""openrouter-models.py here.

This Python program calls OpenRouter.ai URL to retrieve a CSV file of its models.
See https://bomonike.github.io/ai-providers/

BEFORE RUNNING, on internet browser:
   At https://agentfactory.panaversity.org/docs/General-Agents-Foundations/general-agents/free-claude-setup
       OPENROUTER_API_KEY="..." (Models rotate with daily request limits)

   # POLICY: On the CLI Terminal, do not export system variables containing sensitive values, so they are not stored in CLI logs.

BEFORE RUNNING, on Terminal:
   # POLICY: Create a folder for git clone repositories to be created.
   git clone https://github.com/wilsonmar/python-samples.git --depth 1
   cd python-samples
   # uv init was run to set pyproject.toml & .python-version
   uv self update
   python3 -m pip install uv
   python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
   # POLICY: Add vulnerability scanning utilities. Fail if pyproject.toml and uv.lock are out of sync.
   uv add bandit safety semgrep dynaconf --frozen  # instead of pip install of utilities
   # POLICY: In production, uv sync --frozen --no-build installs project dependencies exactly as specified in the lockfile, without allowing any changes, with --no-build from source, only from pre-built .whl (wheel) executable binaries.

BEFORE RUNNING, on Terminal EVERY DAY:
   uv venv .venv                   # create folder .venv to import packages
   source .venv/bin/activate       # on macOS & Linux
        # ./scripts/activate       # PowerShell only
        # ./scripts/activate.bat   # Windows CMD only
   uv lock --upgrade               # to latest version available publicly, including SHA-256 hashes
   uv sync                         # Install dependencies

   chmod +x openrouter-models.py

   ruff check openrouter-models.py    # Fast Flake8, Black, isort, pydocstyle, pyupgrade, autoflake
   safety scan openrouter-models.py   # Check dependencies in pyproject.toml for bad CVEs
   semgrep --config=auto . --verbose  # Find code security errors using pattern-based analysis
   bandit -r ./openrouter-models.py   # Security linter

BEFORE RUNNING, on Terminal EVERY TIME:
    uv run openrouter-models.py -p -m
    # -s = --silent (no run statistics)
    # -j = --json to print JSON
    # -m = --models
    # -p = --providers to list providers
    # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__

"""
#### SECTION 02: Dundar variables for git command gxp to git add, commit, push

# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-05-08"
__commit_msg__ = "26-05-08 v008 [feat] + tenacity @openrouter-models.py"
__repository__ = "https://github.com/wilsonmar/python-samples/blob/main/openrouter-models.py"
__status__ = "WORKING: ruff check openrouter-models.py => All checks passed!"

# TODO: Store providers and models in PostgreSQL database.


#### SECTION 03: imports from Python libraries:

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
import logging
import os
import requests
import sys
import time
import re

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)
try:
    import psycopg2  # PostgreSQL library (optional)
except ImportError:
    psycopg2 = None  # type: ignore[assignment]


#### SECTION: Printing functions:  TODO: Move this to myutils.py module

def elapsed_time2format(seconds) -> str:
    """Format elapsed monotonic floating number to human-readable."""
    # seconds = time.monotonic()
    # import time
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    readable = f"{int(hours):02}:{int(minutes):02}:{secs:06.3f}"

    # POLICY: Match regex ^(00:)+ one or more 00 so groups at the start of the string are removed all at once:
    # import re  # regular expressions
    truncated = re.sub(r"^(00:)+", "", str(readable))  # 00:00:45.123 to 45.123
    return truncated

def craft_runid(args, utc_now) -> str:
    """Define Run ID as a GUID."""
    # Using utc_now captured at start of program run.
    if not args.silent:
        runid = utc_now.strftime('%Y%m%dT%H%M%S')  # UTC
        local_now = utc_now.astimezone()   # datetime.now().astimezone() would obtain another time.
        print(f"runid={runid} = {utc_now} {local_now} local time.") # like a GUID
    # TODO: Add base64?
    return runid

def define_outfilepath(args, runid) -> str:
    """Define output full filepath."""
    filename_no_ext = os.path.splitext(os.path.basename(__file__))[0]  # like "openrouter-models"
    outfilepath = f"{os.getcwd()}/{filename_no_ext}_{runid}.csv"
    #if not args.silent:     # "-s", "--silent"
    #    print(f"outfilepath={outfilepath}")
            # like outfilepath=/Users/johndoe/github-wilsonmar/python-samples/20260506T151542UTC.csv
    return outfilepath


def print_program_greeting(args, pgm_runid, elapsedsecs):
    """Print start-of-program greeting."""
    if not args.silent:     # "-s", "--silent"
        if args.verbose:
            local_now = utc_now.astimezone()
            print(f"RunID: {pgm_runid} at {local_now.strftime('%Y-%m-%d %H:%M:%S %p %Z')}" \
                f" = {utc_now.strftime('%Y-%m-%d %H:%M:%S %p %Z')}")
            print(f"From uptime: {elapsed_time2format(elapsedsecs)} ({elapsedsecs}).")

            # import sys
            current_module = sys.modules[__name__]
            if hasattr(current_module, "__file__"):
                print(f"At {current_module.__file__}")  
                # like "/Users/johndoe/github-wilsonmar/python-samples/openrouter-models.py

            print(f"TRACE: __commit_msg__={__commit_msg__}")


#### SECTION: App-specific functions

_LOG = logging.getLogger(__name__)

REQUEST_TIMEOUT_SECS = 30
MAX_RETRY_ATTEMPTS = 3

def _is_retryable_error(exc: BaseException) -> bool:
    """Return True for transient network/server errors worth retrying."""
    if isinstance(exc, requests.exceptions.HTTPError):
        return exc.response is not None and exc.response.status_code in {429, 500, 502, 503, 504}
    return isinstance(exc, (requests.exceptions.Timeout, requests.exceptions.ConnectionError))

@retry(
    retry=retry_if_exception(_is_retryable_error),
    stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    before_sleep=before_sleep_log(_LOG, logging.WARNING),
    reraise=True,
)
def _fetch_openrouter_response() -> requests.Response:
    """GET /api/v1/models with automatic retry/backoff on transient errors."""
    response = requests.get("https://openrouter.ai/api/v1/models", timeout=REQUEST_TIMEOUT_SECS)
    response.raise_for_status()
    return response


def get_openrouter_models(args, outfilepath) -> list | None:
    """List models in openrouter.ai.

    Column	Description:
    * model_id	Unique identifier for the model when making API calls
    * name	Human-readable display name
    * provider	Primary provider or organization offering the model
    * ctx = context_length	Maximum tokens the model can process (input + reasoning)
    * pricing_prompt	Cost per 1,000 input tokens (in USD)
    * pricing_completion	Cost per 1,000 output tokens (in USD)
    * is_free	TRUE if both input and output costs are $0
    * modalities	Supported input types (text, image, audio, video, file)
    """
    # POLICY: Use tenacity library for a common & simple way to request retries with backoff
    try:
        response = _fetch_openrouter_response()
    except requests.exceptions.Timeout:
        print(f"ERROR: Request timed out after {REQUEST_TIMEOUT_SECS}s ({MAX_RETRY_ATTEMPTS} attempts).")
        return None
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Could not connect to openrouter.ai ({MAX_RETRY_ATTEMPTS} attempts).")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP {e.response.status_code} from openrouter.ai.")
        return None
    models = response.json()["data"]

    if not outfilepath:  # if filepath parm is empty
        print("ERROR: outfilepath not provided!")
        return None

    with open(outfilepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["model_id", "name", "provider", "ctx", 
                                            "pricing_prompt", "pricing_completion", "is_free", "modalities"])
        writer.writeheader()
        # POLICY: Convert values in $/M columns to numeric before display
        for m in models:
            writer.writerow({
                "model_id": m["id"],
                "name": m["name"],
                "provider": m["id"].split("/")[0] if "/" in m["id"] else "other",
                "ctx": m["context_length"],
                "pricing_prompt": m["pricing"]["prompt"],
                "pricing_completion": m["pricing"]["completion"],
                "is_free": m["pricing"]["prompt"] == "0" and m["pricing"]["completion"] == "0",
                "modalities": ", ".join(m["architecture"].get("input_modalities", []))
            })
    return models


def list_openrouter_models(models: list) -> None:
    """Print a human-readable summary of OpenRouter models."""
    sorted_models = sorted(models, key=lambda m: m["context_length"], reverse=True)
    print(f"\n{'='*90}")
    print(f"{'MODEL ID':<45} {'NAME':<30} {'CTX':>8}  {'FREE':>5}")
    print(f"{'='*90}")
    for m in sorted_models:
        model_id = m["id"]
        name = m["name"][:29] if len(m["name"]) > 29 else m["name"]
        ctx = m["context_length"]
        is_free = m["pricing"]["prompt"] == "0" and m["pricing"]["completion"] == "0"
        print(f"{model_id:<45} {name:<30} {ctx:>8,}  {'YES' if is_free else '':>5}")
    print(f"{'='*90}")
    print(f"Total models: {len(models)}")


def list_openrouter_providers(models: list) -> int:
    """Print providers sorted alphabetically with model counts. Returns unique provider count."""
    provider_counts = Counter(
        m["id"].split("/")[0] if "/" in m["id"] else "other"
        for m in models
    )
    sorted_providers = sorted(provider_counts.items())
    print(f"\n{'='*50}")
    print(f"{'PROVIDER':<35} {'MODELS':>6}")
    print(f"{'='*50}")
    for provider, count in sorted_providers:
        print(f"{provider:<35} {count:>6}")
    print(f"{'='*50}")
    print(f"Unique providers: {len(sorted_providers)}")
    return len(sorted_providers)


#### SECTION: Main function run if this was not imported.

if __name__ == "__main__":

    # POLICY: Begin the monotonic (uptime) run timer as soon as the program starts.
    pgm_strt_elapsedsecs = time.monotonic()  # uptime like 1208973.03808275 since the system was last booted.
    
    # TODO: POLICY: Get a runid based on the pgm_start and a random plug for scalability.
    utc_now = datetime.now(timezone.utc)

    # POLICY: Recognize parameter flags to optionally output files and reports.
    parser = argparse.ArgumentParser(description="Fetch and list OpenRouter models.")
    parser.add_argument("-s", "--silent", action="store_true", help="No run stats")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print run stats")
    parser.add_argument("-j", "--json", action="store_true", help="Print raw JSON model list")
    parser.add_argument("-m", "--models", action="store_true", help="Print models list with CTX")
    parser.add_argument("-p", "--providers", action="store_true", help="Print sorted providers with models count")
    # TODO: Add a --sort-by flag to allow users to choose between sorting by input_cost or output_cost in the output.
    # TODO: Add a --help flag description of program parameters.
    args = parser.parse_args()

    pgm_runid = craft_runid(args, utc_now) # like a GUID
    # POLICY: Start program STDOUT output (if not silenced)
    print_program_greeting(args, pgm_runid, pgm_strt_elapsedsecs)
    outfilepath = define_outfilepath(args, pgm_runid)

    model_list = get_openrouter_models(args, outfilepath)
    if model_list is None:
        sys.exit("FATAL: models list not gen'd!")
    if args.json:        # "-j", "--json"
        print(f"model_list={model_list}")
    if args.models:      # "-m", "--models"
        list_openrouter_models(model_list)
    if args.providers:   # "-p", "--providers"
        list_openrouter_providers(model_list)

    if not args.silent:
        # Separate provider in front of slash and mordle id
        unique_providers = len(set(
            m["id"].split("/")[0] if "/" in m["id"] else "other"
            for m in model_list
        ))    
        elapsed = time.monotonic() - pgm_strt_elapsedsecs
        print(f"\nSUMMARY: {len(model_list)} models from {unique_providers} providers saved in {elapsed:.2f}s\nto {outfilepath}")

"""
$ uv run openrouter-models.py
runid=20260508T123443 = 2026-05-08 06:34:43.121395-06:00 local time.

SUMMARY: 367 models from 60 providers saved in 0.35s
to /Users/johndoe/github-wilsonmar/python-samples/openrouter-models_20260508T123443.csv
"""