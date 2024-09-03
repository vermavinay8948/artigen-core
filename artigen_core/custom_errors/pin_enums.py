from .error_enum import ErrorCode


class PinErrorCodes(ErrorCode):
    PIN_NOT_FOUND = ("PIN-1001", "The requested PIN does not exist.")
    INVALID_PIN_STATUS = ("PIN-1002", "The specified PIN status is invalid.")
    USER_NOT_AUTHORIZED = ("PIN-1003", "User is not authorized to perform this action.")
    DUPLICATE_PIN = ("PIN-1004", "A PIN with the same ID already exists.")
    PIN_CREATION_FAILED = ("PIN-1005", "Failed to create a new PIN.")
    INVALID_PIN_TYPE = ("PIN-1006", "The specified PIN type is invalid.")
    REDIS_CONNECTION_ERROR = ("PIN-1007", "Failed to connect to the Redis server.")
    INVALID_PIN_REQUEST = ("PIN-1008", "The PIN request is invalid or malformed.")
    TOKEN_EXPIRED = ("PIN-1009", "Authentication token has expired.")
    UNKNOWN_ERROR = ("PIN-1010", "An unknown error occurred in the PIN service.")

