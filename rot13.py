#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rot13.py
At https://github.com/wilsonmar/python-samples/blob/main/rot13.py

git commit -m "v004 + unittest :rot13.py"
STATUS: Working

This program provides a utility to encode text using "ROT13"
(Rotation 13 characters out).
based on: https://en.wikipedia.org/wiki/ROT13
"""

import unittest

# TODO: Make the string a parameter argument:

def encode_rot13(string):
    # FIXME: Handle special characters
    for abcd in ["abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]:
        string = ''.join([abcd[(abcd.index(char) + 13) % 26] if char in abcd else char for char in string])
    return string


if __name__ == "__main__":
    # unittest.main()

    # TODO: Obtain from CLI attribute
    # TODO: Add unit test assertion
    string = "The quick brown fox jumps over the lazy dog"
            # Gur dhvpx oebja sbk whzcf bire gur ynml qbt
    print(f"Encode string : {string}")
    encoded = encode_rot13(string)
    print(f"Encoded string: {encoded}")

    # TODO: Send out log.