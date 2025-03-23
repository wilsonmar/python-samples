#!/usr/bin/env python3

"""sorting.py at https://github.com/wilsonmar/python-samples/blob/main/sorting.py

This program sorts a list of numbers using several algorithms:
quick sort, bubble sort, merge sort, 
TODO: selection sort, insertion sort, and counting sort.

STATUS: Working on macOS.

git commit -m "v005 + matplotlib :sorting.py"

from https://www.cuantum.tech/app/section/41-divide-and-conquer-algorithms-ecd63b96c8dc4f919456d4a54ea43fb7
 See https://aistudio.google.com/app/prompts/time-complexity?_gl=1*9jhuuq*_ga*NTY0MTM5MjUwLjE3MzY5OTM0Mjg.*_ga_P1DBVKWT6V*MTczNjk5MzQyOC4xLjEuMTczNjk5Mzc0NC4yNC4wLjEwMTQ2Njk0NzI.


# Before running this program:
1. In Terminal:
    # INSTEAD OF: conda install -c conda-forge ...
    python3 -m venv venv
    source venv/bin/activate
2. Scan Python program using flake8, etc.
3. Edit the program to define run parameters.
4. # USAGE: Run this program:
    chmod +x big-o.py
    ./big-o.py
5. Within VSCode install Ruff (from Astral Software), written in Rust
   to lint Python code. 
   Ruff replaces Flake8, Pylint, Xenon, Radon, Black, isort, pyupgrade, etc.

# TODO: SECTION 1 - Set Utilities, parameters, secrets in .env file

"""

# For the time taken to execute a small bit of Python code:
import time    # for timed_func()
import timeit
import random
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# For timsort():
#from insertion_sort import insertion_sort
#from merge_sort import merge_sorted_lists


# Globals:
SECS2MICROSECS = 1000000
ITERATIONS_TODO = 10
LIST_IS_RANDOM = True

SHOW_UNSORTED = True
SHOW_SORTED = True
SHOW_RUNTIMES_IN_FUNC = False
SHOW_RUNTIMES = True


def timed_func(func_to_time):
    def timed(*args, **kwargs):
        start = time.perf_counter()
        res = func_to_time(*args, **kwargs)
        print(time.perf_counter() - start)
        return res
    return timed


def fibonicci():
    pass


def bubble_sort(task_name,array):
    """ The Bubble Sort algorithm has a time complexity of 
    O(n^2) in the worst and average cases, 
    and O(n) in the best case (already sorted list). 
    This is because it iterates through the list multiple times, 
    comparing and swapping adjacent elements. 
    The nested loops lead to the quadratic time complexity.
    """
    strt_time = timeit.default_timer()

    # Create a copy of the list to avoid modifying the original:
    sorted_list = array.copy()
    n = len(sorted_list)

    # Iterate through the list n-1 times:
    for i in range(n-1):
        # Flag to track if any swaps were made in a pass:
        swapped = False
        # Iterate through the unsorted portion of the list:
        for j in range(n-i-1):
            # Compare adjacent elements and swap if necessary:
            if sorted_list[j] > sorted_list[j+1]:
                sorted_list[j], sorted_list[j+1] = sorted_list[j+1], sorted_list[j]
                swapped = True
        # If no swaps were made, the list is already sorted:
        if not swapped:
            break

    stop_time = timeit.default_timer()
    elap_time = stop_time - strt_time
    report_elap_time(task_name, elap_time)

    return sorted_list


def quicksort(task_name,array):
    """quicksort has worst-case runtime complexity of O(n^2) but otherwise
    best/average case time & space complexity of O(n log n). 
    But it is not considered as "stable" as other sorting algorithms.
    Args: list_to_sort: A list of numbers to be sorted.
    Returns: A new list with the numbers sorted in ascending order.
    """
    strt_time = timeit.default_timer()

    # A copy of the list is not needed because swaps use indexes:
    if len(array) < 2:
        stop_time = timeit.default_timer()
        elap_time = stop_time - strt_time
        if SHOW_RUNTIMES_IN_FUNC:
            report_elap_time(task_name, elap_time)
        return array
    else:
        pivot = array[0]
        less = [i for i in array[1:] if i <= pivot]
        greater = [i for i in array[1:] if i > pivot]
        # WARNING: Function calls itself (is recursive):
        array = quicksort(task_name,less) + [pivot] + quicksort(task_name,greater)

        stop_time = timeit.default_timer()
        global elap_time_quicksort
        elap_time = stop_time - strt_time
        if SHOW_RUNTIMES_IN_FUNC:
            report_elap_time(task_name, elap_time)

        global elap_time_quicksort
        elap_time_quicksort =+ elap_time

        return array


