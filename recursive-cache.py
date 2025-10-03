#!/usr/bin/env python3

"""recursive-cache.py here.

At https://github.com/wilsonmar/python-samples/blob/main/recursive-cache.py

This program runs recursively a Fibonacci sequence (see https://en.wikipedia.org/wiki/Fibonacci_sequence#Binet's_formula), 
where each number is the sum of the two preceding ones.
Without memoization, each iteration takes _exponentially_ longer and longer until
the 30th-some iteration when it slows to a crawl.
It's much quicker when created here with memoization using the @cache decorator introduced in Python 3.9
or the @lru_cache decorator available earlier.

Without memoization, the time complexity (Theta) of a recursive Fibonacci algorithm is
exponential or O(2^n), where n is the number of iterations calculating the Fibonacci value.
Each node spawns two child nodes until reaching the base cases (n = 0 or n = 1).
The total number of operations grows exponentially with n, as each level of the tree roughly doubles the number of calls.
With memoization (caching) of previously calculated values, time complexity is reduced to O(n).

The functions are repeated here so no source code commenting is needed to see the difference in run-times.

Based on https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/030_the_single_most_useful_decorator_in_python/cache_decorator.py
illustrated at https://www.youtube.com/watch?v=DnKxKFXB4NQ "The Single Most Useful Decorator in Python"
by James Murphy of mCoding.com, with comments.

Advanced techniques can further reduce the time complexity to O(log n).
See https://www.reddit.com/r/algorithms/comments/o8zsxv/complexity_of_recursive_fibonacci_sequence_with/
https://www.perplexity.ai/search/write-python-code-to-display-f-Kj0kEkvUQJa5TzGKZxKIHw

"""
__last_change__ = "25-10-03 v005 + RUN_ITERATIONS perf ray :recursive-cache.py"

# Default Python library:
from datetime import datetime
import time  # for sleep.
from time import perf_counter_ns
import sys
#import functools

# External libraries defined in requirements.txt:
try:
    # flake8: E401 multiple imports on one line
    from functools import wraps, cache, lru_cache
except Exception as e:
    print(f"Python module import failed: {e}")
    # uv run log-time-csv.py
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    print("Please activate your virtual environment:\n  uv env env\n  source .venv/bin/activate")
    exit(9)


# Globals:
RUN_ITERATIONS = 2056   # [32, 64, 128, 256, 512, 1024, 2056]
SHOW_EACH_ITERATION = False
runtime_total = 0
runtime = 0

#import sys
sys.setrecursionlimit(30000)  # set higher limit

# Program Timings:
# For wall time measurements:
pgm_strt_datetimestamp = datetime.now()

class RuntimeTracker:
    """Track runtime."""

    def __init__(self):
        """Initialize."""
        self.total_runtime = 0

    def zero_total_runtime(self):
        """Zero out to init Total Runtime."""
        self.total_runtime = 0

    def add_runtime(self, runtime):
        """Add Total Runtime."""
        self.total_runtime += runtime

    def get_total_runtime(self):
        """Get Total Runtime."""
        return self.total_runtime


tracker = RuntimeTracker()


def speed_decorator(func):
    """Decorate @warps."""
    @wraps(func)  # function after the @speed_decorator decorator:
    def wrapper(*args, **kwargs):
        # Record start time:
        start_time = time.time()
        # Call the original function:
        result = func(*args, **kwargs)
        # Record end time:
        end_time = time.time()
        # Calculate and print the runtime:
        runtime = end_time - start_time

        # Add to total runtime:
        tracker.add_runtime(runtime)
        if SHOW_EACH_ITERATION:
            # Using Dunder method:
            print(f"{func.__name__} ran in {runtime:.6f} seconds")
        if SHOW_EACH_ITERATION:
            print(f"Cumulative runtime so far: {tracker.get_total_runtime():.6f} seconds")
        return result
    return wrapper


@cache   # from functools
@speed_decorator
def fib(n):
    """Define Fibonacci infinite logic."""
    try:
        if n <= 1:
            # Base case: factorial of 0 is 1
            return n
        if SHOW_EACH_ITERATION:
            print(f"{fib.__name__} {n}...")
        return fib(n - 1) + fib(n - 2)
    except KeyboardInterrupt:
        sys.exit('FATAL: User-issued interrupt stopping program!')


