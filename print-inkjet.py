#!/usr/bin/env python3

"""print-inkjet.py at https://github.com/wilsonmar/python-samples/blob/main/print-inkjet.py."""

# SECTION 01: Define Python modules used by this program (in alphabetical order):
# See https://bomonike.github.io/python-samples.py/#PackagesInstalled

# built-in modules:
import os
import subprocess   # to run CLI commands
import time   # for time.sleep(1.5)
from datetime import datetime

# For wall time measurements:
std_strt_datetimestamp = datetime.now()
# For wall time of standard imports:
std_stop_datetimestamp = datetime.now()

# For wall time of xpt (external) imports:
xpt_strt_datetimestamp = datetime.now()
try:
    import numpy as np
    import matplotlib.pyplot as plt

    from fpdf import FPDF   # pip install fpdf2
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    from reportlab.lib.colors import red, green, blue

    from PIL import Image   # Pillow  -> replace with CV2?
    # if verbose: print("(PIL) Image version:",Image.__version__)

    from sh import lp
    import docx
    from docx2pdf import convert
    # import schedule
except Exception as e:
    print(f"Python module import failed: {e}")
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    print("Please activate your virtual environment:\n  python3 -m venv venv\n  source .venv/bin/activate")
    exit(9)
# For wall time of xpt imports:
xpt_stop_datetimestamp = datetime.now()

"""
    # SECTION 01: Preparations before running this program:
    # SECTION 02: Define Python modules used by this program:
    # SECTION 03: Capture pgm start date/time
    # SECTION 04: Define generic utilities to print timed log messages:
    # SECTION 05: Define hard-coded Global variables and their values: COLORS
    # SECTION 06: Define generic utilities to read and delete files and folders:
    # SECTION 07: Define generic utilities to list and print to printers:
        # CHECK_FOR_FILE_IN_PATH if an existing .pdf file exists in path to print.

    # SECTION 08: TODO: Obtain parameters from .env file, cmd parm, or hard-coded default:
    MY_PRINTER, etc.

    # SECTION 08: Create image files (jpg/png):
    # SECTION 09: Create documents in Word format:
    # SECTION 10: Create documents in Word & PDF format:
    # SECTION 11: TODO:    If not, Retrieve & color text from the database (if requested by RETRIEVE_TEXT_FROM_DB from INTEXT_FILEPATH)
    # SECTION 12: TODO:    If not, Create blocks of color (if requested by CREATE_COLOR_BLOCKS)
    # SECTION 13: Create pdf file:
    # SECTION 14: List printers & print file:

    # SECTION 15: Clean up: Delete (remove) .pdf file created by this program if REMOVE_PDF_FILE_CREATED = True    
    # SECTION 16: print_wall_times run stats:

Based on a specified (hard coded) folder/file path,
this program creates a .docx format Microsoft Word file, then
converts it to a .pdf file for generic printing on the default printer.

This is a local solution instead of having the Epson company send pages over the internet:
https://www.youtube.com/watch?v=53nOTAc0Oy8
That EpsonConnect technique prints out a cover sheet as well the file
if you don't uncheck "print email body" under Email Print settings.

# SECTION 01: Preparations before running this program:

# USAGE: Before running this:
   uv pip install Pillow   # for import PIL. The original PIL library is no longer maintained.
   sudo launchctl list | grep org.cups.cupsd
# start it: 
   sudo launchctl start org.cups.cupsd
#
    # Schedule the printing task to run daily at a specific time (e.g., 9:00 AM)
    # schedule.every().day.at("09:00").do(print_sheet)
    # Keep the script running:
    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)
   # cron   # to run every day
   
   uv add reportlab fpdf2 Pillow matplotlib sh python-docx docx2pdf 
   python3 -m venv venv
   # deactivate
   source .venv/bin/activate
   uv run print-inkjet.py

Based on https://www.perplexity.ai/search/how-fix-traceback-most-recent-nbgP9TlPQXKUNqDGUS0LkQ#0
and https://www.perplexity.ai/search/python-code-to-print-to-a-prin-s8yMJhEOSsqSC1HH4gS.hA#0

STATUS: Ruff likes. Works. No lookups yet.
date: "2025-08-18"
"""
__last_commit__ = "v007 + ruff checks & fixes :print-inkjet.py"



