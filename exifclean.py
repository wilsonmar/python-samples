#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pillow",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file

"""exifclean.py to remove location and other exif (Exchangeable Image File Format) metadata in photo files within the specified folder.

from https://medium.com/pythoneers/i-wrote-100-python-automation-scripts-these-11-changed-everything-431009f96d6b

BEFORE RUNNING, on Terminal:
   # cd to a folder to receive
   git clone https://github.com/wilsonmar/python-samples.git --depth 1
   cd python-samples
   python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
   uv venv .venv
   source .venv/bin/activate
   uv add pillow --frozen

   ruff check exifclean.py
   chmod +x exifclean.py
   uv run exifclean.py    # Terminal freezes.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__
"""

__last_change__ = "26-03-23 v001 new :exifclean.py"
__status__ = "WORKS on macOS Sequoia 15.6.1"

from PIL import Image  # , JpegImagePlugin
from PIL.ExifTags import TAGS

def fetch_exif(image_path):
    """Fetch exit."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is not None:
            # Convert EXIF data to a readable dictionary
            exif_dict = {TAGS[key]: exif_data[key] for key in exif_data.keys() if key in TAGS and isinstance(exif_data[key], (int, str))}
            return exif_dict
        else:
            print("No EXIF data found in the image.")
            return None
    except Exception as e:
        print(f"Error fetching EXIF data: {e}")
        return None

def remove_exif(image_path, output_path):
    """Remove exif metadata."""
    try:
        image = Image.open(image_path)
        image.save(output_path, exif="")
        print(f"EXIF data removed and saved to {output_path}")
    except Exception as e:
        print(f"Error removing EXIF data: {e}")

if __name__ == "__main__":
    """Main loop."""

    ## Asking Use Image Path:
    image_path = input('Paste your Image path : ')
    
    # Fetch and print EXIF data
    exif_data = fetch_exif(image_path)
    if exif_data:
        print("EXIF Data:")
        for key, value in exif_data.items():
            print(f"{key}: {value}")
    
    # Remove EXIF data and save it on the same location:
    remove_exif(image_path, image_path+'_noexif.png')
