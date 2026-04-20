#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "anthropic",
#   "certifi",
#   "openai",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

#### SECTION 01: Define

"""claude-vulscan.py here.

This Python program calls Anthropic Claude APIs to obtain status and to 
scan Python code for vulnerabilities.
Additional LLM models 
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

BEFORE RUNNING, on internet browser:
   At https://platform.claude.com/settings/organization click "Set up organization".
   Answer questions about country, usage, etc. Submit to "Allow creating new API keys in default workspace".
   At https://platform.claude.com/settings/admin-keys click "Create admin key". Name such as "admin261231"
   Click "Copy key" and paste in your secrets manager or file ~/.secrets.env specified in .gitignore.
   The value is retrieved by code as api03="supersecret"
   ANTHROPIC_ADMIN_KEY="sk-ant-admin01-..." from console by org admins
   ANTHROPIC_API_KEY="sk-ant-api03-..."
   # POLICY: On the CLI Terminal, do not export system variables containing sensitive values, so they are not stored in CLI logs.

BEFORE RUNNING, on Terminal:
   # POLICY: Create a folder for git clone repositories to be created.
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
   uv add bandit safety semgrep dynaconf --frozen  # instead of pip install of utilities
   # POLICY: In production, uv sync --frozen --no-build installs project dependencies exactly as specified in the lockfile, without allowing any changes, with --no-build from source, only from pre-built .whl (wheel) executable binaries.

   ruff check claude-vulscan.py
   bandit -r ./my_project          # Security linter
   safety scan claude-vulscan.py   # Check dependencies in pyproject.toml for bad CVEs
   semgrep --config=auto .         # Pattern-based analysis

   chmod +x claude-vulscan.py
   uv run claude-vulscan.py -v -vv -b -m "haiku" -f "claude-vulscan.py"
      # -v for verbose, -b for bill (stats), -sl --sizelimit of code in bytes "1gb"
      # OPTIONAL: -pt for --prompt, -r --recursive,
      # -f for file to --target for scanning (at end of CWD: /Users/johndoe/github-wilsonmar/python-samples/)
           # Not specifying -f would result in this program processing all .py files in the current folder
      # -m for --model ID recognized by Claude ("claude-opus-4-7" or "claude-sonnet-4-20250514")
      # --nometric to not write csv file of results for each call.
      # Avg run time: Terminal should not freeze.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__

"""
#### SECTION 02: Dundar variables for git command gxp to git add, commit, push

# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-04-20"
__commit_msg__ = "26-04-20 v023 after warp changes @claude-vulscan.py"
__repository__ = "https://github.com/bomonike/google/blob/main/claude-vulscan.py"
# __repository__ = "https://github.com/wilsonmar/python-samples/blob/main/claude-vulscan.py"
__status__ = "WORKING: ruff check claude-vulscan.py => All checks passed!"
# STATUS: Python 3.13.3 working on macOS Sequoia 15.3.1

# based on https://github.com/trkonduri/vulscan/blob/master/claude-vulscan.py

# TODO: Display menu of CLI parameters.
# TODO: Get default model_id from .env file.
# TODO: Add external enterprise robust logging
# TODO: import myutils  # in folder python-samples
# TODO: Track externally history of requests & responses metrics for trending
# batch https://platform.claude.com/docs/en/api/sdks/python#getting-results-from-a-batch

import argparse
from calendar import monthrange
import base64
import csv
from datetime import datetime, timezone  #, timedelta
import httpx
# import json
import os
from pathlib import Path
import re
import requests
import ssl
import sys
import time

# POLICY: Use of 3rd-party packages are limited to minimize potential supply chain attacks, 
import anthropic   # Anthropic Client SDK - from anthropic import Anthropic
import certifi
from dotenv import load_dotenv  # install python-dotenv
from openai import OpenAI

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
        "--trace", "-vv",
        action="store_true",
        help="Enable detailed trace output"
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
        "--recursive", "-r",
        type=str,
        required=False,
        help="-r = --recursive process sub-folders too."
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
        "--nometric",
        type=str,
        required=False,
        help="--nometric write to csv file"
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
        choices=["opus", "sonnet", "haiku", "gemma", "qwen", "kimi", "minimax", "mistral"],
        default="opus",
        help="-m = --model alias without model version"
    )
    # POLICY: No processing occurs if neither -r nor -f is specified.
    return parser.parse_args()


#### SECTION TODO: Move these functions to myutils.py and call the module.

def elapsedsecs_timestamp():
    """Capture timestamp for  elapsed time."""
    # POLICY: Use a common function to capture elapsed timestamps to ensure method is consistent.
    # POLICY: Capture start time for measuring standard python library load time.
    # NOTE: time.time() has been obsoleted.
    # from time import perf_counter_ns
    return time.monotonic()

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

def format_elapsed_time(time_str: str) -> str:
    """Format elapsed time."""
    # Remove leading "00:" groups
    # import re
    result = re.sub(r'^(00:)+', '', str(time_str))
    return result

def elapsed_time2format(seconds) -> str:
    """Format elapsed monotonic floating number to human-readable."""
    # seconds = time.monotonic()
    # import time
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    readable = f"{int(hours):02}:{int(minutes):02}:{secs:06.3f}"

    # POLICY: Match regex ^(00:)+ one or more 00 so groups at the start of the string are removed all at once:
    # import re  # regular expression
    truncated = re.sub(r'^(00:)+', '', str(readable))  # 00:00:45.123 to 45.123
    return truncated


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



def print_table(headers, rows, col_width=25):
    """Print table with lines."""
    separator = "+" + "+".join(["-" * (col_width + 2)] * len(headers)) + "+"
    def format_row(cells):
        return "|" + "|".join(f" {str(c):<{col_width}} " for c in cells) + "|"
    
    print(separator)
    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))
    print(separator)



#### SECTION files and folder handling utilities



#### SECTION 03 - .env file


