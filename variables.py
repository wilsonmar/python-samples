#!/usr/bin/env python3

"""variables.py at https://github.com/wilsonmar/python-samples/blob/main/variables.py
"v004 + comma at end of list :variables.py"
STATUS: working but under construction.
This program demonstrates the creation and analysis of various data types of variables,
to experiment with defining and viewing objects of various data types.

BACKGROUND: In Python, when a variable is defined, an object is created.
This is unlike C, which directly allocates a memory location.
The type of data created (such as str or int, etc.) is defined as an object attribute.
This is how Python can have dynamic data typing.

Each object is assigned a unique identifier that can be accessed using the id() function.
This ID is useful when you want to track objects, especially when working with 
mutable data types like lists or dictionaries. 
To know whether two variables point to the same object in memory.

* https://www.w3schools.com/python/python_datatypes.asp

From https://medium.com/pythoneers/28-insanely-useful-python-code-snippets-for-everyday-problems-49aeb95c5927
"""

def define_datatypes():

    # Define None Type: 	NoneType
    x = None
    print(f"x = {x} of {type(x)}")
       # When a return statement is not at the  ottom of a function def, Python implicity returns None.

    print(f"\n")

    print("\n*** Define Text Type: 	str:")
    # https://docs.python.org/3/tutorial/introduction.html#text
    x = "Hello World"
    print(f"x=\"{x}\" of {type(x)}")

    print("\n*** Define Boolean Type: 	bool:")
    # https://docs.python.org/3/library/stdtypes.html#boolean-type-bool
    x = bool(5)
    print(f"bool(5)={x} of {type(x)}")

    print("\n*** Numeric: int, float, complex:")
    # Define Numeric Types: int
    # https://docs.python.org/3/tutorial/introduction.html#numbers
    x = int(20)
    print(f"int({x}) of {type(x)}")

    print("\n*** Define Numeric Types: float:")
    x = float(20.5)
    print(f"float({x}) of {type(x)}")

    # Define Numeric Types: complex numbers:
    # https://docs.python.org/3/library/cmath.html
    x = complex(1j)
    print(f"complex({x}) of {type(x)}")

    # https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
    print("\n*** Sequence: range:")
    # Define Sequence Type: range
    # https://docs.python.org/3/library/stdtypes.html#range
    x = range(6)
    print(f"range(6) = {x} of {type(x)}")
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    list(range(1, 11))

    print("\n*** Sequence: tuple, list to hold collection of items:")
    x1 = ("apple", "banana", "cherry",)
    print(f"x1 = ({x1}) of {type(x1)}")

    print("\n*** Sequence: list to hold collection of items:")
    # Define Sequence Type: tuples and squences:
    # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
    x2 = ["apple", "banana", "cherry",]
    # PROTIP: Comma at end of list makes it easier to copy/paste values.
    print(f"x2 = ({x2}) of {type(x2)}")

    # Nested Tuples:

    # Define Sequence Type: list
    # https://docs.python.org/3/tutorial/introduction.html#lists
    # https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    x = list(("apple", "banana", "cherry"))
    print(f"x = list({x}) of {type(x)}")

    print("\n*** Set: set, frozenset to hold collection of unique items:")
    # Define Set Types: 	set
    # https://docs.python.org/3/tutorial/datastructures.html#sets
    x = {"apple", "banana", "cherry"}
    print(f"x={x} of {type(x)} <- using curly braces")

    # Define Set Types: 	frozenset
    x = frozenset({"apple", "banana", "cherry"})
    print(f"{x} of {type(x)}")

    # Define Mapping Type: 	dict
    # https://docs.python.org/3/tutorial/datastructures.html#dictionaries
    # https://www.youtube.com/watch?v=lTgLOuaQsvk
    x = {"name" : "John", "age" : 36}
    print(f"x = {x} of {type(x)} for Mapping data in key-value pairs:")


    print(f"\n*** Bytes and bits:")
    # Define Binary Types: 	bytes
    x = b"Hello"
    print(f"b\"Hello\" = {x} of {type(x)}")

    # Define Binary Types: 	bytearray
    x = bytearray(5)
    print(f"x = bytearray(5) = {x} of {type(x)}")

    # Define Binary Types: 	memoryview
    x = memoryview(bytes(5))
    print(f"x = memoryview(bytes(5)) = {x} of {type(x)}")


def compare_ids():

    # Define a list:
    a = [1, 2, 3]

    # Print unique ID of the variable 'a'
    print(f"id(a) : {id(a)}")

    # Assign 'a' to a new variable 'b'
    b = a
    print(f"b = a")

    # Print unique ID of variable 'b' to verify if both point to the same object
    print(f"id(b) : {id(b)}")

    # Define a new list and print its unique ID to show the difference
    c = [1, 2, 3]
    print(f"c = [1, 2, 3]")
    print(f"id(c) : {id(c)}")

    # Check if 'a' and 'b' are the same object
    print(f"'a' and 'b' are the same object? {a is b}")
    # Check if 'a' and 'c' are the same object
    print(f"'a' and 'c' are the same object? {a is c}")

print(f"\n*** define_datatypes():")
define_datatypes()
"""
    *** define_datatypes():
    x="Hello World" of <class 'str'>
    bool(5)=True of <class 'bool'>

    Numeric: int, float, complex:
    int(20) of <class 'int'>
    float(20.5) of <class 'float'>
    complex(1j) of <class 'complex'>

    Sequence: range, tuple, list to hold collection of items:
    range(6) = range(0, 6) of <class 'range'>
    x = (('apple', 'banana', 'cherry')) of <class 'tuple'>
    x = list(['apple', 'banana', 'cherry']) of <class 'list'>

    Set: set, frozenset to hold collection of unique items:
    x={'apple', 'banana', 'cherry'} of <class 'set'> <- using curly braces
    frozenset({'apple', 'banana', 'cherry'}) of <class 'frozenset'>
    x = {'name': 'John', 'age': 36} of <class 'dict'> for Mapping data in key-value pair form:

    Bytes:
    b"Hello" = b'Hello' of <class 'bytes'>
    x = bytearray(5) = bytearray(b'\x00\x00\x00\x00\x00') of <class 'bytearray'>
    x = memoryview(bytes(5)) = <memory at 0x102df56c0> of <class 'memoryview'>
    x = None of <class 'NoneType'>
"""

print(f"\n*** compare_ids():")
compare_ids()
"""*** compare_ids(): Expected output when run:
    id(a) : 4382571392
    b = a
    id(b) : 4382571392
    c = [1, 2, 3]
    id(c) : 4381446272
    'a' and 'b' are the same object? True
    'a' and 'c' are the same object? False
"""
