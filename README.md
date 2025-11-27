---
layout: post
lastchange: "25-11-27 v060 + planets-turtle.py :README.md"
url: "https://github.com/wilsonmar/python-samples/blob/main/README.md"
---

This README describes practical examples of production-quality Python-language code which
exhibit the security and scalability features needed in a (hostile) production environment where debugging needs to occur quickly.

Programs here make use of uv (from astral.sh) instead of pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, etc. 
To catch dependency issues, we recommend that the latest set of dependencies is assembled daily by 
creating <tt>requirements.txt</tt>, <tt>pyprojects.toml</tt>, and <tt>uv.lock</tt> with every run.

We also recommend that libraries download historical versions of each library downloaded so that in case of issues, forensics and fall-back can be performed even though public versions become corrupted.

<a name="Featured"></a>

## Featured Projects

Code which we think have the most <strong>practical usefulness</strong>:

* <a href="./dundars-list.py">dundars-list.py</a> lists programs by date, along with the <tt>__last_change__</tt> and <tt>__status__</tt> text in each python program.

* <a href="git-commit.sh">git-commit.sh</a> is copied to this repo's .git/hooks folder to run
   * <tt>ruff</tt> is catch code formatting issues 
   * <a target="_blank" href="https://bandit.readthedocs.io/en/latest/start.html#usage">>bandit</a> to identify secure coding issues
   * GitGuardian, GitLeaks, TruffleHog, Legit, etc. to identify what looks like secrets stored in the repo.
   <br /><br />
   Note that <tt>safety</tt> is needed to identify libraries (versions) marked as vulnerable in CVS, it is no longer run because the vendor now requires login. That makes it too inconvenient, especially offline.

* <a href="#diagrams-graphwiz.py">diagrams-graphwiz.py</a> generate diagrams (image files) from text, based on the graphwiz tool library.

* <a href="planets-turtle.py">planets-turtle.py</a> illustrates a simple 2D map of planets around our sun, using the turtle library and Python object-oriented programming.

* <a href="python-samples.py">python-samples.py</a> is a conglomeration of many features.

* <a href="retry-flask.py">retry-flask.py</a> is a Flask server app that purposely returns errors to client responses from <br />
* <a href="retry-client.py">retry-client.py</a> using the tenacity library to handle errors (500 server err, Timelout, 404, 204 rate limit, 204 empty response).

* <a href="gpu-sample.py">gpu-sample.py</a> recognizes what GPU is available (CUDA or Apple MPS) and runs sample PyTorch <strong>microbenchmarks</strong> of timings and memory used. Enhancements:

* About Google's Tensorflow: <a target="_blank" href="https://github.com/ageron/handson-ml3">ipynb</a> based on the <a target="_blank" href="https://learning.oreilly.com/videos/-/0636920876441/">VIDEO</a>: Awaiting the 2025 4th edition to <a target="_blank" href="https://learning.oreilly.com/library/view/hands-on-machine-learning/9781098125967/">October 2022 O'Reilly book: Hands-on Machine Learning with Scikit-Learn, Keras and TensorFlow (3rd edition)</a> by <a target="_blank" href="https://www.linkedin.com/in/aurelien-geron/">Aurélien Geron</a> (<a target="_blank" href="https://www.youtube.com/c/AurelienGeron">YouTube</a>, <a target="_blank" href="https://www.linkedin.com/feed/update/urn:li:activity:7368776563716186113/">interview</a>, <a target="_blank" href="https://x.com/aureliengeron/with_replies">X</a>)

* <a href="print-inkjet.py">print-inkjet.py</a> keeps print heads clear by sending a pdf containing colored text and images. Features and enhancements:
   * Quotes scraped from the internet to print.
   <br /><br />
* <a href="ls_al.py"><strong>ls_al.py</strong></a> lists files in a directory like the Linux command ls -al.

* <a href="mondrian-gen.py"><strong>mondrian-gen.py</strong></a> to generate a png art in the style of Mondrian. References macOS Keychain to keep OpenAI API key.

* <a href="saytime.py"><strong>saytime.py</strong></a> to use the macos say CLI command to voice the time or other text.

* <a href="sorting.py"><strong>sorting.py</strong></a> to run different sorting algorithms to compare performance as n rises, on a matplotlib visualization.

* <a href="dash-streaming.py"><strong>dash-streaming.py</strong></a> to use Plotly Dash library to animate a stream of real-time updates (random values) within a Flask app.

* <a href="sqlite-sample.py"><strong>sqlite-sample.py</strong></a> to create and maintain a SQLite database. 

In the <strong>weather</strong> folder:

