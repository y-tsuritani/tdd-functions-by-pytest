import logging
import os

from google.api_core.exceptions import Forbidden, NotFound
from google.cloud import bigquery, storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_csv_from_gcs(gcs_client: storage.Client, bucket_name: str, blob_name: str) -> str:
    """Load CSV data from Google Cloud Storage.

    Args:
        gcs_client (storage.Client): Google Cloud Storage client.
        bucket_name (str): Bucket name.
        blob_name (str): Blob name.

    Returns:
        str: CSV data.
    """
    try:
        bucket = gcs_client.get_bucket(bucket_name)
        blob = bucket.get_blob(blob_name)
        if not blob:
            raise NotFound(f"Blob '{blob_name}' not found in bucket '{bucket_name}'.")
        return blob.download_as_string().decode("utf-8")
    except NotFound:
        logger.error(
            f"bucket: {bucket_name}, blob: {blob_name} is not found.\n"
            "Please check the bucket name and blob name."
        )
        raise
    except Forbidden:
        logger.error(
            f"Access denied on bucket: {bucket_name}, blob: {blob_name}.\n"
            "Please check the permission of Service Account."
        )
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
