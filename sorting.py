#!/usr/bin/env python3

"""sorting.py at https://github.com/wilsonmar/python-samples/blob/main/sorting.py

This program sorts a list of numbers using several algorithms
(bubble sort, merge sort, quicksort),
implementing https://www.youtube.com/watch?v=D6xkbGLQesk "Intro to BigO".

STATUS: Working on macOS.

git commit -m "v015 mtm sort :sorting.py"

from https://www.cuantum.tech/app/section/41-divide-and-conquer-algorithms-ecd63b96c8dc4f919456d4a54ea43fb7
 See https://aistudio.google.com/app/prompts/time-complexity?_gl=1*9jhuuq*_ga*NTY0MTM5MjUwLjE3MzY5OTM0Mjg.*_ga_P1DBVKWT6V*MTczNjk5MzQyOC4xLjEuMTczNjk5Mzc0NC4yNC4wLjEwMTQ2Njk0NzI.

# Before running this program:
1. In Terminal:
    # INSTEAD OF: uv or  conda install -c conda-forge ...
    python3 -m venv venv
    source venv/bin/activate
2. Scan Python program using flake8, etc.
3. Edit the program to define run parameters.
4. # USAGE: Run this program:
    chmod +x sorting.py
    ./sorting.py
5. Within VSCode install Ruff (from Astral Software), written in Rust
   to lint Python code. 
   Ruff replaces Flake8, Pylint, Xenon, Radon, Black, isort, pyupgrade, etc.

# TODO: SECTION 1 - Set Utilities, parameters, secrets in .env file
# TODO: Capture memory to calculate usage for measuring space complexity.

"""

# For the time taken to execute a small bit of Python code:
import argparse
import datetime
from datetime import datetime
import random
import threading
import time    # for timed_func()
import timeit
from timeit import default_timer as timer

try:
    import matplotlib.pyplot as plt
    # import seaborn as sns
    import numpy as np
except Exception as e:
    print(f"Python module import failed: {e}")
    print(f"Please activate your virtual environment:\n  python3 -m venv venv\n  source venv/bin/activate")
    exit(9)


def timed_func(func_to_time):
    def timed(*args, **kwargs):
        start = time.perf_counter()
        res = func_to_time(*args, **kwargs)
        print(time.perf_counter() - start)
        return res
    return timed


def bubble_sort(array):
    """ The Bubble Sort algorithm has a time complexity of 
    O(n^2) in the worst and average cases, 
    and O(n) in the best case (already sorted list). 
    This is because it iterates through the list multiple times, 
    comparing and swapping adjacent elements. 
    The nested loops lead to the quadratic time complexity.
    """
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

    return sorted_list


def quicksort(array):
    """quicksort has worst-case runtime complexity of O(n^2) but otherwise
    best/average case time & space complexity of O(n log n). 
    But it is not considered "stable" as other sorting algorithms.
    Args: list_to_sort: A list of numbers to be sorted.
    Returns: A new list with the numbers sorted in ascending order.
    """
    # A copy of the list is not needed because swaps use indexes:
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        less = [i for i in array[1:] if i <= pivot]
        greater = [i for i in array[1:] if i > pivot]
        # WARNING: Function calls itself (is recursive):
        array = quicksort(less) + [pivot] + quicksort(greater)

        return array


def insertion_sort(items, left=0, right=None):
    """ This is slightly more efficient than Bubble sort by 
    working on a slice of a list rather than the full list.
    # O(n^2) in worst case as it's less efficient on large lists than quicksort, or merge sort.
    # @author Liam Pulsifer at RealPython
    """
    if right is None:  # If None, we want to sort the full list
        right = len(items) - 1
    for i in range(left + 1, right + 1): # If right is len(items) - 1, this sorts the full list.
        current_item = items[i]
        j = i - 1 # Chose the element right before the current element

        while (j >= left and current_item < items[j]): # Break when the current el is in the right place
            items[j + 1] = items[j] # Moving this item up
            j -= 1 # Traversing "leftwards" along the list

        items[j + 1] = current_item # Insert current_item into its correct spot

    return items


