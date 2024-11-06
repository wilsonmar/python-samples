#!/usr/bin/env python3

""" otel-flask.py at https://github.com/wilsonmar/python-samples/blob/main/otel-flask.py

STATUS: NOT TESTED on macOS M2 14.5 (23F79) using Python 3.12.7.
git commit -m "v001 + README :otel-flask.py"

This is a simple Flask app with automatic 
OpenTelemetry instrumentation custom spans 
(in two routes: / and /api/data).

BEFORE RUNNING: Run this in BASH CLI:

# Navigate or mkdir to a receiving folder.
RUN_FOLDER="$HOME/Projects/otel-flask" 
cd ; cd "$RUN_FOLDER"
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install opentelemetry-api
pip install opentelemetry-sdk
pip install opentelemetry-exporter-otlp
pip install opentelemetry-instrumentation-flask

chmod +x otel-flask.py
./otel-flask.py  # or python app.py
visit http://localhost:5000/ and 
visit http://localhost:5000/api/data to generate telemetry data to
Visit http://localhost:4317  # OTLP_RECEIVER_URL
TODO: Setup observIQ cloud to receive spans for distribution
TODO: Setup the backend system that receives and visualizes this data,
such as Jaeger, Zipkin, or cloud-based observability platform 
TODO: Grafana Cloud (https://grafana.com/blog/2023/12/18/opentelemetry-best-practices-a-users-guide-to-getting-started-with-opentelemetry/)
TODO: To better identify this app among all telemetry data,
pre-set a service name and other resource attributes based on:
https://github.com/open-telemetry/semantic-conventions/blob/main/docs/README.md
TODO: Config more sampling, error handling, and 
TODO: Config OpenTelemetry Collector for data processing & forwarding
"""

from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor


# Globals:
OLTP_RECEIVER_URL = "http://localhost:4317"

# Set up OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure the OTLP exporter http://localhost:4317
otlp_exporter = OTLPSpanExporter(endpoint=OLTP_RECEIVER_URL)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route('/')
def hello():
    with tracer.start_as_current_span("hello_span"):
        return "Hello, OpenTelemetry!"

@app.route('/api/data')
def get_data():
    with tracer.start_as_current_span("get_data_span"):
        # Simulate some work
        import time
        time.sleep(0.1)
        return {"data": "Some important data"}

if __name__ == '__main__':
    app.run(debug=True)
