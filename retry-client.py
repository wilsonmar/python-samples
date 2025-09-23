#!/usr/bin/env python3
# https://www.perplexity.ai/search/how-to-use-uv-to-create-the-eq-O8ocUS3VSCum2i.ARsyQGQ

"""mock-client.py here.

https://github.com/wilsonmar/python-samples/blob/main/mock-client.py

A mock client using tenacity library to test recovery from errors purposely returned by Flask server app mock-flask.py (500 server err, Timelout, 404, 204 rate limit, 204 empty response).

Based on https://parottasalna.com/2024/09/07/mastering-request-retrying-in-python-with-tenacity-a-developers-journey/

NOTE: Alternative is using a proxy such as https://decodo.com/blog/python-requests-retry#h2-requests_retries_with_decorator

"""
# SECTION 1: Custom Dunder variables of metadata about this program:

__last_change__ = "25-09-23 v001 + new from Jafer :mock-client.py"

# TODO: Code both client and server code and use parallel?

# SECTION 2: Import internal libraries:

import requests
import logging

# SECTION 3: Import External libraries:

try:
    from tenacity import retry_any, retry, retry_if_exception_type, retry_if_result
    from tenacity import wait_fixed, wait_exponential
    from tenacity import stop_after_attempt
    from tenacity import before_log, after_log
    from requests.exceptions import HTTPError, Timeout
except Exception as e:
    print(f"Python module import failed: {e}")
    print("Please activate your virtual environment:")
    print("\n  uv venv .venv\n  source .venv/bin/activate\n  uv add ___")
    exit(9)

# SECTION 4: Define global variables:

server_port = 5001  # 5000 is the default used by mock-flask.py
   # 5000 is already used. by AirPlay Receiver.

# SECTION 5: Utility functions:

# SECTION 6: Override with run parameters:

# SECTION 7: Audit run parameters:

# SECTION 8: Configure logging:

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# SECTION 9: Invoke retry() from the tenacity library:


@retry(retry=retry_any(retry_if_exception_type((HTTPError, Timeout)), 
        retry_if_result(lambda x: x is None)),   
        stop=stop_after_attempt(3), 
        before=before_log(logger, logging.INFO),
        after=after_log(logger, logging.INFO))
def fetch_all_responses():
    """Respond to all responses. Retry after empty response 204."""
    response = requests.get(f"http://localhost:{server_port}/timeout")
    if response.status_code == 204:
        return None  # Simulate an empty response
    response.raise_for_status()
    return response.json()


@retry(stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type((HTTPError, Timeout)),
        before=before_log(logger, logging.INFO),
        after=after_log(logger, logging.INFO))
def fetch_data():
    """Apply wait_fixed 2 seconds."""
    response = requests.get(f"http://localhost:{server_port}/timeout", timeout=2)  # Set a short timeout to simulate failure
    response.raise_for_status()
    return response.json()


@retry(stop=stop_after_attempt(5),
       wait=wait_exponential(multiplier=1, min=2, max=10),
       before=before_log(logger, logging.INFO),
       after=after_log(logger, logging.INFO))
def fetch_rate_limit():
    """Apply wait_exponential back-off 2-10 seconds of rate-limited response.
    
    Wait time between retries increases exponentially, 
    reducing the load on the server and preventing further rate limiting.
    """
    response = requests.get(f"http://localhost:{server_port}/rate_limit")
    response.raise_for_status()
    return response.json()


@retry(retry=retry_if_result(lambda x: x is None), 
       stop=stop_after_attempt(3), before=before_log(logger, logging.INFO),
       after=after_log(logger, logging.INFO))
def fetch_empty_response():
    """Retry after empty response 204."""
    response = requests.get(f"http://localhost:{server_port}/empty_response")
    if response.status_code == 204:
        return None  # Simulate an empty response
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':

    # SECTION 10: Reach mock-flask.py API server:

    try:
        data = fetch_all_responses()
        print("fetch_all_responses() successful.", data)
    except Exception as e:
        print("fetch_all_responses() failed:", str(e))


    try:
        data = fetch_data()
        print("fetch_data() successful.", data)
    except Exception as e:
        print("fetch_data() failed:", str(e))

    try:
        data = fetch_rate_limit()
        print("fetch_rate_limit() successful.", data)
    except Exception as e:
        print("fetch_rate_limit() failed:", str(e))

    try:
        data = fetch_empty_response()
        print("fetch_empty_response() successful.", data)
    except Exception as e:
        print("fetch_empty_response() failed:", str(e))
    

"""
INFO:__main__:Starting call to '__main__.fetch_all_responses', this is the 1st time calling it.
fetch_all_responses() successful. {'message': 'Delayed response'}
INFO:__main__:Starting call to '__main__.fetch_data', this is the 1st time calling it.
INFO:__main__:Finished call to '__main__.fetch_data' after 2.003(s), this was the 1st time calling it.
INFO:__main__:Starting call to '__main__.fetch_data', this is the 2nd time calling it.
INFO:__main__:Finished call to '__main__.fetch_data' after 6.012(s), this was the 2nd time calling it.
INFO:__main__:Starting call to '__main__.fetch_data', this is the 3rd time calling it.
INFO:__main__:Finished call to '__main__.fetch_data' after 10.023(s), this was the 3rd time calling it.
fetch_data() failed: RetryError[<Future at 0x103b7df30 state=finished raised ReadTimeout>]
INFO:__main__:Starting call to '__main__.fetch_rate_limit', this is the 1st time calling it.
fetch_rate_limit() successful. {'message': 'Success'}
INFO:__main__:Starting call to '__main__.fetch_empty_response', this is the 1st time calling it.
fetch_empty_response() successful. {'message': 'Success'}
"""