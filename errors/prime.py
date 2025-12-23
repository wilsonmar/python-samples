#!/usr/bin/env python3

"""prime.py here.

Identity whether a candidate number is prime.

About the 10th largest ECP found use by DeCSS to bypass MPAA copyright in 1999
See https://youtube.com/shorts/wYKHyTxDbZ0?si=9oSnUG1ixC_sgfVG
https://t5k.org (The Prime Glossary)

"""
from math import sqrt

def is_prime(number):
    """Return True or false if number is prime."""
    if not isinstance(number, int):
        raise TypeError(
            f"integer number expected, got {type(number).__name__}"
        )
    if number < 2:
        return False
    for candidate in range(2, int(sqrt(number)) + 1):
        if number % candidate == 0:
            return False
    return True

print(is_prime(-3))