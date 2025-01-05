#!/usr/bin/env python3

"""mondrian-gen.py at https://github.com/wilsonmar/python-samples/blob/main/mondrian-gen.py
This program creates a PNG file of art in the style of Piet Mondrian.
CURRENT STATUS: WORKING for multiple files.
git commit -m"v002 + SHOW_SUMMARY_COUNTS :mondrian-gen.py"

Based on https://www.perplexity.ai/search/write-a-python-program-to-crea-nGRjpy0dQs6xVy9jh4k.3A#0
Tested on macOS 14.5 (23F79) using Python 3.13.
flake8  E501 line too long, E222 multiple spaces after operator

Before running this:
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pycairo Pillow pytz tzlocal
   # Downloading pycairo-1.27.0.tar.gz (661 kB)
   * Downloading pillow-11.1.0-cp312-cp312-macosx_11_0_arm64.whl (3.1 MB)
   * Downloading tzlocal-5.2-py3-none-any.whl.metadata (7.8 kB)
chmod +x mondrian-gen.py
./mondrian-gen.py
"""

# pip install pycairo (https://pycairo.readthedocs.io/en/latest/)
import cairo
from datetime import datetime, timezone
import pytz

import os
from pathlib import Path

# import Pillow
from PIL import Image

import platform
import random
import sys
import time
import tzlocal

# Start with program name (without ".py" file extension) such as "modrian-gen":
PROGRAM_NAME = Path(__file__).stem
    # See https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    # Instead of os.path.splitext(os.path.basename(sys.argv[0]))[0]

# Global Constants:
WIDTH, HEIGHT = 500, 500
TILE_SIZE = 10
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
# This is the pallette of primary RBG colors:
# COLORS = [(1, 1, 1), (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 1)]
# Plus green, orange, and purple:
COLORS = [(1, 1, 1), (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 1), (0, 1, 0), (1, 0.5, 0), (0.5, 0, 0.5)]
    # See https://www.schoolofmotion.com/blog/10-tools-to-help-you-design-a-color-palette

# Console display options:
SHOW_DEBUG = False
INCLUDE_DATE_OUT = True  # date/time stamp within file name
DATE_OUT_Z = True  # save files with Z time (in UTC time zone now) instead of local time.
OPEN_OUTPUT_FILE = True
PRINT_OUTPUT_FILE_LOG = True
PRINT_OUTPUT_COUNT = True
DELETE_OUTPUT_FILE = True
SHOW_SUMMARY_COUNTS = True

# User preferences:
USER_FOLDER = ""  # args.folder (like a mount)
FILES_TO_GEN = 1


if os.name == "nt":  # Windows operating system
    SLASH_CHAR = "\\"
    # if platform.system() == "Windows":
    print(f"*** Windows Edition: {platform.win32_edition()} Version: {platform.win32_ver()}")
else:
    SLASH_CHAR = "/"

# SAVE_PATH = os.getcwd()  # cwd=current working directory (python-examples code folder)
SAVE_PATH = os.path.expanduser("~")  # user home folder path like "/User/johndoe"
if SHOW_DEBUG:
    print(f"*** DEBUG: SAVE_PATH={SAVE_PATH}")

if USER_FOLDER == "":
    # No prefix (mount) specified:
    OUTPUT_PATH_PREFIX = SAVE_PATH + SLASH_CHAR + "Downloads"
else:
    OUTPUT_PATH_PREFIX = SAVE_PATH + SLASH_CHAR + USER_FOLDER
if SHOW_DEBUG:
    print(f"*** DEBUG: OUTPUT_PATH_PREFIX={OUTPUT_PATH_PREFIX}")

# Check to make sure folder exists:
if not os.path.isdir(OUTPUT_PATH_PREFIX):  # Confirmed a directory:
    try:
        print(f"*** WARNING: Folder {OUTPUT_PATH_PREFIX} does not exist. Creating.")
        os.mkdirs(OUTPUT_PATH_PREFIX)
    except FileExistsError:
        print(f"*** FileExistsError creating {OUTPUT_PATH_PREFIX}. Exiting.")
        exit()

import tzlocal

def get_file_timezone(file_path):
    # Get the file's modification time
    mod_time = os.path.getmtime(file_path)

    # Convert to a datetime object
    dt = datetime.fromtimestamp(mod_time)

    # Get the system's local timezone
    local_tz = datetime.now(ZoneInfo("UTC")).astimezone().tzinfo

    # Localize the datetime object
    localized_dt = dt.replace(tzinfo=local_tz)

    return localized_dt.tzinfo


