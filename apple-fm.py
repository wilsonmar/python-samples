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
   Explained at https://wilsonmar.github.io/apple-fm
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
__last_commit__ = "26-10-07 v002 new @apple-fm.py"


import myutils

import asyncio
import csv
import platform
import sys
from pathlib import Path

import apple_fm_sdk as fm


MIN_MACOS_MAJOR = 27
PROMPTS_CSV = Path(__file__).with_name("apple-fm.csv")

def is_supported_platform() -> bool:
    """Return True if macOS supports."""
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
    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        return [row for row in csv.DictReader(csv_file) if row["Prompt"].strip()]


async def main():
    if not is_supported_platform():
        sys.exit(1)

    if not PROMPTS_CSV.exists():
        myutils.print_error(f"Prompts file not found: {PROMPTS_CSV}")
        sys.exit(1)
    prompts = read_prompts(PROMPTS_CSV)
    myutils.print_info(f"{len(prompts)} prompts read from {PROMPTS_CSV.name}")

    model = fm.SystemLanguageModel()

    is_available, reason = model.is_available()
    if not is_available:
        myutils.print_error(f"Foundation Models not available: {reason}")
        sys.exit(1)

    for row in prompts:
        myutils.print_heading(f"Prompt {row['Seq']}: {row['Prompt']}")
        session = fm.LanguageModelSession(model=model)
        try:
            response = await session.respond(prompt=row["Prompt"])
        except Exception as error:
            myutils.print_error(f"Prompt {row['Seq']} failed: {error}")
            continue
        myutils.print_info(f"Model response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
