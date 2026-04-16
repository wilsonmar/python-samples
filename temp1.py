#!/usr/bin/env python3

"""other-charts.py here.

Create chart for the data side-by-side using plt.subplots().

Based on https://www.youtube.com/watch?v=B_cAyrU1Jw0&t=76s
TECHNIQUE: Install module not in Pip but in GitHub:
pip install git+https://github.com/parafoxia/python-touch-id
# Make the scripts executable: 
chmod +x python-scripts/install-python && chmod +x python-scripts/uninstall-python
# Add the scripts to your path by adding the following to your .bashrc/.zshrc/etc.: 
PATH=$PATH:/path/to/python-scripts
# Apply the changes: source .bashrc

"""

__last_change__ = "25-10-02 v013 + Side-by-Side Plotting"


# Internal imports (no pip/uv add needed):
#from datetime import datetime, timezone
#import sys
from pathlib import Path

def define_path(*path_parts):
    """
    Define a cross-platform file path by joining given parts.
    Works seamlessly on Windows, macOS, and Linux.
    
    Args:
        path_parts: Variable length argument list of path elements (strings).
        
    Returns:
        A Path object representing the combined path.
    """
    return Path(*path_parts)

# Example usage
p = define_path("folder", "subfolder", "file.txt")
print(p)  # Prints path using correct slashes on current OS

exit()

try:
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import statsmodels.multivariate.manova as manova    
    
except Exception as e:
    print(f"Python module import failed: {e}")
    print("Please activate your virtual environment:\n  python3 -m venv venv\n  source venv/bin/activate")
    sys.exit(9)

import time

from io import StringIO
from dotenv import dotenv_values

# Create an in-memory stream with key-value pairs
env_content = "API_KEY=\"12345\"\nDB_NAME=testdb\n"
stream = StringIO(env_content)
stream.seek(0)  # Ensure the cursor is at the start

# Parse key-value pairs
config = dotenv_values(stream=stream)

print(config)  # Output: {'API_KEY': '12345', 'DB_NAME': 'testdb'}


print("Times")
print("%42.21f" % time.time())
#print("%42.21f" % time.clock())
print("%42.21f" % time.monotonic())
print("%42.21f" % time.perf_counter())
print("%42.21f" % time.process_time())

print("Resolution in sec")
print("%.21f" % time.get_clock_info('time').resolution)
#print("%.21f" % time.get_clock_info('clock').resolution)
print("%.21f" % time.get_clock_info('monotonic').resolution)
print("%.21f" % time.get_clock_info('perf_counter').resolution)
print("%.21f" % time.get_clock_info('process_time').resolution)

