---
layout: post
lastchange: "25-11-26 v001 + new >fastapi:README.md"
url: "https://github.com/wilsonmar/python-samples/blob/main/fastapi/README.md"
---

<a target="_blank" href="https://www.uvicorn.org/">Uvicorn</a> as the 
ASGI server you need to run your application.

A separate folder is used for this program:

1. This README.md file.
1. A web.py file which defines a backend web server using the FastAPI library.
2. A client.py file which sends REST calls to the URL of the web server.
3. A database holding the history of activity.
4. The <a href="#config">config.yml</a> configuration file referenced by web.py and client.py.
5. A GUI front-end web server to make changes to configurations.

Files above this folder (root at python-samples repo cloned from github.com):
* .gitignore folder
* .git folder
* README.md for all files in the repo,.

Files away from python-samples github:
* Binary image files at cloudinary.com
* Powerpoint files at 
* Video files at youtube.com

Bring up server:
   https://localhost     

React formatting

<a name="config"></a>

## config.yml

This file defines configuration settings, which can be changed by the GUI:

Configuration variables can be overridden at run-time by parmaters supplied when starting the program.


### Config changes

* Server responses can be configured to exhibit anomalies to ensure that mechanisms at the client can really detect, report, and remediate issues:
   * No response (for 404 error)
   * delay to slow response 
   <br /><br />
   These conditions can be specified by changing the config file before runs,
   by specifying parameters at run time, or in real time in the GUI.

* Client requests can be include forcing some anomalies identified by the server:
   * Incorrect version
   * No API specified
   * Mispelled API
   * API with no more access
   <br /><br />


<hr />


* Port the web server uses.

## The web.py

1. Creates the database if it doesn't exist.
2. Shows its URL in stdout.

## Documentation:
This was written with assist from several LLM models (Perpelexity, Google Gemini3, Warp.dev CLI)
* Tutorial at https://realpython.com/fastapi-python-web-apis/
* https://developers.google.com/gemini-code-assist/docs/use-agentic-chat-pair-programmer


## Install

# How to Serve a Website With FastAPI Using HTML and Jinja2

This folder contains the code discussed in the tutorial [How to Serve a Website With FastAPI Using HTML and Jinja2](https://realpython.com/fastapi-jinja2-template/).

## Installation

The [recommended way to install FastAPI](https://realpython.com/get-started-with-fastapi/#install-fastapi-the-right-way) is with the `[standard]` extra dependencies. This ensures you get all the tools you need for developing an API without having to hunt down additional packages later:

```console
$ python -m pip install "fastapi[standard]"
```

The quotes around `"fastapi[standard]"` ensure the command works correctly across different [terminals](https://realpython.com/terminal-commands/) and operating systems. With the command above, you install several useful packages, including the [FastAPI CLI](https://fastapi.tiangolo.com/fastapi-cli/) and [`uvicorn`](https://www.uvicorn.org/), an [ASGI](https://en.wikipedia.org/wiki/Asynchronous_Server_Gateway_Interface) server for running your application.

You can also use the `requirements.txt` file in this folder and run `python -m pip install -r requirements.txt` to install the standard dependencies of FastAPI.
