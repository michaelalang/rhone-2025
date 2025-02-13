"""
# use environment to configure the trace like
OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4317 OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
 OTEL_SERVICE_NAME=test OTEL_SERVICE_NAMESPACE=namespace \
 OTEL_SERVICE_VERSION=v1.1.2 \
 TRACEPARENT=01-xxxxx-xxx-01 python example-trace.py

# use Protocol=console if you do not have any trace store available
OTEL_EXPORTER_OTLP_PROTOCOL=console \
 OTEL_SERVICE_NAME=test OTEL_SERVICE_NAMESPACE=namespace \
 OTEL_SERVICE_VERSION=v1.1.2 \
"""

import os

from opentelemetry import trace
import opentelemetry.context
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.resources import (
    SERVICE_NAME,
    SERVICE_NAMESPACE,
    SERVICE_VERSION,
    Resource,
)
from opentelemetry.trace.status import StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as grpcOTLPSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as httpOTLPSpanExporter,
)

if os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "grpc") == "http":
    exporter = httpOTLPSpanExporter(
        endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318"),
        insecure=True,
    )
elif os.environ.get("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc") == "grpc":
    exporter = grpcOTLPSpanExporter(
        endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"),
        insecure=True,
    )
else:
    exporter = ConsoleSpanExporter()

trace.set_tracer_provider(TracerProvider(
resource=Resource.create(
            {
                SERVICE_NAME: os.environ.get("OTEL_SERVICE_NAME", "example"),
                SERVICE_NAMESPACE: os.environ.get("OTEL_SERVICE_NAMESPACE", "example"),
                SERVICE_VERSION: os.environ.get("OTEL_SERVICE_VERSION", "v1.0"),
            }
        )
))
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(exporter)
)
tracer = trace.get_tracer(__name__)
try:
    ctx = TraceContextTextMapPropagator().extract({"traceparent": os.environ.get("TRACEPARENT", False)})
except:
    ctx = opentelemetry.context.get_current()

print(ctx)

with tracer.start_as_current_span("example",
    context=ctx) as span:
    span.set_status(StatusCode.OK)
    span.add_event(
            "Hello World",
            attributes={
                "name": "example",
                "another": "attribute",
            },
        )
