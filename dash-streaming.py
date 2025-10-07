#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "dash",
#   "plotly",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file

"""dash-streaming.py here.

At https://github.com/wilsonmar/python-samples/blob/main/dash-streaming.py

Use Plotly Dash library to animate a stream of real-time updates (random values) within a Flask app.

Based on https://www.perplexity.ai/search/python-code-to-create-a-dashbo-kndpQ8EfThWOL8r7a7bgsg
https://pythonprogramming.net/live-graphs-data-visualization-application-dash-python-tutorial/#google_vignette

TODO: Instead of random numbers, use real-time.

USAGE:
    chmod +x dash-streaming.py
    uv run dash-streaming.py
    In browser: http://127.0.0.1:8050/
"""

__last_change__ = "25-10-07 v001 + new :dash-streaming.py"
__status__ = "working with random data"

import random
from collections import deque

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash(__name__)

# Set up data storage with a max length for streaming effect:
max_length = 50
times = deque(maxlen=max_length)
values = deque(maxlen=max_length)

# Initiate data:
times.append(0)
values.append(random.randint(0, 10))

app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1000,  # Update every 1000 milliseconds (1 second)
        n_intervals=0
    ),
])

@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
def update_graph_live(n):
    """Update live graph with new data points."""
    times.append(times[-1] + 1)
    values.append(values[-1] + random.uniform(-1, 1))

    data = go.Scatter(
        x=list(times),
        y=list(values),
        mode='lines+markers'
    )

    layout = go.Layout(
        xaxis=dict(range=[max(0, times[-1] - max_length), times[-1] + 1]),
        yaxis=dict(range=[min(values) - 1, max(values) + 1]),
        title='Real-Time Streaming Chart'
    )

    return {'data': [data], 'layout': layout}

if __name__ == '__main__':
    app.run(debug=True)
    # app.run_server(debug=True)   # previous call format obsoleted?

"""
uv run dash-streaming.py
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'dash-streaming'
 * Debug mode: on

"""