def open_env_file(global_env_path: str) -> str:
    """Load global variables from .env file based on hard-coded default location.

    Args: global ENV_FILE
    See https://wilsonmar.github.io/python-samples/#envLoad
    See https://stackoverflow.com/questions/40216311/reading-in-environment-variables-from-an-environment-file
    """
    # from pathlib import Path
    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        global_env_path = None
        print(f'FATAL: {sys._getframe().f_code.co_name}(): global_env_path: not at "{global_env_path}" ')
        exit()

    # from dotenv import load_dotenv
    # See https://www.python-engineer.com/posts/dotenv-python/
    # See https://pypi.org/project/python-dotenv/
    load_dotenv(global_env_path)  # using load_dotenv
    # Wait until variables for print_trace are retrieved:
    print(f'VERBOSE: {sys._getframe().f_code.co_name}(): global_env_path=\"{global_env_path}\" ')
    return


def get_str_from_env_file(key_in: str) -> str:
    """Return a value of string data type from OS environment or .env file."""
    # load the .env file:
    # load_dotenv(Path.home() / "python-samples.env")

    # retrieve a variable like key_in = "API_KEY":
    env_value = os.getenv(key_in)

    # POLICY: Display only first 3 characters of a potentially secret long string.
    # if len(env_var) > 5:
    #     print_("TRACE: (key_in + "=\"" + str(env_var[:5]) +" (remainder removed)")
    # else:
    #     print("TRACE: (key_in + "=\"" + str(env_var) + "\" from .env")
    #     return str(env_var)

    return env_value


def safe_path(base: Path, target: str) -> Path:
    """Return file path if it's resolved as not escapable and thus safe to use."""
    resolved = (base / target).resolve()
    if not resolved.is_relative_to(base):
        raise ValueError(f"Path traversal detected: '{target}' escapes the base directory.")
        return None
    # TODO: Apply scan on file
    return resolved


def read_github_repo(owner, repo, branch="main", token=None):
    """
    Read all files within a public GitHub repo via the GitHub API.
    
    files = read_github_repo("owner", "repo-name")
    for path, content in files.items():
        print(f"--- {path} ---")
        print(content[:500])  # Print first 500 chars of each file

    Args:
        owner: GitHub username or org (e.g. "torvalds")
        repo: Repository name (e.g. "linux")
        branch: Branch name (default "main")
        token: Optional GitHub personal access token (for private repos / higher rate limits)
    """
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        # POLICY: Validate token to prevent HTTP header injection.
        # GitHub tokens (classic PATs, fine-grained, OAuth) are alphanumeric + underscores/hyphens only.
        if not re.match(r'^[\w\-]+$', token):
            raise ValueError("GitHub token contains invalid characters.")
        headers["Authorization"] = f"Bearer {token}"

    base_url = f"https://api.github.com/repos/{owner}/{repo}"

    def get_files(path=""):
        url = f"{base_url}/contents/{path}?ref={branch}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        files = {}
        for item in response.json():
            if item["type"] == "file":
                # Fetch and decode file content
                file_response = requests.get(item["url"], headers=headers)
                file_response.raise_for_status()
                content = base64.b64decode(file_response.json()["content"]).decode("utf-8", errors="replace")
                files[item["path"]] = content
            elif item["type"] == "dir":
                # Recurse into subdirectory
                files.update(get_files(item["path"]))
        
        return files

    return get_files()


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


#### SECTION

def _make_anthropic_client(api_key: str) -> anthropic.Anthropic:
    """Create an Anthropic client with strict SSL verification via certifi CA bundle.

    POLICY: Always pass an explicit httpx.Client so SSL hardening is active for every
    Anthropic API call. Using anthropic.Anthropic() without http_client uses the SDK's
    default transport which does not enforce our certificate pinning policy.
    """
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.load_verify_locations(certifi.where())
    ssl_ctx.verify_mode = ssl.CERT_REQUIRED
    ssl_ctx.check_hostname = True
    http_client = httpx.Client(verify=ssl_ctx, timeout=30.0)
    return anthropic.Anthropic(api_key=api_key, http_client=http_client)


def _extract_anthropic_error_message(err: Exception) -> str:
    """Return the human-readable `error.message` from an Anthropic APIStatusError, or ''.

    The SDK wraps HTTP errors with a `.response` httpx.Response; its JSON body looks like
    {"type": "error", "error": {"type": "invalid_request_error", "message": "..."}}.
    We defensively try multiple access paths so a malformed body never masks the original
    exception from the caller's except-block.
    """
    # Preferred: parse the response body.
    response = getattr(err, "response", None)
    if response is not None:
        try:
            body = response.json()
            if isinstance(body, dict):
                error_obj = body.get("error") or {}
                if isinstance(error_obj, dict):
                    msg = error_obj.get("message")
                    if isinstance(msg, str) and msg:
                        return msg
        except (ValueError, AttributeError):
            pass
    # Fallback: SDK-populated attribute, then str(err).
    msg = getattr(err, "message", None)
    if isinstance(msg, str) and msg:
        return msg
    return str(err) if err else ""


