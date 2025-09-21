#!/usr/bin/python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# USAGE: Simulates a 6-sided die rolled repeated until "quit".
#    ./rolldice.py

# For a study in programming user features:
# The value from a few rolls can be skewed.
# But with several thousand rolls, each value should be the same percentage.

# Based on Claude

"""rolldice.py here.

> uv run rolldice.py
> h
Dice Roll Histogram Metrics:
Value  Rolls  Percent   Frequency bar
1     88     17.8% ████████
2     80     16.2% ████████
3     75     15.2% ███████
4     87     17.6% ████████
5     89     18.0% ████████
6     76     15.4% ███████
Total: 495 rolls
Range:                    5.00    (between smallest and largest)
Mode (most common value): 5
Mean (Average):                3.48 
Median:                        4.00 
Standard deviation:            1.71 
Coefficient of Variation:      0.49 (Std. Dev./Average)
Variance (spread of data):     2.93 (high variance)
Skewness (distribution asymmetry):  -0.03 (>0 = tendency for lower values on the left)
Kurtosis (extreme tailedness):      -1.28 (-3 = platykurtic = low (skinny) # of outliers)
"""

__commit_text__ = "2025-09-18 v013 + line graph for outcome vs variance :rolldice.py"

import random
import time     # for timestamp

try:
    import numpy as np
    from scipy import stats
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
except Exception as e:
    print(f"Python module import failed: {e}")
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    #print(f"Please setup your virtual environment:\n  python3 -m venv venv && source venv/bin/activate")
    print("Please setup your virtual environment:\n  uv venv && source .venv/bin/activate")
    print("  uv pip install --upgrade numpy matplotlib scipy")
    exit(9)


#### Global variables:
dice_sides = 6   # as the standard cube in Yahtzee
dice_count = 5   # as in Yahtzee
repeat_count = 1
dice_history = []  # array to store dice roll results
rolled_count = 0
unicode_show = False

dice_faces = {  # Dice emoji Unicode characters
    1: '⚀',  # '\u2680' U+2680
    2: '⚁',  # U+2681
    3: '⚂',  # U+2682
    4: '⚃',  # U+2683
    5: '⚄',  # U+2684
    6: '⚅'   # U+2685
}

def roll_die(sides=6) -> int:
    """Roll a 6-sided (non-physical) die and return an integer."""
    return random.randint(1, sides)


def is_number(s) -> bool:
    """Return True if input s is number data type."""
    try:
        float(s)
        return True
    except ValueError:
        return False

#Reduced width to 10, from 40 so as to make it 1/4
def display_detailed_histogram(dice_history, width=10):
    """Display a detailed text histogram with percentages."""
    if not dice_history:
        print("No data to display")
        return
    
    # Count occurrences
    counts = {}
    for entry in dice_history:
        value = entry['value']
        counts[value] = counts.get(value, 0) + 1
    
    total_rolls = len(dice_history)
    max_count = max(counts.values())
    sorted_values = sorted(counts.keys())
    
    print("histogram of dice roll history (from 1/6 = 16.67%):")
    print(f"{'Value':<5} │ {'Rolls':<5} │ {'Percent':<6} │ {'Frequency bars':<{width}}")
    # print("─" * (width + 25))
    
    for value in sorted_values:
        count = counts[value]
        percentage = (count / total_rolls) * 100
        bar_length = int((count / max_count) * width)
        bar = "█" * bar_length
        
        print(f"{value:5d} │ {count:5d} │ {percentage:5.1f}%  │ {bar:<{width}}")
    
    print("=" * (width + 25))
    print(f" Total: {total_rolls:<14}")



