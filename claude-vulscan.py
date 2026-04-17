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
   # POLICY: Add vulnerability scanning utilities. Fail if pyproject.toml and uv.lock are out of sync.
   uv add bandit safety semgrep --frozen  # instead of pip install
   # POLICY: In production, uv sync --frozen --no-build installs project dependencies exactly as specified in the lockfile, without allowing any changes, with --no-build from source, only from pre-built .whl (wheel) executable binaries.

   ruff check claude-vulscan.py
   bandit -r ./my_project          # Security linter
   safety scan claude-vulscan.py          # Check dependencies in pyproject.toml for bad CVEs
   semgrep --config=auto .         # Pattern-based analysis

   chmod +x claude-vulscan.py
   uv run claude-vulscan.py -v -b -f "claude-vulscan.py"
      # -v for verbose, -b for bill (stats), -sl --sizelimit of code in bytes "1gb"
      # OPTIONAL: -pt for --prompt,
      # -f for file to --target for scanning (at end of CWD: /Users/johndoe/github-wilsonmar/python-samples/)
           # Not specifying -f would result in this program processing all .py files in the current folder
      # -m for --model ID recognized by Claude ("claude-opus-4-5" or "claude-sonnet-4-20250514")
      # Avg run time: Terminal should not freeze.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__

