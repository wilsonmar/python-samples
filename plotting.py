#!/usr/bin/env python3

""" plotting.py at https://github.com/wilsonmar/python-samples/blob/main/plotting.py

This is starter sample code to create common visualizations using matplotlib.

STATUS: Working on macOS M2 14.5 (23F79) using Python 3.12.7.
"v003 + density histogram :plotting.py"

Before running this program:
brew install miniconda
conda create -n py312
conda install -c conda-forge python=3.12 matplotlib numpy scienceplots
conda activate py312
chmod +x plotting.py
./plotting.py

See https://matplotlib.org/stable/users/explain/quick_start.html

TODO: Matplotlib advanced features: 
* Twin axes
* Logarithmic scales
* Customizable colormaps
* 2D Contour Plots
* 3D plotting
* Animations https://www.youtube.com/watch?v=bNbN9yoEOdU

TODO: Use https://seaborn.pydata.org/installing.html
See https://www.youtube.com/watch?v=ooqXQ37XHMM for Seaborn
"""

import matplotlib.pyplot as plt
# FIXME: print(matplotlib.__version__)
import numpy as np
import scienceplots  # https://github.com/garrettj403/SciencePlots


# Globals:
SAVE_PNG = False  # FIXME: png files created with blanks.


# STAGE: Define sample data:
#x = [1, 2, 3, 4]
#y = [1, 4, 9, 16]
x = np.array([1, 2, 3, 4])
y = np.array([1, 4, 9,16])


# STAGE: Define enviornment:
plt.style.use(['science','ieee','no-latex','grid'])  # https://github.com/garrettj403/SciencePlots/wiki/Gallery
plt.rcParams.update({'figure.dpi': '100'})    # dots per inch for IEEE publications


# STAGE: Create a density histogram: https://www.youtube.com/watch?v=cTJBJH8hacc&t=9m10s
# https://github.com/lukepolson/youtube_channel/blob/main/Python%20Tutorial%20Series/matplotlib_essentials.ipynb
# DEFINITION: A density plot normalizes the area of the histogram sums to 1.
res = np.random.randn(1000)*0.2 + 0.4

plt.suptitle('Sample Density Histogram')
plt.ylabel('Frequency')
plt.xlabel('X-axis')
#plt.figure(figsize=(8,3))
plt.hist(res, bins=5, density=True)
plt.show()
if SAVE_PNG:
    plt.savefig('my_histogram.png')

exit()

# STAGE: Create a scatter dots plot:
# From https://matplotlib.org/stable/users/explain/quick_start.html#types-of-inputs-to-plotting-functions
np.random.seed(19680801)  # seed the random number generator.
data = {'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)}
data['b'] = data['a'] + 10 * np.random.randn(50)
data['d'] = np.abs(data['d']) * 100

fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
ax.set_title('Sample Scatter Dots Plot')
ax.scatter('a', 'b', c='c', s='d', data=data)
ax.set_xlabel('entry a')
ax.set_ylabel('entry b')

# See https://matplotlib.org/stable/users/explain/text/annotations.html#basic-annotation
ax.annotate('(0,0)\nzero', xy=(0, 0), xytext=(10, 40),
            arrowprops=dict(facecolor='grey', shrink=0.05))
plt.show()
if SAVE_PNG:
    plt.savefig('my_scatterdots.png')


# STAGE: Create a scatter plot: https://www.youtube.com/watch?v=cTJBJH8hacc
plt.suptitle('Sample Scatter Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.scatter(x, y)
plt.show()
if SAVE_PNG:
    plt.savefig('my_scatterplot.png')
# TODO: Add regression line.


# STAGE: Create a line chart:
fig, ax = plt.subplots()
ax.set_title('Sample Line Chart')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
ax.plot(x, y, color='red', linestyle='--', marker='o')
plt.show()
if SAVE_PNG:
    plt.savefig('my_line_chart.png')


# STAGE: Create a bar chart:
plt.suptitle('Sample Bar Chart')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.bar(x, y)
plt.show()
if SAVE_PNG:
    plt.savefig('my_bar_chart.png')
# TODO: Stacked Barchart


# TODO: Close pop-up window programmatically vs. manually with control+W.


# A figure with one Axes on the left, and two on the right:
#fig, axs = plt.subplot_mosaic([['left', 'right_top'],
#                               ['left', 'right_bottom']])