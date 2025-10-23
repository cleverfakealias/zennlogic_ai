"""Health check endpoint."""

from fastapi import APIRouter


router = APIRouter()


@router.get("/healthz", summary="Health check", description="Returns service health status.")
def health_check():
    """Return service health status."""
    return {"status": "ok"}