"""
#### SECTION 02: Dundar variables for git command gxp to git add, commit, push

# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-04-17"
__commit_msg__ = "26-04-17 v018 total bytes run @claude-vulscan.py"
__repository__ = "https://github.com/bomonike/google/blob/main/claude-vulscan.py"
# __repository__ = "https://github.com/wilsonmar/python-samples/blob/main/claude-vulscan.py"
__status__ = "WORKING: ruff check claude-vulscan.py => All checks passed!"
# STATUS: Python 3.13.3 working on macOS Sequoia 15.3.1

# based on https://github.com/trkonduri/vulscan/blob/master/claude-vulscan.py

# TODO: Display menu
# TODO: Make prompt text a variable.
# TODO: Get default model_id from ,env file.
# TODO: Add external enterprise robust logging
# TODO: import myutils  # in folder python-samples
# TODO: Track externally each request

# POLICY: Use of 3rd-party packages are limited to minimize potential supply chain attacks, 
import time
from pathlib import Path
import argparse
import os
import ssl
import httpx
from datetime import datetime, timezone  #, timedelta
from calendar import monthrange

import anthropic   # Anthropic Client SDK - from anthropic import Anthropic


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
        "--target", "-f",
        type=str,
        required=False,
        help="-t = --target file to process within current folder"
    )
    parser.add_argument(
        "--sizelimit", "-sl",
        type=str,
        required=False,
        help="-sl = --sizelimit of code other than default 2gb"
    )
    parser.add_argument(
        "--prompt", "-pt",
        type=str,
        required=False,
        help="-pt = --prompt of ext for AI to process"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="results.json",
        help="Output file path (default: results.json)"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        choices=["opus", "sonnet", "haiku", "gemma", "qwen", "kimi", "minimax"],
        default="opus",
        help="Nickname without model version"
    )
    # TODO: Specify model ids to open source model list.

    return parser.parse_args()


#### SECTION TODO: Move these functions to myutils.py and call the module.

def add_commas_in_int_string(number_string):
    """Add commas for thousands in a number within a string."""
    return f"{int(number_string):,}"  # Remove .2f if you don't want decimal places

def infer_from_utc(utc_timestamp) -> str:
    """Infer from system the local timestamp for UTC timestamp like 2026-04-16T21:58:31Z."""
    # from datetime import datetime
    utc_time = datetime.fromisoformat(utc_timestamp.replace("Z", "+00:00"))
    local_time = utc_time.astimezone()  # uses system timezone
    return local_time.strftime("%Y-%m-%d %I:%M:%S %p %Z %z")
       # See https://www.geeksforgeeks.org/python/python-strftime-function/

def parse_bytes(size_str: str) -> int:
    """Convert human-readable byte size string to number of bytes."""
    units = {
        'b': 1,
        'kb': 1024,
        'mb': 1024 ** 2,
        'gb': 1024 ** 3,
        'tb': 1024 ** 4,
        'pb': 1024 ** 5,
    }
    
    size_str = size_str.strip().lower()
    
    # Split number and unit:
    i = 0
    while i < len(size_str) and (size_str[i].isdigit() or size_str[i] == '.'):
        i += 1
    
    number = float(size_str[:i])
    unit = size_str[i:].strip()
    
    if unit not in units:
        raise ValueError(f"Unknown unit: '{unit}'. Valid units: {list(units.keys())}")
    
    return int(number * units[unit])

def format_bytes(num_bytes: int, precision: int = 2) -> str:
    """Convert number of bytes to human-readable string."""
    units = ['b', 'kb', 'mb', 'gb', 'tb', 'pb']

    value = float(num_bytes)
    for unit in units:
        if abs(value) < 1024 or unit == units[-1]:
            if unit == 'b':
                return f"{int(value)}b"
            formatted = f"{value:.{precision}f}".rstrip('0').rstrip('.')
            return f"{formatted}{unit}"
        value /= 1024
    return

def format_bytes_test():
    """Test format_bytes function."""
    print("parse_bytes tests:")
    # For use by 
    test_cases = [
        ("1kb", 1024),
        ("1mb", 1048576),
        ("1gb", 1073741824),
        ("1.5gb", 1610612736),
        ("512b", 512),
        ("2tb", 2199023255552),
    ]
    for s, expected in test_cases:
        result = parse_bytes(s)
        status = "✓" if result == expected else "✗"
        print(f"  {status} parse_bytes({s!r}) = {result} (expected {expected})")

    print("\nformat_bytes tests:")
    roundtrip = ["1kb", "1mb", "1gb", "2tb"]
    for s in roundtrip:
        b = parse_bytes(s)
        back = format_bytes(b)
        print(f"  {s!r} → {b} bytes → {back!r}")

    print("\nformat_bytes edge cases:")
    for b in [0, 500, 1023, 1536, 1048576 * 2.5]:
        print(f"  format_bytes({int(b)}) = {format_bytes(int(b))!r}")


def target_within_sizelimit(code_size,args) -> bool:
    """Format messages around True if file is within limit defined by args.sizelimit or default_sizelimit."""
    # Convert code_size to human-readable format like "2gb"
    code_size_formatted = format_bytes(code_size)
    if args.verbose:
        print(f"INFO: code file {args.target} contains {code_size_formatted} bytes ({add_commas_in_int_string(code_size)} characters)")

    if args.sizelimit:  # -sl specified in command parameter:
        code_size_limit = parse_bytes(args.sizelimit)
    else:  # TODO: Adjust sizelimit scientifically rather than a random default of "1gb".
        code_size_limit = parse_bytes("1gb")

    if code_size > code_size_limit:
        print(f"ERROR: code file {args.target} is larger than the {add_commas_in_int_string(code_size_limit)} character limit.")
        return False
    else:
        print(f"GREAT: code file {args.target} is within the {add_commas_in_int_string(code_size_limit)} character limit.")
        return True


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


def program_greeting(args,elapsedsecs):
    """Print start-of-program greeting."""
    if args.verbose:
        print(f"{get_user_local_timestamp()} Scanning file: \"{args.target}\" at uptime: {elapsed_time2format(elapsedsecs)} ({elapsedsecs}).")

# In the file handling section:
def safe_path(base: Path, target: str) -> Path:
    """Return whether input path is not escapable and thus safe to use."""
    resolved = (base / target).resolve()
    if not resolved.is_relative_to(base):
        raise ValueError(f"Path traversal detected: '{target}' escapes the base directory.")    
    return resolved



#### SECTION

def print_table(headers, rows, col_width=25):
    separator = "+" + "+".join(["-" * (col_width + 2)] * len(headers)) + "+"
    def format_row(cells):
        return "|" + "|".join(f" {str(c):<{col_width}} " for c in cells) + "|"
    
    print(separator)
    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))
    print(separator)


def run_is_within_budget(tokens_expected) -> bool:
    """
    Issue an Anthropic API to print out subscription token limits for the org.
    
    This is used instead of using the Console at https://platform.claude.com/usage
    Although Anthropic currently doesn't have a 'get subscription plan' endpoint,
    so we infer tier info from the rate limit headers returned on every API call.
    Limits are set at the organization level on the Limits page in the Claude Console.
    Rate limits differ by tier: Free (Tier 1) vs paid tiers (Tier 2, 3, 4).
    See: https://platform.claude.com/docs/en/api/rate-limits#spend-limits
    Under Anthropic's token bucket algorithm (https://en.wikipedia.org/wiki/Token_bucket)
    tiers are increased automatically as you reach certain thresholds while using the API.
    Maximum input and output tokens per minute vary by model version. 
    See https://platform.claude.com/settings/limits
    """
    # import anthropic
    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

    # Make a minimal API call to capture response headers
    response = client.messages.with_raw_response.create(
        model="claude-sonnet-4-20250514",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hi"}]
    )

    print("=== Anthropic Claude Organization Limits: Rate Limits on API capacity ===")
        # Also shown on GUI Console at https://platform.claude.com/settings/limits
    headers = response.headers
    # POLICY: Keep timestamps using GMT/UTC but convert to local time zone for printing out to user.
    token_reset_local_time = infer_from_utc(headers.get("anthropic-ratelimit-tokens-reset"))
    requests_local_time =    infer_from_utc(headers.get("anthropic-ratelimit-requests-reset"))
    print(f"requests_reset on : {requests_local_time} ({headers.get("anthropic-ratelimit-requests-reset")}) UTC")
    print(f"tokens_reset on   : {token_reset_local_time} ({headers.get("anthropic-ratelimit-tokens-reset")}) UTC")
    # Infer approximate tier from requests-per-minute limit:

    rpm = int(headers.get('anthropic-ratelimit-requests-limit'))
    # if limits["requests_limit"] else None
    if not rpm:
        print(f"No rpm to identify tier!")
        tier = "???"
    else:
        if rpm <= 50:
            tier = "Tier 1 (Build - likely free or new account)"
        elif rpm <= 1000:
            tier = "Tier 2 (Build)"
        elif rpm <= 2000:
            tier = "Tier 3 (Scale)"
        else:
            tier = "Tier 4 (Scale) or higher"
        # print(f"\nInferred tier: {tier}")
    limits = {
        "requests_limit"     : (f"{headers.get('anthropic-ratelimit-requests-limit')}",f"per minute = {tier}"),
        "input_tokens_limit" : (f"{headers.get('anthropic-ratelimit-input-tokens-limit')}","per minute"),
        "output_tokens_limit": (f"{headers.get('anthropic-ratelimit-output-tokens-limit')}","per minute"),

        "requests_remaining" : (f"{headers.get('anthropic-ratelimit-requests-remaining')}","-"),
        "tokens_limit"       : (f"{headers.get('anthropic-ratelimit-tokens-limit')}","-"),
        "tokens_remaining"   : (f"{headers.get('anthropic-ratelimit-tokens-remaining')}","-"),
    }
    for key, (value, extra) in limits.items():
        if value:
            extra_col = extra if extra else "N/A"
            print(f"  {key:<20}: {value:<8}  {extra_col:<9}")

    # NOTE: Claude.ai plans (Free/Pro/Team/Enterprise) are for the chat interface 
    # NOTE: Claude API accounts use a tiered system (Tier 1–4) based on usage history and spending, reflected in rate limits.
    # See https://docs.anthropic.com/en/api/rate-limits

    #print(f"ERROR: Not enough tokens to use {tokens_expected} tokens for this run.")
    #   return False   # DEBUGGING
    return True

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

    # Billing resets ond day 1 (the start) of each calendar month:
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


def obtain_file(args) -> str | None:
    """Obtain code of individual file targeted."""
    # POLICY: To block Traversal vulnerabilities, do not allow higher level part of path to be specified outside the program.
    # POLICY: Obtain the top part of the filepath from the operating system ("/User/johndoe/gh-wm/proj1/").
    if not args.target:
       print("-t or --target file name not specified!")
       return None 
    # POLICY: Use the cross-platform pathlib to concatenate parts of a filepath (rather than construct a string).
    # from pathlib import Path
    filepath = safe_path(Path.cwd() , args.target)
    if args.verbose:
       print(f"VERBOSE: filepath = \"{filepath}\"")

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
        file_size = len(code)
        if args.verbose:
           print(f"TRACE: code_from_file contains {file_size} characters.")
        if target_within_sizelimit(file_size,args):
            # POLICY: Limit **Unrestricted file read** Any file readable by the process can be scanned and its contents exfiltrated to the external API.
            print(f"TRACE: obtain_file() returning code with file_size {file_size}.")
            return code
        else:
            # ERROR message is issued by the called function so it can be customized using args settings.
            print(f"ERROR: obtain_file() returning None with file_size {file_size}.")
            return None


def scan_code(filepath: str, code: str, ai_model="claude-opus-4-5") -> dict:
    """Scan file using API call to Anthropic AI.
    
    CAUTION: **Sensitive data sent to external API** File contents are sent to Anthropic's API without sanitization. If scanned files contain secrets/credentials, they are exfiltrated.
    """
    print(f"TRACE: scan_code({len(code)} bytes, \"{ai_model}\" )")

    # TODO: POLICY: Specify correct max_tokens based on code size and tokens consumed?
    response = client.messages.create(
        model=ai_model,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"List only real security vulnerabilities in this Python file. Be concise.\n\n{code}"
        }]
    )
    # QUESTION: Still specify filepath here?
    return {"file": filepath, "findings": response.content[0].text}

def scan_project(directory: str):
    """Scan all .py files within the project folder."""
    # POLICY: To avoid errors, initiate with blanks all iterables at the top of function.
    results = []
    # TODO: FIXME: **Path Traversal in `scan_project()`** Uses `os.walk()` and `os.path.join()` without the `safe_path()` validation that `scan_file()` uses. An attacker-controlled `directory` argument could traverse outside intended boundaries.
    # **Path Traversal in `scan_project()`** (line 217-225): Uses `os.walk(directory)` without validating the `directory` argument against traversal attacks. The `safe_path()` call on line 223 uses `root` (from `os.walk`) as the base, not a fixed safe base directory, defeating the protection.
    # POLICY: Block path traversal attacking such as "../../etc/passwd" by not using os.walk()
    
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                # path = os.path.join(root, file)
                filepath = safe_path(root , file)
                if args.verbose:
                    print(f"scan_project filepath: {filepath}")
                result = scan_code(filepath, code_from_file, my_model)
                results.append(result)
                print(f"Scanned: {filepath}")
    """
    return results