# SECTION 03: Define generic utilities to print timed log messages:

# See https://bomonike.github.io/python-samples/#StartingTime
# For wall time of program run:
pgm_strt_datetimestamp = datetime.now()
# the most accurate difference between two times. Used by timeit.
# pgm_strt_perf_counter = time.perf_counter()
# To display date & time of program start:
pgm_strt_timestamp = time.monotonic()
# TODO: Display Z (UTC/GMT) instead of local time
pgm_strt_epoch_timestamp = time.time()
pgm_strt_local_timestamp = time.localtime()
# NOTE: Can't display the dates until formatting code is run below


# -clear Console before starting so output always appears at top of screen.
clear_cli = True       # -clear

show_logging = False

global show_dates_in_logs
show_dates_in_logs = False

# PROTIP: Global variable referenced within functions:
# values obtained from .env file can be overriden in program call arguments:
show_fail = True       # Always show
show_error = True      # Always show
show_warning = True    # -wx  Don't display warning
show_todo = True       # -td  Display TODO item for developer
show_info = True       # -qq  Display app's informational status and results for end-users
show_heading = True    # -q  Don't display step headings before attempting actions
show_verbose = True    # -v  Display technical program run conditions
show_trace = True      # -vv Display responses from API calls for debugging code
show_secrets = False   # Never show

class BColors:
    """Set ANSI escape sequences."""

    BOLD = '\033[1m'       # Begin bold text
    UNDERLINE = '\033[4m'  # Begin underlined text

    HEADING = '\033[37m'   # [37 white
    FAIL = '\033[91m'      # [91 red
    ERROR = '\033[91m'     # [91 red
    WARNING = '\033[93m'   # [93 yellow
    INFO = '\033[92m'      # [92 green
    VERBOSE = '\033[95m'   # [95 purple
    TRACE = '\033[96m'     # [96 blue/green
                 # [94 blue (bad on black background)
    CVIOLET = '\033[35m'
    CBEIGE = '\033[36m'
    CWHITE = '\033[37m'

    RESET = '\033[0m'   # switch back to default color

def print_separator():
    """Put a blank line in CLI output. Used in case the technique changes throughout this code."""
    print(" ")

def print_heading(text_in):
    """Highlight the beginning of a set of messages to come."""
    if show_heading:
        if str(show_dates_in_logs) == "True":
            print('\n***', get_log_datetime(), BColors.HEADING+BColors.UNDERLINE,f'{text_in}', BColors.RESET)
        else:
            print('\n***', BColors.HEADING+BColors.UNDERLINE,f'{text_in}', BColors.RESET)

def print_fail(text_in):
    """Highlights when program should stop."""
    if show_fail:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), BColors.FAIL, "FAIL:", f'{text_in}', BColors.RESET)
        else:
            print('***', BColors.FAIL, "FAIL:", f'{text_in}', BColors.RESET)

def print_error(text_in):
    """Show when a programming error is evident."""
    if show_fail:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), BColors.ERROR, "ERROR:", f'{text_in}', BColors.RESET)
        else:
            print('***', BColors.ERROR, "ERROR:", f'{text_in}', BColors.RESET)

def print_warning(text_in):
    """To remind user about a troubling value."""
    if show_warning:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), BColors.WARNING, f'{text_in}', BColors.RESET)
        else:
            print('***', BColors.WARNING, f'{text_in}', BColors.RESET)

def print_todo(text_in):
    """To remind programmer about a TODO item."""
    if show_todo:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), BColors.CVIOLET, "TODO:", f'{text_in}', BColors.RESET)
        else:
            print('***', BColors.CVIOLET, "TODO:", f'{text_in}', BColors.RESET)

def print_info(text_in):
    """To inform user about changes in values."""
    if show_info:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), BColors.INFO+BColors.BOLD, f'{text_in}', BColors.RESET)
        else:
            print('***', BColors.INFO+BColors.BOLD, f'{text_in}', BColors.RESET)