def calculate_histogram_metrics(data, bins=6):
    """Calculate comprehensive metrics for a histogram.
    
    Args:
        data: array-like, the input data
        bins: int or array-like, number of bins or bin edges
    
    Returns
    -------
        dict: Dictionary containing all calculated metrics
    """
    data = np.array(data)
    
    # Create histogram
    counts, bin_edges = np.histogram(data, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width = bin_edges[1] - bin_edges[0]
    
    # Basic statistics
    metrics = {
        'data_size': len(data),
        'num_bins': len(counts),
        'bin_width': bin_width,
        'total_count': np.sum(counts),
        
        # Central tendency
        'mean': np.mean(data),
        'median': np.median(data),
        'mode': stats.mode(data, keepdims=True)[0][0],
        
        # Spread measures
        'std_dev': np.std(data, ddof=1),
        'variance': np.var(data, ddof=1),
        'range': np.max(data) - np.min(data),
        'iqr': np.percentile(data, 75) - np.percentile(data, 25),
        
        # Shape measures
        'skewness': stats.skew(data),
        'kurtosis': stats.kurtosis(data),
        
        # Percentiles
        'min': np.min(data),
        'q1': np.percentile(data, 25),
        'q3': np.percentile(data, 75),
        'max': np.max(data),
        
        # Histogram-specific metrics
        'peak_bin_count': np.max(counts),
        'peak_bin_center': bin_centers[np.argmax(counts)],
        'empty_bins': np.sum(counts == 0),
        'bin_density': counts / (len(data) * bin_width),  # Probability density
        'cumulative_counts': np.cumsum(counts),
        'relative_frequency': counts / len(data),
        
        # Additional metrics
        'coefficient_of_variation': np.std(data, ddof=1) / np.mean(data) if np.mean(data) != 0 else np.inf,
        'mad': stats.median_abs_deviation(data),  # Median Absolute Deviation
        
        # Arrays for plotting
        'bin_edges': bin_edges,
        'bin_centers': bin_centers,
        'counts': counts
    }
    
    # Create the seaborn line plot
    plt.figure(figsize=(10, 6))
    #plt.xticks([1,2,3,4,5,6])
    plt.xticks(metrics['bin_centers'], labels=[1, 2, 3, 4, 5, 6])
    sns.lineplot(x=metrics['bin_centers'], y=metrics['counts'])

    # Add vertical lines for mean, median, and standard deviation
    plt.axvline(metrics['mean'], color='red', linestyle='--', label=f"Mean: {metrics['mean']:.2f}")
    plt.axvline(metrics['median'], color='green', linestyle='--', label=f"Median: {metrics['median']:.2f}")
    #plt.axvline(metrics['mean'] + metrics['std_dev'], color='purple', linestyle=':', label=f"Mean + 1 Std Dev: {metrics['mean'] + metrics['std_dev']:.2f}")
    plt.axvline(metrics['variance'], color='purple', linestyle=':', label=f"variance: {metrics['variance']:.2f}")

    # Set labels and title
    plt.xlabel('Value')
    plt.ylabel('Number of Events')
    plt.title(f"Distribution of Events with Mean, Median, and Variance spread for {metrics['total_count']} rolls")
    plt.legend()
    plt.grid(True)
    #plt.savefig('events_distribution_plot.png')
    plt.show()
    return metrics

def print_histogram_summary(dice_history):
    """Display histogram metrics for dice roll history.
    
    Args:
        dice_history: List of dictionaries containing dice roll history
    """
    if not dice_history:
        print("No dice roll data to display")
        return
    result=[]
    event=[]
    times=[]
    # Extract the 'value' field from each roll in the history
    roll_values = [entry['value'] for entry in dice_history]
    
    # Calculate histogram metrics
    hist_metrics = calculate_histogram_metrics(roll_values, bins=6)
    
    # Print summary
    print("\nDice Roll Histogram Metrics:")
    # Create a simple ASCII histogram
    # print("\nDistribution of dice values:")
    print("Value  Rolls  Percent   Frequency bar")
    for i in range(len(hist_metrics['counts'])):
        #bin_center = hist_metrics['bin_centers'][i]
        count = hist_metrics['counts'][i]
        percent = hist_metrics['relative_frequency'][i] * 100
        # Reduced from 2 to 0.5 to make the graph 1 quater of previous display
        bar = "█" * int(percent * 0.5)  # Scale the bar length
        #print(f"{int(bin_center):2d}   {count:4d}    {percent:5.1f}% {bar}")
        print(f"{i+1}   {count:4d}    {percent:5.1f}% {bar}")
        result.append(i+1)
        event.append(count)
        times.append(percent)
        #print(hist_metrics)     
    print(f"Total: {hist_metrics['data_size']} rolls")
    print(f"Range:                    {hist_metrics['range']:.2f}    (between smallest and largest)")
    print(f"Mode (most common value): {hist_metrics['mode']}")
    print(f"Mean (Average):                {hist_metrics['mean']:.2f} ")
    print(f"Median:                        {hist_metrics['median']:.2f} ")
    print(f"Standard deviation:            {hist_metrics['std_dev']:.2f} ")
    cov = hist_metrics['std_dev'] / hist_metrics['mean']
    #https://www.investopedia.com/terms/c/coefficientofvariation.asp
    print(f"Coefficient of Variation:      {cov:.2f} (Std. Dev./Average)")
    sns.set_theme(style='darkgrid')
    plt.title(f"In {hist_metrics['data_size']} rolls of dice!")
    plt.ylabel('y = Probability of events %')
    plt.xlabel("x= Possible Events ")
    x_values=result
    y_values = times
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    sns.lineplot(x=x_values,y=y_values,marker='o',linestyle='-',color='cornflowerblue')
    plt.show()
    
    
    # Additional statistics:
    if hist_metrics['variance'] > 0:
        variance_text = "(high variance)"
    else:
        variance_text = "(low variance)"
    print(f"Variance (spread of data):     {hist_metrics['variance']:.2f} {variance_text}")

    # https://www.investopedia.com/terms/k/skewness.asp
    if hist_metrics['skewness'] == 0:
        skewness_text = "(=0 = perfectly symmetrical both ends)"
    elif hist_metrics['skewness'] > 0:
        skewness_text = "(>0 = tendency for higher values on the right)"
    else:  # < 0:
        skewness_text = "(>0 = tendency for lower values on the left)"
    print(f"Skewness (distribution asymmetry):  {hist_metrics['skewness']:.2f} {skewness_text}")

    # https://www.investopedia.com/terms/k/kurtosis.asp
    if hist_metrics['kurtosis'] == 3:
        kurtosis_text = "(=3 = mesokurtic = normal # of outliers)"
    elif hist_metrics['kurtosis'] > 3:
        kurtosis_text = "(+3 = leptokurtic = high (wide) # of outliers)"
    else: # < 3
        kurtosis_text = "(-3 = platykurtic = low (skinny) # of outliers)"
    print(f"Kurtosis (extreme tailedness):      {hist_metrics['kurtosis']:.2f} {kurtosis_text}")




if __name__ == "__main__":

    print("UTF-8 characters are too tiny to read:")
    for num, emoji in dice_faces.items():
        print(f"{num}:{emoji} ", end="")
    print("")

    print("\nPress Enter to roll, or type 'q' (press contorl+C) to exit. Press\n")
    print("h for histogram,\n u for unicode, \n n for number, or a ")
    print("number for repeat count:")
    while True:  # infinite loop
        user_input = input()
        if user_input.lower() == 'q':  # for quit like linux commands.
            break
        if user_input.lower() == 'u':  # for unicode
            unicode_show = True
        if user_input.lower() == 'n':  # for number
            unicode_show = False
        if user_input.lower() == 'h':
            #display_detailed_histogram(dice_history)
            print_histogram_summary(dice_history)
        if is_number(user_input):
            # If a number was entered, use it as the rolls to repeat.
            repeat_count = int(user_input)
        else:
            repeat_count = 1
    
        # Repeat rolls:
        for rolls in range(repeat_count):
            if dice_count > 1:
                print(f"\nRolling {dice_count} times: ", end="")
            result_str = ""  # reset from previous roll.
            for i in range(dice_count):
                # print(f"{roll_die()} ", end="")
                roll = roll_die(dice_sides)
                if unicode_show:
                    result_str = result_str + " " + dice_faces[roll]
                else:
                    result_str = result_str + " " + str(roll)
                # TODO: Recognize full house and other Yahtzee combinations.
                round_num = i + 1   # ordinal
                current_epoch = time.time()
                dice_history.append({
                    'round': round_num,
                    'value': roll,
#                   'timestamp': f"{current_epoch}"
                })
            rolled_count += 1  # increment
            # ALT: dice_array = np.random.randint(1, 7, size=5)  # 5 dice
            print(f"{result_str}")
        
    print(f"Thank you for playing {rolled_count} rolls!")

    #print("\n" + "="*60 + "\n")
    # Display detailed histogram:
    display_detailed_histogram(dice_history)

"""
Python features in this program:
* comments
* UTF-8 encoding for non-English characters
* Increment a variable using +=
"""