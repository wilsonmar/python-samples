#!/usr/bin/env python3

# Since Python version 3.7, dictionaries are ordered. 
actions_tuple = {  # as ordered key-value:
    "calculator": ["sys_app", "Calculator.app" ],
    "claude": ["user_app", "Claude.app" ],
    "facebook": ["website", "facebook.com" ],
    "github": ["website", "github.com" ],
    "linked in": ["website", "linkedin.com" ],
    "you tube": ["website", "youtube.com" ],
}
print(f"{actions_tuple}")
tar = "github"  # target element
func, parm = actions_tuple.get(tar, (None, None))
print(f"DEBUG: len(actions_tuple)={len(actions_tuple)} key={tar}, func={func}, parm={parm}")
exit()

# https://www.geeksforgeeks.org/python/python-find-the-tuples-containing-the-given-element-from-a-list-of-tuples/
# any() search stops early once a match is found, making it efficient:
res = [tup for tup in actions_tuple if any(element == tar for element in tup)]
print(res)
exit()


# Based on https://www.geeksforgeeks.org/python/namedtuple-in-python/
import collections
from collections import namedtuple
Action = collections.namedtuple('Actions', ['keyword', 'func', 'parm'])

# REMEMBER: tuples are immutable: does not support item assignment.
A = Action("calculator", "sys_app", "Calculator.app" )
A = Action("claude", "user_app", "Claude.app" )
A = Action("github", "website", "github.com" )

print(f"DEBUG: {A.keyword} {A.func} {A.parm}")
print(getattr(A, 'parm'))


exit()

print("\nSample dictionary:")
my_dict = {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "occupation": "Engineer"
}

# Method 1: Using print() function directly
print("Method 1: Using print() function directly")
print(my_dict)
print()

# Method 2: Iterating through items
print("Method 2: Iterating through items")
for key, value in my_dict.items():
    print(f"{key}: {value}")
print()

# Method 3: Using pprint for prettier output
print("Method 3: Using pprint for prettier output")
from pprint import pprint
pprint(my_dict)
print()

# Method 4: Formatting as a string
print("Method 4: Formatting as a string")
dict_str = "\n".join(f"{k}: {v}" for k, v in my_dict.items())
print(dict_str)
print()