def print_verbose(text_in):
    """For debugging logic."""
    if show_verbose:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), BColors.VERBOSE, f'{text_in}', BColors.RESET)
        else:
            print('***', BColors.VERBOSE, f'{text_in}', BColors.RESET)

def print_trace(text_in):
    """Display each object as it is created in pgm."""
    if show_trace:
        if str(show_dates_in_logs) == "True":
            print('***',get_log_datetime(), BColors.TRACE, f'{text_in}', BColors.RESET)
        else:
            print('***', BColors.TRACE, f'{text_in}', BColors.RESET)


# SECTION 04: Define hard-coded Global variables and their values.

# The .env location can't be read in from .env:
use_env_file = True    # -env "python-samples.env"
global ENV_FILE
ENV_FILE="python-samples.env"  # hard-coded!

np_img_file_path = "$HOME/.images/print-inkjet.png"
# TODO: Enable specification of path in a CLI attribute:
# TODO: docx_file_path = fr"{user_home_path}/{docx_file_name}"
# docx_file_name = "print-inkjet.py.docx"
# "fr"
#docx_file_path = fr"images/{docx_file_name}"
#pdf_file_name = "print-inkjet.py.pdf"
#pdf_file_path = fr"images/{pdf_file_name}"

SHOW_START_TIME = False
OVERWRITE_FILE_CREATED = True
SHOW_FILE_CONTENTS = False
RETRIEVE_TEXT_FROM_DB = False
CREATE_COLOR_BLOCKS = True
REMOVE_PDF_FILE_CREATED = False
DISPLAY_RUN_STATS = False

LIST_PRINTERS = False
SEND_TO_PRINTER = False
MY_PRINTER = "EPSON_ET_2850_Series"

show_sys_info = True
show_config = True   # not used?


# SECTION 05: Define generic utilities to read and delete files and folders:


#  if show_dates:  https://medium.com/tech-iiitg/zulu-module-in-python-8840f0447801
def get_log_datetime() -> str:
    """Get timestamp for showing on log messages."""
    # from datetime import datetime
    # importing timezone from pytz module
    # from pytz import timezone

    # getting the current time in UTC timezone
    # now_utc = datetime.now(timezone('UTC'))

    # TODO: Give datetime the user or system defined LOCALE:
    #MY_DATE_FORMAT = "%Y-%m-%d %H:%M:%S %Z%z"
    # Format the above DateTime using the strftime() https://stackoverflow.com/questions/7588511/format-a-datetime-into-a-string-with-milliseconds
    time_str=datetime.utcnow().strftime('%F %T.%f')
       # ISO 8601-1:2019 like 2023-06-26 04:55:37.123456 https://www.iso.org/news/2017/02/Ref2164.html
    # time_str=now_utc.strftime(MY_DATE_FORMAT)

    # TODO: Converting to Asia/Kolkata time zone using the .astimezone method:
    # now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    # Format the above datetime using the strftime()
    # print('Current Time in Asia/Kolkata TimeZone:',now_asia.strftime(format))

    return time_str

def get_file_datetime(file_path) -> str:
    """Get the file creation timestamp."""
    creation_time = os.path.getctime(file_path)
    # Convert the timestamp to a datetime object:
    creation_date = datetime.fromtimestamp(creation_time)
    # Print the creation date in a human-readable format:
    return creation_date.strftime('%Y-%m-%d %H:%M:%S')

def get_file_size(file_path) -> str:
    """Get the file size in bytes."""
    try:
        file_size = os.path.getsize(file_path)
        return str(file_size)  # TODO: Format
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# read_file()

# delete_file()

# SECTION 06: TODO: 

# SECTION 07: Read quote from database

