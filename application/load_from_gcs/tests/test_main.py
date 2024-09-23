import os

import pytest
from google.api_core.exceptions import Forbidden, NotFound
from src.main import load_csv_from_gcs

from tests.conftest import (
    MockStorageClient,
    MockStorageClientWithBlobNotFound,
    MockStorageClientWithBucketForbidden,
    MockStorageClientWithBucketNotFound,
    MockStorageClientWithUnexpectedError,
)


def test_load_csv_from_gcs_with_monkeypatch(monkeypatch):
    def mock_storage_client(*args, **kwargs):
        return MockStorageClient()

    BUCKET_NAME = os.environ["GCS_BUCKET"]
    BLOB_NAME = "test_blob.csv"

    monkeypatch.setattr("google.cloud.storage.Client", mock_storage_client)

    # GCSからCSV文字列を読み込む
    csv_data = load_csv_from_gcs(mock_storage_client(), BUCKET_NAME, BLOB_NAME)

    # 期待されるCSVデータ（文字列）
    expected_csv_data = "1,2,3\n4,5,6\n"

    # CSVデータが期待通りの文字列かをチェック
    assert csv_data == expected_csv_data


def test_load_csv_from_gcs_bucket_notfound(monkeypatch):
    BUCKET_NAME = os.environ["GCS_BUCKET"]
    BLOB_NAME = "no_data.csv"

    # `get_bucket`が失敗するモッククライアントを設定
    monkeypatch.setattr("google.cloud.storage.Client", MockStorageClientWithBucketNotFound)

    with pytest.raises(NotFound) as exc_info:
        csv_data = load_csv_from_gcs(MockStorageClientWithBucketNotFound(), BUCKET_NAME, BLOB_NAME)

    assert str(exc_info.value) == f"404 {BUCKET_NAME} is not found."


def test_load_csv_from_gcs_blob_notfound(monkeypatch):
    BUCKET_NAME = os.environ["GCS_BUCKET"]
    BLOB_NAME = "no_data.csv"

    # `get_blob`が失敗するモッククライアントを設定
    monkeypatch.setattr("google.cloud.storage.Client", MockStorageClientWithBlobNotFound)

    with pytest.raises(NotFound) as exc_info:
        csv_data = load_csv_from_gcs(MockStorageClientWithBlobNotFound(), BUCKET_NAME, BLOB_NAME)

    assert (
        str(exc_info.value)
        == f"404 blob_name: {BLOB_NAME} is not found in bucket '{BUCKET_NAME}'."
    )


def test_load_csv_from_gcs_forbidden(monkeypatch):
    BUCKET_NAME = os.environ["GCS_BUCKET"]
    BLOB_NAME = "test_blob.csv"

    # `get_bucket`が失敗するモッククライアントを設定
    monkeypatch.setattr("google.cloud.storage.Client", MockStorageClientWithBucketForbidden)

    with pytest.raises(Forbidden) as exc_info:
        csv_data = load_csv_from_gcs(
            MockStorageClientWithBucketForbidden(), BUCKET_NAME, BLOB_NAME
        )

    assert str(exc_info.value) == f"403 Access denied on bucket: {BUCKET_NAME}."


def test_load_csv_from_gcs_unexpected_error(monkeypatch):
    BUCKET_NAME = os.environ["GCS_BUCKET"]
    BLOB_NAME = "test_blob.csv"

    # 予期せぬエラーを発生させるモッククライアントを設定
    class MockStorageClientWithUnexpectedError(MockStorageClient):
        def download_as_string(self):
            raise Exception("An unexpected error occurred.")

    monkeypatch.setattr("google.cloud.storage.Client", MockStorageClientWithUnexpectedError)

    with pytest.raises(Exception, match="An unexpected error occurred.") as exc_info:
        csv_data = load_csv_from_gcs(
            MockStorageClientWithUnexpectedError(), BUCKET_NAME, BLOB_NAME
        )

    assert str(exc_info.value) == "An unexpected error occurred."
