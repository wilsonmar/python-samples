#!/usr/bin/env python3

"""dundars-list.py here.

https://github.com/wilsonmar/python-samples/blob/main/dunders-list.py

This script lists the value of module-level special dunder variables 
from all python (.py) files in this repo, without opening the files.
Examples: (such as <tt>__last_change__</tt>)
```
    __license__ = "MIT"
    __commit_date__ = "2025-05-20"
    __version__ = "1.0.0". # https://peps.python.org/pep-0396/
    __status__ = "Debugging"
    __doc__ = "This module demonstrates the use of custom dunder (double underscore) variables in Python."
    __last_change__ = "25-05-20 v001 + new :dunders-list.py"
```
https://www.pythonmorsels.com/dunder-variables/
Dunder (double underscore) variables in the module define metadata about the program. PEP specifies that such variables can be read by other programs without opening the source code.

Run usage:
    ruff check dundars-list.py
    chmod +x dundars-list.py
    ./dundars-list.py
"""
__doc__ = "List the contents of special dunder variables from all python (.py) files in this repo, without opening the files."
__status__ = "Debugging"
__last_change__ = "25-09-11 v007 + fix list with no dunder by pgm :dundars-list.py"

import os
import time
import ast  # has coding error.

SHOW_VERBOSE = False
SHOW_DEBUG = False


def get_module_docstring(module_path):
    """Get value of __doc__ for module."""
    with open(module_path, 'r', encoding='utf-8') as file:
        source = file.read()
    parsed = ast.parse(source)
    return ast.get_docstring(parsed)


def print_sorted_last_change(folder_path="."):
    """Get list of all Python files with their full paths."""
    py_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.py')]

    # Sort files by last modification time:
    py_files.sort(key=os.path.getmtime)
    
    for filepath in py_files:
        pgm_name = os.path.basename(filepath)
        # DateTime Last Modified such as "2024-04-20 10:05:08 AM MDT-0600"
        mod_time = os.path.getmtime(filepath)
        readable_time = time.strftime('%Y-%m-%d %I:%M:%S %p %Z%z', time.localtime(mod_time))
        print(f"{pgm_name:<30}  {readable_time}")
            # TODO: File size
        if SHOW_VERBOSE:
            print(f"   {__last_change__}")

            #print(f"   {__doc__}")
            #docstring = get_module_docstring(os.path.basename(filepath))
            #print(f"    {docstring}")

            #print(f"   {os.path.basename(filepath).__last_change__}")
            #print([method for method in dir(obj) if method.startswith('__') and method.endswith('__')])
    print(f"{len(py_files)} *.py files listed.")

# Example usage: Replace '.' with the folder you want to inspect
print("\n# All __last_change__ dundar entries:")
print_sorted_last_change('.')

if SHOW_DEBUG:
    print("\n# All dundar methods:")
    # See https://www.pythonmorsels.com/every-dunder-method/
    # See https://rszalski.github.io/magicmethods/
    dunders = [method for method in dir(int) if method.startswith('__') and method.endswith('__')]
    print(dunders)