# @timed_func cannot be used because of recursive logic.
def merge_sort(list_to_sort):
    """The Merge Sort algorithm has a time complexity of 
    O(n log n). 
    The list is split into sublists of size 1,
    and then merged back together in a sorted order.
    Args:
        list_to_sort: A list of numbers to be sorted.
    Returns:
        A new list with the numbers sorted in ascending order.
    """
    if len(list_to_sort) <= 1:
        return list_to_sort

    mid = len(list_to_sort) // 2
    left_half = list_to_sort[:mid]
    right_half = list_to_sort[mid:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    return merge(left_half, right_half)

def merge(left, right):
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


def multi_threaded_merge_sort(arr, num_threads=4):
    if num_threads <= 1:
        return merge_sort(arr)

    chunk_size = len(arr) // num_threads
    if chunk_size == 0:
        chunk_size = 1

    sublists = [arr[i:i+chunk_size] for i in range(0, len(arr), chunk_size)]
    if SHOW_RESULTS_CALCS:
        print(f"len(arr)={len(arr)} // num_threads={num_threads} = chunk_size={chunk_size}")

    threads = []
    sorted_sublists = []

    for sublist in sublists:
        thread = threading.Thread(
            target=lambda sl=sublist: sorted_sublists.append(merge_sort(sl))
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    while len(sorted_sublists) > 1:
        new_sublists = []
        for i in range(0, len(sorted_sublists), 2):
            if i+1 < len(sorted_sublists):
                new_sublists.append(merge(sorted_sublists[i], sorted_sublists[i+1]))
            else:
                new_sublists.append(sorted_sublists[i])
        sorted_sublists = new_sublists

    return sorted_sublists[0] if sorted_sublists else []


def timsort(items):
    """ TimSort was the default in Python until v3.11. 
    # Named for its inventor Tim Peters. https://www.youtube.com/watch?v=rbbTd-gkajw&t=8m39s
    # For avg. complexity of O(n log n), it creates "runs" using insertion_sort, then 
    # uses merge-sort on the smallet arrays and merges them. 
    # @author Liam Pulsifer
    """
    # TODO: Test this timsort

    min_subsection_size = 32

    # Sort each subsection of size 32
    # (The real algorithm carefully chooses a subsection size for performance.)
    for i in range(0, len(items), min_subsection_size):
        # WARNING: Recursive function call:
        insertion_sort(items, i, min((i + min_subsection_size - 1), len(items) - 1))

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

    return items


def report_elap_time(cur_batch, task_in, elap_time ):
    """ Vertically aligned columns of human-reable numbers converted to microseconds/nanoseconds:
    8 Bubble sort    elap_time:   1390.2921 microseconds
    8 Insertion sort elap_time:    832.5831 microseconds
    8 Quicksort      elap_time:    951.2911 microseconds
    8 Merge sort     elap_time:    178.7501 microseconds
    """
    elap_time_ms = float(elap_time) * 1000000
    if SHOW_RUNTIMES:
        # NOTE: Microseconds (µs) are a millionth of a second.
        unit_type_label = "microseconds"
        # FEATURE: Display text a fixed number of characters to achieve vertical alignment:
        # TODO: Print elap_time with leading spaces for a fixed vertical show:
        print(f"{cur_batch} {task_in.ljust(14)} elap_time: {elap_time_ms:>8.4f} {unit_type_label}")

    # Store in a matrix of a row for each run's x and y:
    global results_x
    global bubble_sort_results
    global quicksort_results
    global insertion_sort_results
    global merge_sort_results
    global timsort_results
    global mtm_sort_results

    if task_in == "Bubble sort":
        bubble_sort_results.append(elap_time_ms)
    elif task_in == "Quicksort":
        quicksort_results.append(elap_time_ms)
    elif task_in == "Insertion sort":
        insertion_sort_results.append(elap_time_ms)
    elif task_in == "Merge sort":
        merge_sort_results.append(elap_time_ms)
    elif task_in == "Timsort":
        timsort_results.append(elap_time_ms)
    elif task_in == "MTM sort":
        mtm_sort_results.append(elap_time_ms)
    else:
        print(f"task_in \"{task_in}\" not found. Programming error.")
        exit(9)
    if SHOW_RESULTS_CALCS:
        print(f"{task_in} => {task_in} => {elap_time_ms}")


def plot_multiple_lines(x1,bubble_sort_results, merge_sort_results, quicksort_results, mtm_sort_results):
    """
    See https://matplotlib.org/stable/tutorials/pyplot.html
    and https://www.w3schools.com/python/matplotlib_line.asp
    """
    # Generate data for 4 lines
    plt.title(f"BigO Time Complexity by sorting.py on {RANDOMNESS} data")
    plt.ylabel('y = Microseconds Run Time')
    plt.xlabel(f"x = N elements (growing geometrically within {len(x1)} batches)")

    # no marker='o':
    plt.plot(x1, bubble_sort_results, label='Bubble sort')
    plt.plot(x1, quicksort_results, label='Quicksort')
    plt.plot(x1, insertion_sort_results, label='Insertion sort')
    plt.plot(x1, merge_sort_results, label='Merge sort')
    plt.plot(x1, mtm_sort_results, label='MTM sort')
    #plt.plot(x1, timsort_results, label='Timsort')

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
            bbox=dict(facecolor='white', edgecolor='white', alpha=0.7))

    # At upper-left corner:
    current_date = datetime.now()
    run_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
    plt.text(50, last_bubble_sort_y, run_date, fontsize=12, ha='center', va='center',
           bbox=dict(facecolor='white', edgecolor='white', alpha=0.7))

    last_quicksort_index = len(quicksort_results) -1
    last_quicksort_y = int(quicksort_results[last_quicksort_index] * 0.5)
    if SHOW_RESULTS_CALCS:
       print(f"last_quicksort_index = {last_quicksort_index}")
       print(f"last_quicksort_y = {last_quicksort_y}")
    plt.text(last_x1, last_quicksort_y, "Quicksort O(logN)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='white', alpha=0.7))

    last_insertion_sort_index = len(insertion_sort_results) -1
    last_insertion_sort_y = int(insertion_sort_results[last_insertion_sort_index] * 1.1)
    if SHOW_RESULTS_CALCS:
       print(f"last_insertion_sort_index = {last_insertion_sort_index}")
       print(f"last_insertion_sort_y = {last_insertion_sort_y}")
    plt.text(last_x1, last_insertion_sort_y, "Insertion sort", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='white', alpha=0.7))

    last_merge_sort_index = len(merge_sort_results) -1
    last_merge_sort_y = int(merge_sort_results[last_merge_sort_index] * 1.2)
    if SHOW_RESULTS_CALCS:
       print(f"last_merge_sort_index = {last_merge_sort_index}")
       print(f"last_merge_sort_y = {last_merge_sort_y}")
    plt.text(last_x1, last_merge_sort_y, "Merge sort O(logN)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='white', alpha=0.7))

    last_mtm_sort_index = len(mtm_sort_results) -1
    last_mtm_sort_y = int(mtm_sort_results[last_mtm_sort_index] * 1.2)
    if SHOW_RESULTS_CALCS:
       print(f"last_mtm_sort_index = {last_mtm_sort_index}")
       print(f"last_mtm_sort_y = {last_mtm_sort_y}")
    plt.text(last_x1, last_mtm_sort_y, "MTM sort O(?logN)", fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='white', alpha=0.7))

    # TODO: At lower-right corner: timsort()

    # TODO: mtm_sort

    # Adjust the layout to make room for the footer:
#   plt.tight_layout()

    # plt.legend()

    #plt.plot(y2, marker = '*')

    # Display the plot
    plt.show()


if __name__ == "__main__":

    # TODO: SECTION 2 - A Results db is created to store runtimes for each complexity level invocation.

    # Processing Preferences:
    parser = argparse.ArgumentParser()
    # USAGE: ./sorting.py -v -vv -b 8
    parser.add_argument('-q', '--quiet', action='store_true', help="Don't show stats in Terminal")  # on flag
    parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity")  # on flag
    parser.add_argument('-vv', '--trace', action='store_true', help="Increase output trace")  # on flag
    parser.add_argument(
        "-b", "--batches",
        type=str,
        nargs="+",
        help="Batches"
    )
    args = parser.parse_args()
    LIST_IS_RANDOM = True

    SHOW_UNSORTED = False
    SHOW_SORTED = False

    SHOW_RUNTIMES_IN_FUNC = False

    if args.trace:
        SHOW_RESULTS_CALCS = True
    else:
        SHOW_RESULTS_CALCS = False
    if args.verbose:
        SHOW_ITERATION = True
        SHOW_RUNTIMES = True  # True or False
    else:
        SHOW_ITERATION = False
        SHOW_RUNTIMES = False

    SHOW_PLOTS = True
    if args.quiet:
        SHOW_RESULTS_CALCS = True  # True or False
    else:
        SHOW_RESULTS_CALCS = False

    # Array of numbers increasing geometrically in base 2: 1,2,4,8,16,32,64,128,256,512, etc.
    array_elements_start = 2
    if args.batches:
        num_of_batches = int(' '.join(map(str, args.batches)))  # convert list to string to integer.
    else:   # defaults:
        num_of_batches = 8

    batches_array = [array_elements_start * (2**i) for i in range(num_of_batches)]
    if SHOW_UNSORTED:
        print(f"{num_of_batches} batches={str(batches_array)}")

    # TODO: Stop when maximum run time threshold is reached.

    # Initialize results across batches:
    results_x = []
    bubble_sort_results = []
    quicksort_results = []
    insertion_sort_results = []
    merge_sort_results = []
    timsort_results =[]
    mtm_sort_results =[]

    cur_batch = 1
    for index, num_elements in enumerate(batches_array):
        list_strt_value = 1    # Desired start value of range
        list_max_value = num_elements - list_strt_value + 2
        if SHOW_ITERATION:
            print(f"{cur_batch} list_max_value={list_max_value}")
        if LIST_IS_RANDOM:
            RANDOMNESS = "random"
            my_list = []  # initialize list
            for _ in range(num_elements):
                another_number = random.randint(list_strt_value, list_max_value)
                my_list.append(another_number)
        else:  # Construct sequential list:
            RANDOMNESS = "sequential"   # already sorted!
            if list_strt_value == 0:
                list_max_value -= 2
            # import numpy as np  # https://numpy.org/doc/stable/reference/generated/numpy.arange.html
            my_list = np.arange(list_strt_value, list_max_value, 1 )
        # TODO: Generate random numbers in Fibonocci seq.
        if SHOW_UNSORTED:
            print(f"{cur_batch} {RANDOMNESS} my_list={str(my_list)}")

        list_element_count = len(my_list)    # within array for sorting
        results_x.append(list_element_count)
        if SHOW_ITERATION:
            print(f"Run batch {cur_batch} of {list_element_count} {RANDOMNESS} elements:")
               # {list_max_value} containing " +
        if SHOW_UNSORTED:
            print("Unsorted list: "+str(my_list))

        task_name = "Bubble sort"
        strt_time = timeit.default_timer()
        sorted_list = bubble_sort(my_list)
        report_elap_time(cur_batch, task_name, timeit.default_timer() - strt_time)

        if SHOW_SORTED:
            print("  Sorted list: "+str(sorted_list) )

        # Now on to "Divide and Conquer" sorting algorithms:

        task_name = "Insertion sort"
        strt_time = timeit.default_timer()
        sorted_list = insertion_sort(my_list)
        report_elap_time(cur_batch, task_name, timeit.default_timer() - strt_time)

        task_name = "Quicksort"
        strt_time = timeit.default_timer()
        sorted_list = quicksort(my_list)
        report_elap_time(cur_batch, task_name, timeit.default_timer() - strt_time)

        task_name = "Merge sort"
        strt_time = timeit.default_timer()
        sorted_list = merge_sort(my_list)
        report_elap_time(cur_batch, task_name, timeit.default_timer() - strt_time)

        task_name = "MTM sort"
        strt_time = timeit.default_timer()
        sorted_list = multi_threaded_merge_sort(my_list, num_threads=4)
        report_elap_time(cur_batch, task_name, timeit.default_timer() - strt_time)

        # TODO: Add Selection sort, Counting sort, heapsort, etc.?
        # TODO: Add run using NVIDIA GPU for multi-processing merge?

        cur_batch += 1
        print("")

    if SHOW_PLOTS:
        # Display results of runs to plot using Matplotlib or Seaborn.
        x = np.array(batches_array)
        plot_multiple_lines(results_x, bubble_sort_results, merge_sort_results, quicksort_results, mtm_sort_results)

