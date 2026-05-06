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

   ruff check openrouter-models.py
   safety scan openrouter-models.py   # Check dependencies in pyproject.toml for bad CVEs
   semgrep --config=auto . --verbose  # Find code security errors using pattern-based analysis
   bandit -r ./my_project          # Security linter

BEFORE RUNNING, on Terminal EVERY TIME:
    uv run openrouter-models.py

    # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__

"""
#### SECTION 02: Dundar variables for git command gxp to git add, commit, push

# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-05-05"
__commit_msg__ = "26-05-05 v002 add model sort by CTX @openrouter-models.py"
__repository__ = "https://github.com/wilsonmar/python-samples/blob/main/openrouter-models.py"
__status__ = "WORKING: ruff check openrouter-models.py => All checks passed!"

# TODO: Add count of models from each provider, sorted alphabetically. The provider is the first part of model name separated by a slash.

#### SECTION 03: imports from Python libraries:

import argparse
import csv
import requests
import sys
import time


#### SECTION: App-specific functions

def get_openrouter_models() -> list:
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

    with open("openrouter_models.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["model_id", "name", "provider", "context_length", 
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


#### SECTION: Main function run if this was not imported.

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Fetch and list OpenRouter models.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print raw JSON model list")
    parser.add_argument("-m", "--models", action="store_true", help="Print models")
    parser.add_argument("-p", "--providers", action="store_true", help="Print sorted providers with models count")
    args = parser.parse_args()

    # POLICY: Begin the monotonic (uptime) run timer as soon as the program starts.
    pgm_strt_elapsedsecs = time.monotonic()  # uptime like 1208973.03808275 since the system was last booted.

    model_list = get_openrouter_models()
    if args.verbose:
        print(f"model_list={model_list}")
    if model_list is None:
        sys.exit()

    list_openrouter_models(model_list)

    elapsed = time.monotonic() - pgm_strt_elapsedsecs
    print(f"\nCompleted in {elapsed:.2f}s. CSV saved to openrouter_models.csv")

