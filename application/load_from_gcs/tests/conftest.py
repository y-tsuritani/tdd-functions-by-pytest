import os

import pytest
import requests
from google.api_core.exceptions import Forbidden, NotFound
from src.main import load_csv_from_gcs


@pytest.fixture(scope="session", autouse=True)
def set_env_vars():
    os.environ["GCP_PROJECT"] = "your_project_id"
    os.environ["GCS_BUCKET"] = "your_bucket_name"


class MockStorageClient:
    def get_bucket(self, bucket_name):
        return self

    def get_blob(self, blob_name):
        return self

    def download_as_string(self):
        # テスト用のモックデータをCSV形式のバイナリとして返す
        return b"1,2,3\n4,5,6\n"


class MockStorageClientWithBucketNotFound(MockStorageClient):
    def get_bucket(self, bucket_name):
        raise NotFound(f"{bucket_name} is not found.")


# Blobが存在しない場合のモッククラス
class MockStorageClientWithBlobNotFound(MockStorageClient):
    def get_bucket(self, bucket_name):
        self.bucket_name = bucket_name
        return self  # バケットは正常に取得できる

    def get_blob(self, blob_name):
        raise NotFound(f"blob_name: {blob_name} is not found in bucket '{self.bucket_name}'.")


class MockStorageClientWithBucketForbidden(MockStorageClient):
    def get_bucket(self, bucket_name):
        raise Forbidden(f"Access denied on bucket: {bucket_name}.")


class MockStorageClientWithUnexpectedError(MockStorageClient):
    def get_bucket(self, bucket_name):
        raise Exception("An unexpected error occurred.")
