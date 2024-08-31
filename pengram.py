#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
"""
This is pengram.py of Pengram holoalphabetic sentence that 
contains every letter of the 26 letters of the alphabet at least once.
Used to display typefaces and test typing equipment.
https://github.com/wilsonmar/python-samples/blob/main/pengram.py

gas "v003 Printout sentence before substitutions :pengram.py"

Created by perpexity.ai based on this prompt:
For the sentence "The quick brown fox jumps over the lazy dog", 
write a python program to substitute each letter of the sentence with 
a NATO pengram alphabet word.
"""

import platform  # to detect if this program is running Windows OS.

def nato_pengram_substitution(sentence):
    # NATO pengram alphabet dictionary
    nato_alphabet = {
        'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
        'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliet',
        'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November', 'O': 'Oscar',
        'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
        'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray',
        'Y': 'Yankee', 'Z': 'Zulu'
    }

    # Method to Convert the sentence to uppercase:
    sentence = sentence.upper()
    # FIXME:sentence = sentence.lower()
    print(sentence.upper() )

    # Initialize an empty list to store the NATO words:
    nato_words = []
    # Add space to the beginning of output.
    nato_words.append("")

    # Iterate through each character in the sentence:
    for char in sentence:
        if char.isalpha():
            # If the character is a letter, append its NATO word
            nato_words.append(nato_alphabet[char])
        else:
            # If it's not a letter, append the character itself:
            # nato_words.append(char)
            # If it's not a letter, add a newline:
            if platform.system() == "Windows":
                # Add newline + \r carriage return:
                nato_words.append("\r\n")
            else:  # Linux or Mac:
                nato_words.append("\n")

    # Join the NATO words with spaces:
    return ' '.join(nato_words)

# The sentence to convert:
sentence = "The quick brown fox jumps over the lazy dog"

# Call the function and print the result
result = nato_pengram_substitution(sentence)

print(result)