#!/usr/bin/env python3

"""log-time-csv.py at https://github.com/wilsonmar/python-samples/blob/main/log-time-csv.py.

Features of this program include:
* Read the sequence number
* Console messages of various types (INFO, WARNING, ERROR, FATAL)

Based on https://www.youtube.com/watch?v=wVPAHI9on0o by D-I-Ry
         https://www.youtube.com/watch?v=VjwhdqWDG5M by Arcade Spinner
USAGE:
1. install external: pytz for time zones
""" 

__last_change__ = "v003 + ruff fixes, rename from log-text.py :log-time-csv.py"

# Built-in libraries:
import os
from datetime import datetime, timezone
import time
# import pytz
from pathlib import Path
import csv

# External libraries: NONE!

# Global static variables:
SHOW_VERBOSE = True
MAX_LOOPS = 5
SLEEP_SECS = 1
MAX_FILE_SIZE_B = 1024

# Utility Functions:

def count_log_path(file_path) -> str:
    """Return count of rows in csv file at file_path."""
    # import csv
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        row_count = len(rows)

        first_value_last_row = "0" # Default value

        if row_count > 0:
            last_row = rows[-1]
            if len(last_row) > 0: # Check if the last row itself is not empty
                first_value_last_row = last_row[0]
            else:
                print(f"WARNING: Last row in {file_path} is empty.")

        print(f"INFO: {row_count} records in {file_path} ending with Seq# {first_value_last_row}.")
        return first_value_last_row


def create_log_path() -> str:
    """Create path to log file based on static naming standards (in user's $HOME folder).

    Returns the path to the log file.
    """
    # from pathlib import Path
    home_dir = Path.home()
    # TODO: Load from .env or -parm?
    file_path = home_dir / "log-text.txt"   # string concatenated.
    if os.path.exists(file_path):
        print(f"VERBOSE: file_path {file_path} already exists.")
        return file_path
    else:
        print(f"WARNING: verify_filepath( {file_path} does not exist.")

    with open(file_path, "w") as f:
        f.write("seq,timestamp\n")
        # pass
    if os.path.exists(file_path):
        print(f"INFO: file_path {file_path} created.")
        return file_path


def log_utc_time(loops_count, log_path):
    """Log UTC timestamp to csv file."""
    # import time
    timestamp = time.time()   # UTC epoch time.

    # from datetime import datetime, timezone
    # Get the current UTC time as a timezone-aware datetime object
    now_utc = datetime.now(timezone.utc)
    # Format the UTC timestamp as a string, e.g., ISO 8601 format
    timestamp = now_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

    write_mode = 'a'
    if os.path.isfile(log_path):   # exists:
        file_size = os.path.getsize(log_path)
        if file_size >= MAX_FILE_SIZE_B:
           write_mode = 'w'
        else:
            print(f"FATAL: Maximum file size of {MAX_FILE_SIZE_B} bytes reached.")
            exit(9)

        with open(log_path, mode=write_mode) as output_file:
            log_record=f"{loops_count},{timestamp}"
            output_file.write(f"{log_record}\n")
            if SHOW_VERBOSE:
                print(log_record)


if __name__ == '__main__':

    # import pytz
    # now = datetime.now(tz)  # adds time zone.

    # Get current local date and time with time zone info (Python 3.6+)
    # from datetime import datetime
    local_time = datetime.now().astimezone()

    local_timestamp = local_time.strftime("%Y-%m-%d_%I:%M:%S %p %Z%z")  # local timestamp with AM/PM & Time zone codes

    log_path = create_log_path()
    first_value_last_row = count_log_path(log_path)
    # TODO: Verify first_value_last_row is a number.
    loops_seq = int(first_value_last_row) + 1
    print(f"INFO: log-time-csv.py starting at {local_timestamp} from {loops_seq} ...")

    MAX_LOOPS_COUNT = loops_seq + MAX_LOOPS    # the largest sequence from a run of this program.

    loops_count = 0
    while True:  # infinite loop:
        loops_count += 1   # increment
        loops_seq += 1 
        if MAX_LOOPS_COUNT > 0:   # infinite.
            if loops_count > MAX_LOOPS_COUNT:
                exit()

        log_utc_time(loops_seq, log_path)
        time.sleep(SLEEP_SECS)

    print(f"INFO: Stopped at loop # {loops_count} for next run.")
    