# @timed_func cannot be used because of recursive logic.
def merge_sort(task_name,list_to_sort):
    """The Merge Sort algorithm has a time complexity of 
    O(n log n). 
    The list is split into sublists of size 1,
    and then merged back together in a sorted order.
    Args:
        list_to_sort: A list of numbers to be sorted.
    Returns:
        A new list with the numbers sorted in ascending order.
    """
    strt_time = timeit.default_timer()

    if len(list_to_sort) <= 1:
        return list_to_sort

    mid = len(list_to_sort) // 2
    left_half = list_to_sort[:mid]
    right_half = list_to_sort[mid:]

    left_half = merge_sort(task_name,left_half)
    right_half = merge_sort(task_name,right_half)

    # WARNING: Function calls itself (is recursive), so reports elap_time every time:
    stop_time = timeit.default_timer()
    elap_time = stop_time - strt_time
    if SHOW_RUNTIMES_IN_FUNC:
        report_elap_time(task_name, elap_time)

    global elap_time_merge_sort
    elap_time_merge_sort =+ elap_time

    return merge_sort_merge(left_half, right_half)

def merge_sort_merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def insertion_sort(task_name, items, left=0, right=None):
    """ A basic insertion sort, modified slightly to allow sorting
    # a slice of a list rather than the full list if desired.
    # O(n^2) in worst case.
    # @author Liam Pulsifer
    """
    # TODO: Test this insertion_sort
    strt_time = timeit.default_timer()

    if right is None:  # If None, we want to sort the full list
        right = len(items) - 1
    for i in range(left + 1, right + 1): # If right is len(items) - 1, this sorts the full list.
        current_item = items[i]
        j = i - 1 # Chose the element right before the current element

        while (j >= left and current_item < items[j]): # Break when the current el is in the right place
            items[j + 1] = items[j] # Moving this item up
            j -= 1 # Traversing "leftwards" along the list

        items[j + 1] = current_item # Insert current_item into its correct spot

        stop_time = timeit.default_timer()
        global elap_time_insertion_sort
        elap_time = stop_time - strt_time
        if SHOW_RUNTIMES_IN_FUNC:
            report_elap_time(task_name, elap_time)

        global elap_time_insertion_sort
        elap_time_insertion_sort =+ elap_time

    return items


def timsort(task_name, items):
    """ TimSort was the default in Python until v3.11. 
    # Named for its inventor Tim Peters. https://www.youtube.com/watch?v=rbbTd-gkajw&t=8m39s
    # For avg. complexity of O(n log n), it creates "runs" using insertion_sort, then 
    # uses merge-sort on the smallet arrays and merges them. 
    # @author Liam Pulsifer
    """
    # TODO: Test this timsort
    strt_time = timeit.default_timer()

    min_subsection_size = 32

    # Sort each subsection of size 32
    # (The real algorithm carefully chooses a subsection size for performance.)
    for i in range(0, len(items), min_subsection_size):
        # WARNING: Recursive function call:
        insertion_sort(task_name, items, i, min((i + min_subsection_size - 1), len(items) - 1))

    # Move through the list of subsections and merge them using merge_sorted_lists
    # (Again, the real algorithm carefully chooses when to do this.)
    size = min_subsection_size
    while size < len(items):
        for start in range(0, len(items), size * 2):
            midpoint = start + size - 1
            end = min((start + size * 2 - 1), (len(items) - 1)) # arithmetic to properly index

            # Merge using merge_sorted_lists
            merged_array = merge_sorted_lists(
                items[start:midpoint + 1],
                items[midpoint + 1:end + 1])

            items[start:start + len(merged_array)] = merged_array # Insert merged array
        size *= 2 # Double the size of the merged chunks each time until it reaches the whole list

        stop_time = timeit.default_timer()
        global elap_time_timsort
        elap_time = stop_time - strt_time
        if SHOW_RUNTIMES_IN_FUNC:
            report_elap_time(task_name, elap_time)

        global elap_time_timsort
        elap_time_timsort =+ elap_time

    return items


def report_elap_time( task_name, elap_time ):
    """ Display vertically aligned columns:
    Bubble sort  elap_time:   2.8340 microseconds
    Merge sort   elap_time:  13.3750 microseconds
    Quicksort    elap_time:  10.9170 microseconds
    """
    if SHOW_RUNTIMES:
        # NOTE: Microseconds (µs) are a millionth of a second.
        elap_time_ms = float(elap_time) * 1000000
        unit_type_label = "microseconds"
        # FEATURE: Display text a fixed number of characters to achieve vertical alignment:
        print(task_name.ljust(12),f"elap_time: {elap_time_ms:>8.4f} {unit_type_label}")


