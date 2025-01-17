#!/usr/bin/env python3

""" async-samples.py

git commit -m"v001 + new :async-samples.py"

STATUS: FIXME: File "/Users/johndoe/github-wilsonmar/python-samples/async-samples.py", line 74
       asyncio.run(main())
SyntaxError: invalid non-printable character U+00A0  Regex:[\xa0]

This evaluates how much execution time can be reduced/optimized using 
various ways to achieve concurrency:

   A. With Python asyncio (asynchronous I/O) library introduced in Python 3.4,
      as documented at https://pypi.org/project/asyncio/
      Note: Async IO, AsyncIO, and asyncio are used interchangeably throughout this article.

   B. s

   C. x

(Faster execution time means faster test time and overall delivery time) 

Running API calls asynchronously avoids blocking of other tasks.

From https://dzone.com/articles/python-asyncio-tutorial-a-complete-guide

Before running this:
python3 -m venv venv
source venv/bin/activate
python3 -m pip install asyncio

chmod +x async-samples.py
./async-samples.py

"""

# For all functions defined:
import asyncio
import sys
import time
from datetime import datetime

def run_env():
   print("Enter " + sys._getframe().f_code.co_name + " " + str(datetime.now().time()))
   # TODO: Print out hardware, OS, Python version, Memory, Drive type, Disk free, etc.
   print("Exit " + sys._getframe().f_code.co_name + " " + str(datetime.now().time()))
   return

async def test_1():
   # Get function name
   # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function
   print("Enter " + sys._getframe().f_code.co_name + " " + str(datetime.now().time()))
   # Could be an I/O operation, network request, database operation, and more
   await asyncio.sleep(2)
   ret_info = await test_2()
   print("After sleep " + sys._getframe().f_code.co_name + " " + str(datetime.now().time()))
   return "test_1"


async def test_2():
   print("Enter " + sys._getframe().f_code.co_name + " " + str(datetime.now().time()))
   await asyncio.sleep(2)
   print("After sleep " + sys._getframe().f_code.co_name + " " + str(datetime.now().time()))
   return "test_2"


async def run_asyncio():
   print("Enter main")
   start_time = time.perf_counter()
   # Execution is paused since the await keyword is encountered.
   # Control is yield back to the event loop and other coroutine (if any) is executed
   # Control is handed back to test_1 once the sleep of 2 seconds is completed
   ret_info = await test_1()
   print(f"Data received from the test_1: {ret_info}" + " " + str(datetime.now().time()))
   ret_info = await test_2()
   print(f"Data received from the test_2: {ret_info}" + " " + str(datetime.now().time()))
   end_time = time.perf_counter()
   print("Exit main")
   print(f'It took {round(end_time - start_time,0)} second(s) to complete.')


if __name__ == '__main__':
   # Run the main coroutine
   # asyncio.run(run_asyncio())

   # asyncio.run(run_asyncio())