#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rot13.py
At https://github.com/wilsonmar/python-samples/blob/main/rot13.py

gas "v003 rename from cyphers.py :rot13.py"
STATUS: Working

This program provides a utility to encode text using "ROT13"
(Rotation 13 characters out).
based on: https://en.wikipedia.org/wiki/ROT13
"""
# TODO: Make the string a parameter argument:
string = "The quick brown fox jumps over the lazy dog"
        # Gur dhvpx oebja sbk whzcf bire gur ynml qbt

for abcd in ["abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]:
	string = ''.join([abcd[(abcd.index(char) + 13) % 26] if char in abcd else char for char in string])

print(string)
