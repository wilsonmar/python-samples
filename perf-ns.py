#!/usr/bin/env python3

""" perf-ns.py
An example of obtaining timings in nanosecond-level resolution.

CURRENT STATUS: WORKING on macOS M2 14.5 (23F79) using Python 3.12.7.
git commit -m"v002 + different decimal points :perf-ns.py"

The duration is the difference between timestamps. 
NOTE: time.perf_counter_ns() returns a monotonic time that only increases. 
However, time.time() can decrease, such as when the system clock is synchronised
with an external NTP server.
"""

# import time
from time import perf_counter_ns
import time  # for sleep.

# Start time stamp:
t_start = perf_counter_ns()

# Do something that takes time:
time.sleep(0.5)  # seconds

# Stop time stamp:
t_stop = time.perf_counter_ns()

# The difference between both time stamps is the duration:
duration_ns = (t_stop - t_start)      # naonseconds (ns)
duration_µs = duration_ns / 1000      # microseconds (µs)
duration_ms = duration_µs / 1000      # milliseconds (ms)
duration_secs = duration_ms / 1000    #      seconds (secs)
duration_mins = duration_secs / 1000  #      minutes (mins)

print(f"*** INFO: Elapsed time: {duration_secs:,.3f} secs"
      f", {duration_ms:,.2f} millisecs-ms"
      f", {duration_µs:,.1f} microsecsonds-µs"
      f", {duration_ns:,} nano-secs"
      )
# PROTIP: Different levels of precision:
# OUTPUT: *** INFO: Elapsed time: 0.505 secs, 504.91 millisecs-ms, 504,906.6 microsecsonds-µs, 504,906,625 nano-secs