def resolve_model_family(alias: str) -> dict:
    """Resolve model info from input model_family."""
    client_api_key = get_str_from_env_file("ANTHROPIC_API_KEY")
    client = _make_anthropic_client(client_api_key)
    client_api_key = ""
    # import anthropic
    try:
        model = client.models.retrieve(alias)
        return {
            "id": model.id,
            "display_name": model.display_name,
            "type": model.type,
            "created_at": model.created_at.isoformat() if isinstance(model.created_at, datetime) else model.created_at,
            "max_input_tokens": model.max_input_tokens,
            "max_tokens": model.max_tokens,
            "capabilities": {
                "batch": model.capabilities.batch.supported if model.capabilities else None,
                "citations": model.capabilities.citations.supported if model.capabilities else None,
                "code_execution": model.capabilities.code_execution.supported if model.capabilities else None,
                "image_input": model.capabilities.image_input.supported if model.capabilities else None,
                "pdf_input": model.capabilities.pdf_input.supported if model.capabilities else None,
                "structured_outputs": model.capabilities.structured_outputs.supported if model.capabilities else None,
                "thinking": model.capabilities.thinking.supported if model.capabilities else None,
                "effort": model.capabilities.effort.supported if model.capabilities else None,
            } if model.capabilities else None,
        }
        """ print(json.dumps(result_json, indent=2))
        ModelInfo(id='claude-sonnet-4-20250514', capabilities=ModelCapabilities(batch=CapabilitySupport(supported=True), citations=CapabilitySupport(supported=True), code_execution=CapabilitySupport(supported=False), context_management=ContextManagementCapability(clear_thinking_20251015=CapabilitySupport(supported=True), clear_tool_uses_20250919=CapabilitySupport(supported=True), compact_20260112=CapabilitySupport(supported=False), supported=True), effort=EffortCapability(high=CapabilitySupport(supported=False), low=CapabilitySupport(supported=False), max=CapabilitySupport(supported=False), medium=CapabilitySupport(supported=False), supported=False), image_input=CapabilitySupport(supported=True), pdf_input=CapabilitySupport(supported=True), structured_outputs=CapabilitySupport(supported=False), thinking=ThinkingCapability(supported=True, types=ThinkingTypes(adaptive=CapabilitySupport(supported=False), enabled=CapabilitySupport(supported=True)))), created_at=datetime.datetime(2025, 5, 22, 0, 0, tzinfo=datetime.timezone.utc), display_name='Claude Sonnet 4', max_input_tokens=1000000, max_toke
        """                        
    except anthropic.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx
        raise RuntimeError("Failed to connect to Anthropic API") from None
    except anthropic.AuthenticationError: # 401
        raise RuntimeError("Invalid or missing Anthropic API key") from None
    except anthropic.NotFoundError: # 404
        raise ValueError(f"Model alias '{alias}' not found") from None
    except anthropic.RateLimitError: # 429
        print("A 429 status code was received; we should back off a bit.")
    except anthropic.APIStatusError as e: 
        print("Another non-200-range status code was received. {e}")
        print(e.status_code)
        print(e.response)
        raise RuntimeError(f"Anthropic API error {e.status_code}: {e.message}") from None

def print_model_info(model: dict, indent: int = 4) -> None:
    """Print model info from json."""
    pad = " " * indent
    for key, value in model.items():
        if isinstance(value, dict):
            print(f"{pad}{key}:")
            for k, v in value.items():
                print(f"{pad}  {k}: {v}")
        else:
            print(f"{pad}{key}: {value}")

def model_id_from_args(args) -> str:
    """Get model_id from what Anthropic has to offer."""
    claude_model_list = latest_models_dict()
        # claude_model_list={'opus': 'claude-opus-4-7', 'sonnet': 'claude-sonnet-4-6', 'haiku': 'claude-haiku-4-5-20251001'}
    model_id = claude_model_list.get(args.model.lower().strip())
    if args.trace:
        print(f"TRACE: {model_id} from claude_model_list: {claude_model_list}")

    if model_id is None:
        # POLICY: When processing each item of a list, Use match case python structure instead of if sttements.
        match args.model:
            case str() if "gemma" in args.model:
                # TODO: Turn temporary placeholder assignment to use Google's LLM via ollama.
                return "claude-haiku-4-5-20251001"
            case str() if "qwen" in args.model:
                # Lookup latest qwen version:
                return "qwen2.5"
            case str() if "kimi" in args.model:
                # TODO: Turn temporary placeholder assignment to use Moonshot's LLM via ollama.
                return "claude-haiku-4-5-20251001"
            case str() if "minimax" in args.model:
                # TODO: Turn temporary placeholder assignment to use minimax's LLM via ollama.
                return "claude-haiku-4-5-20251001"
            case str() if "mistral" in args.model:
                # TODO: Turn temporary placeholder assignment to use Mistral's LLM via ollama.
                return "claude-haiku-4-5-20251001"
            case _:
                model_id = "claude-opus-4-7" #'claude-haiku-4-5-20251001' # default
                print(f"WARNING: model is using hard-coded default of \"{model_id}\" ")
                # TODO: If file is not available, download model for ollama localhost:11434 "Ollama is running"
  # TODO: POLICY: Get default model from .env file so it can be used across all programs when updated automatically.
                # TODO: Specify model version (4), variant ("E2B"), and size (8GB) as well.
                # print(f"WARNING: model is using model \"{model_id}\" defined in .env file.")

    if args.verbose:
        print(f"INFO: -m \"{args.model}\" => model_id=\"{model_id}\" ")
    if args.trace: # details about model_id:
        model_json = resolve_model_family(model_id)
        print_model_info(model_json)
        """
            id: claude-opus-4-7
            display_name: Claude Opus 4.7
            type: model
            created_at: 2026-04-14T00:00:00+00:00
            max_input_tokens: 1000000
            max_tokens: 128000
            capabilities:
            batch: True
            citations: True
            code_execution: True
            image_input: True
            pdf_input: True
            structured_outputs: True
            thinking: True
            effort: True
        """
        # The response above (except for cutoff dates) are shown 
        # at https://platform.claude.com/docs/en/about-claude/models/overview
        # The response above does not include older models
        # nor https://platform.claude.com/docs/en/about-claude/model-deprecations
        # Get detailed "Model Cards" pdf for each model at https://platform.claude.com/docs/en/resources/overview
    return model_id


