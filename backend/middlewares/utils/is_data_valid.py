from logging import getLogger
from typing import List

from ..exceptions import InvalidDataFormatError
from .types import DataType

# Configure logger
logger = getLogger(__name__)


# Data Validation
def is_data_valid(data: DataType | None, expected_keys: List[str]) -> DataType:
    if not data or not isinstance(data, dict):
        logger.error("Invalid data format: Data is missing or not a dictionary")
        raise InvalidDataFormatError(
            message="Response data must be a valid dictionary format.",
            code="invalid_format",
            details="The response data is either missing or not in dictionary format",
        )

    if sorted(data.keys()) != sorted(expected_keys):
        logger.error(f"Invalid keys: Expected {expected_keys}, got {data.keys()}")
        raise InvalidDataFormatError(
            message="Response data is missing required fields or contains invalid fields.",
            code="invalid_keys",
            details=f"Expected fields: {', '.join(expected_keys)}. Received fields: {', '.join(data.keys())}",
        )

    return data