* <a href="openweather.py"><strong>openweather.py</strong></a> to obtain from API calls and format weather data (as fuzzy tokens). Features 
   * Lookup Longitude/Latitude by zip code
   * <strong>wttr-weather.py</strong> issues curl commands for weather data (https://github.com/chubin/wttr.in)
   * Display on a monitor information about the location of people you communicate with
   * <a target="_blank" href="https://www.geeksforgeeks.org/python/how-to-extract-weather-data-from-google-in-python/">Use BeautifulSoup</a> to scrape predictions from google.com (which references Weather.com).
   * Compare actuals vs. predictions of each prediction service.
   * Compare accuracy of different predictors (weather.com vs. wattr.in vs. Openweather. etc.)
   <br /><br />

* <a href="sunset-speed.py"><strong>sunset-speed.py</strong></a> calculates how fast one would need to drive to experience a continuous sunset. This theoretical question is designed to make math fun and make for curiosity about programming math. This shows a use for the cosign trigonometry function.

* <a href="youtube-download.py"><strong>youtube-download.py</strong></a> downloads videos based on its URL from a list of URLs in a CSV file.

In the <strong>recommender</strong> folder:

* <a href="it-media.py">it-media.py</a> is a popular way to show off skill at database manipulation, analytics, and machine learning. Related enhancements:
   * Bulk load into database movie info (such as "m1-100k") 
   * Reconcile data about the same movie from various sources.
   * Sorting by several factors: genre, content rating, year, actors, directors, academy awards
   * Link to rottentomatoes.com and other reviews
   * Link availability of movie on various streaming platforms (Netflix, Prime, etc.)
   * Enable entry of user ratings and use that data to influence recommendations.
   * Link release dates to calendar 

   * Catalog DVD collection by scanning UPC labels.
   * Play a particular video in a media app after scanning the UPC on the video box.
   * <strong>surprise.py</strong> provides a GUI created (using tkinter) to select movies and TV shows as an example of machine learning matrix eigenvector SVD (Singular Value Decomposition) & PCA (Principal Component Analysis) feature extraction algorithms from <a target="_blank" href="https://jonathan-hui.medium.com/machine-learning-singular-value-decomposition-svd-principal-component-analysis-pca-1d45e885e491">data science</a>.
   * <a target="_blank" href="https://www.geeksforgeeks.org/machine-learning/recommendation-system-in-python/">Recommend movies</a> based on what friends watched.
   <br /><br />

* <a href="pdf2llm.py">pdf2llm.py</a> converts PDF files to ".md" (markdown) format files, which LLMs can read (and are smaller files). There are two algorithms (libraries). pymupdf4llm converts to "###" headings and "**" bold.


<a name="OtherPrograms"></a>

## Other Programs in this repo (alphabetically):

* <a href="argparse-samples.py">argparse-samples.py</a> to specify command line arguments into this program.
* <a href="bookmarks_export.py">bookmarks_export.py</a> to export bookmarks from Chrome to a HTML file.

* <a href="calculator-tk.py">calculator-tk.py</a> is a calculator created using the Tk GUI library.
* <a href="dijkstras.py">dijkstras.py</a> to compare calculations of shortest path on a graph
* <a href="dijkstra-yt.py">dijkstra-yt.py</a> to calculate shortest path using heapq library
* <a href="endecode-protobuf.py">endecode-protobuf.py</a> encodes/decodes a comma-separated list so each word in front of a # prefix has a char count, like Protobuf does for gRPC.
* <a href="fido2-titan.py">fido2-titan.py</a> to use the FIDO2/WebAuthn protocol to read FIDO2-compliant OTP+FIDO+CCID keys

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

In the <strong>countries</strong> folder:

* <strong>country_info.csv</strong>
* <strong>country_lang_info.xlsx</strong>
* Comparison of countries: <a target="_blank" href="https://media.geeksforgeeks.org/wp-content/uploads/20240926123327/WHR2023.csv">csv from a year of</a> the World Happiness Report and statistics from the CIA Factbook</a>.
* Future program to use GeoAI: 
   * Rasterio works with raster data such as satellite images and elevation models
   * GeoPandas extends GeoPandas
   * Folium creates interactive maps
   * Prestereo, Shapeley)

<a name="Experiments"></a>

## Experiments being built

* <a target="_blank" href="https://medium.com/the-pythonworld/12-python-multithreading-secrets-nobody-explains-well-1182948667a5">Multi-threading</a>

* Use OpenCV to recognize hand signals (Sign Language), then take an automatic action or raise an alarm when touching your face (bad hygiene).

In the <strong>predictions</strong> folder is an example

