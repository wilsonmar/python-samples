#!/usr/bin/env python3

""" print-cups.py at https://github.com/wilsonmar/python-samples/blob/main/print-cups.py

STATUS: Working but under construction on macOS M2 14.5 (23F79) using Python 3.12.7.
git commit -m "v002 + docstring desc ren cups.py :print-cups.py"

This makes use of the Linux cups utility to control printers.

Before running this program:
brew install miniconda
conda create -n py312
conda activate py312
# conda install -c conda-forge python=3.12 matplotlib numpy scienceplots
   # ModuleNotFoundError: No module named 'pycups'
pip install pycups  docx  docx2pdf  
chmod +x print-cups.py  # pycups-2.0.4
./print-cups.py
"""

# pip install pycups, docx, docx2pdf
import pycups
import docx
from docx2pdf import convert
# import schedule

# built-in modules:
import os
import datetime
import subprocess   # to run CLI commands

# Globals:

def list_printers():
    conn = cups.Connection()
    printers = conn.getPrinters()

    print("Available printers:")
    for i, printer in enumerate(printers.keys(), 1):
        print(f"{i}. {printer}")

    return list(printers.keys())

def select_printer(printers):
    while True:
        try:
            choice = int(input("Enter the number of the printer you want to select: "))
            if 1 <= choice <= len(printers):
                return printers[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    printers = list_printers()

    if not printers:
        print("No printers found.")
        return

    selected_printer = select_printer(printers)
    print(f"You selected: {selected_printer}")

    # Set the selected printer as the default
    conn = cups.Connection()
    conn.setDefault(selected_printer)
    print(f"{selected_printer} has been set as the default printer.")

if __name__ == "__main__":
    main()
