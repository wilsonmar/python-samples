#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "anthropic",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

#### SECTION 01: Define

"""claude-vulscan.py here.

This Python program scans Python code for vulnerabilities and errors using 
LLM models within Anthropic Claude, as described by
https://bomonike.github.io/claude-vulscan 

RISK ACCEPTED: **Potential sensitive data exposure in output** (line 178): The scanned file contents are sent to an external API and findings are printed to stdout, which could leak secrets if scanning files containing credentials.

Vulnerabilities Anthropic Claude is told to check for:
* **Injection** : SQL injection, command injection, LDAP injection
* **Secrets** : Hardcoded passwords, API keys, tokens
* **Crypto** : Weak hashing (MD5/SHA1), insecure random
* **Auth** : Broken auth, missing rate limiting
* **Input validation** : Missing sanitization, path traversal
* **Dependencies** : Outdated/vulnerable imports
* **Deserialization** : Unsafe `pickle`, `yaml.load()`
* **SSRF / XSS** : In web frameworks like Flask/Django

BEFORE RUNNING, on Terminal:
   export ANTHROPIC_API_KEY="..."
   export ANTHROPIC_ADMIN_KEY from console by org admins
   # cd to a folder to receive folder (such as github-wilson):
   git clone https://github.com/wilsonmar/python-samples.git --depth 1
   cd python-samples
   # uv init was run to set pyproject.toml & .python-version 
   python3 -m pip install uv
   python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
   uv venv .venv
   source .venv/bin/activate       # on macOS & Linux
        # ./scripts/activate       # PowerShell only
        # ./scripts/activate.bat   # Windows CMD only
   uv add bandit safety semgrep --frozen  # instead of pip install

   ruff check claude-vulscan.py
   bandit -r ./my_project          # Security linter
   safety scan claude-vulscan.py          # Check dependencies in pyproject.toml for bad CVEs
   semgrep --config=auto .         # Pattern-based analysis

   chmod +x claude-vulscan.py
   uv run claude-vulscan.py -v -b --target "claude-vulscan.py"
      # -v for verbose, -b for bill (stats)
      # --target for file to process (at end of CWD: /Users/johndoe/github-wilsonmar/python-samples/)
      # --model for model ID recognized by Claude ("claude-opus-4-5" or "claude-sonnet-4-20250514")
      # Avg run time: Terminal should not freeze.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__

"""
#### SECTION 02: Dundar variables for git command gxp to git add, commit, push

# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-04-15"
__commit_msg__ = "26-04-15 v014 + argparse cmd path @claude-vulscan.py"
__repository__ = "https://github.com/bomonike/google/blob/main/claude-vulscan.py"
# __repository__ = "https://github.com/wilsonmar/python-samples/blob/main/claude-vulscan.py"
__status__ = "WORKING: ruff check claude-vulscan.py => All checks passed!"
# STATUS: Python 3.13.3 working on macOS Sequoia 15.3.1

# based on https://github.com/trkonduri/vulscan/blob/master/claude-vulscan.py

#import myutils  # in folder python-samples

import time
from pathlib import Path
import argparse
import os
import ssl
import httpx
from datetime import datetime, timezone  #, timedelta
from calendar import monthrange

from anthropic import Anthropic


# Global default values:
my_model="claude-sonnet-4-20250514" # "claude-opus-4-5"   # "mythos" when available 

# defaults overriden by command:
def parse_args():
    """Read parameters from command CLI."""
    parser = argparse.ArgumentParser(
        description="Claude vulnerability scanner"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--bill", "-b",
        action="store_true",
        help="Enable billing output"
    )
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="Target to scan (e.g. a file path or URL)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results.json",
        help="Output file path (default: results.json)"
    )
    parser.add_argument(
        "--severity",
        type=str,
        choices=["low", "medium", "high", "critical"],
        default="medium",
        help="Minimum severity level to report"
    )

    return parser.parse_args()

def get_token_usage(response) -> dict:
    """Extract token usage from an Anthropic API response."""
    usage = response.usage
    return {
        "input_tokens":  usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "total_tokens":  usage.input_tokens + usage.output_tokens
    }

