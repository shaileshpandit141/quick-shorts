import logging
from typing import Dict, Optional, Type

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model
from rest_framework.serializers import Field, ModelSerializer

logger = logging.getLogger(__name__)


class BaseModelSerializer(ModelSerializer):
    Meta: Optional[Type]

    def get_fields(self) -> Dict[str, Field]:
        fields = super().get_fields()
        meta = getattr(self, "Meta", None)
        model: Optional[Type[Model]] = getattr(meta, "model", None)

        if model is None:
            raise ValueError("Meta.model must be defined in subclasses.")

        logger.debug("Initializing fields for model: %s", model.__name__)

        for field_name, field in fields.items():
            try:
                model_field = model._meta.get_field(field_name)
                if hasattr(model_field, "error_messages"):
                    logger.debug("Updating error messages for field: %s", field_name)
                    field.error_messages.update(model_field.error_messages)
            except FieldDoesNotExist:
                logger.debug(
                    "Field '%s' does not exist on model '%s'; skipping.",
                    field_name,
                    model.__name__,
                )
                pass  # Ignore non-model fields

        return fields
