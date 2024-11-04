#!/usr/bin/env python3

""" roman2int.py at https://github.com/wilsonmar/python-samples/blob/main/roman2int.py

This coverts Roman letters to interger, solving Leetcode #13.
(Roman letters are in the bottom of movie credits to make the year of publication less obvious.)

STATUS: WORKING on macOS M2 14.5 (23F79) using Python 3.12.7.
git commit -m "v004 + err check input() :roman2int.py"

Based on https://github.com/gahogg/Leetcode-Solutions/blob/main/Roman%20to%20Integer%20-%20Leetcode%2013/Roman%20to%20Integer%20-%20Leetcode%2013.py
explained at https://www.youtube.com/watch?v=JlVOzbOJiv0
"""

# Globals:
ROMAN_DEFAULT="MCMXCIV"  # 1994
SHOW_INPUTS = True

# Romans use 7 numerals with varying values:
d = {'I': 1, 'V':5, 'X':10, 'L':50, 'C':100, 'D': 500, 'M':1000}
if SHOW_INPUTS:
    print(f"roman_letters={d}")


def romanToInt(s: str) -> int:
    """ Convert string to base 10 numbers """
    n = len(s)
    i = 0  # the incremeting pointer.
    summ = 0  # to accumulate the answer numeric (base 10) year.

    while i < n:
        # Roman numerals are written left-to-right, from the largest to the smallest value.
        # TODO: Add error checking for wrong numeral entered:
        if s[i] not in d:
            return f"*** ERROR: {s[i]} is not a Roman numeral."
        #if s[i+1] not in d:
        #    return "are not Roman numerals."
        if i < n - 1 and d[s[i]] < d[s[i+1]]:
            # Exception: numeral "IV" is 4 by subtracting 1 from 5 (the "V"):
            summ += d[s[i+1]] - d[s[i]]
            i += 2
        else:
            summ += d[s[i]]
            i += 1
    return summ
    # Time: O(n)
    # Space: O(1)


def test_roman2int():
    # Test case 1: Normal case
    assert romanToInt("MCMXCIV") == 1994, "Should be 1994"


###############

if __name__ == "__main__":

    while True:
        roman_letters = input(f"Roman numerals: ")
        # Press Enter without entry to exit:
        if roman_letters is None:
            exit()

        roman_letters = roman_letters.upper()
        response = romanToInt(roman_letters)
        if response :
            print(f"{response}")
        else:
            print(f"Roman {roman_letters}", response )
            exit()

# TODO: Add assert in unit test statements.
# TODO: Create a GUI calculator so user can just tap each letter instead of typing.