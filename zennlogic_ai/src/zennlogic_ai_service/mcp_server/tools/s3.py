"""MCP S3 tool: list objects."""

from zennlogic_ai_service.aws.s3 import get_s3_client
from zennlogic_ai_service.config import settings


def list(prefix: str):
    """List S3 objects with prefix."""
    s3 = get_s3_client()
    resp = s3.list_objects_v2(Bucket=settings.s3_bucket, Prefix=prefix)
    return {"objects": [obj["Key"] for obj in resp.get("Contents", [])]}