* Use Box charts and descriptive statistics to compare trends in currency exchange rates (of euros, Japanese yen, Chinese runbei, etc.) vs. price of <a target="_blank" href="https://www.geeksforgeeks.org/machine-learning/gold-price-prediction-using-machine-learning/">gold</a>, bitcoin, etc.


* <a target="_blank" href="https://learning.oreilly.com/library/view/3d-data-science/9781098161323/">3D Point Cloud Data Science</a>


* <a target="_blank" href="https://www.geeksforgeeks.org/python/analyzing-selling-price-of-used-cars-using-python/">Analyze Selling Price of used Cars</a> using AI

* https://codepen.io/freeCodeCamp/pen/dNVazZ Recipe Box app in JavaScript for
<a target="_blank" href="https://www.freecodecamp.org/learn/coding-interview-prep/take-home-projects/build-a-recipe-box">a Take Home Project</a>.

NOTE: Other pograms are in the https://github.com/bomonike organization:
* https://github.com/bomonike/memon calculate super strong word phrases and remember them via LLM gen'd songs. See https://www.youtube.com/watch?v=KAjkicwrD4I
on how to memorize using PAO (Person Action Object)

* palindromes.py - I personally don't understand the intellectual curiosity for words and phrases that spell the same forward and backward. Examples: TENET, 747, KAYAK, TACO CAT, RACECAR, NEVER ODD OR EVEN, STEP ON NO PETS, UFO TOFU

* A dashboard like https://towardsdatascience.com/build-a-data-dashboard-using-html-css-javascript/


<a name="CloudAI"></a>

## Cloud AI comparisons

In programs that make use of Cloud AI LLMs, (such as listen4cmd.py and mondrian.py) 
capture timings and costs for each request. Here is a sample table for recognizing the word "docker":

<table border="1" cellpadding="4" cellspacing="0">
<tr><th> LLM </td><td> Output </td><td> MiliSecs.</td><td> Cost USD </td></tr>
<tr align="right" valign="top"><td align="left"> Anthropic </td><td align="left"> 91% </td><td align="right"> 33 </td><td> $0.00420 </td></tr>
<tr align="right" valign="top"><td align="left"> AWS </td><td align="left"> 89% </td><td align="right"> 28 </td><td> $0.00680 </td></tr>
<tr align="right" valign="top"><td align="left"> Azure </td><td align="left"> 78% </td><td align="right"> 39 </td><td> $0.00431 </td></tr>
<tr align="right" valign="top"><td align="left"> DeepSeek </td><td align="left"> 63% </td><td align="right"> 43 </td><td> $0.00532 </td></tr>
<tr align="right" valign="top"><td align="left"> Google </td><td align="left"> 95% </td><td align="right"> - </td><td> - </td></tr>
<tr align="right" valign="top"><td align="left"> IBM </td><td align="left"> 87% </td><td align="right"> 29 </td><td> $0.00267 </td></tr>
<tr align="right" valign="top"><td align="left"> Mistral </td><td align="left"> 77%r </td><td align="right"> 43 </td><td> $0.00532 </td></tr>
<tr align="right" valign="top"><td align="left"> Cohere </td><td align="left"> 82% </td><td align="right"> 13 </td><td> $0.00255 </td></tr>
<tr align="right" valign="top"><td align="left"> OpenAI </td><td align="left"> 88% </td><td align="right"> 23 </td><td> $0.00490 </td></tr>
<tr align="right" valign="top"><td align="left"> Qwen 3 </td><td align="left"> 72% </td><td align="right"> 63 </td><td> $0.00230 </td></tr>
<tr align="right" valign="top"><td align="left"> Sphinx </td><td align="right"> 55% </td><td align="right"> - </td><td> - </td></tr>
<tr align="right" valign="top"><td align="left"> Wit.ai </td><td align="left"> 63% </td><td align="right"> 61 </td><td> $0.00320 </td></tr>
</table>

<tt>==</tt> above means the word was recognized correctly.<br />
<tt>- </tt> above means the word was NOT recognized.<br />

* Google is free but is limited to 50 requests per day.
* Azure 
* Mistral is based in France.
* Qwen tests used by Alibaba in China with servers in Singapore.
* Sphinx is the only local LLM, from CMU. But it didn't recognize many words correctly.
<br /><br />
Cost USD is calculated from tokens charged times price.

Another table contains sums from all runs, from which analytics charts are drawn.


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


<a name="CodingPractices"></a>

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


The STATUS of each program is noted within each file.

Before running each:
```
chmod +x dijkstras.py
./dijkstras.py
```

<hr />

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

https://www.debuggingbook.org/

https://www.programmingworld.tech/blog/django-framework-build-url-shortener-application-using-django-and-pyshorteners
Django Framework : Build URL Shortener Application Using Django and Pyshorteners