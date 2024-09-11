#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""
This is pengram2nato.py of Pengram holoalphabetic sentence that 
contains every letter of the 26 letters of the alphabet at least once.
Used to display typefaces and test typing equipment.
https://github.com/wilsonmar/python-samples/blob/main/pengram2nato.py

gas "v006 Add t to Juliet & CR/LF explainer :pengram2nato.py"

Created by perpexity.ai based on this prompt:
For the sentence "The quick brown fox jumps over the lazy dog", 
write a python program to substitute each letter of the sentence with 
a NATO pengram alphabet word.
"""

import platform  # to detect if this program is running Windows OS.
import os

# use OS-agnostic line ending constants:
line_ending = os.linesep

def nato_pengram_substitution(sentence):
    # NATO pengram alphabet dictionary
    nato_alphabet = {
        'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
        'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett',
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
            # INSTEAD OF: If it's not a letter, append the character itself:
            # nato_words.append(char)
            # If it's not a letter, add a newline: https://www.youtube.com/watch?v=TtiBhktB4Qg
            nato_words.append("\n")  # LF  (ASCII 10, Hex 8a)
            # Python handleS the conversion to the appropriate platform-specific line ending.
    # git config --global core.autocrlf input

    # Join the NATO words with spaces:
    return ' '.join(nato_words)

# To allow this file to be both imported as a module and run directly:
if __name__ == "__main__":

    # The sentence to convert:
    sentence = "The quick brown fox jumps over the lazy dog"

    # Call the function and print the result
    result = nato_pengram_substitution(sentence)

    print(result)
    # Tango Hotel Echo
    # Quebec Uniform India Charlie Kilo
    # Bravo Romeo Oscar Whiskey November
    # Foxtrot Oscar X-ray
    # Juliet Uniform Mike Papa Sierra
    # Oscar Victor Echo Romeo
    # Tango Hotel Echo
    # Lima Alpha Zulu Yankee
    # Delta Oscar Golf
