import os


# Tests should run against an editable install of the package (recommended):
#   pip install -e .[dev,test]
# If the package is not installed, fail fast with a clear instruction.
try:
    # Verify the package is installed; import only to check availability.
    # The import is only used to confirm the package is importable.
    import importlib

    importlib.import_module("service")
except Exception as exc:  # pragma: no cover - developer environment error
    raise RuntimeError(
        "Tests require the package to be installed in editable mode. "
        "Run: `pip install -e .[dev,test]` from the repo root"
    ) from exc

import boto3
from moto import mock_aws
import pytest


# Make sure boto3 has a default region to avoid NoRegionError
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")


@pytest.fixture(autouse=True)
def aws_mocks():
    """Automatically mock AWS for every test."""
    with mock_aws():
        yield


@pytest.fixture
def s3_client():
    """Example S3 client inside the mocked context."""
    s3 = boto3.client("s3", region_name="us-east-1")
    # If you need a default bucket for many tests, create it here:
    s3.create_bucket(Bucket="test-bucket")
    return s3


@pytest.fixture
def ssm_client():
    """Example SSM client inside the mocked context."""
    return boto3.client("ssm", region_name="us-east-1")