def file_creation_datetime(path_to_file):
    """ Get the datetime stamp for a file, 
    falling back to when it was last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    WARNING: Use of epoch time means resolution is to the seconds (not microseconds)
    """
    if path_to_file is None:
        print(f"*** path_to_file="+path_to_file)
    # print_trace("platform.system="+platform.system())
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            timestamp = os.path.getmtime(path_to_file)
            # Convert the timestamp to a human-readable datetime format:
            mod_time = datetime.fromtimestamp(timestamp)
            # Format the datetime to a string:
            formatted_timestamp = mod_time.strftime("%Y-%m-%dT%H:%M:%S")
            # if SHOW_DEBUG: print(f"formatted_timestamp={formatted_timestamp}")
            #return stat.st_birthtime # epoch datestamp like 1696898774.0
            return formatted_timestamp
        except AttributeError as e:
            print(f"*** ERROR: {e}")
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def get_file_size_on_disk(file_path):
    """Returns integer bytes from the OS for a file path """
    try:
        file_size = os.path.getsize(file_path)
        return file_size
        # Alternately:
        # stat_result = os.stat(file_path)
        # return stat_result.st_blocks * 512  # st_blocks is in 512-byte units
    except FileNotFoundError:
        print(f"*** File path not found: {file_path}")
        return None
    except Exception as e:
        print(f"*** Error getting file size: {e}")
        return None


def generate_mondrian():
    """Create a grid and adds random horizontal and vertical lines12.
    """
    # Initialize grid:
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Generate lines
    # TODO: Use golden ratios
    for _ in range(random.randint(6, 15)):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        direction = random.choice(['horizontal', 'vertical'])

        if direction == 'horizontal':
            for i in range(GRID_WIDTH):
                grid[y][i] = 1
        else:
            for i in range(GRID_HEIGHT):
                grid[i][x] = 1

    # Fill areas with primary colors using a flood fill algorithm2:
    for _ in range(random.randint(3, 8)):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        color = random.randint(2, 4)
        flood_fill(grid, x, y, 0, color)

    return grid


def flood_fill(grid, x, y, old_color, new_color):
    """Fill grid with colors:
    """
    if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
        return
    if grid[y][x] != old_color:
        return

    grid[y][x] = new_color
    flood_fill(grid, x+1, y, old_color, new_color)
    flood_fill(grid, x-1, y, old_color, new_color)
    flood_fill(grid, x, y+1, old_color, new_color)
    flood_fill(grid, x, y-1, old_color, new_color)


def draw_mondrian(grid, filename):
    """Use the Cairo graphics library to render the grid as an image2.
    """
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = COLORS[grid[y][x]]
            ctx.set_source_rgb(*color)
            ctx.rectangle(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            ctx.fill()

    surface.write_to_png(filename)


def gen_one_file(in_seq,path_prefix):
    """Generate image and draw to a file.
    """
    # Generate Mondrian-style art in memory:
    mondrian_grid = generate_mondrian()

    # Assemble output file name onto path:
    local_time = time.localtime()
    TZ_OFFSET = time.strftime("%z", local_time)

    # SYS_TIMEZONE = tzlocal.get_localzone()
        # returns "America/Denver"
    # TZ_OFFSET = datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)
        # returns timedelta object representing the offset from UTC1.
    # TZ_CODE = time.tzname[0]   # returns "MST"

    if DATE_OUT_Z:
        # Add using local time zone Z (Zulu) for UTC (GMT):
        now = datetime.now(timezone.utc)
        OUTPUT_FILE_NAME = PROGRAM_NAME+"-"+ now.strftime("%Y%m%dT%H%M%SZ")+"-"+str(in_seq)+".png"
    else:
        # Add using local time zone offset:
        now = datetime.now()
        OUTPUT_FILE_NAME = PROGRAM_NAME+"-"+ now.strftime("%Y%m%dT%H%M%S")+TZ_OFFSET+"-"+str(in_seq)+".png"

    output_file_path = path_prefix + SLASH_CHAR + OUTPUT_FILE_NAME
    if SHOW_DEBUG:
       print(f"*** DEBUG: output_file_path = {output_file_path}")

    # Output to a PNG file:
    draw_mondrian(mondrian_grid, output_file_path )
    file_create_datetime = file_creation_datetime(output_file_path)
    file_bytes = get_file_size_on_disk(output_file_path)  # type = number
    if PRINT_OUTPUT_FILE_LOG:
        print(f"*** LOG: {output_file_path},{file_bytes}")

    return output_file_path


if __name__ == "__main__":

    gened_count = 0
    for seq in range(FILES_TO_GEN):
        gened_count += 1
        output_file_path = gen_one_file(seq,OUTPUT_PATH_PREFIX)

        if OPEN_OUTPUT_FILE:
            img = Image.open(output_file_path)
            # Display the image:
            img.show()

        if DELETE_OUTPUT_FILE:
            os.remove(output_file_path)
            if SHOW_DEBUG:
                print(f"*** DEBUG: file {output_file_path} deleted.")

    if SHOW_SUMMARY_COUNTS:
       if PRINT_OUTPUT_COUNT == 1:
           print(f"*** SUMMARY: 1 file generated.")
       else:
           print(f"*** SUMMARY: {gened_count} files generated.")
