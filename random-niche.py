#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
"""
This is app.py at 
https://github.com/bomonike/memon/blob/main/random.py

gas "v007 subst urandom for random :app.py"

https://github.com/sobolevn/awesome-cryptography
Based on https://paragonie.com/blog/2016/05/how-generate-secure-random-numbers-in-various-programming-languages#python-csprng
Cryptographically Secure Randomness in Python
If you aren't using libsodium:
If you need random bytes, use os.urandom().
If you need other forms of randomness, you want an instance of 
   random.SystemRandom() instead of just random.
"""

import os
import sys
import random

# Random bytes
bytes = os.urandom(32)
csprng = random.SystemRandom()

# Random (probably large) integer
random_int = csprng.randint(0, sys.maxint)

#####################################################
# FIXME: Here is the response the last time this was run:
#Traceback (most recent call last):
#  File "/Users/johndoe/github-wilsonmar/python-samples/./random.py", line 19, in <module>
#    import random
#  File "/Users/johndoe/github-wilsonmar/python-samples/random.py", line 23, in <module>
#    csprng = random.SystemRandom()
#             ^^^^^^^^^^^^^^^^^^^
#AttributeError: partially initialized module 'random' has no attribute 'SystemRandom' (most likely due to a circular import)
