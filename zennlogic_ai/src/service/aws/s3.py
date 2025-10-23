"""S3 helpers for snapshot sync."""

import boto3
from zennlogic_ai_service.config import settings


def get_s3_client():
    """Get configured S3 client."""
    return boto3.client("s3", region_name=settings.aws_region)
