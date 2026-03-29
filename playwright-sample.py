#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "playwright",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file

"""playwright-sample.py using uv to setup browser test automation using Playwright open-sourced by Microsoft.

BEFORE RUNNING, on Terminal:
   # cd to a folder to receive
   git clone https://github.com/wilsonmar/python-samples.git --depth 1
   cd python-samples
   python3 -m pip install uv
   python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
   uv venv .venv
   source .venv/bin/activate
   uv add playwright --frozen
   python3 -m playwright install   # to install on browsers

   ruff check playwright-sample.py
   chmod +x playwright-sample.py
   uv run playwright-sample.py
           # Terminal does not freeze.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__

"""

__last_change__ = "26-03-29 v001 new :playwright-sample.py"
__status__ = "WORKS on macOS Sequoia 15.6.1"

from playwright.sync_api import sync_playwright, Playwright

def run_sample(playwright: Playwright) -> str:
    """Run Playwright."""
    # with sync_playwright() as p:
    if use_browser == "firefox":
       browser = playwright.firefox.launch()
    elif use_browser == "chromium":
       browser = playwright.chromium.launch()
    elif use_browser == "webkit":
       browser = playwright.webkit.launch()

    page = browser.new_page()
    page.goto(use_url)

    title = page.title()
    print(f"run_sample({use_browser} at {use_url}) page.title: \"{title}\"")

    assert title == page_title_expected, f"FAIL {use_browser}: expected \"{page_title_expected}\", got \"{title}\""
    print(f"PASS {use_browser}: page.title == \"{page_title_expected}\"")

    # TODO: other actions...

    browser.close()

    return True

with sync_playwright() as playwright:

   use_url="https://google.com"
    # google.com contains text "Google".
   page_title_expected="Google"

   use_browser="firefox"
   response=run_sample(playwright)

   use_browser="chromium"
   response=run_sample(playwright)

   use_browser="webkit"
   response=run_sample(playwright)

"""

# TODO: Additional targets  
#   use_url="https://example.com"
   page_title_expected="Example Domain"

# TODO: See https://wilsonmar.github.io/flood-the-internet/#playwright

https://medium.com/@modirahul2019/building-a-robust-automation-framework-with-playwright-and-python-99bc27989325
https://www.thoughtworks.com/radar/languages-and-frameworks/playwright
https://www.scrapingbee.com/blog/playwright-for-python-web-scraping/
https://github.com/nirtal85/Playwright-Python-Example

https://playwright.dev/python/

https://playwright.dev/python/docs/api/class-playwright

"""    