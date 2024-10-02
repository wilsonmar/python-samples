#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cyphers.py
at https://github.com/wilsonmar/python-samples/blob/main/cyphers.py
STATUS: Working
from: https://en.wikipedia.org/wiki/ROT13
"""
# TODO: Put this is a parameter:
string = "Quartz glyph job vext cwm porshrop finks?!"

for abcd in ["abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]:
	string = ''.join([abcd[(abcd.index(char) + 13) % 26] if char in abcd else char for char in string])

print(string)
   # Dhnegm tylcu wbo irkg pjz cbefuebc svaxf?!