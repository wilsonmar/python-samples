#!/usr/bin/env python3

""" unittest_calculator.py at https://github.com/wilsonmar/python-samples/blob/main/unittest_calculator.py

STATUS: Testing
git commit -m "v002 + description :unittest_calculator.py"

This is a simple calculator as an example of 
how to use Python's Unit Test feature.

"""

# Globals: TODO: Specify in program attributes when calling it.
RUN_UNITTESTS = False
LENGTH_IN = 2
WIDTH_IN = 3
UNIT_NAME = "feet"  # or "meters"


def calculate_rectangle_area(length, width):
    """
    Calculate the area of a rectangle.
    
    Args:
    length (float): The length of the rectangle.
    width (float): The width of the rectangle.
    
    Returns:
    float: The area of the rectangle.
    
    Raises:
    ValueError: If length or width is negative or zero.
    """
    if length <= 0 or width <= 0:
        raise ValueError("*** Length and width must be positive numbers.")
    return length * width


import unittest

class TestRectangleArea(unittest.TestCase):

    def test_positive_numbers(self):
        self.assertEqual(calculate_rectangle_area(4, 5), 20)
        self.assertEqual(calculate_rectangle_area(3.5, 2), 7)

    def test_large_numbers(self):
        self.assertEqual(calculate_rectangle_area(1000000, 1000000), 1000000000000)

    def test_small_numbers(self):
        self.assertAlmostEqual(calculate_rectangle_area(0.1, 0.1), 0.01, places=5)

    def test_negative_numbers(self):
        with self.assertRaises(ValueError):
            calculate_rectangle_area(-4, 5)

    def test_zero(self):
        with self.assertRaises(ValueError):
            calculate_rectangle_area(0, 5)

    def test_non_numeric_input(self):
        with self.assertRaises(TypeError):
            calculate_rectangle_area("4", 5)

if __name__ == '__main__':
    if RUN_UNITTESTS:
        print(f"*** INFO: Running unit tests...")
        unittest.main()
    else:
        calculated_area = calculate_rectangle_area(LENGTH_IN, WIDTH_IN)
        print(f"*** length {LENGTH_IN} x width {WIDTH_IN} = {calculated_area} square {UNIT_NAME}.")

# OUTPUT:
# *** INFO: Running unit tests...
# ......
# ----------------------------------------------------------------------
# Ran 6 tests in 0.000s
# OK