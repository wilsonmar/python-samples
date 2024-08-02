# binary-search.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 JetBloom LLC
# SPDX-License-Identifier: MPL-2.0
# from https://www.youtube.com/watch?v=BgLTDT03QtU&t=11m3s

# STATUS: errors:
# ./binary-search.py: line 7: nums: command not found
# ./binary-search.py: line 8: target: command not found
# ./binary-search.py: line 9: syntax error near unexpected token `('
# ./binary-search.py: line 9: `l, r = 0, len(nums) - 1'

print("binary-search.py")
nums = [1, 2, 3, 4, 5]
target = 6
l, r = 0, len(nums) - 1
while l <= r:
    m = (l + 4) // 2
    if target < nums[m]:
        r = m - 1
    elif target > nums[m]:
        l = m + 1
    else:
        print("m=",m)
        break