---
layout: post
lastchange: "25-08-30 v020 + log-time-csv.py :README.md"
url: "https://github.com/wilsonmar/python-samples/blob/main/README.md"
---

The objective of this repo is to provide examples of professional use of the Python language.

There are plenty of other sites and repos offering code to play games or demonstrate a coding trick.

Not here. 

Here we aim to provide code that exhibit the security and technical features needed in a (hostile) production environment where debugging needs to occur quickly.


<a name="Sections"></a>

## Code sections sequence

The features in each code section:

* SECTION 01: Preparations before running this program:
   Bash CLI commands to load external libraries (such as <tt>uv add matplotlib ...</tt>

   <tt>__last_commit__ = "v007 + ruff checks & fixes :print-inkjet.py"</tt>

* SECTION 02: Load modules used by this program:
   External libraries are imported within a try/except structure so instructions are given on fail.

* SECTION 03: Logging: <a target="_blank" href="https://bomonike.github.io/python-samples/#StartingTime">Capture pgm start date/time</a>
   (as global variables)

* SECTION 04: Define utilities to print messages:

* SECTION 05: Globals: Define hard-coded Global variables as parm defaults:

* SECTION 06: Show args_prompt() menu and read params specified on program command line:
   -v SHOW_VERBOSE 
   * See https://bomonike.github.io/linux-setup/#Args
   * See https://bomonike.github.io/linux-setup/#EchoFunctions
* SECTION 06-2: Set display and exit
* SECTION 06-3: Read parameters as command arguments:
# SECTION 06-4: Show start time & pgm values:
* SECTION 06-5: Edit parameter values from command arguments:

* SECTION 07: Obtain variables from .env file and secrets vault (in cloud):
   MY_USERNAME, MY_LOCATION, MY_PRINTER, MY_REGION, etc.

* SECTION 08: Validate values from all sources above:
   * File or database specified of correct format and exists?

* SECTION 09: Login:

* SECTION 10: Define utilities to read and delete files and folders:
   (folder_, file_, csv_, pdf, png, sqldb_, docdb_, graphdb_, rag_, etc. => 
   _check, _create, _search, _seqread, _delete, _update, _audit, _graph, etc.)

* SECTION 11: Define utilities to list and print to printers:
    * CHECK_FOR_FILE_IN_PATH if an existing .pdf file exists in path to print.

* SECTION 12: Create custom outputs:
   * Create a pdf containing colors printed (if requested by CREATE_COLOR_BLOCKS)

* SECTION 13: Audit outputs and send alerts

* SECTION 14: Clean up: Delete (remove) .pdf file created by this program if REMOVE_PDF_FILE_CREATED = True    

* SECTION 15: pgm_stats() to show how long the program ran and how many items were processed.

* SECTION 16: Main calls to functions defined above:


## Featured Projects

These contain various utilities I wrote which have the most <strong>practical usefulness</strong>.

Each contains helpful features implemented as identified during each build.

* <a href="print-inkjet.py">print-inkjet.py</a> keeps print heads clear by sending a pdf containing colored text and images.

* <a href="ls_al.py"><strong>ls_al.py</strong></a> lists files in a directory like the Linux command ls -al.

* <a href="mondrian-gen.py"><strong>mondrian-gen.py</strong></a> to generate a png art in the style of Mondrian. References macOS Keychain to keep OpenAI API key.

* <a href="openweather.py"><strong>openweather.py</strong></a> to obtain from API calls and format weather data (as fuzzy tokens)

* <a href="saytime.py.py"><strong>saytime.py</strong></a> to use the macos say CLI command to voice the time or other text.

* <a href="sorting.py"><strong>sorting.py</strong></a> to run different sorting algorithms to compare performance as n rises, on a matplotlib visualization.

* <a href="sqlite-sample.py"><strong>sqlite-sample.py</strong></a> to create and maintain a SQLite database and 

* <a href="youtube-download.py"><strong>youtube-download.py</strong></a> downloads videos based on its URL from a list of URLs in a CSV file.


<a name="OtherPrograms"></a>

## Other Programs in this repo (alphabetically):

* <a href="python-samples.py">python-samples.py</a> is a conglomeration of many features.
* <a href="argparse-samples.py">argparse-samples.py</a> to specify command line arguments into this program.
* <a href="bookmarks_export.py">bookmarks_export.py</a> to export bookmarks from Chrome to a HTML file.

* <a href="calculator-tk.py">calculator-tk.py</a> is a calculator created using the Tk GUI library.
* <a href="dijkstras.py">dijkstras.py</a> to compare calculations of shortest path on a graph
* <a href="dijkstra-yt.py">dijkstra-yt.py</a> to calculate shortest path using heapq library
* <a href="endecode-protobuf.py">endecode-protobuf.py</a> encodes/decodes a comma-separated list so each word in front of a # prefix has a char count, like Protobuf does for gRPC.
* <a href="fido2-titan.py">fido2-titan.py</a> to use the FIDO2/WebAuthn protocol to read FIDO2-compliant OTP+FIDO+CCID keys
* <a href="it-media.py">it-media.py</a> to create a database of IT movies and sort them by rating, year, or title.

* <a href="log-time-csv.py"><strong>log-time-csv.py</strong></a> creates the path to a CSV file based on static naming standards to write a sequential time stamp to a CSV file. Has limits to an infinite loop.
* <a href="logging.py">logging.py</a> to use the logging module to log messages to a file.
* <a href="ml-metrics.py">ml-metrics.py</a> to use PyTorch & Scikit to generate metrics for Machine Learning.

* <a href="num2words.py">num2words.py</a> simply converts a number input to its word.
* <a href="otel-flask.py">otel-flask.py</a> - a simple Flask app with automatic OpenTelemetry instrumentation

* <a href="pengram2nato.py">pengram2nato.py</a> to use the NATO phonetic alphabet spell out a sentence.
* <a href="perf-ns.py">perf-ns.py</a> obtains timings in nanosecond-level resolution.
* <a href="plotting.py">plotting.py</a> to create common visualizations using matplotlib.
* <a href="pytorch-mnist.py">pytorch-mnist.py</a> to use PyTorch to build, train and evaluate a neural network to recognize a hand written digit MNIST

* <a href="random-niche.py">random-niche.py</a> to generate a 19-digit cryptographically secure random number.
* <a href="recursive-cache.py">recursive-cache.py</a> shows faster Fibonnici recursion calls when using functools cache.
* <a href="rolldice.py">rolldice.py</a> rolls a 6-sided die used in Yahtzee, rolled repeated until "quit".
* <a href="rot13.py">rot13.py</a> is used on UseNet to encode sentences using a cypher that's 13 characters away.
* <a href="roku-set.py">roku-set.py</a> opens Roku at a given IP address to the YouTube video specified.
* <a href="roman2int.py">roman2int.py</a> converts Roman numerals to base 10 numbers.

* <a href="sklearn-sample.py">sklearn-sample.py</a> calculates
* <a href="try-accept.py">try-accept.py</a> to show usage of try/except/else/finally exceptions
* <a href="unittest_calculator.py">unittest_calculator.py</a> to use Python's Unit Test feature.
* <a href="variables.py">variables.py</a> to experiment with defining and viewing objects of various data types.

<a href="#OtherPrograms">Other coding samples</a> 

* bomonike/memon to generate a strong passphrase based on random words in English and German.
* bomonike/google/<strong>gcp-services</strong> has authentication and other functions to access services within the Google Cloud Platform (GCP)
* bomonike/google/<strong>myutils.py</strong> contains utility functions useful for calling by other programs.


## Coding Practices

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


## Ones I would like to create

* Reset all my passwords automatically. This would involve my database in KeePassXC and 1Password, then programmatic control operating Authy and emails to confirm.

* Functions to reference a physical Yubikey containing secrets and cryptographic certificates.


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

