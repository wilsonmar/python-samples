# Sample dictionary
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