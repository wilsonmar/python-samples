#!/usr/bin/env python3

""" roman2int.py at https://github.com/wilsonmar/python-samples/blob/main/roman2int.py

This coverts Roman letters to interger, solving Leetcode #13.
Roman letters are in the bottom of movie credits to make the year of publication less obvious.

STATUS: Working on macOS M2 14.5 (23F79) using Python 3.12.7.
"v001 new for APCSP :roman2int.py"

Based on https://github.com/gahogg/Leetcode-Solutions/blob/main/Roman%20to%20Integer%20-%20Leetcode%2013/Roman%20to%20Integer%20-%20Leetcode%2013.py
explained at https://www.youtube.com/watch?v=JlVOzbOJiv0
"""

def romanToInt(s: str) -> int:
    # The value of each of 7 Roman numerals:
    d = {'I': 1, 'V':5, 'X':10, 'L':50, 'C':100, 'D': 500, 'M':1000}
    n = len(s)
    i = 0  # the incremeting pointer.
    summ = 0  # to accumulate the answer numeric (base 10) year.

    while i < n:
        # Roman numerals are written left-to-right, from the largest to the smallest value.
        # TODO: Add error checking for wrong numeral entered.
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

roman_letters="MCMXCIV"  # 1994
print(f"Roman {roman_letters}=", romanToInt(roman_letters) )

# TODO: Create a GUI calculator so user can just tap each letter instead of typing.