def latest_models_dict() -> dict:
    """Obtain json structure from call to Anthropic API."""
    # TODO: POLICY: To keep secrets off logs, obtain api_keys by lookup from a secrets manager rather than from CLI parameters.
    # POLICY: It's better to take a bit longer than to expose the key while running code that doesn't require the secret.
    client_api_key = get_str_from_env_file("ANTHROPIC_API_KEY")

    # POLICY: Do not print api key to avoid **API key length logged to stdout** hackers use for fingerprinting encryption.
    # POLICY: Exit the run immediately if the API KEY is unavailable.
    if not client_api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. "
            "Please export it before running this script."
        )
    client = _make_anthropic_client(client_api_key)
    try:
        models = client.models.list()
    except anthropic.AuthenticationError:
        raise RuntimeError("Invalid or missing Anthropic API key") from None
    except anthropic.APIConnectionError:
        raise RuntimeError("Failed to connect to Anthropic API") from None
    except anthropic.APIStatusError as e:
        raise RuntimeError(f"Anthropic API error {e.status_code}: {e.message}") from None

    # print(f"VERBOSE: {sys._getframe().f_code.co_name}(): {models}")
    # Display Name.     Model ID                   Created.      Max Input  Max Output
    # Claude Opus 4.7.  claude-opus-4-7            Apr 14, 2026. 1,000,000  128,000
    # Claude Haiku 4.5  claude-haiku-4-5-20251001  Oct 15, 2025.   200,000   64,000
    # Shorthand Aliases

    client_api_key = ""

    # TODO: POLICY: When working with lists, write code that accomodates new values rather than fixed known items.
    latest = {"opus": None, "sonnet": None, "haiku": None}
    for model in models.data:
        match model.id:
            case str() if "opus" in model.id:
                family = "opus"
            case str() if "sonnet" in model.id:
                family = "sonnet"
            case str() if "haiku" in model.id:
                family = "haiku"
        # TODO: family = "mythons"
            case _:
                continue
        current = latest[family]
        if current is None or model.created_at > current.created_at:
            latest[family] = model

    # claude_model_list={'opus': 'claude-opus-4-7', 'sonnet': 'claude-sonnet-4-6', 'haiku': 'claude-haiku-4-5-20251001'}
    return {
        family: model.id
        for family, model in latest.items()
        if model is not None
    }

