#!/usr/bin/env python3
# https://www.perplexity.ai/search/how-to-use-uv-to-create-the-eq-O8ocUS3VSCum2i.ARsyQGQ

"""mock-flask.py here.

https://github.com/wilsonmar/python-samples/blob/main/mock-flask.py

A mock Flask server app run for testing how mock-client.py recovers from request errors (500 server err, Timelout, 404, 204 rate limit, 204 empty response).

Based on https://parottasalna.com/2024/09/07/mastering-request-retrying-in-python-with-tenacity-a-developers-journey/
by https://www.linkedin.com/in/syedjaferk/ Syed Jafer K

"""

__last_change__ = "25-09-23 v001 + new from Jafer :mock-flask.py"

import random
import time

try:
    from flask import Flask, jsonify, make_response
except Exception as e:
    print(f"Python module import failed: {e}")
    print("Please activate your virtual environment:")
    print("\n  uv venv .venv\n  source .venv/bin/activate\n  uv add ___")
    exit(9)

server_port = 5001

app = Flask(__name__)
 
# Scenario 1: Random server errors
@app.route('/random_error', methods=['GET'])
def random_error():
    """Simulate a 500 error randomly."""
    if random.choice([True, False]):
        return make_response(jsonify({"error": "Server error"}), 500)
    return jsonify({"message": "Success"})
 
# Scenario 2: Timeouts
@app.route('/timeout', methods=['GET'])
def timeout():
    """Simulate a long delay that can cause a timeout."""
    time.sleep(5)  
    return jsonify({"message": "Delayed response"})
 
# Scenario 3: 404 Not Found error
@app.route('/not_found', methods=['GET'])
def not_found():
    """Return 404 not found."""
    return make_response(jsonify({"error": "Not found"}), 404)
 
# Scenario 4: Rate-limiting (simulated with a fixed chance)
@app.route('/rate_limit', methods=['GET'])
def rate_limit():
    """Rate-limit response by not responding to some requests."""
    if random.randint(1, 10) <= 3:  # 30% chance to simulate rate limiting
        return make_response(jsonify({"error": "Rate limit exceeded"}), 429)
    return jsonify({"message": "Success"})
 
# Scenario 5: Empty response
@app.route('/empty_response', methods=['GET'])
def empty_response():
    """Return empty response."""
    if random.choice([True, False]):
        return make_response("", 204)  # Simulate an empty response with 204 No Content
    return jsonify({"message": "Success"})
 
if __name__ == '__main__':
    # Verify if port is available for use:
    # 5000 is used by an AirTunes service (Apple AirPlay), not the Flask server.
    # TODO: lsof -nP +c 15 | grep LISTEN

    app.run(host='localhost', port=server_port, debug=True)

"""
$ chmod +x mock-flask.py
$ source .venv/bin/activate
$ uv run mock-flask.py &    # & for run in background
 * Serving Flask app 'mock-flask'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://localhost:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 791-292-641
 * Detected change in '/Users/johndoe/github-wilsonmar/python-samples/mock-flask.py', reloading
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 754-560-600
$ rm -f "/Users/johndoe/.safety/safety-uv.lock"
$ uv run mock-client.py
$ deactivate
"""