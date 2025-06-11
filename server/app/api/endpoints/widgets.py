"""Widgets API endpoints.
Allows CRUD operations for individual widget configurations.
In-memory store only – to be replaced by persistent storage.
"""
from typing import List, Dict
from fastapi import APIRouter, HTTPException, Path, Body
from uuid import uuid4
from datetime import datetime

from app.models.widget import WidgetConfig
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

_WIDGET_STORE: Dict[str, WidgetConfig] = {}


def _get_widget_or_404(widget_id: str) -> WidgetConfig:
    if widget_id not in _WIDGET_STORE:
        raise HTTPException(status_code=404, detail="Widget not found")
    return _WIDGET_STORE[widget_id]


@router.get("/", response_model=List[WidgetConfig])
async def list_widgets() -> List[WidgetConfig]:
    """Return all widgets in store."""
    return list(_WIDGET_STORE.values())


@router.post("/", response_model=WidgetConfig, status_code=201)
async def create_widget(widget: WidgetConfig = Body(...)) -> WidgetConfig:
    """Create a widget config."""
    if not widget.id:
        widget.id = str(uuid4())
    if widget.id in _WIDGET_STORE:
        raise HTTPException(status_code=400, detail="Widget ID already exists")
    widget.created_at = datetime.now()
    widget.updated_at = datetime.now()
    _WIDGET_STORE[widget.id] = widget
    logger.info("Created widget %s", widget.id)
    return widget


@router.get("/{widget_id}", response_model=WidgetConfig)
async def get_widget(widget_id: str = Path(..., description="Widget ID")) -> WidgetConfig:
    """Retrieve widget by id."""
    return _get_widget_or_404(widget_id)


@router.put("/{widget_id}", response_model=WidgetConfig)
async def update_widget(
    widget_id: str = Path(..., description="Widget ID"),
    widget_update: WidgetConfig = Body(...),
) -> WidgetConfig:
    stored = _get_widget_or_404(widget_id)
    widget_update.created_at = stored.created_at
    widget_update.updated_at = datetime.now()
    _WIDGET_STORE[widget_id] = widget_update
    logger.info("Updated widget %s", widget_id)
    return widget_update


@router.delete("/{widget_id}", status_code=204)
async def delete_widget(widget_id: str = Path(..., description="Widget ID")) -> None:
    _get_widget_or_404(widget_id)
    _WIDGET_STORE.pop(widget_id)
    logger.info("Deleted widget %s", widget_id)
    return None
