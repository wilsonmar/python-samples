#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests",
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
   uv lock --upgrade               # to latest version available publicly
   uv sync

   chmod +x openrouter-models.py

   ruff check openrouter-models.py    # Fast Flake8, Black, isort, pydocstyle, pyupgrade, autoflake
   safety scan openrouter-models.py   # Check dependencies in pyproject.toml for bad CVEs
   semgrep --config=auto . --verbose  # Find code security errors using pattern-based analysis
   bandit -r ./my_project          # Security linter

BEFORE RUNNING, on Terminal EVERY TIME:
    uv run openrouter-models.py -p
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
__commit_date__ = "2026-05-06"
__commit_msg__ = "26-05-06 v005 csv filename @openrouter-models.py"
__repository__ = "https://github.com/wilsonmar/python-samples/blob/main/openrouter-models.py"
__status__ = "WORKING: ruff check openrouter-models.py => All checks passed!"


#### SECTION 03: imports from Python libraries:

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
import os
from pathlib import Path
import requests
import sys
import time


#### SECTION: App-specific functions

def get_openrouter_models(outfilepath) -> list:
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
    response = requests.get("https://openrouter.ai/api/v1/models")
    models = response.json()["data"]

    if not outfilepath:  # if filepath is empty
        filename_no_ext = os.path.splitext(os.path.basename(__file__))[0]
        outfilepath = f"{os.getcwd()}/{filename_no_ext}_{datetime.now().strftime('%Y%m%dT%H%M%S%s')}.csv"
        print(f"Default outfilepath={outfilepath}")
    with open(outfilepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["model_id", "name", "provider", "ctx", 
                                            "pricing_prompt", "pricing_completion", "is_free", "modalities"])
        writer.writeheader()
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

    # POLICY: Recognize parameter flags to optionally output files and reports.
    parser = argparse.ArgumentParser(description="Fetch and list OpenRouter models.")
    parser.add_argument("-s", "--silent", action="store_true", help="No run stats")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print run stats")
    parser.add_argument("-j", "--json", action="store_true", help="Print raw JSON model list")
    parser.add_argument("-m", "--models", action="store_true", help="Print models list with CTX")
    parser.add_argument("-p", "--providers", action="store_true", help="Print sorted providers with models count")
    args = parser.parse_args()

    utc_now = datetime.now(timezone.utc)
    local_now = datetime.now().astimezone()
    filename_no_ext = os.path.splitext(os.path.basename(__file__))[0]
    outfilepath = f"{os.getcwd()}/{filename_no_ext}-{utc_now.strftime('%Y%m%dT%H%M%S%Z')}.csv"
    
    if not args.silent:      # "-s", "--silent"
        # import sys
        current_module = sys.modules[__name__]
        if hasattr(current_module, "__file__"):
            print(f"At {current_module.__file__}")
        print(f"outfilepath={outfilepath}")
        # from datetime import datetime, timezone
        print(f"    {local_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"    {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    model_list = get_openrouter_models(outfilepath)
    if model_list is None:
        sys.exit()
    if args.json:        # "-j", "--json"
        print(f"model_list={model_list}")
    if args.models:      # "-m", "--models"
        list_openrouter_models(model_list)
    if args.providers:   # "-p", "--providers"
        list_openrouter_providers(model_list)

    if not args.silent:
        unique_providers = len(set(
            m["id"].split("/")[0] if "/" in m["id"] else "other"
            for m in model_list
        ))    
        elapsed = time.monotonic() - pgm_strt_elapsedsecs
        print(f"\nSUMMARY: {len(model_list)} models from {unique_providers} providers saved in {elapsed:.2f}s\nto {outfilepath}.")

"""
$ uv run openrouter-models.py
At /Users/johndoe/github-wilsonmar/python-samples/openrouter-models.py
outfilepath=/Users/johndoe/github-wilsonmar/python-samples/20260506T151542UTC.csv
    2026-05-06 09:15:42 MDT
    2026-05-06 15:15:42 UTC

SUMMARY: 370 models from 60 providers saved in 0.56s
to /Users/johndoe/github-wilsonmar/python-samples/20260506T151542UTC.csv.
"""