def run_is_within_budget(model_id: str, code_from_file_bytes: bytes) -> float | None:
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
    # POLICY: Use _make_anthropic_client() to enforce SSL hardening on all Anthropic API calls.
    client_api_key = get_str_from_env_file("ANTHROPIC_API_KEY")
    # POLICY: Fail fast with a clean message (no traceback, no secret) if the key is missing.
    if not client_api_key:
        print("FATAL: ANTHROPIC_API_KEY is not set. Export it or add it to ~/.claude-vulscan.env before running.")
        return None
    client = _make_anthropic_client(client_api_key)
    client_api_key = ""
    # Make a minimal API call to capture response headers:
    # POLICY: This probe itself consumes credits, so billing failures must be surfaced here
    # with an actionable message instead of letting a raw 400 traceback escape to the user.
    try:
        response = client.messages.with_raw_response.create(
            model=model_id,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
    except anthropic.BadRequestError as e:  # 400 — includes "credit balance too low"
        api_message = _extract_anthropic_error_message(e)
        lowered = api_message.lower()
        if (
            "credit balance" in lowered
            or "insufficient" in lowered
            or "billing" in lowered
            or "upgrade" in lowered
        ):
            print("FATAL: Anthropic credit balance is too low to access the API.")
            print("   Add credits or upgrade your plan at:")
            print("   https://console.anthropic.com/settings/billing")
            if api_message:
                print(f"   API said: {api_message}")
        else:
            print(f"FATAL: Anthropic API rejected the budget probe (400): {api_message or e}")
        return None
    except anthropic.AuthenticationError:  # 401
        print("FATAL: Invalid or missing Anthropic API key (ANTHROPIC_API_KEY).")
        return None
    except anthropic.PermissionDeniedError as e:  # 403
        print(f"FATAL: Anthropic API permission denied for model '{model_id}': {e}")
        return None
    except anthropic.NotFoundError:  # 404
        print(f"FATAL: Anthropic model '{model_id}' not found or not available to this key.")
        return None
    except anthropic.RateLimitError:  # 429
        print("ERROR: Rate limit exceeded during budget probe — back off and retry shortly.")
        return None
    except anthropic.APIConnectionError as e:
        print(f"FATAL: Could not connect to Anthropic API: {e}")
        return None
    except anthropic.APIStatusError as e:  # catch-all for other non-2xx responses
        api_message = _extract_anthropic_error_message(e)
        print(f"FATAL: Anthropic API error {e.status_code}: {api_message or getattr(e, 'message', e)}")
        return None

    print("=== Anthropic Claude Organization Limits: Rate Limits on API capacity ===")
        # Also shown on GUI Console at https://platform.claude.com/settings/limits
    headers = response.headers
    # POLICY: Keep timestamps using GMT/UTC but convert to local time zone for printing out to user.
    token_reset_local_time = infer_from_utc(headers.get("anthropic-ratelimit-tokens-reset"))
    requests_local_time =    infer_from_utc(headers.get("anthropic-ratelimit-requests-reset"))
    print(f"requests_reset on : {requests_local_time} ({headers.get("anthropic-ratelimit-requests-reset")}) UTC")
    print(f"tokens_reset on   : {token_reset_local_time} ({headers.get("anthropic-ratelimit-tokens-reset")}) UTC")
    # Infer approximate tier from requests-per-minute limit:

    # NOTE: Rate limit is to protect the vendor from sudden rush crashing their system:
    rpm = int(headers.get('anthropic-ratelimit-requests-limit'))
    # if limits["requests_limit"] else None
    if not rpm:
        print("No rpm to identify tier!")
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
    #   return False

    # TODO: POLICY: Plug in a random number until we can figure out what nmber to give ;)
    tokens_expected = 2048
    
    return tokens_expected


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
        # POLICY: Use hardened SSL context (certifi CA bundle, CERT_REQUIRED) for all outbound
        # HTTPS calls carrying sensitive credentials — including the admin API key.
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.load_verify_locations(certifi.where())
        ssl_ctx.verify_mode = ssl.CERT_REQUIRED
        ssl_ctx.check_hostname = True
        with httpx.Client(verify=ssl_ctx, timeout=10.0) as http_client:
            response = http_client.get(url, headers=headers, params=params)
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


def obtain_file(args, target: str, filepath: str) -> str | None:
    """Obtain code of individual file targeted."""
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

def ollama_is_running():
    """Verify ollama server is running by listing its models."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama is running with {len(models)} model(s):")
            for m in models:
                print(f"   - {m['name']}")
            return True
    except requests.ConnectionError:
        print("❌ Ollama is not running — start it with: `ollama serve`")
        return False


def openai_vulscan_code(filepath: str, code: str, prompt_text: str, model_id: str) -> dict | None:
    """Run OpenAI API call via Ollama."""
    # POLICY: Before using olamma, first check if Olamma is running.
    if not ollama_is_running():
        return None
        # ✅ Ollama is running with 2 model(s):
           # - kimi-k2.5:cloud
           # - llava:latest
    
    if not model_id:
        model_id = "qwen2.5"
        # https://qwen.ai/blog?id=qwen2.5 
        # Qwen2.5: 0.5B, 1.5B, 3B, 7B, 14B, 32B, and 72B
        # Qwen2.5-Coder: 1.5B, 7B, and 32B on the way
    # from openai import OpenAI
    try:
        # call_api_key = get_str_from_env_file("OPENAI_API_KEY")
        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        response = client.chat.completions.create(
            model={model_id},
            messages=[{"role": "user", "content": {prompt_text}}]
        )
        return (response.choices[0].message.content)
    # print("FATAL: Run cannot continue without OpenAI client!")
    # POLICY: Even on failure, do not exit program until billing info for run is displayed.
    except FileNotFoundError:
        print(f"Error: Target file '{filepath}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to access '{filepath}'.")
    except KeyError as e:
        print(f"Error: Expected key missing in scan results: {e}")
    except TypeError as e:
        print(f"Error: Unexpected return type from ant_vulscan_code(): {e}")
    except Exception as e:
        print(f"Unexpected error while scanning '{filepath}': {e}")


def ant_vulscan_code(args, filepath: str, code: str, prompt_text: str, model_id: str, api_max_tokens=2048) -> dict | None:
    """Scan file using Anthropic API call.
    
    CAUTION: **Sensitive data sent to external API** File contents are sent to Anthropic's API without sanitization. If scanned files contain secrets/credentials, they are exfiltrated.
    """
    # POLICY: Hard-code a api_max_tokens variable to ensure one.
    # TODO: POLICY: Specify api_max_tokens based emphirically what is needed for code size, tokens consumed, etc.
    #if not api_max_tokens:
    #    api_max_tokens = 2048 # or 1024

    # TODO: POLICY: To keep secrets off logs, obtain api_keys by lookup from a secrets manager rather than from CLI parameters.
    # POLICY: It's better to take a bit longer than to expose the key while running code that doesn't require the secret.
    client_api_key = get_str_from_env_file("ANTHROPIC_API_KEY")
    # POLICY: Avoid **API key length logged to stdout** hackers use for fingerprinting encryption.
    # POLICY: Exit the run immediately if the API KEY is unavailable.
    if not client_api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. "
            "Please export it before running this script."
        )
    try:
        client = _make_anthropic_client(client_api_key)
        client_api_key = ""
        # POLICY: Set a generous per-request timeout for large file scans to prevent indefinite hangs.
        response = client.messages.create(
            model=model_id,
            max_tokens=api_max_tokens,
            timeout=120.0,
            messages=[{
                "role": "user",
                "content": f"{prompt_text}\n\n{code}"
            }]
        )
        # See https://platform.claude.com/docs/en/api/sdks/python#token-counting
        # print(f"DEBUGGING: {response.input_tokens}")
            # Usage(input_tokens=25, output_tokens=13)      
        # QUESTION: Still specify filepath here?
        return {"file": filepath, "findings": response.content[0].text}

    # print("FATAL: Run cannot continue without Anthropic client!")
    # POLICY: Even on failure, do not exit program until billing info for run is displayed.
    except anthropic.AuthenticationError as e:
        # POLICY: Auth failures are security events — re-raise to halt execution.
        print(f"Error: Authentication failed — check ANTHROPIC_API_KEY: {e}")
        raise
    except anthropic.RateLimitError:
        print(f"Error: Rate limit exceeded while scanning '{args.target}'.")
    except anthropic.APIConnectionError as e:
        print(f"Error: Connection to Anthropic API failed: {e}")
    except anthropic.APIStatusError as e:
        print(f"Error: Anthropic API error {e.status_code} while scanning '{args.target}': {e.message}")
    except FileNotFoundError:
        print(f"Error: Target file '{args.target}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to access '{args.target}'.")
    except KeyError as e:
        print(f"Error: Expected key missing in scan results: {e}")
    except TypeError as e:
        print(f"Error: Unexpected return type from ant_vulscan_code(): {e}")
    except Exception as e:
        print(f"Unexpected error while scanning '{args.target}': {e}")


def vulscan_project(directory: str):
    """Scan all .py files within the project folder."""
    # POLICY: To avoid errors, initiate with blanks all iterables at the top of function.
    results = []
    # TODO: FIXME: **Path Traversal in `vulscan_project()`** Uses `os.walk()` and `os.path.join()` without `safe_path()` validation. An attacker-controlled `directory` argument could traverse outside intended boundaries.
    # **Path Traversal in `vulscan_project()`** (line 217-225): Uses `os.walk(directory)` without validating the `directory` argument against traversal attacks. The `safe_path()` call on line 223 uses `root` (from `os.walk`) as the base, not a fixed safe base directory, defeating the protection.
    # POLICY: Block path traversal attacking such as "../../etc/passwd" by not using os.walk()
    
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                # path = os.path.join(root, file)
                filepath = safe_path(root , file)
                if args.verbose:
                    print(f"vulscan_project filepath: {filepath}")
                result = ant_vulscan_code(filepath, code_from_file, my_prompt_text, my_model_id)
                results.append(result)
                print(f"Scanned: {filepath}")
    """
    return results

def expose_global_args(args) -> str | None:
    """Expose specific args to become global."""
    return args.prompt

def write_call_to_csv(args, target_file, call_seq, call_start_utc: str, elapsed_seconds: float, bytes_processed: int, model_id: str, lines_out: str, metrics_filepath: str) -> None:
    """Write line to call metadata csv."""
    # POLICY: Use a --nometric parameter to optionally not write call metrics to a .csv file.
    if args.nometric:
        print("METRIC: Not shown due to --nometric parameter in program call in CLI.")
        return None
    
    bytes_processed_fmt = format_bytes(bytes_processed)
    elapsed_seconds_fmt = format_elapsed_time(elapsed_seconds)
    # POLICY: Do not put sensitive text within unencrypted csv files.
    print(f"\nMETRIC: At {call_start_utc}, {bytes_processed_fmt} bytes {target_file} took {elapsed_seconds_fmt} secs for {lines_out} findings thru {model_id}.")

    # import csv
    row = {
        "call_seq": call_seq,
        "target_file": target_file,
        "start_utc": call_start_utc,
        "elapsed_seconds": elapsed_seconds,
        "bytes_processed": bytes_processed,
        "model_id": model_id,
        "lines_out": lines_out,
    }

    if args.verbose:
        print(f"VERBOSE: {sys._getframe().f_code.co_name}( filepath = {metrics_filepath}")
    if not metrics_filepath:
        return None
    
    file_exists = os.path.exists(metrics_filepath)
    with open(metrics_filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def program_greeting(pgm_name:str, args, elapsedsecs):
    """Print start-of-program greeting."""
    if args.verbose:
        print(f"STARTING: {pgm_name} from uptime: {elapsed_time2format(elapsedsecs)} ({elapsedsecs}).")
    if args.trace:
        print(f"TRACE: __commit_msg__={__commit_msg__}")


def print_cost_report(cost_report):
    """Print Anthropic cost report line.

    cost_report: {'data': [{'starting_at': '2026-04-01T00:00:00Z', 'ending_at': '2026-04-02T00:00:00Z', 'results': []}, {'starting_at': '2026-04-02T00:00:00Z', 'ending_at': '2026-04-03T00:00:00Z', 'results': [{'currency': 'USD', 'amount': '59.225', 'workspace_id': None, 'description': None, 'cost_type': None, 'context_window': None, 'model': None, 'service_tier': None, 'token_type': None, 'inference_geo': None}]}, {'starting_at': '2026-04-03T00:00:00Z', 'ending_at': '2026-04-04T00:00:00Z', 'results': []}, {'starting_at': '2026-04-04T00:00:00Z', 'ending_at': '2026-04-05T00:00:00Z', 'results': []}, {'starting_at': '2026-04-05T00:00:00Z', 'ending_at': '2026-04-06T00:00:00Z', 'results': []}, {'starting_at': '2026-04-06T00:00:00Z', 'ending_at': '2026-04-07T00:00:00Z', 'results': []}, {'starting_at': '2026-04-07T00:00:00Z', 'ending_at': '2026-04-08T00:00:00Z', 'results': []}], 'has_more': True, 'next_page': 'page_?='}
    """
    # Summarize:
    pairs = [
        (r['currency'], float(r['amount']))
        for item in cost_report['data']
        for r in item['results']
    ]
    # TODO: Lookup currency symbols for currencies of all countries' currencies.
    currency_symbols = {"USD": "$", "EUR": "€", "GBP": "£"}

    # Default to blank currency_symbol.
    currency_symbol = ""
    for currency, amount in pairs:
        currency_symbol = currency_symbols.get(currency, "")
        print(f"  cost_report: {currency}: {currency_symbol}{amount} MTD (Month-To-Date)")
            #   cost_report: USD: $59.225 MTD

def ant_billing(model_id) -> float | None:
    """Make API call to get rate limit headers."""
    # Billing runs on a calendar month cycle — invoices are issued at the end of every calendar month via Stripe. 
    # The ANTHROPIC_ADMIN_KEY (sk-ant-admin...) required to get the Cost Report is different from a standard API key
    admin_api_key = get_str_from_env_file("ANTHROPIC_ADMIN_KEY")
    if not admin_api_key:
        print("ERROR: ANTHROPIC_ADMIN_KEY retrieval from .env failed!")
        return None
              
    # POLICY: Admin keys (sk-ant-admin01-...) are only valid for Admin API endpoints, not the Messages API.
    # Use ANTHROPIC_API_KEY for messages.create() and ANTHROPIC_ADMIN_KEY only for billing endpoints.
    client_api_key = get_str_from_env_file("ANTHROPIC_API_KEY")
    if not client_api_key:
        print("ERROR: ANTHROPIC_API_KEY retrieval from .env failed!")
        return None
    client = _make_anthropic_client(client_api_key)
    # POLICY: Delete each secret value after every use rather than let secret keys linger (exposed to theft).
    client_api_key = ""

    # POLICY: Use a appropriate number of max_tokens when calling API for response headers, identified by experimentation.
    response = client.messages.create(
        model=model_id,
        max_tokens=10,
        messages=[{"role": "user", "content": "Hi"}]
    )
    result = get_billing_period(admin_api_key)   # make the API call
    # POLICY: Delete ANTHROPIC_ADMIN_KEY value after every use rather than let secret keys to linger (exposed to theft).
    admin_api_key = ""

    if result:
        print(f"\nFor model: \"{my_model_id}\" ")
        print(f"Billing period month: {result['billing_period_start']} → {result['billing_period_end']}")
                    # 2026-04-01T00:00:00+00:00 → 2026-04-30T23:59:59+00:00
        print(f"  Days elapsed   : {result['days_elapsed']}")
        print(f"  Days remaining : {result['days_remaining']}")
        print_cost_report(result['cost_report'])

    tokens = get_token_usage(response)  # in every message response:
    if tokens:  
        # See https://platform.claude.com/docs/en/api/python/messages/count_tokens
        print(f"  usage.input_tokens  : {tokens['input_tokens']}")
        print(f"  usage.output_tokens : {tokens['output_tokens']}")
        print(f"         total.tokens : {tokens['total_tokens']}")
    
    # TODO: POLICY: Return estimate of cost to do run, in USD.
    run_dollars = 0

    return run_dollars


def open_python_files(args, folder_path: str):
    """Open and read all .py files in a folder, returning their contents.
    
    The key difference is that os.walk yields (root, dirs, files) tuples for every directory it encounters, so the key becomes the full path instead of just the filename to avoid collisions.

    """
    py_files = {}
    # POLICY: Resolve the base path once so safe_path() symlink checks are not bypassable.
    base = Path(folder_path).resolve()
    for filename in os.listdir(folder_path):
        if filename.endswith('.py'):
            try:
                file_path = safe_path(base, filename)
            except ValueError:
                print(f"WARNING: Skipping '{filename}': path traversal detected.")
                continue
            with open(file_path, 'r', encoding='utf-8') as f:
                py_files[filename] = f.read()

    return py_files

    """
    # Usage
    If you also want to search subfolders recursively, swap os.listdir for os.walk:
    pythondef open_python_files_recursive(folder_path):
    """
    files = open_python_files('/path/to/folder')
    for name, content in files.items():
        print(f"--- {name} ---")
        print(content)

        py_files = {}
        
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith('.py'):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        py_files[file_path] = f.read()
        
        return py_files
        

if __name__ == "__main__":
    """Show claude-vulscan.py being used."""
    # POLICY: Begin the monotonic (uptime) run timer as soon as the program starts.
    pgm_strt_elapsedsecs = time.monotonic()   # uptime like 1208973.03808275 since the system was last booted.

    # POLICY: Pass args (parameter values) from CLI call in a parse_args() function so the args structure is global.
    args = parse_args()    # read in arguments from command CLI using explicit passing.
    # POLICY: Specify a global ENVIRONMENT flag to designate whether DEV or PROD to vary processing accordingly.

    # import sys
    PROGRAM_NAME = os.path.basename(os.path.normpath(sys.argv[0]))
    # POLICY: Pass the entire global args structure into functions to work with.
    program_greeting(PROGRAM_NAME,args,pgm_strt_elapsedsecs)

    # POLICY: Track the total number of bytes and files processed during pgm run to establish a time rate of processing.
    run_bytes_processed = 0
    run_files_processed = 0

    # POLICY: Expose some args as global using expose_global_args() function.
    my_prompt_text = expose_global_args(args)
    if not my_prompt_text:
        print("WARNING: -pt = --prompt text not specified. Hard-coded default vulscan will be processed.")
    # POLICY: Hard-code the full path to the .env file based on the program name
    global_env_path = Path.home() / ".claude-vulscan.env"
    open_env_file(global_env_path)

    # POLICY: Increament the metrics about what the program processed this run.
    run_files_processed = 0
    run_bytes_processed = 0
    run_findings_output = 0

# TODO: Loop through csv file to get each folder and model to process:

    my_model_id = model_id_from_args(args)  # like "claude-opus-4-7"

    if not args.target:
       print("FATAL: -t or --target file name not specified!")
       exit()
    
    # POLICY: Use the cross-platform pathlib to concatenate parts of a filepath (rather than construct a string).
    # from pathlib import Path
    # POLICY: To block Traversal vulnerabilities, do not allow higher level part of path to be specified outside the program.
    # POLICY: Obtain the top part of the filepath from the operating system ("/User/johndoe/gh-wm/proj1/").
    # POLICY" Avoid **CSV write path unsanitized** by using safe_path() to validate path traversal on write if caller-controlled.
    # POLICY: Resolve CWD before passing to safe_path() so symlinks cannot bypass is_relative_to() check.
    filepath = safe_path(Path.cwd().resolve(), args.target)
    if args.verbose:
       print(f"VERBOSE: filepath = \"{filepath}\"")

    # POLICY: Use Path.cwd() from Pathlib to construct full filepath from Current Working Directory.
    # POLICY: Name the metrics output file the same as the program name to make it easier to find.
    my_metrics_filepath = safe_path( Path.cwd().resolve() , (PROGRAM_NAME.split(".")[0] + ".csv") )
    if args.verbose:
       print(f"VERBOSE: my_metrics_filepath = \"{my_metrics_filepath}\" ")

    # CAUTION: The entire file is in this string, which may consume more memory than allocated.
    # TODO: Get computer memory as basis for maximum code size allowed.
    code_from_file = obtain_file(args, args.target, filepath)  # individual file.
    if code_from_file is None:
        print("FATAL: code_from_file not valid!")
        exit()
    else:
        code_from_file_bytes = len(code_from_file)

    # POLICY: Code a hard-coded default and print a warning message if it's used.
    if not args.prompt:
        my_prompt_text = "List only real security vulnerabilities in this Python file. Be concise."
        print(f"WARNING: prompt text default: \"{my_prompt_text}\" ")

    # TODO: POLICY: Calculate tokens_expected budget to be consumed during this run.
    # TODO: Use prior run metric statistics as basis to calculate tokens_expected to be consumed during this run.
    tokens_expected = run_is_within_budget(my_model_id, code_from_file_bytes)
    # POLICY: Do not proceed if there is not enough tokens available within budget to run this.
    # run_is_within_budget() prints its own FATAL for API/billing failures and returns None;
    # on success it returns a positive token estimate. Treat None and non-positive as abort,
    # and avoid interpolating the sentinel (which would print the literal "None").
    if tokens_expected is None:
        print("FATAL: Aborting run — budget check failed (see error above).")
        sys.exit(1)
    if tokens_expected <= 0:
        print(f"FATAL: Aborting run — estimated {tokens_expected} tokens is not within budget.")
        sys.exit(1)

    
    """
    #### SECTION: Loop through each file within a folder:
    
    # Loop through files in folder if -r = --recurse was specified:
    read_github_repo(owner, repo, branch="main", token=None):
    Reads all files from a public GitHub repo via the GitHub API.
    
    files = read_github_repo("owner", "repo-name")
    for path, content in files.items():
        print(f"--- {path} ---")
        print(content[:500])  # Print first 500 chars of each file

    # Read only Python (.py) files:
    if item["type"] == "file" and item["name"].endswith(".py"):        
    """

    # POLICY: Calculate the time each file took to process.
    # from datetime import datetime, timezone
    call_start_utc = datetime.now(timezone.utc).isoformat()
        # print(timestamp.isoformat())                        # 2026-04-17T18:32:01.123456+00:00
        # print(timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"))  # 2026-04-17 18:32:01 UTC    
    call_start_elapsedsecs = elapsedsecs_timestamp()
    # POLICY: Because a crash can bypass metrics logging when an exception is raised, `call_took_elapsedsecs` is undefined.

    findings = ant_vulscan_code(args, filepath, code_from_file, my_prompt_text, my_model_id)  # & max_tokens for individual file.
    # POLICY: Capture individual call timings immediately after return and before formatting of output.
    call_took_elapsedsecs = elapsedsecs_timestamp() - call_start_elapsedsecs
    # print(f"DEBUG: {findings}")
    # POLICY: Print findings in json returned between blank spacer lines.
    print(f"\n{'='*40}\n{findings['file']}\n{findings['findings']}")
    # POLICY: Accumulate run metrics after processing each file.
    # POLICY: Identify number of findings by counting ". **" in the file.
    call_findings_output = findings['findings'].count('. **')  # NOT: len(findings['findings'].splitlines())

    # TODO: POLICY: Optionally output specific findings to a file for follow-up.
    
    run_files_processed += 1
    run_bytes_processed += code_from_file_bytes
    run_findings_output += call_findings_output
    # POLICY: Use the increment count of files processed (run_files_processed) as an index.

    write_call_to_csv(args, args.target, run_files_processed, call_start_utc, call_took_elapsedsecs, code_from_file_bytes, my_model_id, call_findings_output, my_metrics_filepath)
    # TODO: Optionally aditionally output findings to a database, real-time. 


    # POLICY: Analyze metrics collected by this program using a different program than this.

    #### SECTION: End of run processing:

    if args.bill:
        ant_billing(my_model_id)

    pgm_stop_elapsedsecs = time.monotonic()
    pgm_took_elapsedsecs = pgm_stop_elapsedsecs - pgm_strt_elapsedsecs
    run_bytes_processed_fmt = format_bytes(run_bytes_processed)
    pgm_took_elapsedsecs_fmt = elapsed_time2format(pgm_took_elapsedsecs)

    print(f"TOTALS: {run_findings_output} findings from {run_bytes_processed_fmt} bytes of code within {run_files_processed} file(s) in {pgm_took_elapsedsecs_fmt} seconds.")
        # TOTALS: 7 findings from 42.58kb bytes of code within 1 file(s) in 00:00:09.815 seconds.
    # CAUTION: The quantity of findings needs to be evaluated for the quality of those findings.

"""
$ uv run claude-vulscan.py -v -vv -b -m "sonnet" -f "claude-vulscan.py"
STARTING: claude-vulscan.py from uptime: 381:29:13.963 (1373353.96277725).
TRACE: __commit_msg__=26-04-18 v022 billing, tokens, Admin sdk @claude-vulscan.py
WARNING: -pt = --prompt text not specified. Hard-coded default vulscan will be processed.
VERBOSE: open_env_file(): global_env_path="/Users/johndoe/.claude-vulscan.env" 
=== Anthropic Claude Organization Limits: Rate Limits on API capacity ===
requests_reset on : 2026-04-18 04:14:53 PM MDT -0600 (2026-04-18T22:14:53Z) UTC
tokens_reset on   : 2026-04-18 04:14:53 PM MDT -0600 (2026-04-18T22:14:53Z) UTC
  requests_limit      : 50        per minute = Tier 1 (Build - likely free or new account)
  input_tokens_limit  : 30000     per minute
  output_tokens_limit : 8000      per minute
  requests_remaining  : 49        -        
  tokens_limit        : 38000     -        
  tokens_remaining    : 38000     -        
VERBOSE: filepath = "/Users/johndoe/github-wilsonmar/python-samples/claude-vulscan.py"
TRACE: code_from_file contains 52464 characters.
INFO: code file claude-vulscan.py contains 51.23kb bytes (52,464 characters)
GREAT: code file claude-vulscan.py is within the 1,073,741,824 character limit.
TRACE: obtain_file() returning code with file_size 52464.
TRACE: call_api_key (a secret) contains 108 chars.
TRACE: claude_model_list: {'opus': 'claude-opus-4-7', 'sonnet': 'claude-sonnet-4-6', 'haiku': 'claude-haiku-4-5-20251001'}
INFO: -m "sonnet" => model_id="claude-sonnet-4-6" 
    id: claude-sonnet-4-6
    display_name: Claude Sonnet 4.6
    type: model
    created_at: 2026-02-17T00:00:00+00:00
    max_input_tokens: 1000000
    max_tokens: 128000
    capabilities:
      batch: True
      citations: True
      code_execution: True
      image_input: True
      pdf_input: True
      structured_outputs: True
      thinking: True
      effort: True
WARNING: prompt text default: "List only real security vulnerabilities in this Python file. Be concise." 

========================================
claude-vulscan.py
## Real Security Vulnerabilities

1. **Hardened SSL/httpx client never passed to Anthropic client**: The `httpx.Client` with strict SSL context is created but `anthropic.Anthropic(api_key=call_api_key)` ignores it, making the SSL hardening completely ineffective against MITM attacks.

2. **`safe_path()` uses unresolved CWD**: `Path.cwd()` without `.resolve()` allows symlinks in the working directory to bypass the `is_relative_to()` traversal check.

3. **CSV output path not sanitized**: `write_call_to_csv()` opens `filepath` (defaulting to `"claude-vulscan.csv"`) with no `safe_path()` validation, allowing path traversal on write if the argument is attacker-controlled.

4. **No timeout on main API calls**: `client.messages.create()` in `ant_vulscan_code()` has no timeout, enabling indefinite hangs and potential resource exhaustion.

5. **Full file contents exfiltrated to external API**: Scanned file contents are sent to Anthropic's API without secret-scrubbing; files containing credentials or keys are fully exposed to the third party.

6. **Broad `except Exception` suppresses security-relevant failures**: In `ant_vulscan_code()`, SSL errors, authentication anomalies, and other critical exceptions are silently caught and swallowed instead of halting execution.

7. **`open_python_files()` uses `os.path.join()` without traversal validation**: No `safe_path()` check is applied, allowing an attacker-controlled `folder_path` to read files outside intended boundaries.

METRIC: At 2026-04-18T22:14:54.241193+00:00, 52464 byte claude-vulscan.py took 6.927548170089722 secs for 15 lines.

For model: "claude-sonnet-4-6" 
Billing period month: 2026-04-01T00:00:00+00:00 → 2026-04-30T23:59:59+00:00
  Days elapsed   : 18
  Days remaining : 13
  cost_report: USD: $59.225 MTD
  usage.input_tokens  : 8
  usage.output_tokens : 10
         total.tokens : 18
TOTALS: 1 call(s) took 00:00:11.562 seconds for 51.23kb bytes of code.
"""
# EOF