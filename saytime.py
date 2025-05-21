#!/usr/bin/python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# USAGE: say text out loud using the say command built into macOS:
#    ./saytime.py           # says the local time (such as "twenty-two past five")
#    ./saytime.py "hello"   # to say "hello" or whatever you type in.
#    ./saytime.py -h        # for menu of parameters to control this program.
#    ./saytime.py -w        # list words

__commit_text__ = "v001 Fix SyntaxWarning: is from rlaneyjr :saytime.py"

""" "https://github.com/wilsonmar/python-samples/blob/main/saytime.py"
# Based on https://github.com/rlaneyjr/myutils/blob/master/saytime.py 
# initially created for Python 3 Essential Training on lynda.com
# by Bill Weinman [http://bw.org/] 2010 The BearHeart Gorup, LLC

TROUBLESHOOTING: 
If no sound is heard:
1. Hold down fn and press F10 to toggle mute.
2. Hold down fn and press F12 to turn up volume.
3. Switch to a Terminal to use the say command directly:
   say "Testing voice output"
4. Check the audio service run status (password needed):
   sudo killall coreaudiod
5. Open System Preferences → Accessibility → Speech to check if text-to-speech is enabled
6. Check System Preferences → Security & Privacy → Microphone/Input to ensure Terminal has necessary permissions
7. To see the log of activity:
   log show --predicate 'subsystem == "com.apple.speech"' --last 1h
"""

import argparse
import os
#import sys
import time

def list_voices():
    """List all available voices (built into macOS say command)"""
    print("say -v ?  # Available voices:")
    os.system('say -v "?"')
    print("")


def say_string(text, voice=None, rate=None):
    """
    Use macOS 'say' command to speak text aloud.
    
    Args:
        text (str): The text to speak
        voice (str, optional): The voice to use (e.g., 'Alex', 'Samantha')
        rate (int, optional): Speech rate (words per minute)
    """
    command = ['say']
    
    if voice:  # other than value = None:
        command.extend(['-v', voice])
    
    if rate:
        command.extend(['-r', str(rate)])
    
    command.append(text)
    os.system(' '.join(command))


class numwords():
    """
    return a number as words, e.g., 42 becomes "forty-two"
    """
    _words = {
        'ones': (
            'oh', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
        ), 'tens': (
            '', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'
        ), 'teens': (
            'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen' 
        ), 'quarters': (
            'o\'clock', 'quarter', 'half'
        ), 'range': {
            'hundred': 'hundred'
        }, 'misc': {
            'minus': 'minus'
        }
    }
    _oor = 'OOR'    # Out Of Range

    def __init__(self, n):
        self.__number = n;

    def numwords(self, num = None):
        "Return the number as words"
        n = self.__number if num is None else num
        s = ''
        if n < 0:           # negative numbers
            s += self._words['misc']['minus'] + ' '
            n = abs(n)
        if n < 10:          # single-digit numbers
            s += self._words['ones'][n]  
        elif n < 20:        # teens
            s += self._words['teens'][n - 10]
        elif n < 100:       # tens
            m = n % 10
            t = n // 10
            s += self._words['tens'][t]
            if m: s += '-' + numwords(m).numwords()    # recurse for remainder
        elif n < 1000:      # hundreds
            m = n % 100
            t = n // 100
            s += self._words['ones'][t] + ' ' + self._words['range']['hundred']
            if m: s += ' ' + numwords(m).numwords()    # recurse for remainder
        else:
            s += self._oor
        return s

    def number(self):
        "Return the number as a number"
        return str(self.__number);

class saytime(numwords):
    """
        return the time (from two parameters) as words,
        e.g., fourteen til noon, quarter past one, etc.
    """

    _specials = {
        'noon': 'noon',
        'midnight': 'midnight',
        'til': 'til',
        'past': 'past'
    }

    def __init__(self, h, m):
        self._hour = abs(int(h))
        self._min = abs(int(m))

    def words(self):
        h = self._hour
        m = self._min
        
        if h > 23: return self._oor     # OOR errors
        if m > 59: return self._oor

        sign = self._specials['past']        
        if self._min > 30:
            sign = self._specials['til']
            h += 1
            m = 60 - m
        if h > 23: h -= 24
        elif h > 12: h -= 12

        # NOTE: To overcome SyntaxWarning: "is" with a literal. Did you mean "=="?

        # hword is the hours word)
        if h == 0: hword = self._specials['midnight']
        elif h == 12: hword = self._specials['noon']
        else: hword = self.numwords(h)

        if m == 0:
            if h in (0, 12): return hword   # for noon and midnight
            else: return "{} {}".format(self.numwords(h), self._words['quarters'][m])
        if m % 15 == 0:
            return "{} {} {}".format(self._words['quarters'][m // 15], sign, hword) 
        return "{} {} {}".format(self.numwords(m), sign, hword) 

    def digits(self):
        "return the traditionl time, e.g., 13:42"
        return "{:02}:{:02}".format(self._hour, self._min)

class saytime_t(saytime):   # wrapper for saytime to use time object
    """
        return the time (from a time object) as words
        e.g., fourteen til noon
    """
    def __init__(self, t):
        self._hour = t.tm_hour
        self._min = t.tm_min


def test():
    print("\nnumbers test:")
    list = (
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 19, 20, 30, 
        50, 51, 52, 55, 59, 99, 100, 101, 112, 900, 999, 1000 
    )
    for l in list:
        print(l, numwords(l).numwords())

    print("Text enumeration: press control+c to interrupt and stop.")
    list = (
        (0, 0), (0, 1), (11, 0), (12, 0), (13, 0), (12, 29), (12, 30),
        (12, 31), (12, 15), (12, 30), (12, 45), (11, 59), (23, 15), 
        (23, 59), (12, 59), (13, 59), (1, 60), (24, 0)
    )
    for l in list:
        texttosay = (saytime(*l).digits() +" "+ saytime(*l).words())
        say_string(texttosay)

def main():
    parser = argparse.ArgumentParser(description='Speak text using macOS text-to-speech.')
    parser.add_argument('text', nargs='?', help='Text to speak aloud')
    parser.add_argument('-l', '--list-voices', action='store_true', help='List all available voices')
    parser.add_argument('-w', '--words', action='store_true', help='Word display')
    parser.add_argument('-v', '--voice', help='Voice to use (e.g., Alex, Samantha)')
    parser.add_argument('-r', '--rate', type=int, help='Speech rate (words per minute)')
    
    args = parser.parse_args()
    
    if args.list_voices:
        list_voices()
        return
    
    if args.words:
        test()
        return

    if not args.text:  # no parameters entered:
        texttosay = f"{saytime_t(time.localtime()).words()} is the local time."
        # TODO: Obtain the system's local time zone.
        say_string(texttosay, args.voice, args.rate)
    else:
        texttosay = args.text
        say_string(texttosay, args.voice, args.rate)    


if __name__ == "__main__": main()
