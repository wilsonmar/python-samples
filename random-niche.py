#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# rust noqa: D210 [*] No whitespaces allowed surrounding docstring text

"""Generate a 19-digit cryptographically Secure Random number.

https://github.com/wilsonmar/python-samples/blob/main/random-niche.py

gxp "v008 + show digits for random 19 digitis :random-niche.py"

https://github.com/sobolevn/awesome-cryptography
Based on https://paragonie.com/blog/2016/05/how-generate-secure-random-numbers-in-various-programming-languages#python-csprng
If you aren't using libsodium:
If you need random bytes, use os.urandom().
If you need other forms of randomness, you want an instance of 
   random.SystemRandom() instead of just random.
"""

import sys
import random

# Random bytes
# csprng = os.urandom(32)

csprng = random.SystemRandom()
random_int = csprng.randint(0, sys.maxsize)
random_digits = len(str(random_int))

print(f"At random-niche.py os.urandom(32) => {random_int} ({random_digits} digits)")