def plot_multiple_lines(results_array):
    """
    See https://matplotlib.org/stable/tutorials/pyplot.html
    and https://www.w3schools.com/python/matplotlib_line.asp
    """
    # Generate data for 4 lines
    plt.title('BigO Complexity (FAKE NUMBERS)')
    plt.xlabel('X - Number of elements')
    plt.ylabel('Y - Microseconds Perf.')

    x = np.array([8, 16, 32, 64, 128, 256, 512, 1024])

    # Floating text "O(log N), O(n), O(1), O(n^2)
    plt.text(50, 2300, "O(n!)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))

    plt.text(150, 2000, "O(N^2)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))

    y1 = np.array([20, 40, 80, 160, 320, 640, 1280, 2560])
    plt.plot(x, y1, label='Bubble sort')
    plt.text(1000, 2200, "O(n)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))

    y2 = np.array([2, 4, 50, 100, 200, 230, 240, 256])
    plt.plot(x, y2, label='Merge sort')
    plt.text(800, 300, "O(logN)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))

    y3 = np.array([2, 2, 2, 2, 2, 2, 2, 2])
    plt.plot(x, y3, label='Memoized')
    plt.text(1000, 50, "O(1)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))

    plt.legend()

    # TODO: Add labels and title
    # plt.plot(y1, marker = 'o')
    #plt.plot(y2, marker = '*')

    # Display the plot
    plt.show()


if __name__ == "__main__":

    # TODO: SECTION 2 - A Results db is created to store runtimes for each complexity level invocation.
    # TODO: SECTION 3 - A Fibonicci db is accessed to memoize numbers created at O(1) complexity.

    cur_iteration = 1     # of max_val_in_list
    max_val_in_list = 8.0

    # TODO: SECTION 6 - Loop-within-loop: Loop thru each algorithm at larger and larger numbers (N).
        # TODO: Iterate until maximum runtime threshold is reached.

    # TODO: SECTION 4 - Generate random numbers from the Fibonocci db or gen'd and added to the db.

    num_elements = 8    # Number of entries in my_list

    if LIST_IS_RANDOM:
        randomness = "random"
        my_list = []  # initialize list
        list_strt_value = 1        # Start of range for random numbers (e.g., between 1 and 100)
        list_max_value = 100
        for _ in range(num_elements):
            another_number = random.randint(list_strt_value, list_max_value)
            my_list.append(another_number)
    else:  # Construct sequential list:
        randomness = "sequential"
        list_strt_value = 1       # Start of range for random numbers (e.g., between 1 and 100)
        list_max_value = 10
        my_list = [1, 9, 5, 2, 10, 8, 6, 3, 4, 7]

    list_element_count = len(my_list)    # within array for sorting
    print(f"For run iteration {cur_iteration} to {max_val_in_list} containing " +
          f"{list_element_count} {randomness} elements:")

    if SHOW_UNSORTED:
        print("Unsorted list: "+str(my_list))
    sorted_list = bubble_sort("Bubble sort",my_list)
    if SHOW_SORTED:
        print("  Sorted list: "+str(sorted_list) )
    # TODO: Saved reported times to array for showing at any time.

    task_name = "Merge sort"
    sorted_list = merge_sort(task_name,my_list)
    report_elap_time(task_name, elap_time_merge_sort)

    task_name = "Quicksort"
    sorted_list = quicksort(task_name,my_list)
    report_elap_time(task_name, elap_time_quicksort)

    """ SAMPLE OUTPUT:
    For run iteration 1 to 8.0 containing 8 elements:
    [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    Unsorted list: [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    Bubble sort  elap_time:   2.8340 microseconds
    Sorted list: [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    Merge sort   elap_time:  13.3750 microseconds
    Quicksort    elap_time:  10.9170 microseconds
    """

    print("\n")
    # TODO: Increase number in logN for log-log plotting:
    print(f"For run iteration 2 of 16 numbers:")
    # my_list = [1, 9, 5, 2, 1, 8, 6, 6, 3, 4, 10, 7, 1, 9, 5, 2]
    # Output: [1, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]
    print("...") # TODO

    # TODO: In results show human-reable numbers converted to microseconds/nanoseconds.

    # TODO: Add Timsort, a combination of sorts. The fastest?
    # TODO: Add Selection sort, Insertion sort, Counting sort,

    # TODO: Read results of runs to plot using Matplotlib or Seaborn.
        # See my plotting.py

    # results_array = (Iteration, )
    x = np.array([1, 2, 3, 4, 5])
    plot_multiple_lines(x)
