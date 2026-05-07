#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests",
# ]
# ///
# NOTE: Specific versions are defined in pyproject.toml for project.
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

#### SECTION 01: Define

"""orq-models.py here.

This Python program fetches https://router.orq.ai/models and parses its
embedded Framer CMS JSON data to produce a CSV of models and providers.
No API key is required — the model catalogue is publicly embedded in the
SSR HTML of the page.
See https://bomonike.github.io/ai-providers/

BEFORE RUNNING, on Terminal:
   git clone https://github.com/wilsonmar/python-samples.git --depth 1
   cd python-samples
   uv self update
   uv venv .venv
   source .venv/bin/activate
   uv lock --upgrade
   uv sync

   chmod +x orq-models.py

   ruff check orq-models.py
   safety scan orq-models.py

COMMAND-LINE ARGUMENTS:
    -h, --help              Show this help message and exit
    -s, --silent            Suppress run statistics (timestamp, filepath, summary)
    -v, --verbose           Print extra run statistics
    -j, --json              Print raw Python model list to stdout
    -m, --models            Print models table sorted by output cost (highest first)
    -p, --providers         Print providers table sorted alphabetically with model counts
    -o, --output FILE       CSV output filepath; .csv extension added if omitted
                            (default: orq-models-<UTC-timestamp>.csv)
    -b, --sort-by COLUMN    Column to sort by: input_cost or output_cost (default: output_cost)

SAMPLE COMMANDS:
    uv run orq-models.py -p                           # providers summary + timestamped CSV
    uv run orq-models.py -m                           # full models table + timestamped CSV
    uv run orq-models.py -mp                          # both tables
    uv run orq-models.py -p -o orq-models-latest      # save to orq-models-latest.csv
    uv run orq-models.py -m -b input_cost             # sort by input cost
    uv run orq-models.py -s -o /tmp/orq.csv           # silent, custom path
    # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate
    rm -rf .venv .pytest_cache __pycache__

"""
#### SECTION 02: Dunder variables for git command gxp to git add, commit, push

# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-05-06"
__commit_msg__ = "2026-05-06 v003 add am/pm @orq-models.py"
__repository__ = "https://github.com/wilsonmar/python-samples/blob/main/orq-models.py"
__status__ = "WORKING: ruff check orq-models.py => All checks passed!"


#### SECTION 03: Imports from Python libraries

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
import json
import os
import re
import requests
import sys
import time


#### SECTION: App-specific functions

# Framer CMS field key mapping (obfuscated keys decoded from the SSR payload)
_FIELD_PROVIDER    = "Hh2TO07Dx"
_FIELD_TYPE        = "sZeZ0UUzp"
_FIELD_LOCATION    = "yNZLxRkHG"
_FIELD_MODEL_ID    = "NkvMLBzXh"
_FIELD_DESCRIPTION = "VDpx5JpAP"
_FIELD_INPUT_COST  = "Aa_Bvvuy5"
_FIELD_OUTPUT_COST = "rpPXjmCFz"

_ORQ_MODELS_URL = "https://router.orq.ai/models"
_REQUEST_TIMEOUT_SECS = 30


def _resolve(data: list, idx: int):
    """Dereference a Framer SSR pointer: {type, value} -> actual value."""
    v = data[idx]
    if isinstance(v, dict) and "type" in v and "value" in v:
        return data[v["value"]]
    return v


def _to_float(val) -> float:
    """Safely coerce a raw Framer value to float, returning 0.0 on failure."""
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