def get_billing_period(admin_api_key: str) -> dict:
    """
    Return the current billing period (calendar month).

    Also fetches usage cost from Anthropic's Cost Report API.
    Requires an Admin API key (sk-ant-admin...) from the Claude Console.
    """
    now = datetime.now(timezone.utc)

    # Billing resets at the start of each calendar month
    period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day = monthrange(now.year, now.month)[1]
    period_end = now.replace(day=last_day, hour=23, minute=59, second=59, microsecond=0)
    days_remaining = (period_end - now).days + 1

    # Query Anthropic Cost Report API for this billing period
    url = "https://api.anthropic.com/v1/organizations/cost_report"
    headers = {
        "x-api-key": admin_api_key,
        "anthropic-version": "2023-06-01",
    }
    params = {
        "starting_at": period_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ending_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bucket_width": "1d",
    }

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=10.0)
        response.raise_for_status()
        cost_data = response.json()
    except httpx.HTTPStatusError as e:
        cost_data = {"error": str(e)}
    except httpx.RequestError as e:
        cost_data = {"error": f"Request failed: {e}"}

    return {
        "billing_period_start": period_start.isoformat(),
        "billing_period_end": period_end.isoformat(),
        "days_elapsed": now.day,
        "days_remaining": days_remaining,
        "queried_at": now.isoformat(),
        "cost_report": cost_data,
    }


def get_user_local_timestamp(format_str: str = "yymmddhhmm") -> str:
    """Return a string formatted with datetime stamp in local timezone.

    Not used in logs which should be in UTC.
    Example: "07:17 AM (07:17:54) 2025-04-21 MDT"
    """
    current_time = time.localtime()  # localtime([secs])
    year = str(current_time.tm_year)[-2:]  # Last 2 digits of year
    month = str(current_time.tm_mon).zfill(2)  # .zfill(2) = zero fill
    day = str(current_time.tm_mday).zfill(2)  # Day with leading zero
    hour = str(current_time.tm_hour).zfill(2)  # Day with leading zero
    minute = str(current_time.tm_min).zfill(2)  # Day with leading zero
    if format_str == "yymmdd":
        return f"{year}{month}{day}"
    if format_str == "yymmddhhmm":
        return f"{year}{month}{day}{hour}{minute}"

def elapsed_time2format(seconds) -> str:
    """Format elapsed monotonic floating number to human-readable."""
    # seconds = time.monotonic()
    # import time
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    readable = f"{int(hours):02}:{int(minutes):02}:{secs:06.3f}"
    return readable  # e.g. 00:03:45.123

def safe_path(base: Path, target: str) -> Path:
    """Return whether input path is not escapable and thus safe to use."""
    resolved = (base / target).resolve()
    if not resolved.is_relative_to(base):
        raise ValueError(f"Path traversal detected: '{target}' escapes the base directory.")    
    return resolved

def scan_file(file_target: str, ai_model="claude-opus-4-5") -> dict:
    """Scan file using API call to Anthropic AI."""
    # POLICY: To block Traversal vulnerabilities, do not allow higher level part of path to be specified outside the program.
    # POLICY: Obtain the top part of the filepath from the operating system ("/User/johndoe/gh-wm/proj1/").
    if not file_target:
       print("--target file name not specified!")
       return None 
    # POLICY: Use the cross-platform pathlib to concatenate parts of a filepath.
    # from pathlib import Path
    filepath = safe_path(Path.cwd() , file_target)
    if args.verbose:
       print(f"filepath = \"{filepath}\"")

    # TODO: try @retries
    try:
        with open(filepath, "r") as f:
            code = f.read()
    # POLICY: Catch specific exceptions for better debugging.
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None  # or raise, or sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied to read '{filepath}'.")
        return None
    except IsADirectoryError:
        print(f"Error: '{filepath}' is a directory, not a file.")
        return None
    except UnicodeDecodeError as e:
        print(f"Error: Unable to decode file '{filepath}': {e}")
        return None
    except OSError as e:
        print(f"Error: OS error while reading '{filepath}': {e}")
        return None

    # POLICY: Before proceeding, use Guard check to ensure code to be processed did not encounter exception.
    if code is None:
        return None
    else:
        if args.verbose:
            print(f"code contains {len(code)} characters.")
        # IGNORE POLICY: **Unrestricted file read** Any file readable by the process can be scanned and its contents exfiltrated to the external API.
        # **Sensitive data sent to external API** File contents are sent to Anthropic's API without sanitization. If scanned files contain secrets/credentials, they are exfiltrated.

    # TODO: POLICY: Specify correct max_tokens=1024,
    response = client.messages.create(
        model=ai_model,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"List only real security vulnerabilities in this Python file. Be concise.\n\n{code}"
        }]
    )
    return {"file": filepath, "findings": response.content[0].text}

