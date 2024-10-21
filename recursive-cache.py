#!/usr/bin/env python3
""" recursive-cache.py
"v001 + new Fibonacci recursive-cache.py"
STATUS: WORKING.

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

# Default Python library:
from functools import wraps, cache, lru_cache
import time, sys


# Globals:
RUN_ITERATIONS = 32
SHOW_EACH_ITERATION = False
runtime_total = 0
runtime = 0

class RuntimeTracker:
    def __init__(self):
        self.total_runtime = 0

    def zero_total_runtime(self):
        self.total_runtime = 0

    def add_runtime(self, runtime):
        self.total_runtime += runtime

    def get_total_runtime(self):
        return self.total_runtime

tracker = RuntimeTracker()

def speed_decorator(func):
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

@speed_decorator
def fib(n):
    try:
        if n <= 1:
            return n
        if SHOW_EACH_ITERATION:
            print(f"{func.__name__} {n}...")
        return fib(n - 1) + fib(n - 2)
    except KeyboardInterrupt as e:
        sys.exit('FATAL: User-issued interrupt stopping program!')

@cache
@speed_decorator
def fib_cache(n):
    if n <= 1:
        return n
    if SHOW_EACH_ITERATION:
        print(f"fib_cache {n}...")
    return fib_cache(n - 1) + fib_cache(n - 2)

@lru_cache(maxsize=5)
@speed_decorator
def fib_lru_cache(n):
    if n <= 1:
        return n
    if SHOW_EACH_ITERATION:
        print(f"fib_lru_cache {n}...")
    return fib_lru_cache(n - 1) + fib_lru_cache(n - 2)

def main():
    # Run the decorated functions:
    print(f"*** {RUN_ITERATIONS} Fibonacci recursions without caching:")
    result1 = fib(RUN_ITERATIONS)
    print(f"       cumulative runtime: {tracker.get_total_runtime():.6f} seconds.")

    tracker.zero_total_runtime()

    print(f"*** {RUN_ITERATIONS} Fibonacci recursions with functools @cache:")
    result2 = fib_cache(RUN_ITERATIONS)
    print(f"       cumulative runtime: {tracker.get_total_runtime():.6f} seconds.")

    tracker.zero_total_runtime()

    print(f"*** {RUN_ITERATIONS} Fibonacci recursions with functools @lru_cache(maxsize=5):")
    result3 = fib_lru_cache(RUN_ITERATIONS)
    print(f"       cumulative runtime: {tracker.get_total_runtime():.6f} seconds.")

if __name__ == '__main__':
    main()
