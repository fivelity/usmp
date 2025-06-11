import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Path, Depends, Request
from datetime import datetime, timedelta

from app.models.sensor import (
    SensorReading,
    SensorDefinition,
    SensorProviderStatus,
    SensorCategory,
    HardwareType,
    DataQuality,
)
from app.services.sensor_manager import SensorManager
from app.core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()


# Dependency to get the sensor manager
def get_sensor_manager(request: Request) -> SensorManager:
    """Retrieve SensorManager from FastAPI app state."""
    sensor_manager: SensorManager = request.app.state.sensor_manager  # type: ignore
    if sensor_manager is None:
        raise HTTPException(status_code=503, detail="Sensor manager not initialized")
    return sensor_manager


# Real-time sensor data endpoints using SensorManager


@router.get("/status", response_model=List[SensorProviderStatus])
async def get_sensor_status(
    sensor_manager: SensorManager = Depends(get_sensor_manager),
) -> List[SensorProviderStatus]:
    """
    Get the status of all available sensor sources.
    """
    logger.info("Fetching status of all sensor sources")
    try:
        sources = sensor_manager.get_available_sources()
        return sources
    except Exception as e:
        logger.error(f"Error retrieving sensor statuses: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to retrieve sensor statuses"
        )


@router.get("/definitions", response_model=List[SensorDefinition])
async def get_sensor_definitions(
    source: Optional[str] = Query(None, description="Filter by sensor source ID"),
    sensor_manager: SensorManager = Depends(get_sensor_manager),
) -> List[SensorDefinition]:
    """
    Get all sensor definitions. Explicit endpoint for clarity.
    """
    return await list_sensors(source=source, sensor_manager=sensor_manager)


@router.get("/data/all", response_model=Dict[str, List[SensorReading]])
async def get_all_sensor_data(
    sensor_manager: SensorManager = Depends(get_sensor_manager),
) -> Dict[str, List[SensorReading]]:
    """
    Get current data readings from all active sensors, grouped by source.
    """
    logger.info("Fetching all current sensor data")

    try:
        all_data = await sensor_manager.get_all_sensor_data()
        logger.info(f"Retrieved data from {len(all_data)} sensor sources")
        return all_data

    except Exception as e:
        logger.error(f"Error retrieving all sensor data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve sensor data")


@router.get("/", response_model=List[SensorDefinition])
async def list_sensors(
    source: Optional[str] = Query(None, description="Filter by sensor source ID"),
    sensor_manager: SensorManager = Depends(get_sensor_manager),
) -> List[SensorDefinition]:
    """
    List all available sensor definitions from active sensor providers.
    Supports filtering by source ID.
    """
    logger.info("Listing all sensor definitions. Filters: source=%s", source)

    try:
        definitions = await sensor_manager.get_sensor_definitions()

        if source:
            definitions = [defn for defn in definitions if defn.source_id == source]

        logger.info(f"Found {len(definitions)} sensor definitions")
        return definitions

    except Exception as e:
        logger.error(f"Error retrieving sensor definitions: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to retrieve sensor definitions"
        )


@router.get("/{sensor_id}", response_model=SensorDefinition)
async def get_sensor_definition(
    sensor_id: str = Path(..., description="The ID of the sensor to retrieve"),
    sensor_manager: SensorManager = Depends(get_sensor_manager),
) -> SensorDefinition:
    """
    Get the definition of a specific sensor.
    """
    logger.info("Fetching sensor definition for sensor_id: %s", sensor_id)

    try:
        definitions = await sensor_manager.get_sensor_definitions()

        # Find the sensor definition by ID
        for definition in definitions:
            if definition.sensor_id == sensor_id:
                return definition

        logger.warning("Sensor definition not found for sensor_id: %s", sensor_id)
        raise HTTPException(
            status_code=404, detail=f"Sensor definition {sensor_id} not found"
        )

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(
            f"Error retrieving sensor definition for {sensor_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail="Failed to retrieve sensor definition"
        )


@router.get("/{sensor_id}/data", response_model=List[SensorReading])
async def get_sensor_data(
    sensor_id: str = Path(..., description="The ID of the sensor to retrieve data for"),
    limit: Optional[int] = Query(
        10, description="Limit the number of recent readings", ge=1, le=100
    ),
    sensor_manager: SensorManager = Depends(get_sensor_manager),
) -> List[SensorReading]:
    """
    Get recent data readings for a specific sensor.
    """
    logger.info("Fetching data for sensor_id: %s with limit: %s", sensor_id, limit)

    try:
        # Get all current sensor data
        all_data = await sensor_manager.get_all_sensor_data()

        # Find readings for the specific sensor
        sensor_readings = []
        for source_id, readings in all_data.items():
            for reading in readings:
                if reading.sensor_id == sensor_id:
                    sensor_readings.append(reading)

        if not sensor_readings:
            logger.info(
                "No data available for sensor_id: %s. Returning empty list.", sensor_id
            )
            return []

        # Sort by timestamp descending to get the most recent readings
        sorted_readings = sorted(
            sensor_readings, key=lambda r: r.timestamp, reverse=True
        )

        return sorted_readings[:limit]

    except Exception as e:
        logger.error(
            f"Error retrieving sensor data for {sensor_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to retrieve sensor data")
