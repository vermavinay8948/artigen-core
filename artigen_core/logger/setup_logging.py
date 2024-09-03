import logging

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs._internal.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.resources import Resource
from pythonjsonlogger import jsonlogger


def setup_logging(**kwrgs):
    service_name = kwrgs.get('service_name', '')
    resource = Resource.create(
        {
            "service.name": service_name
        }
    )

    # Set up the LoggerProvider
    logger_provider = LoggerProvider(resource=resource)
    console_log_exporter = ConsoleLogExporter()
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(console_log_exporter))
    set_logger_provider(logger_provider)

    # Create and configure the log handler
    log_handler = LoggingHandler(level=logging.INFO)

    # Set up the formatter with the service_name included
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s service_name=%(service_name)s %(X-USER-ID)s %(X-SESSION-ID)s %(X-REQUEST-ID)s %(trace_id)s %(url)s %(url_params)s %(request_body)s %(response_body)s %(response_status)s %(error_message)s %(stack_trace)s'
    )
    log_handler.setFormatter(formatter)

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(log_handler)

    # Add service_name to the extra context in log entries
    logging.LoggerAdapter(root_logger, {"service_name": service_name})
