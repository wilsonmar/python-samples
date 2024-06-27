# https://www.perplexity.ai/search/write-a-python-l.mp30N1SyeUcoARHAm6QQ
# write a python program to retrieve a value from a key value text file

def get_value(file_path, key):
    """
    Retrieves the value associated with the given key from a key-value text file.

    Args:
        file_path (str): The path to the key-value text file.
        key (str): The key for which the value needs to be retrieved.

    Returns:
        str: The value associated with the given key, or None if the key is not found.
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    key_value = line.split('=', 1)
                    if len(key_value) == 2:
                        file_key, file_value = key_value
                        if file_key == key:
                            return file_value
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")

    return None

# Example usage
file_path = 'data.txt'
key = 'name'
value = get_value(file_path, key)

if value:
    print(f"The value associated with the key '{key}' is: {value}")
else:
    print(f"Key '{key}' not found in the file.")