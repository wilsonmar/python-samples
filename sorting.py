#!/usr/bin/env python3

"""sorting.py at https://github.com/wilsonmar/python-samples/blob/main/sorting.py

This program sorts a list of numbers using several algorithms
(bubble sort, merge sort, quicksort),
implementing https://www.youtube.com/watch?v=D6xkbGLQesk "Intro to BigO".

STATUS: Working on macOS.

git commit -m "v007 + full matplotlib stats :sorting.py"

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
# TODO: Capture memory to calculate usage for measuring space complexity.

"""

# For the time taken to execute a small bit of Python code:
import time    # for timed_func()
import timeit
import datetime
from datetime import datetime
import random
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# For timsort():
#from insertion_sort import insertion_sort
#from merge_sort import merge_sorted_lists


def timed_func(func_to_time):
    def timed(*args, **kwargs):
        start = time.perf_counter()
        res = func_to_time(*args, **kwargs)
        print(time.perf_counter() - start)
        return res
    return timed


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


def fibonicci_replace(given_array):
    """ Toy function to sleep instead of
    replaces each element in the given array with the nearest Fibonicci number.
    """
    time.sleep(20 / 1000000)   # 20 microseconds - instead of lookup.
    return given_array


def report_elap_time( task_in, elap_time ):
    """ Vertically aligned columns of human-reable numbers converted to microseconds/nanoseconds:
    Bubble sort  elap_time:   2.8340 microseconds
    Merge sort   elap_time:  13.3750 microseconds
    Quicksort    elap_time:  10.9170 microseconds
    """
    elap_time_ms = float(elap_time) * 1000000
    if SHOW_RUNTIMES:
        # NOTE: Microseconds (µs) are a millionth of a second.
        unit_type_label = "microseconds"
        # FEATURE: Display text a fixed number of characters to achieve vertical alignment:
        print(task_in.ljust(12),f"elap_time: {elap_time_ms:>8.4f} {unit_type_label}")

    # Store in a matrix of a row for each run's x and y:
    global results_x
    global bubble_sort_results
    global merge_sort_results
    global quicksort_results

    if task_in == "Bubble sort":
        if SHOW_RESULTS_CALCS:
            print(f"{task_in} => {task_in} => {elap_time_ms}")
        bubble_sort_results.append(elap_time_ms)
    elif task_in == "Merge sort":
        if SHOW_RESULTS_CALCS:
            print(f"{task_in} => {task_in} => {elap_time_ms}")
        merge_sort_results.append(elap_time_ms)
    elif task_in == "Quicksort":
        if SHOW_RESULTS_CALCS:
            print(f"{task_in} => {task_in} => {elap_time_ms}")
        quicksort_results.append(elap_time_ms)
    else:
        print(f"task_in \"{task_in}\" not found. Programming error.")
        exit(9)


