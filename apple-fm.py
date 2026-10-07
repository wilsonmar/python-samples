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
__last_commit__ = "26-10-05 v001 new @apple-fm.py"


import asyncio
import platform
import sys

import apple_fm_sdk as fm

import myutils

MIN_MACOS_MAJOR = 27


def is_supported_platform() -> bool:
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


async def main():
    if not is_supported_platform():
        sys.exit(1)

    # TODO: Retrieve prompt_txt
    prompt_txt = "Hello, how are you?"
    myutils.print_heading(f"apple-fm.py: Model prompt: {prompt_txt}")

    model = fm.SystemLanguageModel()

    is_available, reason = model.is_available()
    if not is_available:
        myutils.print_error(f"Foundation Models not available: {reason}")
        sys.exit(1)

    session = fm.LanguageModelSession(model=model)
    response = await session.respond(prompt=prompt_txt)
    myutils.print_info(f"Model response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
