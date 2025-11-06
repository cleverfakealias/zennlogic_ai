"""S3 helpers for snapshot sync."""

from typing import Any

import boto3

from service.config import settings


def get_s3_client() -> Any:
    """Get configured S3 client.

    Returns a boto3 S3 client. The concrete type is dynamic, so we annotate
    as Any to avoid heavy boto typing dependencies.
    """
    return boto3.client("s3", region_name=settings.aws_region)
