from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def setup_tracer(**kwargs):
    service_name = kwargs.get('service_name', '')
    resource = Resource(attributes={
        "service.name": service_name
    })

    tracer_provider = TracerProvider(resource=resource)

    ## OTLPSpanExporter is used for production ready environments. Requires a backend to export traces.
    # span_exporter = OTLPSpanExporter()

    ## Just for consoling the traces locally
    span_exporter = ConsoleSpanExporter()

    span_processor = BatchSpanProcessor(span_exporter)

    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)
