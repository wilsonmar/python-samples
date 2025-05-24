#!/usr/bin/python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# USAGE: Simulates a 6-sided die rolled repeated until "quit".
#    ./rolldice.py

__lastchange__ = "2025-05-24"
__commit_text__ = "v002 histogram :rolldice.py"

# For a study in programming user features:
# The value from a few rolls can be skewed.
# But with several thousand rolls, each value should be the same percentage.

import random
import time     # for timestamp

# Global variables:
dice_count = 5   # as in Yahtzee
repeat_count = 1
dice_history = []  # array to store dice roll results
rolled_count = 0
unicode_show = False

dice_faces = {  # Dice emoji Unicode characters
    1: '⚀',  # '\u2680' U+2680
    2: '⚁',  # U+2681
    3: '⚂',  # U+2682
    4: '⚃',  # U+2683
    5: '⚄',  # U+2684
    6: '⚅'   # U+2685
}

def roll_die(sides=6) -> int:
    """Roll a 6-sided (non-physical) die and return an integer"""
    return random.randint(1, sides)


def is_number(s) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def display_detailed_histogram(dice_history, width=40):
    """
    Display a detailed text histogram with percentages
    """
    if not dice_history:
        print("No data to display")
        return
    
    # Count occurrences
    counts = {}
    for entry in dice_history:
        value = entry['value']
        counts[value] = counts.get(value, 0) + 1
    
    total_rolls = len(dice_history)
    max_count = max(counts.values())
    sorted_values = sorted(counts.keys())
    
    print("histogram of dice roll history (from 1/6 = 16.67%):")
    print(f"{'Value':<5} │ {'Rolls':<5} │ {'Percent':<6} │ {'Frequency bars':<{width}}")
    # print("─" * (width + 25))
    
    for value in sorted_values:
        count = counts[value]
        percentage = (count / total_rolls) * 100
        bar_length = int((count / max_count) * width)
        bar = "█" * bar_length
        
        print(f"{value:5d} │ {count:5d} │ {percentage:5.1f}%  │ {bar:<{width}}")
    
    print("=" * (width + 25))
    print(f" Total: {total_rolls:<14}")



if __name__ == "__main__":

    print("UTF-8 characters are too tiny to read:")
    for num, emoji in dice_faces.items():
        print(f"{num}:{emoji} ", end="")
    print("")

    print("\nPress Enter to roll, or type 'q' (press contorl+C) to exit:")    
    while True:  # infinite loop
        user_input = input()
        if user_input.lower() == 'q':  # for quit like linux commands.
            break
        if user_input.lower() == 'u':  # for unicode
            unicode_show = True
        if user_input.lower() == 'n':  # for number
            unicode_show = False
        if user_input.lower() == 'h':
            display_detailed_histogram(dice_history)
        if is_number(user_input):
            # If a number was entered, use it as the rolls to repeat.
            repeat_count = int(user_input)
        else:
            repeat_count = 1
    
        # Repeat rolls:
        for rolls in range(repeat_count):
            if dice_count > 1:
                print(f"\nRolling {dice_count} times: ", end="")
            result_str = ""  # reset from previous roll.
            for i in range(dice_count):
                # print(f"{roll_die()} ", end="")
                roll = roll_die()
                if unicode_show:
                    result_str = result_str + " " + dice_faces[roll]
                else:
                    result_str = result_str + " " + str(roll)
                # TODO: Recognize full house and other Yahtzee combinations.
                round_num = i + 1   # ordinal
                dice_history.append({
                    'round': round_num,
                    'value': roll,
                    'timestamp': f"{time.monotonic()}"
                })
            rolled_count += 1  # increment
            # ALT: dice_array = np.random.randint(1, 7, size=5)  # 5 dice
            print(f"{result_str}")
        
    print(f"Thank you for playing {rolled_count} rolls!")

    #print("\n" + "="*60 + "\n")
    # Display detailed histogram:
    display_detailed_histogram(dice_history)

"""
Python features in this program:
* comments
* UTF-8 encoding for non-English characters
* Increment a variable using +=
"""