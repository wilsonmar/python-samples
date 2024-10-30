#!/usr/bin/env python3
""" print-macos.py at 
STATUS: Not working. conn = cups.Connection() AttributeError: module 'cups' has no attribute 'Connection'
"v002 + new :print-macos.py"

This program runs on macOS to print a list of printers for the user to select for printing.
Tested using Python v3.13 
Need to first convert to pdf file.
"""

# pip install cups:
import cups

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
    print(f"This is only for macOS")
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
