#!/usr/bin/env python3

""" perf-ns.py
An example of obtaining timings in nanosecond-level resolution.

CURRENT STATUS: WORKING on macOS M2 14.5 (23F79) using Python 3.12.7.
git commit -m"v003 + program level timer :perf-ns.py"

The t_ns_duration is the difference between timestamps obtained by calling
time.perf_counter_ns() which returns a monotonic time that only increases. 
However, time.time() can decrease, such as when the system clock is synchronised
with an external NTP server.
"""

# import time
from time import perf_counter_ns
import time  # for sleep.

# GLOBALS:
SLEEP_SECS = 0.5

start_time = time.time()  # start the timer running.

TASK_NAME = "Sleep"
t_ns_start = perf_counter_ns()  # Start task time stamp
# Do something that takes time: Replace Sleep with actual work:
time.sleep(SLEEP_SECS)  # seconds
t_ns_stop = time.perf_counter_ns()  # Stop time stamp

# The difference between both time stamps is the t_ns_duration:
t_ns_duration_ns = (t_ns_stop - t_ns_start)      # naonseconds (ns)
t_ns_duration_µs = t_ns_duration_ns / 1000      # microseconds (µs)
t_ns_duration_ms = t_ns_duration_µs / 1000      # milliseconds (ms)
t_ns_duration_secs = t_ns_duration_ms / 1000    #      seconds (secs)
t_ns_duration_mins = t_ns_duration_secs / 1000  #      minutes (mins)

print(f"*** PERF: Task \"{TASK_NAME}\" took: {t_ns_duration_secs:,.3f} secs"
      f", {t_ns_duration_ms:,.2f} millisecs-ms"
      f", {t_ns_duration_µs:,.1f} microsecsonds-µs"
      f", {t_ns_duration_ns:,} nano-secs"
      )
# PROTIP: Different levels of precision:
# OUTPUT: *** PERF: Task "Sleep" took: 0.505 secs, 504.89 millisecs-ms, 504,886.8 microsecsonds-µs, 504,886,792 nano-secs

# STEP: Calculate the execution time:
end_time = time.time()
execution_time = end_time - start_time
print(f"*** PERF: Program took {execution_time:.4f} seconds to run all tasks.")
# OUTPUT: *** PERF: Program took 0.5052 seconds to run all tasks.