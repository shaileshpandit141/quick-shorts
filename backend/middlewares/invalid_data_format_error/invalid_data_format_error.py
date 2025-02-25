from typing import Any


# Custom Exceptions
class InvalidDataFormatError(Exception):
    def __init__(
        self,
        message: str = "Internal server error occurred",
        code: str = "server_error",
        field: str = "server",
        details: Any = "Server encountered an error processing the request",
    ) -> None:
        self.error_dict = {
            "field": field,
            "code": code,
            "message": message,
            "details": {"help": details},
        }
        super().__init__(str(self.error_dict))
