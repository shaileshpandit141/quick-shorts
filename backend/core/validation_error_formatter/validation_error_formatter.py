from typing import Any, Dict, List, Union, Optional, Literal
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.fields import Field
from .types import TypeErrors


class ValidationErrorFormatter:
    """Formats Django and DRF validation errors into a structured format."""

    @staticmethod
    def format(
        errors: Union[
            Dict[str, Any],
            List[Any],
            str,
            DjangoValidationError,
            DRFValidationError,
        ],
        parent_field: Optional[str] = None,
        field_mapping: Optional[Dict[str, Field]] = None,
        nested_format: Literal["dot", "bracket"] = "dot",
    ) -> TypeErrors:
        """Main function to format Django/DRF validation errors."""
        formatted_errors: TypeErrors = []

        errors = ValidationErrorFormatter._normalize_errors(errors)
        ValidationErrorFormatter._process_errors(
            errors, formatted_errors, parent_field, field_mapping, nested_format
        )

        return formatted_errors

    @staticmethod
    def _normalize_errors(errors: Any) -> Union[Dict[str, Any], List[Any], str]:
        """Convert Django & DRF errors into a standard format."""
        if isinstance(errors, DjangoValidationError):
            return (
                errors.message_dict
                if hasattr(errors, "message_dict")
                else {"non_field_errors": errors.messages}
            )

        if isinstance(errors, DRFValidationError):
            return errors.detail if hasattr(errors, "detail") else errors.args[0]

        return errors

    @staticmethod
    def _process_errors(
        errors: Any,
        formatted_errors: TypeErrors,
        parent_field: Optional[str],
        field_mapping: Optional[Dict[str, Field]],
        nested_format: Literal["dot", "bracket"],
    ) -> None:
        """Recursively process and format errors."""
        if isinstance(errors, dict):
            for field, error_messages in errors.items():
                formatted_field = ValidationErrorFormatter._format_field(
                    field, parent_field, nested_format
                )
                ValidationErrorFormatter._handle_field_errors(
                    formatted_field,
                    error_messages,
                    formatted_errors,
                    field_mapping,
                    nested_format,
                )
        elif isinstance(errors, list):
            for message in errors:
                ValidationErrorFormatter._append_error(
                    "none", str(message), formatted_errors
                )
        elif isinstance(errors, str):
            ValidationErrorFormatter._append_error("none", errors, formatted_errors)
        else:
            ValidationErrorFormatter._append_error(
                "none", "An unknown error occurred", formatted_errors
            )

    @staticmethod
    def _handle_field_errors(
        field: str,
        error_messages: Any,
        formatted_errors: TypeErrors,
        field_mapping: Optional[Dict[str, Field]],
        nested_format: Literal["dot", "bracket"],
    ) -> None:
        """Process and append errors for a specific field."""
        if isinstance(error_messages, list):
            for message in error_messages:
                if isinstance(message, dict):
                    ValidationErrorFormatter._append_error(
                        field,
                        message.get("message", "An error occurred."),
                        formatted_errors,
                        message.get("code", "unknown"),
                        message.get("details", {}),
                    )
                else:
                    ValidationErrorFormatter._append_error(
                        field, str(message), formatted_errors
                    )
        elif isinstance(error_messages, dict):
            # Recursively process nested errors
            ValidationErrorFormatter._process_errors(
                error_messages, formatted_errors, field, field_mapping, nested_format
            )
        else:
            ValidationErrorFormatter._append_error(
                field, str(error_messages), formatted_errors
            )

    @staticmethod
    def _format_field(
        field: str, parent_field: Optional[str], nested_format: str
    ) -> str:
        """Apply the selected nested field format (dot or bracket notation)."""
        if parent_field:
            return (
                f"{parent_field}[{field}]"
                if nested_format == "bracket"
                else f"{parent_field}.{field}"
            )
        return field if field != "non_field_errors" else "none"

    @staticmethod
    def _extract_field_details(
        field_name: str, field_mapping: Optional[Dict[str, Field]]
    ) -> Dict[str, Any]:
        """Extract metadata (e.g., required, max_length) for a field."""
        if not field_mapping or field_name not in field_mapping:
            return {}

        field = field_mapping[field_name]
        return {
            "required": getattr(field, "required", None),
            "max_length": getattr(field, "max_length", None),
            "min_length": getattr(field, "min_length", None),
            "field_type": field.__class__.__name__,
        }

    @staticmethod
    def _append_error(
        field: str,
        message: str,
        formatted_errors: TypeErrors,
        code: str = "unknown",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Append a formatted error to the list."""
        formatted_errors.append(
            {
                "field": field,
                "code": code,
                "message": message,
                "details": details or {},
            }
        )