def get_quotes():
    """Retrieve random quote from database."""
    if RETRIEVE_TEXT_FROM_DB:
        # TODO: Get quotes from websites (actual lookedup text)
        # InspiringQuotes.com offers daily positive quotes to start your day with a fresh mindset.
        # Shopify's blog provides over 200 motivational quotes for daily inspiration, covering success, life, work, and more. You can pick favorites and make them part of your routine.
        # Smartphone app "Motivation - Daily Quotes" send daily motivational reminders tailored to your interests and needs. They even include categories like self-care, career, wellness, and relationships.
        # If you prefer email, the Foundation for a Better Life offers a free daily inspirational quote via email delivered every weekday.
        # Websites like Inc. Magazine publish daily inspirational quotes, with a collection of 365 quotes for every day of the year.
        # https://www.americanbible.org/engage/daily-bible-reading/
        # https://www.dailyscripture.net/daily-meditation/ features daily scripture readings with meditations.
        red_text = "?"
        green_text = "?"
        blue_text = "?"
        return red_text, green_text, blue_text
    else:
        # Use placeholder text:
        red_text = "Red Text"
        green_text = "Green Text"
        blue_text = "Blue Text"
        return red_text, green_text, blue_text


# SECTION 08: Create image files (jpg/png/webp, etc.):

def gen_color_img():
    """Create images for pure Y, M, K colors."""
    # Set image size (width 300 px for 3 colors, height 100 px)
    width, height = 300, 100
    # Create a new blank RGB image
    Image.new("RGB", (width, height))


def gen_quote_pdf( red_txt, green_txt, blue_txt, out_file_path):
    """Create a PDF with three lines of text: one red, one green, and one blue."""
    # Each injet model of printer AND paper map to a a different RGB numbers
    # based on ICC profiles of the CMYK inks. However, here are estimates
    # for offet-proofing aims (GRACoL 3013 / FOGRA51, D50 to sRGB adapted):

    # from reportlab.lib.pagesizes import letter
    # from reportlab.pdfgen import canvas
    # from reportlab.lib.colors import HexColor
    # from reportlab.lib.colors import red, green, blue
    c = canvas.Canvas(out_file_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 14)
    #c.setFillColor(black)   # color not defined in reportlab.lib.colors ? (40,40,40)
    #c.drawString(10, height - 10, "print-inkjet.py") # pgm_strt_timestamp

    c.setFillColor(red)
    c.drawString(50, height - 100, red_txt)

    # Draw green text
    c.setFillColor(green)
    c.drawString(50, height - 200, green_txt)

    # Draw blue text
    c.setFillColor(blue)
    c.drawString(50, height - 300, blue_txt)

    if CREATE_COLOR_BLOCKS:
        square_size = 20  # points

        # To print pure ink colors, Epson printers often require working in RGB color mode and rely on printer drivers to convert correctly to CMYK ink outputs. For professional pure ink channel printing, specialized RIP software may be needed.

        # using http://wilsonmar.com/1colors.htm for CMYK to RGB
        square_color = HexColor("#0097da")  # Cyan color (Red 0, G 151, B: 218)
        c.rect(10, 200, square_size, square_size, fill=1)
        c.setFillColor(square_color)

        square_color = HexColor("#dc147d")  # Magenta color (Red 220, G: 20, Blue 125)
        c.rect(10, 100, square_size, square_size, fill=1)
        c.setFillColor(square_color)

        square_color = HexColor("#f5e100")  # Yellow color (R 245, G 225, B 0)
        c.rect(10, 300, square_size, square_size, fill=1)
        c.setFillColor(square_color)

        # Lighter versions of these inks have different RGB values, for example:
        # Light Cyan: RGB (128, 255, 255)
        # Light Magenta: RGB (255, 128, 255)
        # Light Black: RGB (128, 128, 128)

    c.save()  # create file
    print(f"*** INFO: {out_file_path} created {get_file_datetime(out_file_path)} \
                ({get_file_size(out_file_path)} bytes)" )