if __name__ == "__main__":
    """Show claude-vulscan.py being used."""
    # POLICY: It's best practice to pass args from CLI call so the args structure is global.
    args = parse_args()    # read in arguments from command CLI using explicit passing.
    pgm_strt_elapsedsecs = time.monotonic()   # uptime like 1208973.03808275 since the system was last booted.
    # POLICY: Track the total number of bytes processed during entire program run to establish a time rate of processing.
    run_bytes_processed = 0

    # POLICY: Pass the entire global args structure into functions to work with.
    program_greeting(args,pgm_strt_elapsedsecs)

    # TODO: calc_tokens_expected() to be consumed during this run (based on prior runs).
    tokens_expected = 10
    # POLICY: Do not proceed if there is not enough tokens available within budget to run this.
    if not run_is_within_budget(tokens_expected):
        exit()

    # CAUTION: The entire file is in this string, which may consume more memory than allocated.
    # TODO: Get computer memory as basis for maximum code size allowed.
    code_from_file = obtain_file(args)  # individual file.
    if code_from_file is None:
        print(f"FATAL: code_from_file not valid!")
        exit()
    else:
        code_from_file_bytes = len(code_from_file)
        run_bytes_processed =+ code_from_file_bytes

    # POLICY: To secrets off logs, obtain api_keys by lookup from secrets manager rather than from CLI parameters.
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. "
            "Please export it before running this script."
        )
        exit(9)
    if args.verbose:
        # POLICY: Display the number of characters in secrets, not the whole string.
        print(f"TRACE: api_key (a secret) contains {len(api_key)} chars.")

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

    client = anthropic.Anthropic(api_key=api_key)
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
        findings = scan_code(args.target, code_from_file, my_model)  # individual file.
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
        print(f"Error: Unexpected return type from scan_code(): {e}")
        exit()
    except Exception as e:
        print(f"Unexpected error while scanning '{args.target}': {e}")
        exit()

    if args.bill:
        """Make API call to get rate limit headers."""
        # POLICY: Use a appropriate number of max_tokens when calling API for response headers, identified by experimentation.
        response = client.messages.create(
            model=my_model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        # Billing runs on a calendar month cycle — invoices are issued at the end of every calendar month via Stripe. 
        # The Cost Report endpoint requires an ANTHROPIC_ADMIN_KEY (sk-ant-admin...), which is different from a standard API key and can only be created by org admins in https://console.anthropic.com See https://www.youtube.com/watch?v=vgncj7MJbVU
        api_key = os.environ.get("ANTHROPIC_ADMIN_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_ADMIN_KEY is not set. "
                "Please export it before running this script."
            )
        result = get_billing_period(api_key)   # make the API call
        if result:
            print(f"\nFor model: \"{my_model}\" ")
            print(f"Billing period : {result['billing_period_start']} → {result['billing_period_end']}")
                       # 2026-04-01T00:00:00+00:00 → 2026-04-30T23:59:59+00:00
            print(f"  Days elapsed   : {result['days_elapsed']}")
            print(f"  Days remaining : {result['days_remaining']}")
            # FIXME: {'error': "Client error '401 Unauthorized' for url 'https://api.anthropic.com/v1/organizations/cost_report?starting_at=2026-04-01T00%3A00%3A00Z&ending_at=2026-04-16T06%3A01%3A31Z&bucket_width=1d'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401"}
            print(f"  Cost report    : {result['cost_report']}")

    if args.bill:
        tokens = get_token_usage(response)
        if tokens:
            print(f"  Tokens Input   : {tokens['input_tokens']}")
            print(f"  Tokens Output  : {tokens['output_tokens']}")
            print(f"  Tokens Total   : {tokens['total_tokens']}")

    pgm_stop_elapsedsecs = time.monotonic()
    pgm_took_elapsedsecs = pgm_stop_elapsedsecs - pgm_strt_elapsedsecs
    run_bytes_processed_fmt = format_bytes(run_bytes_processed)
    print(f"Run took {elapsed_time2format(pgm_took_elapsedsecs)} seconds to process {run_bytes_processed_fmt} lines of code.")

"""
uv run claude-vulscan.py -v -b -f "claude-vulscan.py"
2604162216 Scanning file: "claude-vulscan.py" at uptime: 353:12:54.759 (1271574.758982041).
=== Anthropic Claude Organization Limits: Rate Limits on API capacity ===
requests_reset on : 2026-04-16 10:16:58 PM MDT -0600 (2026-04-17T04:16:58Z) UTC
tokens_reset on   : 2026-04-16 10:16:58 PM MDT -0600 (2026-04-17T04:16:58Z) UTC
  requests_limit      : 50        per minute = Tier 1 (Build - likely free or new account)
  input_tokens_limit  : 30000     per minute
  output_tokens_limit : 8000      per minute
  requests_remaining  : 49        -        
  tokens_limit        : 38000     -        
  tokens_remaining    : 38000     -        
VERBOSE: filepath = "/Users/johndoe/github-wilsonmar/python-samples/claude-vulscan.py"
TRACE: code_from_file contains 29977 characters.
INFO: code file claude-vulscan.py contains 29.27kb bytes (29,977 characters)
GREAT: code file claude-vulscan.py is within the 1,073,741,824 character limit.
TRACE: obtain_file() returning code with file_size 29977.
TRACE: api_key (a secret) contains 108 chars.
TRACE: scan_code(29977 bytes, "claude-sonnet-4-20250514" )

========================================
claude-vulscan.py
1. **Sensitive data sent to external API** (line 431): File contents are transmitted to Anthropic's API without sanitization, potentially leaking secrets/credentials.

2. **Path traversal in scan_project()** (lines 449-466): Uses `os.walk(directory)` without validating the directory argument against traversal attacks.

3. **Missing exception handling** (lines 365, 520): `EnvironmentError` is raised but not caught, allowing execution to continue in undefined state.

4. **Unrestricted file access** (line 274): Any file readable by the process can be accessed via `--target` parameter and exfiltrated to external API.

For model: "claude-sonnet-4-20250514" 
Billing period : 2026-04-01T00:00:00+00:00 → 2026-04-30T23:59:59+00:00
  Days elapsed   : 17
  Days remaining : 14
  Cost report    : {'error': "Client error '401 Unauthorized' for url 'https://api.anthropic.com/v1/organizations/cost_report?starting_at=2026-04-01T00%3A00%3A00Z&ending_at=2026-04-17T04%3A17%3A03Z&bucket_width=1d'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401"}
  Tokens Input   : 8
  Tokens Output  : 10
  Tokens Total   : 18
Run took 00:00:06.331 seconds to process 12gb of code.
"""
# EOF