#!/usr/bin/env python3

"""sorting.py at https://github.com/wilsonmar/python-samples/blob/main/sorting.py

This program sorts a list of numbers using several algorithms:
quick sort, bubble sort, merge sort, 
TODO: selection sort, insertion sort, and counting sort.

STATUS: Not working. NameError: name 'stop_time_quick_sort' is not defined

git commit -m "v001 + from sorting.py :sorting.py"

from https://www.cuantum.tech/app/section/41-divide-and-conquer-algorithms-ecd63b96c8dc4f919456d4a54ea43fb7
 See https://aistudio.google.com/app/prompts/time-complexity?_gl=1*9jhuuq*_ga*NTY0MTM5MjUwLjE3MzY5OTM0Mjg.*_ga_P1DBVKWT6V*MTczNjk5MzQyOC4xLjEuMTczNjk5Mzc0NC4yNC4wLjEwMTQ2Njk0NzI.

# Before running this program:
4. In Terminal:
# INSTEAD OF: conda install -c conda-forge ...
python3 -m venv venv
source venv/bin/activate
5. Scan Python program using flake8, etc.
6. Edit the program to define run parameters.
7. # USAGE: Run this program:
chmod +x sorting.py
./sorting.py
8. Within VSCode install Ruff (from Astral Software), written in Rust
   to lint Python code. 
   Ruff replaces Flake8, Pylint, Xenon, Radon, Black, isort, pyupgrade, etc.

"""

# For the time taken to execute a small bit of Python code:
import timeit
from timeit import default_timer as timer

def quick_sort(array):
    """Args: list_to_sort: A list of numbers to be sorted.
    Returns: A new list with the numbers sorted in ascending order.
    """
    global strt_time_quick_sort
    strt_time_quick_sort = timeit.default_timer()
    global stop_time_quick_sort
    if len(array) < 2:
        stop_time_quick_sort = timeit.default_timer()
        return array
    else:
        pivot = array[0]
        less = [i for i in array[1:] if i <= pivot]
        greater = [i for i in array[1:] if i > pivot]
        array = quick_sort(less) + [pivot] + quick_sort(greater)
        stop_time_quick_sort = timeit.default_timer()
        return array


def bubble_sort(array):
    """ The Bubble Sort algorithm has a time complexity of 
    O(n^2) in the worst and average cases, 
    and O(n) in the best case (already sorted list). 
    This is because it iterates through the list multiple times, 
    comparing and swapping adjacent elements. 
    The nested loops lead to the quadratic time complexity.
    """
    global strt_time_bubble_sort
    strt_time_bubble_sort = timeit.default_timer()

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

    global stop_time_bubble_sort
    stop_time_bubble_sort = timeit.default_timer()
    # Return the sorted list
    return sorted_list


def merge_sort(list_to_sort):
    """The Merge Sort algorithm, which has a time complexity of 
    O(n log n). 
    The list is split into sublists of size 1,
    and then merged back together in a sorted order.
    Args:
        list_to_sort: A list of numbers to be sorted.

    Returns:
        A new list with the numbers sorted in ascending order.
    """
    global strt_time_merge_sort
    strt_time_merge_sort = timeit.default_timer()
    if len(list_to_sort) <= 1:
        return list_to_sort

    mid = len(list_to_sort) // 2
    left_half = list_to_sort[:mid]
    right_half = list_to_sort[mid:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    global stop_time_merge_sort
    stop_time_merge_sort = timeit.default_timer()
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


if __name__ == "__main__":

    """ SAMPLE OUTPUT:
    Unsorted list: [1, 9, 5, 2, 1, 8, 6, 6, 3, 4, 10, 7]
    Quick sort:    [1, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]
        elap_time:  5.00003807246685e-07
    Bubble sort:   [1, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]
        elap_time:  5.375011824071407e-06
    Merge sort:    [1, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]
        elap_time:  1.5830155462026596e-06
    """

    my_list = [1, 9, 5, 2, 1, 8, 6, 6, 3, 4, 10, 7]
    # Output: [1, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]
    print("Unsorted list: "+str(my_list))
    sorted_list = quick_sort(my_list)
    print("  Sorted list: "+str(sorted_list) )
    elap_time_quick_sort = stop_time_quick_sort - strt_time_quick_sort
    print(f"Quick sort elap_time:   {elap_time_quick_sort}")

    sorted_list = bubble_sort(my_list)
    elap_time_bubble_sort = stop_time_bubble_sort - strt_time_bubble_sort
    print(f"Bubble sort elap_time:  {elap_time_bubble_sort}")

    sorted_list = merge_sort(my_list)
    elap_time_merge_sort = stop_time_merge_sort - strt_time_merge_sort
    print(f"Merge sort elap_time:   {elap_time_merge_sort}")

