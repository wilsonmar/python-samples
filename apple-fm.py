#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "apple_fm_sdk",
#   "click",
#   "cryptography",
#   "dotenv",
#   "geopy",
#   "keyring",
#   "opentelemetry-api",
#   "opentelemetry-sdk",
#   "pillow",
#   "psutil",
#   "pyAesCrypt",
#   "python-dotenv",
#   "qrcode",
#   "requests",
#   "schedule",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

"""apple-fm.py.

   within https://github.com/wilsonmar/python-samples/blob/master/apple-fm/
   Coding explained at https://wilsonmar.github.io/apple-fm
   This is sample code to use Apple's on-device AI Foundational Models in v27+. See https://apple.github.io/python-apple-fm-sdk/

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
   CONDITIONS OF ANY KIND, either express or implied. See the License 
   for the specific language governing permissions and limitations 
   under the License.

# After install of XCode, homebrew, git, uv, claude:
# Usage in CLI to get program source on your laptop:
    git clone https://github.com/wilsonmar/python-samples --depth 1
    cd python-samples/

# Cleanup from previous runs:
    rm -rf .venv venv
    rm pyproject.toml vu.lock   # if created.

# Initialize for this program:
    uv init --no-readme   # initialized pyproject.toml
    uv venv .venv    # --python python3.12   # for Tensorflow
    source .venv/bin/activate  # (.venv) 

    chmod +x apple-fm.py
    # For Flake8, Pylint, Xenon, Radon, Black, isort, pyupgrade:    ruff check apple-fm.py  

    # pip install -r requirements.txt
    uv install apple-fm-sdk   # instead of pip 
    uv add diagrams, requests

    uv run apple-fm.py

# After running this program:
    deactivate
    # TODO: delete ???

https://developer.apple.com/videos/play/wwdc2026/319/
server PCC for apps with less that 1m downloads.

"""

# SECTION 01. Set metadata about this program

# Unlike regular comments, docstrings are available at runtime to the compiler:
__repository__ = "https://github.com/wilsonmar/apple-fm"
__author__ = "Wilson Mar"
__copyright__ = "See the file LICENSE for copyright and license info"
__license__ = "See the file LICENSE for copyright and license info"
__linkedin__ = "https://linkedin.com/in/WilsonMar"
# Using semver.org format per PEP440: change on every commit:
__last_commit__ = "26-10-07 v005 print csv file sizes @apple-fm.py"


import asyncio
import csv
import platform
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import apple_fm_sdk as fm

import myutils

MIN_MACOS_MAJOR = 27
PROMPTS_CSV = Path(__file__).with_name("apple-fm-prompts.csv")
OUTLOG_CSV = Path(__file__).with_name("apple-fm-outlog.csv")
OUTLOG_FIELDS = ["iso_date_run", "seq", "session_creation", "response", "prompt_txt"]


def is_supported_platform() -> bool:
    """Return True if macOS supports. From myutils.py."""
    if not myutils.is_macos():
        myutils.print_error("Apple Foundation Models require macOS.")
        return False
    if platform.machine() != "arm64":
        myutils.print_error(f"Apple silicon (arm64) required, found {platform.machine()}.")
        return False
    macos_version = platform.mac_ver()[0]
    if int(macos_version.split(".")[0]) < MIN_MACOS_MAJOR:
        myutils.print_error(f"macOS {MIN_MACOS_MAJOR}+ required, found {macos_version}.")
        return False
    return True


def read_prompts(csv_path: Path) -> list[dict]:
    """Return prompt text.""" 
    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        return [row for row in csv.DictReader(csv_file) if row["Prompt"].strip()]
        # TODO: Evaluate pompt for errors & tempertment


def report_elapsed(label: str, start: float) -> float:
    """Print and return seconds elapsed since start (a time.perf_counter value)."""
    elapsed = time.perf_counter() - start
    myutils.print_info(f"{label}: {elapsed * 1000:,.1f} ms")
    return elapsed


def append_outlog(iso_date_run: str, seq: str, session_seconds: float, response_seconds: float | None, prompt_txt: str) -> None:
    """Append one result row, in milliseconds, creating the file with a header if needed."""
    is_new_file = not OUTLOG_CSV.exists() or OUTLOG_CSV.stat().st_size == 0
    with OUTLOG_CSV.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=OUTLOG_FIELDS)
        if is_new_file:
            writer.writeheader()
        writer.writerow({
            "iso_date_run": iso_date_run,
            "seq": seq,
            "session_creation": f"{session_seconds * 1000:.1f}",
            "response": "" if response_seconds is None else f"{response_seconds * 1000:.1f}",
            "prompt_txt": prompt_txt,
        })