def scan_project(directory: str):
    """Scan project."""
    results = []
    # FIXME: **Path Traversal in `scan_project()`** Uses `os.walk()` and `os.path.join()` without the `safe_path()` validation that `scan_file()` uses. An attacker-controlled `directory` argument could traverse outside intended boundaries.
    # **Path Traversal in `scan_project()`** (line 217-225): Uses `os.walk(directory)` without validating the `directory` argument against traversal attacks. The `safe_path()` call on line 223 uses `root` (from `os.walk`) as the base, not a fixed safe base directory, defeating the protection.
    # POLICY: Block path traversal attacking such as "../../etc/passwd" by not using os.walk()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                # path = os.path.join(root, file)
                filepath = safe_path(root , file)
                if args.verbose:
                    print(f"scan_project filepath: {filepath}")
                result = scan_file(filepath)
                results.append(result)
                print(f"Scanned: {filepath}")
    return results


if __name__ == "__main__":
    """Show claude-vulscan.py being used."""
    pgm_strt_elapsedsecs = time.monotonic()   # uptime like 1208973.03808275 since the system was last booted.

    args = parse_args()    # read in arguments from command CLI.
    if args.verbose:
        print(f"{get_user_local_timestamp()} Scanning file: \"{args.target}\" at uptime {elapsed_time2format(pgm_strt_elapsedsecs)} ({pgm_strt_elapsedsecs}).")

    # POLICY: Do not obtain api_key via parameters so secrets don't end up in logs.
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. "
            "Please export it before running this script."
        )
        # effectively exit(9)
    if args.verbose:
        # POLICY: Display the number of characters in secrets, not the whole string.
        print(f"api_key (a secret) contains {len(api_key)} chars.")

    # Create SSL context with strict verification:
    ssl_context = ssl.create_default_context()
    ssl_context.verify_mode = ssl.CERT_REQUIRED  # reject connections with invalid/missing certificates
    ssl_context.check_hostname = True  # ensure the certificate hostname matches the server

    # Optionally pin to a specific CA bundle instead of system defaults (stronger protection against MITM):
    # ssl_context.load_verify_locations("/path/to/ca-bundle.crt")

    # Pass custom httpx client with SSL context to Anthropic:
    http_client = httpx.Client(
        verify=ssl_context,
        timeout=30.0
    )

    client = Anthropic(api_key=api_key)
    # client = Anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    # POLICY: Ensure that the API KEY is available, and raise error if not.
    if not client:
        print("Client not established!")
        exit()
    # else: client="<anthropic.Anthropic object at 0x1085e0050>""
    
    # rest of your logic, e.g.:
    # run_scan(args.target, args.severity)
    # save_results(results, args.output)

    # findings = scan_project(my_project_path)
       # TODO: read csv file to process

    try:
        findings = scan_file(args.target)  # individual file.
        print(f"\n{'='*40}\n{findings['file']}\n{findings['findings']}")
    except FileNotFoundError:
        print(f"Error: Target file '{args.target}' not found.")
        exit()
    except PermissionError:
        print(f"Error: Permission denied to access '{args.target}'.")
        exit()
    except KeyError as e:
        print(f"Error: Expected key missing in scan results: {e}")
        exit()
    except TypeError as e:
        print(f"Error: Unexpected return type from scan_file(): {e}")
        exit()
    except Exception as e:
        print(f"Unexpected error while scanning '{args.target}': {e}")
        exit()

    # Usage example
    response = client.messages.create(
        model=my_model,
        max_tokens=1000,
        messages=[{"role": "user", "content": "Hello!"}]
    )

    if args.bill:
        # Billing runs on a calendar month cycle — invoices are issued at the end of every calendar month via Stripe. 
        # The Cost Report endpoint requires an ANTHROPIC_ADMIN_KEY (sk-ant-admin...), which is different from a standard API key and can only be created by org admins in the Console.
        api_key = os.environ.get("ANTHROPIC_ADMIN_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_ADMIN_KEY is not set. "
                "Please export it before running this script."
            )
        result = get_billing_period(api_key)
        if result:
            print(f"Period:        {result['billing_period_start']} → {result['billing_period_end']}")
            print(f"Days elapsed:  {result['days_elapsed']}")
            print(f"Days remaining:{result['days_remaining']}")
            print(f"Cost report:   {result['cost_report']}")

    if args.bill:
        tokens = get_token_usage(response)
        if tokens:
            print("\nFor model: {my_model}:")
            print(f"    Tokens Input  : {tokens['input_tokens']}")
            print(f"    Tokens Output : {tokens['output_tokens']}")
            print(f"    Tokens Total  : {tokens['total_tokens']}")

    pgm_stop_elapsedsecs = time.monotonic()
    pgm_took_elapsedsecs = pgm_stop_elapsedsecs - pgm_strt_elapsedsecs
    print(f"\nRun took {elapsed_time2format(pgm_took_elapsedsecs)} seconds.")

# EOF