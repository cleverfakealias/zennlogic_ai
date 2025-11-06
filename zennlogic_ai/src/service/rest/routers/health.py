"""Health check endpoint."""

from fastapi import APIRouter


router = APIRouter()


@router.get("/healthz", summary="Health check", description="Returns service health status.")
def health_check() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}


# Compatibility alias
@router.get("/health", summary="Health check", description="Returns service health status.")
def health_check_alias() -> dict[str, str]:
    """Alias for health check to match docs that use /health."""
    return health_check()
