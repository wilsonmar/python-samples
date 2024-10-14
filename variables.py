#!/usr/bin/env python3

"""variables.py at https://github.com/wilsonmar/python-samples/blob/main/variables.py
"v001 + new :variables.py"
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

    # Define Text Type: 	str
    x = "Hello World"
    print(f"x=\"{x}\" of {type(x)}")

    # Define Boolean Type: 	bool
    x = bool(5)
    print(f"bool(5)={x} of {type(x)}")

    print("\nNumeric: int, float, complex:")
    # Define Numeric Types: int
    x = int(20)
    print(f"int({x}) of {type(x)}")

    # Define Numeric Types: float
    x = float(20.5)
    print(f"float({x}) of {type(x)}")

    # Define Numeric Types: complex
    x = complex(1j)
    print(f"complex({x}) of {type(x)}")

    print("\nSequence: range, tuple, list to hold collection of items:")
    # Define Sequence Type: range
    x = range(6)
    print(f"range(6) = {x} of {type(x)}")

    # Define Sequence Type: tuple
    x = ("apple", "banana", "cherry")
    print(f"x = ({x}) of {type(x)}")

    # Define Sequence Type: list
    x = list(("apple", "banana", "cherry"))
    print(f"x = list({x}) of {type(x)}")

    print("\nSet: set, frozenset to hold collection of unique items:")
    # Define Set Types: 	set
    x = {"apple", "banana", "cherry"}
    print(f"x={x} of {type(x)} <- using curly braces")

    # Define Set Types: 	frozenset
    x = frozenset({"apple", "banana", "cherry"})
    print(f"{x} of {type(x)}")

    # Define Mapping Type: 	dict
    x = {"name" : "John", "age" : 36}
    print(f"x = {x} of {type(x)} for Mapping data in key-value pairs:")


    print(f"\nBytes and bits:")
    # Define Binary Types: 	bytes
    x = b"Hello"
    print(f"b\"Hello\" = {x} of {type(x)}")

    # Define Binary Types: 	bytearray
    x = bytearray(5)
    print(f"x = bytearray(5) = {x} of {type(x)}")

    # Define Binary Types: 	memoryview
    x = memoryview(bytes(5))
    print(f"x = memoryview(bytes(5)) = {x} of {type(x)}")

    print(f"\n")
    # Define None Type: 	NoneType
    x = None
    print(f"x = {x} of {type(x)}")


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
