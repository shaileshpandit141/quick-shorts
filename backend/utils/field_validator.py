from typing import Any, Callable, Dict, List, Optional, TypedDict


class ErrorsFieldType(TypedDict):
    """Type for API error responses"""

    field: str
    code: str
    message: str
    details: Optional[Dict[str, Any]]


ErrorsType = List[ErrorsFieldType]


class FieldValidator:
    """
    A class to validate fields for emptiness and other conditions.

    This class provides functionality to validate field values against various criteria
    including blank checks, type validation, and custom validation rules.
    """

    # Default error messages for different validation scenarios
    DEFAULT_MESSAGES = {
        "blank": "The {field} field cannot be blank or empty.",
        "invalid": "Please provide a valid {field}.",
        "same_as_field": 'Value "{value}" cannot be the same as field name "{field}".',
        "invalid_type": "Invalid data type for {field}. Expected a string.",
    }

    def __init__(
        self,
        data: Dict[str, Any] = {},
        fields: List[str] = [],
        custom_validators: Dict[str, Callable] | None = None,
        case_sensitive: bool = False,
    ) -> None:
        """
        Initialize the validator with data and validation rules.

        Args:
            data: Dictionary containing field names and their values
            fields: List of field names to validate
            custom_validators: Optional dictionary of custom validation functions
            case_sensitive: Whether to perform case-sensitive comparisons
        """
        self.data = data
        self.fields = fields
        self.errors: ErrorsType = []
        self.custom_validators = custom_validators or {}
        self.case_sensitive = case_sensitive
        self.validate()

    def __get_error_message(self, code: str, field: str, value: str = "") -> str:
        """Generate an error message using the default message template."""
        return self.DEFAULT_MESSAGES[code].format(field=field, value=value)

    def validate(self) -> None:
        """
        Validate all fields according to the defined rules.

        For each field, performs the following checks:
        1. Custom validation if provided
        2. Type validation
        3. Empty/blank validation
        4. Field name matching validation
        """
        for key in self.fields:
            value = self.data.get(key)

            # Run custom validator if provided
            if custom_validator := self.custom_validators.get(key):
                error = custom_validator(value)
                if error:
                    self.errors.append(
                        {
                            "field": key,
                            "code": "code_" + key,
                            "message": error,
                            "details": None,
                        }
                    )
                continue

            # Check for valid type
            if not isinstance(value, (str, type(None))):
                self.errors.append(
                    {
                        "field": key,
                        "code": "invalid_type",
                        "message": self.__get_error_message("invalid_type", key),
                        "details": None,
                    }
                )
            # Check for empty values
            elif value is None or value.strip() == "":
                self.errors.append(
                    {
                        "field": key,
                        "code": "blank",
                        "message": self.__get_error_message("blank", key),
                        "details": None,
                    }
                )
            elif isinstance(value, str):
                # Check if value matches field name
                if (
                    (value.lower() == key.lower())
                    if not self.case_sensitive
                    else (value == key)
                ):
                    self.errors.append(
                        {
                            "field": key,
                            "code": "invalid",
                            "message": self.__get_error_message("invalid", key),
                            "details": None,
                        }
                    )
                elif (
                    "".join(key.split("_")).lower() == "".join(value.split(" ")).lower()
                ):
                    self.errors.append(
                        {
                            "field": key,
                            "code": "same_as_field",
                            "message": self.__get_error_message(
                                "same_as_field", key, value
                            ),
                            "details": None,
                        }
                    )

    def is_valid(self) -> bool:
        """Return True if no validation errors were found."""
        return not self.errors

    def get(self, field: str) -> Any:
        """Return value with provided field name.

        Args:
            field: The field name to get the value for

        Returns:
            The value associated with the field

        Raises:
            KeyError: If the field does not exist in the data
        """
        if field in self.data:
            return self.data[field]
        raise KeyError(f'Field "{field}" does not exist in the data')
