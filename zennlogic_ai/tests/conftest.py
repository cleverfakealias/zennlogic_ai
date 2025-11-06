import os
from pathlib import Path
import sys


# Ensure the project's `src` directory is on sys.path during tests so the
# `service` package (under src/service) can be imported without installing the
# package into the environment. This keeps tests fast and hermetic.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import boto3  # noqa: E402
from moto import mock_aws  # noqa: E402
import pytest  # noqa: E402


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