@cache   # from functools
@speed_decorator
def fib_cache(n):
    """Decorate for Speed."""
    if n <= 1:
        return n
    if SHOW_EACH_ITERATION:
        print(f"fib_cache {n}...")
    return fib_cache(n - 1) + fib_cache(n - 2)


@lru_cache(maxsize=5)   # from functools
@speed_decorator
def fib_lru_cache(n):
    """Decorae for LRU Cache."""
    if n <= 1:
        return n
    if SHOW_EACH_ITERATION:
        print(f"fib_lru_cache {n}...")
    return fib_lru_cache(n - 1) + fib_lru_cache(n - 2)


def main():
    """Run the decorated functions."""
    # TODO: Increase RUN_ITERATIONS exponentialls: [32, 64, 128, 256, 512, 1024, 2056]
    # TODO: Plot results like https://github.com/wilsonmar/python-samples/blob/main/sorting.py
    # https://www.anyscale.com/blog/writing-your-first-distributed-python-application-with-ray

    t_ns_start = perf_counter_ns()  # Start task time stamp
    print(f"*** {pgm_strt_datetimestamp} starting...")

    print(f"*** INFO: {RUN_ITERATIONS} recursions without caching:", end="")
    result1 = fib(RUN_ITERATIONS)
    print(f" cum. runtime: {tracker.get_total_runtime():.6f} seconds. {len(str(result1))}")

    tracker.zero_total_runtime()

    print(f"*** INFO: {RUN_ITERATIONS} recursions with functools @cache:", end="")
    result2 = fib_cache(RUN_ITERATIONS)
    print(f" cum. runtime: {tracker.get_total_runtime():.6f} seconds. {len(str(result2))}")

    tracker.zero_total_runtime()

    print(f"*** INFO: {RUN_ITERATIONS} recursions with functools @lru_cache(maxsize=5):", end="")
    result3 = fib_lru_cache(RUN_ITERATIONS)
    print(f" cum. runtime: {tracker.get_total_runtime():.6f} seconds. {len(str(result3))}")

    # time.sleep(SLEEP_SECS)  # seconds
    t_ns_stop = time.perf_counter_ns()  # Stop time stamp
    # The difference between both time stamps is the t_ns_duration:
    t_ns_duration_ns = (t_ns_stop - t_ns_start)      # naonseconds (ns)
    t_ns_duration_µs = t_ns_duration_ns / 1000      # microseconds (µs)
    t_ns_duration_ms = t_ns_duration_µs / 1000      # milliseconds (ms)
    t_ns_duration_secs = t_ns_duration_ms / 1000    #      seconds (secs)
    t_ns_duration_mins = t_ns_duration_secs / 1000  #      minutes (mins)
    print(f"*** PERF: {RUN_ITERATIONS} took"
        f": {t_ns_duration_mins:,.3f} mins"
        f": ,{t_ns_duration_secs:,.3f} secs"
        f", {t_ns_duration_ms:,.2f} millisecs-ms"
        f", {t_ns_duration_µs:,.1f} microsecsonds-µs"
        f", {t_ns_duration_ns:,} nano-secs"
        )

if __name__ == '__main__':

    main()

    pgm_stop_datetimestamp = datetime.now()
    pgm_elapsed_wall_time = pgm_stop_datetimestamp - pgm_strt_datetimestamp
    print(f"*** {pgm_stop_datetimestamp} ended after {pgm_elapsed_wall_time} seconds.")


"""
*** 2025-10-03 16:51:19.551415 starting...
*** INFO: 2056 recursions without caching: cum. runtime: 2.145089 seconds. 430
*** INFO: 2056 recursions with functools @cache: cum. runtime: 2.215111 seconds. 430
*** INFO: 2056 recursions with functools @lru_cache(maxsize=5): cum. runtime: 2.017658 seconds. 430
*** PERF: 2056 took: 0.006 secs, 6.36 millisecs-ms, 6,356.8 microsecsonds-µs, 6,356,750 nano-secs
*** 2025-10-03 16:51:19.557829 ended after 0:00:00.006414 seconds.
"""