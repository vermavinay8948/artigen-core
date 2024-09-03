import logging
import time

from io import BytesIO
from fastapi import Request
from opentelemetry import trace
from opentelemetry.propagate import inject, extract
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse


class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tracer = trace.get_tracer(__name__)

        # Extract trace context from incoming request headers
        context = extract(request.headers)

        # Start a new span with the extracted context
        with tracer.start_as_current_span(f"HTTP {request.method} {request.url.path}", context=context) as span:
            start_time = time.time()

            # Extract request information
            user_id = request.headers.get("X-USER-ID", "")
            session_id = request.headers.get("X-SESSION-ID", "")
            request_id = request.headers.get("X-REQUEST-ID", "")

            request_body = str(request.stream())

            # Inject trace context into outgoing request headers
            new_header = MutableHeaders(request._headers)
            inject(new_header)
            request._headers = new_header
            request.scope.update(headers=request.headers.raw)

            # Call the next middleware or endpoint
            response = await call_next(request)

            # Capture response body
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            # Create a new response object with the same content
            new_response = StreamingResponse(BytesIO(response_body), status_code=response.status_code,
                                             headers=dict(response.headers))

            try:
                response_body = response_body.decode('utf-8')
            except Exception:
                response_body = str(response_body)


            span_context = span.get_span_context()
            trace_id = format(span_context.trace_id, '032x')  # Convert trace_id to hex string
            span_id = format(span_context.span_id, '016x')  # Convert span_id to hex string

            parent_span_id = None
            if span.parent:
                parent_span_id = format(span.parent.span_id, '016x')

            # Prepare log entry
            log_entry = {
                "timestamp": int(start_time * 1000),  # Convert to milliseconds
                "user_id": user_id,
                "session_id": session_id,
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": span_id,
                "parent_span_id": parent_span_id,
                "url": str(request.url),
                "url_params": dict(request.query_params),
                "request_body": request_body,
                "response_body": response_body,
                "response_status": response.status_code
            }

            # Log the request and response details
            logging.info(log_entry)
            # print(log_entry)

            return new_response
