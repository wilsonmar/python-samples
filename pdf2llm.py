 #!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "platformdirs",
#   "markitdown[pdf]",
#   "pymupdf4llm",
#   "psutil",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file

"""pdf2llm.py here.

https://github.com/wilsonmar/python-samples/blob/main/pdf2llm.py

This code uses several techniques to parse a PDF file for use by LLM.

Sample file "LSDPrep-V8.pdf" is 509 pages in 9.8 MB.

# Before running, on a Terminal
    # Create a folder:

    rm -rf .venv .pytest_cache __pycache__
    rm pyproject.toml
    uv init  # create README.md, pyproject.toml, main.py, .python-version (latest), .gitignore, .git
    python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
    source .venv/bin/activate
    #uv venv --python python3.12
    uv add --frozen MarkItDown[pdf]
    uv add --frozen pymupdf4llm
    uv add --frozen requests
    uv add platformdirs
    uv pip install -e .
    #uv sync
    chmod +x pdf2llm.py
    ruff check pdf2llm.py

    uv run pdf2llm.py -v -vv -f "LSDPrep-V8.pdf"

AFTER RUN:
    deactivate
    rm -rf .venv .pytest_cache __pycache__
"""
__last_change__ = "25-11-17 v001 + new :pdf2llm.py"
__status__ = "NOT WORKING - new"

# Built-in libraries:
import argparse
from datetime import datetime, timezone
#from pathlib import Path
import platform
#import re
import psutil
import time

# External libraries defined in requirements.txt:
try:
    import pymupdf4llm
    from markitdown import MarkItDown
    #import matplotlib. pyplot
    #import requests
except Exception as e:
    print(f"Python module import failed: {e}")
    # uv run log-time-csv.py
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    print("Please activate your virtual environment:\n  uv env .env\n  source .venv/bin/activate")
    exit(9)


# Global static variables default values for override by args:
SHOW_VERBOSE = False
SHOW_DEBUG = False
SHOW_SUMMARY = False
gpu_device = "cpu"
MAX_LOOPS = 3   # 0 = infinite
SLEEP_SECS = 1

# Program Timings:
# For wall time measurements:
pgm_strt_datetimestamp = datetime.now()

print(platform.system())  # Darwin, Linux, Windows, etc.

def read_cmd_args() -> None:
    """Read command line arguments and set global variables.

    See https://realpython.com/command-line-interfaces-python-argparse/
    """
    #import argparse
    #from argparse import ArgumentParser
    parser = argparse.ArgumentParser(allow_abbrev=True,description="swap-a-secret.py")
    parser.add_argument("-q", "--quiet", action="store_true", help="Run without output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show inputs into functions")
    parser.add_argument("-vv", "--debug", action="store_true", help="Debug outputs from functions")
    parser.add_argument("-s", "--summary", action="store_true", help="Show summary stats")
    parser.add_argument("-g", "--gpu", action="store_true", help="gpu device")
    parser.add_argument("-r", "--ray", action="store_true", help="use ray")
    # Default -h = --help (list arguments)
    # uv run gpu-sample.py -v -vv -g "mps"
    args = parser.parse_args()


    #### SECTION 08 - Override defaults and .env file with run-time parms:

    # In sequence of workflow:

    global SHOW_VERBOSE, SHOW_DEBUG, SHOW_SUMMARY
    if args.verbose:       # -v  --verbose
        SHOW_VERBOSE = True
    if args.debug:         # -vv --debug
        SHOW_DEBUG = True
    if args.summary:       # -s  --summary
        SHOW_SUMMARY = True
    if args.gpu:       # -g  --gpu
        gpu_device = args.gpu    # noqa

    if args.quiet:         # -q --quiet
        SHOW_VERBOSE = False
        SHOW_DEBUG = False
        SHOW_SUMMARY = False

    return None


### OS-level utilities:

def is_macos() -> bool:
    """Return True if this is running on macOS."""
    # import platform
    return platform.system() == "Darwin"

# For custom GPU operations in Python, use pyobjc to interface with Apple Metal APIs, but it is more complex than using PyTorch/TensorFlow.


#### Utility Time Functions:

def day_of_week(local_time_obj) -> str:
    """Return day of week string from date object (starts at 0)."""
    # str(days[local_time_obj.weekday()])  # Monday=0 ... Sunday=6
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return str(days[local_time_obj.weekday()])

def timestamp_local() -> str:
    """Generate a timestamp straing containing the local time with AM/PM & Time zone code."""
    # import pytz
    # now = datetime.now(tz)  # adds time zone.

    # from datetime import datetime
    local_time_obj = datetime.now().astimezone()
    local_timestamp = local_time_obj.strftime("%Y-%m-%d_%I:%M:%S %p %Z%z")  # local timestamp with AM/PM & Time zone codes
    return local_timestamp

def timestamp_utc() -> str:
    """Generate a timestamp straing containing the UTC "Z" time with no AM/PM & Time zone code."""
    # import time
    timestamp = time.time()   # UTC epoch time.
    # from datetime import datetime, timezone
    # Get the current UTC time as a timezone-aware datetime object
    now_utc = datetime.now(timezone.utc)
    # Format the UTC timestamp as a string, e.g., ISO 8601 format
    timestamp = now_utc.strftime('%Y%m%dT%H%M%SZ')
       # 20251118T02:50:20Z # : not allowed in file names.
    return timestamp

def func_timer_strt():
    """Capture start time for elapsed seconds calculation by func_timer_stop()."""
    strt_func_time = time.perf_counter()
    return strt_func_time
    