def fpdf_gen_quote_pdf( red_txt, green_txt, blue_txt, out_file_path ):
    """Generate quote pdf using FPDF library."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)

    # Red Text:
    pdf.set_text_color(255, 0, 0)  # RGB for Red
    pdf.cell(200, 10, txt=red_txt, ln=True, align='L')

    # Green Text:
    pdf.set_text_color(0, 255, 0)  # RGB for Green
    pdf.cell(200, 10, txt=green_txt, ln=True, align='L')

    # Blue Text:
    pdf.set_text_color(0, 0, 255)  # RGB for Blue
    pdf.cell(200, 10, txt=blue_txt, ln=True, align='L')

    pdf.output(out_file_path)


# SECTION 09: Create documents in PDF format:



# SECTION 10: TODO:    If not, Retrieve & color text from the database (if requested by RETRIEVE_TEXT_FROM_DB from INTEXT_FILEPATH)
# SECTION 11: TODO:    If not, Create blocks of color (if requested by CREATE_COLOR_BLOCKS)
# SECTION 12: TODO:    If not, Create pdf file.
# SECTION 13: TODO: Delete temporary .pdf file created by this program if REMOVE_PDF_FILE_CREATED = True


# SECTION 10: Define generic utilities to list and print to printers:
        # CHECK_FOR_FILE_IN_PATH if an existing .pdf file exists in path to print.

def show_np_img_file( np_img_file_path_in ):
    """Display numpy matrix file using matplotlib.

    Based on https://www.geeksforgeeks.org/python/matplotlib-pyplot-imshow-in-python/.
    """
    # import numpy as np
    # import matplotlib.pyplot as plt
    #img = mpimg.imread(np_img_file_path_in)
    img = np.random.random((10, 10))  # Pretend this is your image data
    plt.imshow(img, cmap='gray', interpolation='nearest')
       # or cmap='viridis',
    plt.colorbar()  # Adds a scale to the side
    plt.title('Demo Image')
    plt.axis('off')  # Hides the axis, useful for photos
    plt.show()


def list_printers():
    """List printers."""
    if os.name == 'nt':  # For Windows:
        # See https://www.blog.pythonlibrary.org/2010/02/14/python-windows-and-printers/
        # os.startfile(pdf_file_path, "print")
        print("*** FIXME: Add coding to print pdf_file_path on Windows.")
    else:  # For POSIX-based systems (Linux, macOS):
        try:
            result = subprocess.run(['lpstat', '-p'],
                                    capture_output=True,
                                    text=True,
                                    check=True)
            # Split the output into separate lines:
            printer_lines = result.stdout.strip().split('\n')
            # Process each line to extract printer names:
            printers = []
            for line in printer_lines:
                # Example: EPSON_ET_2850_Series is idle.  enabled since Sat Oct 19 09:32:51 2024
                if line.startswith('printer'):
                    # Extract the printer name (second word in the line)
                    printer_name = line.split()[1]
                    printers.append(printer_name)
            return printers
        except subprocess.CalledProcessError:
            print("Error: Unable to retrieve printer list.")
            return []

# See https://www.hexnode.com/mobile-device-management/help/script-to-set-up-printers-on-macos-devices/

def print_file( pdf_file_path ):
    """Print if MY_PRINTER is known."""
        # Printing from a specific folder
        # lp('/your/folder/path/your_filename_here.ext')
    # else:   
    # Print to a specified printer by baking the printer option into the lp command:
    lp_cp = lp.bake('-d')
    lp_cp(MY_PRINTER, pdf_file_path)


def print_subprocess():
    """Print the image file via lp command."""
    # TODO: Find an Epson printer, convert HTML codes to Latin encoding:
    try:
        result = subprocess.run(["lp", "-v"], check=True, capture_output=True, text=True)
        print("Printers:", result.stdout)
        # network dnssd://Brother%20HL-L5200DW%20series._ipp._tcp.local./?uuid=e3248000-80ce-11db-8000-b4220074acab
        # network dnssd://EPSON%20ET-2850%20Series._ipp._tcp.local./?uuid=cfe92100-67c4-11d4-a45f-e0bb9e1ab521
    except subprocess.CalledProcessError as e:
        print("Failed to list printers:", e)
        exit()

    # Print the image file via lp command:
    subprocess.run(["lp", result.stdout], check=True)
    print(f"Sent {result.stdout} to printer")


def print_docx(file_path, printer=""):
    """Print word docx file to specified printer."""
    # TODO: Send to specified printer

    # Read the content of the .docx file
    doc = docx.Document(file_path)

    if SHOW_FILE_CONTENTS:
        print("Content of the .docx file:")
        for paragraph in doc.paragraphs:
            print(paragraph.text)

    # Convert .docx to .pdf
    pdf_path = file_path.rsplit('.', 1)[0] + '.pdf'
    convert(file_path, pdf_path)

    # Print the PDF file
    if os.name == 'nt':  # For Windows
        os.startfile(pdf_path, "print")
    else:  # For Unix-based systems (Linux, macOS)
        subprocess.run(["lpr", pdf_path])
        # 100%|████...████| 1/1 [00:21<00:00, 21.65s/it]

    print(f"*** {pdf_path} sent to the default? printer.")



# SECTION 15: print_wall_times():

def print_wall_times():
    """Print All the timings together for consistency of output."""
    # if DISPLAY_RUN_STATS:
    print_heading("display_run_stats():    Wall times (hh:mm:se.microsecs):")
    # TODO: Write to log for longer-term analytics

    # For wall time of std imports:
    std_stop_datetimestamp = datetime.now()
    std_elapsed_wall_time = std_stop_datetimestamp -  std_strt_datetimestamp
    print_verbose("Import of Python standard libraries: "+ \
        str(std_elapsed_wall_time))

    # For wall time of xpt imports:
    xpt_stop_datetimestamp = datetime.now()
    xpt_elapsed_wall_time = xpt_stop_datetimestamp -  xpt_strt_datetimestamp
    print_verbose("Import of Python extra    libraries: "+ \
        str(xpt_elapsed_wall_time))

    pgm_stop_datetimestamp = datetime.now()
    pgm_elapsed_wall_time = pgm_stop_datetimestamp -  pgm_strt_datetimestamp
    #pgm_stop_perftimestamp = time.perf_counter()
    print_verbose("Whole program run:                   "+ \
        str(pgm_elapsed_wall_time))


###############################################

if __name__ == "__main__":

    if SHOW_START_TIME:
        print_heading("show_dates using localized format:")
        my_local_time = time.localtime()
        print_trace("my_local_time="+str(my_local_time))
        print_trace("pgm_strt_timestamp="+str(pgm_strt_timestamp))

    # SECTION 11: Retrieve & color text from the database (if requested by RETRIEVE_TEXT_FROM_DB from INTEXT_FILEPATH)
    red_txt, green_txt, blue_txt = get_quotes()
    if SHOW_FILE_CONTENTS:
        print(f"red_text={red_txt}, green_text={green_txt}, blue_text={blue_txt}")
    out_file_path = "print-inkjet.py.pdf"
    if os.path.exists(out_file_path):
        # Get the file creation timestamp:
        creation_time = os.path.getctime(out_file_path)
        # Convert the timestamp to a datetime object:
        creation_date = datetime.fromtimestamp(creation_time)
        if creation_date:  # file found:
            # Print the creation date in a human-readable format:
            print(f"*** WARN: {out_file_path} already created {get_file_datetime(out_file_path)} \
                ({get_file_size(out_file_path)} bytes)" )
            if OVERWRITE_FILE_CREATED:
                print(f"*** CAUTION: {out_file_path} being deleted...")
                os.remove(out_file_path)
                gen_quote_pdf( red_txt, green_txt, blue_txt, out_file_path )
            else:
                print(f"*** {out_file_path} NOT created.")
    else:
        gen_quote_pdf( red_txt, green_txt, blue_txt, out_file_path )


    # SECTION 14: List printers & print file:
    if LIST_PRINTERS:
        available_printers = list_printers()
        if available_printers:
            print("*** Available printers:")  # using lpstat -p command:
            for printer in available_printers:
                print(f"- {printer}")
        else:
            print("*** CRTICAL: No printers found. Exiting...")
            exit()

    # Print to MY_PRINTER identified:
    if SEND_TO_PRINTER:
        print_file(out_file_path)

    # SECTION 15: Clean up: Delete (remove) .pdf file created by this program if REMOVE_PDF_FILE_CREATED = True    
    if REMOVE_PDF_FILE_CREATED:
        print(f"CAUTION: Deleting {out_file_path} created {get_file_datetime(out_file_path)} \
            ({get_file_size(out_file_path)} bytes)" )
        os.remove(out_file_path)

    # SECTION 16: print_wall_times run stats:
    if DISPLAY_RUN_STATS:
        print_wall_times()
