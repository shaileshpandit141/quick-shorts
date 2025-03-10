import os
from logging import getLogger
from typing import Optional, Type

import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Model

logger = getLogger(__name__)


def save_image(
    model_class: Type[Model], field_name: str, image_url: str, image_save_name: str
) -> Optional[str]:
    """Downloads an image from a URL and saves it using Django's default
       storage if it doesn't already exist.

    Args:
        model_class (Type[Model]): The Django model containing the ImageField.
        field_name (str): The name of the ImageField in the model.
        image_url (str): The URL of the image to download.
        image_save_name (str): The name to save the image as.

    Returns:
        Optional[str]: The saved image filename (without folder path)
        or None if the download fails or the image already exists.
    """
    try:
        logger.info(f"Starting download of image from URL: {image_url}")
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise error for HTTP failures

        obj = model_class()  # Instantiate the model dynamically
        upload_to_path = getattr(obj._meta.get_field(field_name), "upload_to", None)
        if not upload_to_path:
            return None

        extension = os.path.splitext(image_url)[1] or ".jpg"
        unique_filename = f"{image_save_name}{extension}"
        file_path = os.path.join(upload_to_path, unique_filename)

        if default_storage.exists(file_path):
            logger.info(f"Image already exists at: {file_path}")
            return file_path

        saved_path = default_storage.save(file_path, ContentFile(response.content))
        logger.info(f"Image saved successfully at: {saved_path}")

        return file_path

    except (requests.RequestException, IOError, AttributeError) as e:
        logger.error(f"Error downloading image: {e}")
        return None