def func_timer_stop(strt_time):
    """Calculate elapsed seconds using start time previously captured."""
    stop_time = time.perf_counter()
    elapsed_secs = stop_time - strt_time
    return elapsed_secs


def string_byte_count(string: str, encoding='utf-8') -> int:
    """Encode the string to bytes using the specified (utf-8)."""
    byte_sequence = string.encode(encoding)
    # Return the length of the byte sequence
    return len(byte_sequence)


def user_gb_mem_avail() -> float:
    """Return the GB of RAM for system, using the psutil library.
    
    cross-platform vs. /proc/meminfo Linux sums "MemFree", "Buffers", and "Cached" values in kB.
    """
    #import os, psutil  #  psutil-5.9.5
    memory_bytes = psutil.virtual_memory().available  # for user
    gb = memory_bytes / (1024 ** 3)  # from bytes to Gb
    return gb

def pgm_memory_used() -> (float, str):
    """Return the MiB of RAM for the current process, using the psutil library."""
    #import os, psutil  #  psutil-5.9.5
    process = psutil.Process()
    process_info = str(process)
    mem=process.memory_info().rss / (1024 ** 2)  # in bytes
    return mem, process_info

def pgm_diskspace_free() -> float:
    """Return the GB of disk space free of the partition in use, using the psutil library."""
    #import os, psutil  #  psutil-5.9.5
    disk = psutil.disk_usage('/')
    free_space_gb = disk.free / (1024 * 1024 * 1024)  # = 1024 * 1024 * 1024
    return free_space_gb


def pgm_summary(std_strt_datetimestamp, loops_count):
    """Print summary count of files processed and the time to do them."""
    # For wall time of standard imports:
    pgm_stop_datetimestamp = datetime.now()
    pgm_elapsed_wall_time = pgm_stop_datetimestamp - pgm_strt_datetimestamp

    if SHOW_DEBUG:
        pgm_stop_mem_used, process_data = pgm_memory_used()
        pgm_stop_mem_diff = pgm_stop_mem_used - pgm_strt_mem_used
        print(f"{pgm_stop_mem_diff:.6f} MB memory consumed during run in {process_data}.")

        pgm_stop_disk_diff = pgm_strt_disk_free - pgm_diskspace_free()
        print(f"{pgm_stop_disk_diff:.6f} GB disk space consumed during run.")

        print(f"SUMMARY: Ended while attempting loop {loops_count} in {pgm_elapsed_wall_time} seconds.")
    else:
        print(f"SUMMARY: Ended while attempting loop {loops_count}.")


def use_markitdown(input_pdf):
    """Use use_markitdown to create markdown."""
    # Handles OCR and image descriptions when integrated with LLMs like OpenAI models.
    # from markitdown import MarkItDown
    md = MarkItDown()
    md_text = md.convert(input_pdf)
    return md_text

def use_pymupdf4llm(input_pdf):
    """Use pymupdf4llm to create markdown."""
    # import pymupdf4llm
    md_text = pymupdf4llm.to_markdown(input_pdf)
    return md_text

# Vision Parse: Uses Vision LLMs to convert PDFs, recognizing text, tables, and formatting into Markdown.​ https://www.reddit.com/r/MachineLearning/comments/1hg5d3p/p_vision_parse_parse_pdf_documents_into_markdown/

# llama-parse: Uses an API to convert PDFs to Markdown with structure preservation, requiring API key setup.​ https://stackoverflow.com/questions/77834102/converting-pdf-to-markdown-in-python-with-structure-preservation



if __name__ == '__main__':

    SHOW_VERBOSE = True
    SHOW_DEBUG = True
    SHOW_SUMMARY = True
    print("\n# Program command variables: ")
    print(f"    -v  SHOW_VERBOSE={SHOW_VERBOSE}")
    print(f"    -vv SHOW_DEBUG={SHOW_DEBUG}")
    print(f"    -s  SHOW_SUMMARY={SHOW_SUMMARY}")

    local_timestamp = timestamp_local()
    if SHOW_DEBUG:
        pgm_strt_mem_used, pgm_process = pgm_memory_used()
        print(f"DEBUG: {pgm_process}")
        print("DEBUG: pgm_memory used()="+str(pgm_strt_mem_used)+" MiB being used.")
        user_gb_mem_avail = user_gb_mem_avail()
        print(f"DEBUG: user_gb_mem_avail()={user_gb_mem_avail:.2f} GB")
        pgm_strt_disk_free = pgm_diskspace_free()
        print(f"DEBUG: pgm_diskspace_free()={pgm_strt_disk_free:.2f} GB")
        # list_disk_space_by_device()

    # From https://www.ldsavow.com/LDSPREP/LDSPrep-V8.pdf
    algo = "pymupdf4llm"
    #algo = "MarkItDown"
    input_pdf = "LDSPrep-V8.pdf"
    yymmdd = timestamp_utc()
    md_out_filename = f"LDSPrep-V8-{algo}-{yymmdd}.md"
    if algo == "pymupdf4llm":
        md_out = use_pymupdf4llm(input_pdf)
    elif algo == "MarkItDown":
        md_out = use_markitdown(input_pdf)
        #TODO: Convert UTF-8 "" to "##" markdown
        #input_string = "\f\fFF"
        #output_string = input_string.replace("\f\fFF", "##")
        # print(output_string)
    else:
        print("Invalid algo.")
        exit()
    
    print(f"use_markitdown {string_byte_count(str(md_out))} bytes.")
        #Too big to print(md_text)
    with open(md_out_filename, "w") as file:
        file.write(str(md_out))
    print(f"pdf2llm.py wrote {md_out_filename}") # 2MB

