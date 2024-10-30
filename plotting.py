#!/usr/bin/env python3

""" plotting.py at https://github.com/wilsonmar/python-samples/blob/main/plotting.py

This is starter sample code to create common visualizations using matplotlib.

STATUS: Working.
"v001 + new use matplotlib in :plotting.py"

Before running this program:
brew install miniconda
conda create -n py312
conda activate py312
conda install python=3.12 matplotlib numpy -c conda-forge 
chmod +x plotting.py
./plotting.py

TODO: Matplotlib advanced features: https://matplotlib.org/stable/users/explain/quick_start.html
* 3D plotting
* Animation
* Customizable colormaps
* Logarithmic scales
* Twin axes
"""

import matplotlib.pyplot as plt
# FIXME: print(matplotlib.__version__)
import numpy as np

# Globals:
SAVE_PNG = False

# Sample data
#x = [1, 2, 3, 4]
#y = [1, 4, 9, 16]
x = np.array([1, 2, 3, 4])
y = np.array([1, 4, 9,16])


# Create a figure and an axes:
fig, ax = plt.subplots()
ax.set_title('My Line Chart')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
ax.plot(x, y, color='red', linestyle='--', marker='o')
plt.show()
if SAVE_PNG:
    plt.savefig('my_line_chart.png')


plt.suptitle('My Scatter Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.scatter(x, y)
plt.show()
if SAVE_PNG:
    plt.savefig('my_scatterplot.png')


plt.suptitle('My Bar Chart')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.bar(x, y)
plt.show()
if SAVE_PNG:
    plt.savefig('my_bar_chart.png')
# TODO: Stacked Barchart


plt.suptitle('My Histogram')
plt.ylabel('Y-axis')
plt.xlabel('X-axis')
plt.hist(y)
plt.show()
if SAVE_PNG:
    plt.savefig('my_histogram.png')


# TODO: Close pop-up window programmatically vs. manually with control+W.

# TODO: Use https://seaborn.pydata.org/installing.html

