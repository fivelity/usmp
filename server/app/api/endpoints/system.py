from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthCheckResponse(BaseModel):
    status: str = "OK"
    message: str = "System is healthy"


@router.get("/health", response_model=HealthCheckResponse, tags=["System"])
async def health_check():
    """
    Perform a health check.
    Returns the current health status of the application.
    """
    return HealthCheckResponse()
