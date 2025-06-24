"""
Widget and dashboard models for the frontend.
Production-ready models for widget configuration and dashboard layouts.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum


class GaugeType(str, Enum):
    """Widget gauge type enumeration."""

    TEXT = "text"
    RADIAL = "radial"
    LINEAR = "linear"
    GRAPH = "graph"
    IMAGE = "image"
    GLASSMORPHIC = "glassmorphic"
    SYSTEM_STATUS = "system_status"


class WidgetConfig(BaseModel):
    """Widget configuration model."""

    # Identity
    id: str = Field(..., description="Unique widget identifier")
    sensor_id: str = Field(..., description="Associated sensor ID")
    gauge_type: GaugeType = Field(GaugeType.TEXT, description="Widget gauge type")

    # Position and dimensions
    pos_x: float = Field(0, description="X position on canvas")
    pos_y: float = Field(0, description="Y position on canvas")
    width: float = Field(200, gt=0, description="Widget width")
    height: float = Field(100, gt=0, description="Widget height")
    rotation: float = Field(
        0, ge=-360, le=360, description="Widget rotation in degrees"
    )
    z_index: int = Field(0, description="Z-index for layering")

    # Behavior
    is_locked: bool = Field(False, description="Whether widget is locked from editing")
    is_visible: bool = Field(True, description="Whether widget is visible")
    group_id: Optional[str] = Field(
        None, description="Group ID if widget belongs to a group"
    )

    # Display options
    show_label: bool = Field(True, description="Whether to show sensor label")
    custom_label: Optional[str] = Field(None, description="Custom label text")
    show_unit: bool = Field(True, description="Whether to show unit")
    custom_unit: Optional[str] = Field(None, description="Custom unit text")
    show_value: bool = Field(True, description="Whether to show sensor value")

    # Gauge-specific settings
    gauge_settings: Dict[str, Any] = Field(
        default_factory=dict, description="Gauge-specific configuration"
    )

    # Visual styling
    style_settings: Dict[str, Any] = Field(
        default_factory=dict, description="Widget styling options"
    )

    # Animation settings
    animation_settings: Dict[str, Any] = Field(
        default_factory=dict, description="Animation configuration"
    )

    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )
    version: str = Field("1.0", description="Widget configuration version")

    @validator("width", "height")
    def validate_dimensions(cls, v):
        """Validate widget dimensions are positive."""
        if v <= 0:
            raise ValueError("Widget dimensions must be positive")
        return v

    @validator("gauge_settings", "style_settings", "animation_settings")
    def validate_settings_dict(cls, v):
        """Ensure settings are dictionaries."""
        if not isinstance(v, dict):
            return {}
        return v

    class Config:
        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class WidgetGroup(BaseModel):
    """Widget group model for organizing related widgets."""

    # Identity
    id: str = Field(..., description="Unique group identifier")
    name: str = Field(..., description="Group name")
    description: Optional[str] = Field(None, description="Group description")

    # Group contents
    widget_ids: List[str] = Field(
        default_factory=list, description="List of widget IDs in group"
    )

    # Group positioning
    relative_positions: Dict[str, Dict[str, float]] = Field(
        default_factory=dict, description="Relative positions of widgets within group"
    )

    # Group properties
    is_locked: bool = Field(False, description="Whether group is locked")
    is_visible: bool = Field(True, description="Whether group is visible")
    color: Optional[str] = Field(None, description="Group color identifier")
    icon: Optional[str] = Field(None, description="Group icon")

    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    @validator("name")
    def validate_name_not_empty(cls, v):
        """Validate group name is not empty."""
        if not v or not v.strip():
            raise ValueError("Group name cannot be empty")
        return v.strip()

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class DashboardLayout(BaseModel):
    """Dashboard layout configuration."""

    # Canvas dimensions
    canvas_width: int = Field(1920, gt=0, description="Canvas width in pixels")
    canvas_height: int = Field(1080, gt=0, description="Canvas height in pixels")

    # Background configuration
    background_type: str = Field("solid", description="Background type")
    background_settings: Dict[str, Any] = Field(
        default_factory=dict, description="Background configuration"
    )

    # Grid configuration
    grid_settings: Dict[str, Any] = Field(
        default_factory=lambda: {
            "size": 10,
            "visible": False,
            "snap": True,
            "color": "#e2e8f0",
        },
        description="Grid configuration",
    )

    # Layout metadata
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    @validator("canvas_width", "canvas_height")
    def validate_canvas_dimensions(cls, v):
        """Validate canvas dimensions are positive."""
        if v <= 0:
            raise ValueError("Canvas dimensions must be positive")
        return v

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class VisualSettings(BaseModel):
    """Global visual environment settings."""

    # Core visual dimensions (0-1 range)
    materiality: float = Field(0.5, ge=0, le=1, description="Materiality/depth level")
    information_density: float = Field(
        0.5, ge=0, le=1, description="Information density"
    )
    animation_level: float = Field(0.5, ge=0, le=1, description="Animation intensity")

    # Color scheme
    color_scheme: str = Field("dark", description="Selected color scheme")
    custom_colors: Dict[str, str] = Field(
        default_factory=dict, description="Custom color overrides"
    )

    # Typography
    font_family: str = Field(
        "Inter, system-ui, sans-serif", description="Primary font family"
    )
    font_scale: float = Field(
        1.0, ge=0.5, le=2.0, description="Font size scaling factor"
    )

    # Effects
    enable_blur_effects: bool = Field(True, description="Enable backdrop blur effects")
    enable_animations: bool = Field(True, description="Enable CSS animations")
    enable_shadows: bool = Field(True, description="Enable shadow effects")
    enable_gradients: bool = Field(True, description="Enable gradient effects")
    reduce_motion: bool = Field(False, description="Reduce motion for accessibility")

    # Grid and layout
    grid_size: int = Field(10, ge=1, le=50, description="Grid size in pixels")
    snap_to_grid: bool = Field(True, description="Enable grid snapping")
    show_grid: bool = Field(False, description="Show grid in edit mode")

    # Border radius
    border_radius: int = Field(8, ge=0, le=50, description="Default border radius")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class DashboardPreset(BaseModel):
    """Complete dashboard preset model."""

    # Identity
    id: Optional[str] = Field(None, description="Unique preset identifier")
    name: str = Field(..., description="Preset name")
    description: Optional[str] = Field(None, description="Preset description")

    # Dashboard content
    widgets: List[WidgetConfig] = Field(
        default_factory=list, description="Widget configurations"
    )
    widget_groups: List[WidgetGroup] = Field(
        default_factory=list, description="Widget group definitions"
    )

    # Layout and visual configuration
    layout: DashboardLayout = Field(
        default_factory=DashboardLayout, description="Layout settings"
    )
    visual_settings: VisualSettings = Field(
        default_factory=VisualSettings, description="Visual settings"
    )

    # Metadata
    author: Optional[str] = Field(None, description="Preset author")
    tags: List[str] = Field(default_factory=list, description="Preset tags")
    version: str = Field("2.0", description="Preset format version")

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    # Preview
    preview_image: Optional[str] = Field(
        None, description="Base64 encoded preview image"
    )

    @validator("name")
    def validate_name_not_empty(cls, v):
        """Validate preset name is not empty."""
        if not v or not v.strip():
            raise ValueError("Preset name cannot be empty")
        return v.strip()

    @validator("widgets")
    def validate_unique_widget_ids(cls, v):
        """Validate widget IDs are unique."""
        widget_ids = [widget.id for widget in v]
        if len(widget_ids) != len(set(widget_ids)):
            raise ValueError("Widget IDs must be unique within a preset")
        return v

    class Config:
        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat()}