def plot_multiple_lines(x1,bubble_sort_results, merge_sort_results, quicksort_results):
    """
    See https://matplotlib.org/stable/tutorials/pyplot.html
    and https://www.w3schools.com/python/matplotlib_line.asp
    """
    # Generate data for 4 lines
    plt.title('BigO Time Complexity by sorting.py')
    plt.ylabel('Y = Microseconds Transaction Time')

    # no marker='o':
    plt.plot(x1, bubble_sort_results, label='Bubble sort')
    plt.plot(x1, merge_sort_results, label='Merge sort')
    plt.plot(x1, quicksort_results, label='Quicksort')

    current_date = datetime.now()
    run_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
    plt.xlabel(f"X = # tries over {len(x1)} iterations on {run_date}")

    # Calculate positions of floating text:

    if SHOW_RUNTIMES_IN_FUNC:
       print(f"x1={str(x1)}")
    last_x1_index = len(x1) -1
    last_x1 = int(x1[last_x1_index]) -20
    if SHOW_RESULTS_CALCS:
       print(f"last_x1_index = {last_x1_index}")
       print(f"last_x1 = {last_x1}")

    last_bubble_sort_index = len(bubble_sort_results) -1
    last_bubble_sort_y = int(bubble_sort_results[last_bubble_sort_index]) +0.5
    if SHOW_RESULTS_CALCS:
       print(f"last_bubble_sort_index = {last_bubble_sort_index}")
       print(f"last_bubble_sort_y = {last_bubble_sort_y}")
    plt.text(last_x1, last_bubble_sort_y, "Bubble sort O(n)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))

    last_merge_sort_index = len(merge_sort_results) -1
    last_merge_sort_y = int(merge_sort_results[last_merge_sort_index] * 1.1)
    if SHOW_RESULTS_CALCS:
       print(f"last_merge_sort_index = {last_merge_sort_index}")
       print(f"last_merge_sort_y = {last_merge_sort_y}")
    plt.text(last_x1, last_merge_sort_y, "Merge sort O(logN)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))

    last_quicksort_index = len(quicksort_results) -1
    last_quicksort_y = int(quicksort_results[last_quicksort_index] * .9)
    if SHOW_RESULTS_CALCS:
       print(f"last_quicksort_index = {last_quicksort_index}")
       print(f"last_quicksort_y = {last_quicksort_y}")
    plt.text(last_x1, last_quicksort_y, "Quicksort O(logN)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))

    # At upper-left corner:
    plt.plot(bubble_sort_results)
    plt.text(1, last_bubble_sort_y, "O(n!)", fontsize=12, ha='center', va='center',
           bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))

    # At lower-right corner:
    #fake_list = [10] * len(x1)
    #plt.plot(fake_list)
    plt.text(last_x1, 2, "O(1)", fontsize=12, ha='center', va='center',
           bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))
    # TODO: Font Color for floating text.

    # Add a footer:
#    plt.annotate(f"{run_date}",
#                xy=(0.5, -0.15),  # Position of the footer
#                xycoords='axes fraction',  # Use axes coordinates
#                ha='center',  # Horizontally center the text
#                va='top',  # Vertically center the text
#                fontsize=10)  # Set font size
    # Adjust the layout to make room for the footer
#   plt.tight_layout()

    # plt.legend()

    #plt.plot(y2, marker = '*')

    # Display the plot
    plt.show()


if __name__ == "__main__":

    # TODO: SECTION 2 - A Results db is created to store runtimes for each complexity level invocation.
    # TODO: SECTION 3 - A Fibonicci db is accessed to memoize numbers created at O(1) complexity.

    # Processing Preferences:
    LIST_IS_RANDOM = True

    SHOW_UNSORTED = False
    SHOW_SORTED = False

    SHOW_ITERATION = False
    SHOW_RUNTIMES_IN_FUNC = False
    SHOW_RUNTIMES = False
    SHOW_RESULTS_CALCS = False
    SHOW_PLOTS = True

    # Array of numbers increasing geometrically in base 2: 1,2,4,8,16,32,64,128,256,512, etc.
    array_elements_length = 8
    array_elements_start = 2
    elements_array = [array_elements_start * (2**i) for i in range(array_elements_length)]
    if SHOW_RUNTIMES:
        print(f"elements_array={str(elements_array)}")

    # TODO: SECTION 4 - Generate random numbers from the Fibonocci db or gen'd and added to the db.
    # TODO: SECTION 6 - Loop-within-loop: Loop thru each algorithm at larger and larger numbers (N).
        # TODO: Iterate until maximum runtime threshold is reached.

    # Initialize results:
    results_x = []
    bubble_sort_results = []
    merge_sort_results = []
    quicksort_results = []

    cur_iteration = 1
    for index, num_elements in enumerate(elements_array):
        list_strt_value = 1    # Desired start value of range
        list_max_value = num_elements - list_strt_value + 2

        if LIST_IS_RANDOM:
            randomness = "random"
            my_list = []  # initialize list
            for _ in range(num_elements):
                another_number = random.randint(list_strt_value, list_max_value)
                my_list.append(another_number)
        else:  # Construct sequential list:
            randomness = "sequential"   # already sorted!
            if list_strt_value == 0:
                list_max_value -= 2
            # import numpy as np  # https://numpy.org/doc/stable/reference/generated/numpy.arange.html
            my_list = np.arange(list_strt_value, list_max_value, 1 )

        list_element_count = len(my_list)    # within array for sorting
        results_x.append(list_element_count)
        if SHOW_ITERATION:
            print(f"For run iteration {cur_iteration} to {list_max_value} containing " +
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

        # TODO: Add Selection sort, Insertion sort, Counting sort,
        # TODO: Add Timsort, which uses selection & merge sorts. The fastest?

        cur_iteration += 1
        print("")

    if SHOW_PLOTS:
        # Display results of runs to plot using Matplotlib or Seaborn.
        x = np.array(elements_array)
        plot_multiple_lines(results_x,bubble_sort_results, merge_sort_results, quicksort_results)
