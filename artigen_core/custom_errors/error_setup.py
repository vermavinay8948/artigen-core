from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from .error_enum import ErrorCode


class ErrorResponse:
    def __init__(self, error_code: ErrorCode, service: Optional[str] = None, detailed_message: Optional[str] = None):
        self.message = error_code.message
        self.code = error_code.code
        self.service = service
        self.detailed_message = detailed_message or self.message
        self.timestamp = self._get_current_timestamp()

    def _get_current_timestamp(self):
        # Returns the current UTC timestamp in the specified format
        now = datetime.utcnow()
        return [
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second,
            now.microsecond,
        ]

    def to_dict(self):
        return {
            "message": self.message,
            "code": self.code,
            "detailedMessage": self.detailed_message,
            "service": self.service,
            "timeStamp": self.timestamp,
        }

    def raise_error(
            error_code: ErrorCode,
            status_code: int = 400,
            service: Optional[str] = None,
            detailed_message: Optional[str] = None,
    ):
        # Log the error
        # logger.error(f"Error occurred: code={error_code.code}, message={error_code.message}, type={type}, detailed_message={detailed_message}")

        error_response = ErrorResponse(error_code, service, detailed_message)
        error_content = {"error": error_response.to_dict()}
        raise HTTPException(status_code=status_code, detail=error_content)
