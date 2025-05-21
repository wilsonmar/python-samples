---
layout: post
date: "2025-05-20"
lastchange: "v010 + myutils qr :README.md"
url: "https://github.com/wilsonmar/python-samples/blob/main/README.md"
---
# python-samples/README

The objective of this repo is to provide examples of professional use of the Python language.

There are plenty of other sites and repos offering code to play games or demonstrate a coding trick.

Not here. 

Here we aim to provide code that exhibit the security and technical features needed in a (hostile) production environment where debugging needs to occur quickly.

## Projects

* <strong>myutils.py</strong> is a private python module that provides myutil_ functions used in other Python programs in this repo:

* <strong>gcp-services.py</strong> is a conglomeration of many features.
* <strong>mondrian-gen.py</strong> to generate a png art in the style of Mondrian. References macOS Keychain to keep OpenAI API key.
* <strong>openweather.py</strong> to obtain from API calls and format weather data (as fuzzy tokens)
* <strong>saytime.py</strong> to use the macos say CLI command to voice the time or other text.
* <strong>sorting.py</strong> to run different sorting algorithms to compare performance as n rises, on a matplotlib visualization.
* <strong>youtube-download.py</strong> downloads videos based on its URL from a list of URLs in a CSV file.

<a href="#OtherPrograms">Other samples in this repo</a> 

## Coding Practices to use MyUtils

Below are notes about coding practices, from the top down:

1.  At the very top of the file:
    ```python
    #!/usr/bin/env python3
    ```
    That enables you to run the program as a script without typing python3:
    ```bash
    ./mondrian-gen.py
    ```
    instead of 
    ```bash
    python3 mondrian-gen.py
    ```

1.  This specifies that emjois and non-English characters (such as Japanese, Chinese, etc.) may be in the code file:
    ```python
    # -*- coding: utf-8 -*-
    ```

1.  SPDX (Software Package Data Exchange) license identifiers provide machine-readable tags to communicate the license governing a piece of software. 
    ```python
    # SPDX-License-Identifier: MPL-2.0
    ```
    The MPL-2.0 (Mozilla Public License version 2.0) is a moderately permissive open-source license with some copyleft provisions. Its key characteristics include:
    * Allows code to be freely used, modified, and shared
    * Requires modifications to MPL-licensed files to be shared under the same license
    * Allows MPL-licensed code to be combined with code under different licenses
    * Provides patent protection for contributors and users
    * Requires preservation of copyright notices

1.  Dunder (double underscore) variables in the module define metadata about the program. PEP specifies that such variables can be read by other programs without opening the source code.
    ```python
    __commit_date__ = "2025-05-20"
    __version__ = "1.0.0"
    __author__ = "Your Name"
    __license__ = "MIT"
    __commit_date__ = "2025-05-20"
    __status__ = "Production"
    __doc__ = "This module demonstrates the use of dunder (double underscore) variables in Python."
    ```
    # TODO: Some also have like <tt>__commit_hash__ = "a1b2c3d4e5f6"</tt>
    # But How to get the commit hash? Doesn't adding it change the hash value?

1.  To capture the program start time at the earliest moment, the built-in time module is used:
    ```python
    import time
    std_strt_timestamp = time.monotonic()
    ```
    <tt>time.monotonic()</tt> returns the time since an arbitrary point in the past, which is not affected by system clock changes.

1.  External dependencies are specified in a requirements.txt file.
    ```python
    import requests
    ```

1.  Within the requirements.txt file, the <strong>myutils</strong> module is loaded to provide all other custom Python programs in this repo:
   ```python
   import myutils
   ```

1.  Modules used The ast (Abstract Syntax Tree) module parses Python source code into a structure so code can be better analyzed or modified programmatically.
   ```python
   import ast
   ```
   ast is used by linters, type checkers, and other such tools to analyze code without running it.

1.  All functions defined in this file are prefixed with myutil_ to avoid name conflicts in other modules.
    ```python
    def myutil_print(msg):
        print(msg)
    ```

1.  The function issuing a message to the console is printed along with the message:
    ```python
    def myutil_print(msg):
        print(msg)
    ```


<a name="OtherPrograms"></a>

## Other Programs alphabetically

* argparse-samples.py shows how to specify command line arguments into this program.
* bookmarks_export.py to export bookmarks from Chrome to a HTML file.
* calculator-tk.py is a calculator created using the Tk GUI library.
* dijkstras.py to compare calculations of shortest path on a graph
* dijkstra-yt.py to calculate shortest path using heapq library
* endecode-protobuf.py encodes/decodes a comma-separated list so each word in front of a # prefix has a char count, like Protobuf does for gRPC.
* it-media.py to create a database of IT movies and sort them by rating, year, or title.

* logging.py to use the logging module to log messages to a file.
* ml-metrics.py to use PyTorch & Scikit to generate metrics for Machine Learning.

* num2words.py simply converts a number input to its word.
* otel-flask.py - a simple Flask app with automatic OpenTelemetry instrumentation

* pengram2nato.py to use the NATO phonetic alphabet spell out a sentence.
* perf-ns.py obtains timings in nanosecond-level resolution.
* plotting.py to create common visualizations using matplotlib.
* python-samples.py is a conglomeration of many features.
* pytorch-mnist.py Use PyTorch to build, train and evaluate a neural network to recognize a hand written digit MNIST

* recursive-cache.py shows faster Fibonnici recursion calls when using functools cache.
* roku-set.py opens Roku at a given IP address to the YouTube video specified.
* roman2int.py converts Roman numerals to base 10 numbers.
* rot13.py is used on UseNet to encode sentences using a cypher that's 13 characters away.
* sklearn-sample.py calculates
* try-accept.py to show usage of try/except/else/finally exceptions
* unittest_calculator.py is an example of how to use Python's Unit Test feature.
* variables.py to experiment with defining and viewing objects of various data types.

## Coding Practices

Below 




## Experiments being built

https://codepen.io/freeCodeCamp/pen/dNVazZ
Recipe Box app in JavaScript for
<a target="_blank" href="https://www.freecodecamp.org/learn/coding-interview-prep/take-home-projects/build-a-recipe-box">
a Take Home Project</a>.

NOTE: Other pograms are in the https://github.com/bomonike organization:
* https://github.com/bomonike/memon calculate super strong word phrases and remember them via LLM gen'd songs. See https://www.youtube.com/watch?v=KAjkicwrD4I
on how to memorize using PAO (Person Action Object)

The STATUS of each program is noted within each file.

Before running each:
```
chmod +x dijkstras.py
./dijkstras.py
```


## etc.

https://codehs.com/tutorial/david/sample-a-csp-performance-task-1
Sample A CSP Performance Task

https://codehs.com/tutorial/david/sample-b-csp-performance-task
Sample B CSP Performance Task - Caesar Cipher

https://www.youtube.com/watch?v=LXsdt6RMNfY
Use Python to automate my life

https://www.youtube.com/watch?v=mCk4Rabkmjc
Automate Boring Office Tasks with ChatGPT and Python

https://www.youtube.com/watch?v=Ge-9AhVVOFc
Automate any task using ChatGPT! (my full GPT building framework)


# Run a Bash script
import subprocess
result = subprocess.run(["bash", "path/to/script.sh"], capture_output=True, text=True)
stdout = result.stdout
stderr = result.stderr


https://github.com/Gatsby-Lee/DevOps/tree/master/programming_lang/python

https://www.youtube.com/watch?v=kGcUtckifXc
Please Master These 10 Python Functions…

Have a single import per line to reduce merge conflicts.
See https://github.com/asottile/reorder-python-imports?tab=readme-ov-file#why-this-style