def _fetch_html(url: str) -> str:
    """GET url with a browser-like User-Agent and return response text.

    Raises SystemExit with a descriptive message on any network or HTTP error.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=_REQUEST_TIMEOUT_SECS)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        raise SystemExit(
            f"ERROR: Request timed out after {_REQUEST_TIMEOUT_SECS}s — {url}"
        )
    except requests.exceptions.ConnectionError as exc:
        raise SystemExit(f"ERROR: Connection failed — {exc}")
    except requests.exceptions.HTTPError as exc:
        raise SystemExit(
            f"ERROR: HTTP {exc.response.status_code} {exc.response.reason} — {url}"
        )
    except requests.exceptions.RequestException as exc:
        raise SystemExit(f"ERROR: Request failed — {exc}")
    return resp.text


def _parse_framer_data(html: str) -> list:
    """Extract the Framer SSR JSON payload from the largest <script> block."""
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)
    # The data payload is the largest script block
    largest = max(scripts, key=len)
    return json.loads(largest)


def get_orq_models(outfilepath: str, sort_by: str = "output_cost") -> list[dict]:
    """Fetch router.orq.ai/models and return a list of model dicts.

    Column  Description:
    * provider      Primary infrastructure / API provider (e.g. openai, anthropic)
    * type          Capability type: chat | completion | embedding
    * location      Data-residency region (US, EU, apac, global …)
    * model_id      Model identifier used when routing requests
    * description   Human-readable model summary
    * input_cost    Cost per 1 M input tokens (USD)
    * output_cost   Cost per 1 M output tokens (USD)
    * is_free       TRUE when both input and output cost are 0
    """
    html = _fetch_html(_ORQ_MODELS_URL)
    data = _parse_framer_data(html)

    models = []
    seen: set[tuple] = set()

    for item in data:
        if not (isinstance(item, dict) and _FIELD_PROVIDER in item and _FIELD_MODEL_ID in item):
            continue
        provider   = _resolve(data, item[_FIELD_PROVIDER])
        model_id   = _resolve(data, item[_FIELD_MODEL_ID])
        key = (provider, model_id)
        if key in seen:
            continue
        seen.add(key)

        input_cost  = _to_float(_resolve(data, item[_FIELD_INPUT_COST]))
        output_cost = _to_float(_resolve(data, item[_FIELD_OUTPUT_COST]))
        models.append({
            "provider":    provider,
            "type":        _resolve(data, item[_FIELD_TYPE]),
            "location":    _resolve(data, item[_FIELD_LOCATION]),
            "model_id":    model_id,
            "description": _resolve(data, item[_FIELD_DESCRIPTION]),
            "input_cost":  input_cost,
            "output_cost": output_cost,
            "is_free":     input_cost == 0.0 and output_cost == 0.0,
        })

    # Sort by chosen cost column descending (highest first)
    models.sort(key=lambda m: m[sort_by], reverse=True)

    # Write CSV
    if not outfilepath:
        filename_no_ext = os.path.splitext(os.path.basename(__file__))[0]
        outfilepath = (
            f"{os.getcwd()}/{filename_no_ext}"
            f"_{datetime.now().strftime('%Y%m%dT%H%M%S')}.csv"
        )
        print(f"Default outfilepath={outfilepath}")

    with open(outfilepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "model_id", "provider", "type", "location",
                "input_cost", "output_cost", "is_free", "description",
            ],
        )
        writer.writeheader()
        for m in models:
            writer.writerow({
                "model_id":    m["model_id"],
                "provider":    m["provider"],
                "type":        m["type"],
                "location":    m["location"],
                "input_cost":  f"${m['input_cost']:.2f}",
                "output_cost": f"${m['output_cost']:.2f}",
                "is_free":     m["is_free"],
                "description": m["description"],
            })

    return models


def _fmt_cost(val: float) -> str:
    """Format a float cost as a dollar amount with two decimal places.

    Examples: 0.8 -> '$0.80', 1.25 -> '$1.25', 15.0 -> '$15.00'
    """
    return f"${val:.2f}"


def list_orq_models(models: list[dict], sort_by: str = "output_cost") -> None:
    """Print a human-readable table of ORQ models sorted by a cost column descending."""
    col_label = "IN" if sort_by == "input_cost" else "OUT"
    sorted_models = sorted(models, key=lambda m: m[sort_by], reverse=True)
    w = 96
    print(f"\n{'=' * w}")
    print(f"{'PROVIDER':<15} {'TYPE':<12} {'MODEL ID':<40} {'IN $/M':>10}  {'OUT $/M':>10}  {'FREE':>5}  (sorted by {col_label} $/M)")
    print(f"{'=' * w}")
    for m in sorted_models:
        provider  = (m["provider"] or "")[:14]
        mtype     = (m["type"] or "")[:11]
        model_id  = (m["model_id"] or "")[:39]
        inp       = _fmt_cost(m["input_cost"])
        out       = _fmt_cost(m["output_cost"])
        free      = "YES" if m["is_free"] else ""
        print(f"{provider:<15} {mtype:<12} {model_id:<40} {inp:>10}  {out:>10}  {free:>5}")
    print(f"{'=' * w}")
    print(f"Total models: {len(models)}")


def list_orq_providers(models: list[dict]) -> int:
    """Print providers sorted alphabetically with model counts.

    Returns the number of unique providers.
    """
    provider_counts = Counter(m["provider"] for m in models)
    sorted_providers = sorted(provider_counts.items())
    w = 50
    print(f"\n{'=' * w}")
    print(f"{'PROVIDER':<35} {'MODELS':>6}")
    print(f"{'=' * w}")
    for provider, count in sorted_providers:
        print(f"{provider:<35} {count:>6}")
    print(f"{'=' * w}")
    print(f"Unique providers: {len(sorted_providers)}")
    return len(sorted_providers)


#### SECTION: Main function run if this was not imported.

if __name__ == "__main__":

    # POLICY: Begin the monotonic (uptime) run timer as soon as the program starts.
    pgm_strt_elapsedsecs = time.monotonic()

    # POLICY: Recognize parameter flags to optionally output files and reports.
    parser = argparse.ArgumentParser(
        description=(
            "Fetch models and providers from https://router.orq.ai and save to CSV.\n"
            "No API key required — data is parsed from the public SSR page."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  uv run orq-models.py -p                           providers summary\n"
            "  uv run orq-models.py -m                           full models table (sort: output_cost)\n"
            "  uv run orq-models.py -m -b input_cost             full models table sorted by input_cost\n"
            "  uv run orq-models.py -mp -o snapshot              both tables, save to snapshot.csv\n"
            "  uv run orq-models.py -s  -o /tmp/orq.csv         silent, custom output path"
        ),
    )
    parser.add_argument("-s", "--silent",    action="store_true", help="No run stats")
    parser.add_argument("-v", "--verbose",   action="store_true", help="Print run stats")
    parser.add_argument("-j", "--json",      action="store_true", help="Print raw model list")
    parser.add_argument("-m", "--models",    action="store_true", help="Print models table")
    parser.add_argument("-p", "--providers", action="store_true", help="Print sorted providers with model count")
    parser.add_argument("-o", "--output",    metavar="FILE",      help="CSV output filepath (default: auto-timestamped)")
    parser.add_argument("-b", "--sort-by",   metavar="COLUMN",    default="output_cost",
                        choices=["input_cost", "output_cost"],
                        help="Sort column: input_cost or output_cost (default: output_cost)")
    args = parser.parse_args()

    utc_now   = datetime.now(timezone.utc)
    local_now = datetime.now().astimezone()
    if args.output:
        outfilepath = args.output
        if not outfilepath.endswith(".csv"):
            outfilepath += ".csv"
    else:
        filename_no_ext = os.path.splitext(os.path.basename(__file__))[0]
        outfilepath = (
            f"{os.getcwd()}/{filename_no_ext}"
            f"-{utc_now.strftime('%Y%m%dT%H%M%S%p%Z')}.csv"
        )

    if not args.silent:
        current_module = sys.modules[__name__]
        if hasattr(current_module, "__file__"):
            print(f"At {current_module.__file__}")
        print(f"outfilepath={outfilepath}")
        print(f"    {local_now.strftime('%Y-%m-%d %H:%M:%S%p%Z')}")
        print(f"    {utc_now.strftime('%Y-%m-%d %H:%M:%S%p%Z')}")

    sort_by = args.sort_by
    model_list = get_orq_models(outfilepath, sort_by)
    if model_list is None:
        sys.exit()

    if args.json:
        print(f"model_list={model_list}")
    if args.models:
        list_orq_models(model_list, sort_by)
    if args.providers:
        list_orq_providers(model_list)

    if not args.silent:
        unique_providers = len(set(m["provider"] for m in model_list))
        elapsed = time.monotonic() - pgm_strt_elapsedsecs
        print(
            f"\nSUMMARY: {len(model_list)} models from {unique_providers} providers "
            f"saved in {elapsed:.2f}s\nto {outfilepath}."
        )

"""
$ uv run orq-models.py -p
At /Users/johndoe/github-wilsonmar/python-samples/orq-models.py
outfilepath=/Users/johndoe/github-wilsonmar/python-samples/orq-models-20260506T172900UTC.csv
    2026-05-06 11:29:00 MDT
    2026-05-06 17:29:00 UTC

==================================================
PROVIDER                            MODELS
==================================================
alibaba                                 41
anthropic                               15
aws                                     36
azure                                   25
bytedance                                4
cerebras                                 7
cohere                                  22
contextualai                             3
deepseek                                 2
elevenlabs                               5
fal                                      4
google                                  38
google-ai                               22
groq                                    16
jina                                    12
leonardoai                               4
minimax                                  7
mistral                                 35
moonshotai                               6
openai                                  67
orq                                      1
perplexity                               4
togetherai                               7
xai                                     19
zai                                     11
==================================================
Unique providers: 25

SUMMARY: 413 models from 25 providers saved in 1.23s
to /Users/johndoe/github-wilsonmar/python-samples/orq-models-20260506T172900UTC.csv.
"""