def report_file_stats(*csv_paths: Path) -> None:
    """Print the size in bytes and the number of data rows of each CSV file."""
    for csv_path in csv_paths:
        if not csv_path.exists():
            myutils.print_warning(f"{csv_path.name}: not found")
            continue
        with csv_path.open(newline="", encoding="utf-8") as csv_file:
            row_count = sum(1 for _ in csv.DictReader(csv_file))
        myutils.print_info(f"{csv_path.name}: {csv_path.stat().st_size:,} bytes, {row_count:,} rows")


async def main():
    """Loop."""
    program_start = time.perf_counter()

    phase_start = time.perf_counter()
    if not is_supported_platform():
        sys.exit(1)
    report_elapsed("Platform check", phase_start)

    if not PROMPTS_CSV.exists():
        myutils.print_error(f"Prompts file not found: {PROMPTS_CSV}")
        sys.exit(1)

    phase_start = time.perf_counter()
    prompts = read_prompts(PROMPTS_CSV)
    myutils.print_info(f"{len(prompts)} prompts read from {PROMPTS_CSV.name}")
    report_elapsed("Read CSV", phase_start)

    phase_start = time.perf_counter()
    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()
    if not is_available:
        myutils.print_error(f"Foundation Models not available: {reason}")
        sys.exit(1)
    report_elapsed("Model load and availability check", phase_start)

    iso_date_run = datetime.now(UTC).isoformat(timespec="seconds")
    respond_seconds = []
    for row in prompts:
        myutils.print_heading(f"Prompt {row['Seq']}: {row['Prompt']}")
        session_start = time.perf_counter()
        session = fm.LanguageModelSession(model=model)
        session_seconds = report_elapsed(f"Prompt {row['Seq']} session creation", session_start)

        respond_start = time.perf_counter()
        try:
            response = await session.respond(prompt=row["Prompt"])
        except fm.FoundationModelsError as error:
            myutils.print_error(f"Prompt {row['Seq']} failed: {error}")
            report_elapsed(f"Prompt {row['Seq']} time to failure", respond_start)
            append_outlog(iso_date_run, row["Seq"], session_seconds, None, row["Prompt"])
            continue
        response_seconds = report_elapsed(f"Prompt {row['Seq']} response", respond_start)
        respond_seconds.append(response_seconds)
        append_outlog(iso_date_run, row["Seq"], session_seconds, response_seconds, row["Prompt"])
        myutils.print_info(f"Model response: {response}")

    if respond_seconds:
        average_ms = sum(respond_seconds) / len(respond_seconds) * 1000
        myutils.print_info(f"Average response: {average_ms:,.1f} ms over {len(respond_seconds)} prompts.")
    report_file_stats(PROMPTS_CSV, OUTLOG_CSV)
    report_elapsed("Total elapsed", program_start)


if __name__ == "__main__":
    asyncio.run(main())

"""
$ uv run apple-fm.py
psutil.Process(pid=96574, name='python3.13', status='running')
memory used()=56.125 MiB
diskspace_free()=330.76 GB
📢 is_macos(): Darwin  
✅ Platform check: 3.1 ms 
✅ 2 prompts read from apple-fm-prompts.csv 
✅ Read CSV: 0.3 ms 
✅ Model load and availability check: 9.2 ms 
 
👇 Prompt 1: Hello, how are you? 
✅ Prompt 1 session creation: 0.2 ms 
✅ Prompt 1 response: 1,765.6 ms 
✅ Model response: Hello, I'm doing well, thank you. How can I assist you today? 
 
👇 Prompt 2: What time is it in San Fransicso? 
✅ Prompt 2 session creation: 0.3 ms 
✅ Prompt 2 response: 1,251.4 ms 
✅ Model response: I'm sorry, but I can't provide real-time information. Please check a current clock or a reliable time service for the current time in San Francisco. 
✅ Average response: 1,508.5 ms over 2 prompts. 
✅ apple-fm-prompts.csv: 72 bytes, 2 rows 
✅ apple-fm-outlog.csv: 1,143 bytes, 16 rows 
✅ Total elapsed: 3,032.7 ms 
"""