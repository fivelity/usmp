"""Presets API endpoints.
Provides CRUD operations for dashboard presets.
Currently uses an in-memory store; replace with database persistence later.
"""
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, Path, Body, Depends
from uuid import uuid4
from datetime import datetime

from app.models.widget import DashboardPreset
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

# In-memory preset storage (id -> DashboardPreset)
_PRESET_STORE: Dict[str, DashboardPreset] = {}


def _get_preset_or_404(preset_id: str) -> DashboardPreset:
    if preset_id not in _PRESET_STORE:
        raise HTTPException(status_code=404, detail="Preset not found")
    return _PRESET_STORE[preset_id]


@router.get("/", response_model=List[DashboardPreset])
async def list_presets() -> List[DashboardPreset]:
    """Return all saved presets."""
    return list(_PRESET_STORE.values())


@router.post("/", response_model=DashboardPreset, status_code=201)
async def create_preset(preset: DashboardPreset = Body(...)) -> DashboardPreset:
    """Create a new dashboard preset. Generates an ID if missing."""
    if not preset.id:
        preset.id = str(uuid4())
    if preset.id in _PRESET_STORE:
        raise HTTPException(status_code=400, detail="Preset ID already exists")
    preset.created_at = datetime.now()
    preset.updated_at = datetime.now()
    _PRESET_STORE[preset.id] = preset
    logger.info("Created preset %s", preset.id)
    return preset


@router.get("/{preset_id}", response_model=DashboardPreset)
async def get_preset(preset_id: str = Path(..., description="Preset ID")) -> DashboardPreset:
    """Retrieve a single preset by ID."""
    return _get_preset_or_404(preset_id)


@router.put("/{preset_id}", response_model=DashboardPreset)
async def update_preset(
    preset_id: str = Path(..., description="Preset ID"),
    preset_update: DashboardPreset = Body(...),
) -> DashboardPreset:
    """Replace an existing preset."""
    stored = _get_preset_or_404(preset_id)
    # Preserve creation time
    preset_update.created_at = stored.created_at
    preset_update.updated_at = datetime.now()
    _PRESET_STORE[preset_id] = preset_update
    logger.info("Updated preset %s", preset_id)
    return preset_update


@router.delete("/{preset_id}", status_code=204)
async def delete_preset(preset_id: str = Path(..., description="Preset ID")) -> None:
    """Delete a preset by ID."""
    _get_preset_or_404(preset_id)
    _PRESET_STORE.pop(preset_id)
    logger.info("Deleted preset %s", preset_id)
    return None
