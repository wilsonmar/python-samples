#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""numpy-matrix.py at https://github.com/wilsonmar/python-samples/blob/main/numpy-matrix.py
This program makes use of the Numpy library to create and manage 2D array matrices.
From https://levelup.gitconnected.com/the-end-of-libraries-why-pythons-biggest-overhaul-could-spell-trouble-for-your-favorite-packages-983726f064ce
"""

import numpy as np
import sys  # built-in

def calculate_size(obj):
    # from https://nedbatchelder.com/blog/202002/sysgetsizeof_is_not_what_you_want.html
    # includes shared objects in count.
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(calculate_size(v) for v in obj.values())
        size += sum(calculate_size(k) for k in obj.keys())
    elif isinstance(obj, (list, tuple, set)):
        size += sum(calculate_size(v) for v in obj)
    elif isinstance(obj, bytes):
        size += len(obj)
    elif isinstance(obj, str):
        size += len(obj.encode('utf-8'))
    elif isinstance(obj, type(None)):
        size += 0
    elif isinstance(obj, np.ndarray):
        if obj.dtype == np.uint8:
            size += obj.nbytes
        else:
            size += obj.nbytes + sys.getsizeof(obj)
    elif isinstance(obj, (int, float)):
        size += sys.getsizeof(obj)
    else:
        size += sum(calculate_size(getattr(obj, attr)) for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith('__'))

    return size

# Creating two 3x3 matrices:
matrix_a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix_b = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

print(f"matrix_a is {matrix_a_bytes} bytes")
print(f"matrix_b is {matrix_b_bytes} bytes")

# Performing matrix multiplication:
result = np.matmul(matrix_a, matrix_b)
print(result)
    # [[ 30  24  18]
    # [ 84  69  54]
    # [138 114  90]]

matrix_a_bytes = calculate_size(matrix_a)
matrix_b_bytes = calculate_size(matrix_b)

