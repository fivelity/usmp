# API Documentation (Version 2.0.0)

This document details the API for Ultimate Sensor Monitor Version 2.0.0. This version includes significant enhancements to stability, security, and functionality, with robust Pydantic models on the backend and comprehensive TypeScript types on the frontend.

**Key Changes in v2.0.0 Relevant to API Users/Developers:**
-   **Enhanced Data Models**: Production-ready Pydantic models (`server/app/models/sensor.py`, `widget.py`, `websocket.py`) provide strong type safety and validation for all data exchanged. Frontend TypeScript types (`client/src/lib/types/index.ts`, `sensors.ts`, `widgets.ts`) mirror these structures.
-   **WebSocket Stability & Richness**: Improved WebSocket connection management, error handling, and a wider array of message types for real-time communication. See `server/app/models/websocket.py` for `MessageType` enum and message structures.
-   **Security & Validation**: FastAPI endpoints now perform stricter validation based on Pydantic models. Ensure requests conform to these defined models.
-   **Modular Sensor Backend**: The backend architecture (`server/app/sensors/`) allows for easier integration of new sensor data sources (e.g., `LibreHardwareMonitor`, `HWiNFO`), all feeding into a consistent API structure.

## 1. Backend REST API Endpoints

The backend is a FastAPI application. All endpoints return JSON responses. Pydantic models define request and response structures.

**Base URL**: `http://localhost:8000` (default)

### 1.1. Sensor Data

-   **`GET /api/v1/sensors`**:
-   Description: Retrieves a list of all available sensor sources and their current readings.
-   Response: `List[SensorSource]` (as defined in `server/app/models/sensor.py`). Each `SensorSource` contains a list of `SensorReading` objects.
-   Example: `curl http://localhost:8000/api/v1/sensors`

-   **`GET /api/v1/sensors/{source_id}`**:
-   Description: Retrieves detailed information and current readings for a specific sensor source.
-   Path Parameter: `source_id` (string) - ID of the sensor source.
-   Response: `SensorSource`.
-   Example: `curl http://localhost:8000/api/v1/sensors/librehardwaremonitor`

-   **`GET /api/v1/sensors/{source_id}/{sensor_id_path}`**:
-   Description: Retrieves a specific sensor reading by its full path identifier within a source.
-   Path Parameters:
    -   `source_id` (string)
    -   `sensor_id_path` (string) - e.g., `cpu/0/temperature/0`
-   Response: `SensorReading`.
-   Example: `curl http://localhost:8000/api/v1/sensors/librehardwaremonitor/cpu/0/temperature/0`

### 1.2. Dashboard Configuration (Presets)

-   **`GET /api/v1/presets`**:
-   Description: Lists all saved dashboard presets.
-   Response: `List[DashboardPresetSummary]` (A summary model, likely `id`, `name`, `description`, `updated_at`).
-   Example: `curl http://localhost:8000/api/v1/presets`

-   **`POST /api/v1/presets`**:
-   Description: Saves a new dashboard preset or updates an existing one if an ID is provided and matches.
-   Request Body: `DashboardPreset` (as defined in `server/app/models/widget.py`).
-   Response: `DashboardPreset` (the saved preset, possibly with server-generated `id` and timestamps).
-   Example: `curl -X POST -H "Content-Type: application/json" -d @preset.json http://localhost:8000/api/v1/presets`

-   **`GET /api/v1/presets/{preset_id}`**:
-   Description: Retrieves a specific dashboard preset by its ID.
-   Path Parameter: `preset_id` (string).
-   Response: `DashboardPreset`.
-   Example: `curl http://localhost:8000/api/v1/presets/my_cool_dashboard_v1`

-   **`PUT /api/v1/presets/{preset_id}`**:
-   Description: Updates an existing dashboard preset.
-   Path Parameter: `preset_id` (string).
-   Request Body: `DashboardPreset`.
-   Response: `DashboardPreset` (the updated preset).
-   Example: `curl -X PUT -H "Content-Type: application/json" -d @updated_preset.json http://localhost:8000/api/v1/presets/my_cool_dashboard_v1`

-   **`DELETE /api/v1/presets/{preset_id}`**:
-   Description: Deletes a dashboard preset.
-   Path Parameter: `preset_id` (string).
-   Response: Success/failure message.
-   Example: `curl -X DELETE http://localhost:8000/api/v1/presets/my_cool_dashboard_v1`

### 1.3. Application Configuration / Settings (Hypothetical - if implemented)

-   **`GET /api/v1/settings`**:
-   Description: Retrieves current application settings.
-   Response: A model representing application settings (e.g., polling rates, default theme).

-   **`POST /api/v1/settings`**:
-   Description: Updates application settings.
-   Request Body: Model representing application settings.
-   Response: Updated application settings.

## 2. WebSocket API

The WebSocket API provides real-time updates for sensor data and other system events.

**Endpoint**: `ws://localhost:8000/ws/{client_id}`
-   `client_id`: A unique identifier for the WebSocket client.

All messages are JSON objects adhering to the `WebSocketMessage` base model and specific typed messages defined in `server/app/models/websocket.py` and `client/src/lib/types/sensors.ts` (e.g., `WebSocketSensorMessage`, `SensorDataBatch`).

### Key Message Types (Server to Client):

-   **`MessageType.CONNECTION_ESTABLISHED`**:
-   Payload: `{ "client_id": string, "server_version": string, "message": "Connection successful" }`
-   Sent upon successful WebSocket connection.

-   **`MessageType.SENSOR_DATA` / `MessageType.SENSOR_UPDATE` (often batched as `SensorDataBatch`):**
-   Payload: `SensorDataBatch` (defined in `client/src/lib/types/sensors.ts` and `server/app/models/sensor.py`). Contains a dictionary of `SensorReading` objects, keyed by sensor ID.
-   `SensorDataBatch`: `{ batch_id: string, source_id: string, timestamp: string, sensors: Record<string, SensorReading>, sequence_number: int }`
-   Sent periodically with the latest sensor readings.

-   **`MessageType.SENSOR_SOURCES_UPDATED`**:
-   Payload: `List[SensorSource]`
-   Sent when the list of available sensor sources or their structure changes (e.g., new hardware detected).

-   **`MessageType.HARDWARE_CHANGE`**:
-   Payload: Details about the hardware change (e.g., device added/removed). Structure defined by `HardwareComponent` from `client/src/lib/types/sensors.ts`.
-   Sent when a significant hardware configuration change is detected by a sensor source.

-   **`MessageType.ERROR`**:
-   Payload: `ErrorMessage` (`{ error: string, error_code?: string, details?: any, severity: string }`)
-   Sent when an error occurs on the server related to the WebSocket or data processing.

-   **`MessageType.HEARTBEAT_RESPONSE`**:
-   Payload: `{ timestamp: string, system_status?: any }`
-   Server's response to a client's heartbeat.

### Key Message Types (Client to Server):

-   **`MessageType.CONFIGURE_REALTIME`**:
-   Payload: `RealTimeConfig` (defined in `client/src/lib/types/sensors.ts`)
-   `RealTimeConfig`: `{ polling_rate: number, adaptive_polling: boolean, priority_sensors: string[], ... }`
-   Client requests to change real-time data subscription parameters (e.g., update interval).

-   **`MessageType.HEARTBEAT`**:
-   Payload: `{ timestamp: string }`
-   Client sends periodically to keep the connection alive and indicate activity.

## 3. Data Models Highlights

Refer to the source files for complete definitions:
-   Backend: `server/app/models/sensor.py`, `server/app/models/widget.py`, `server/app/models/websocket.py`
-   Frontend: `client/src/lib/types.ts`, `client/src/lib/types/sensors.ts`, `client/src/lib/types/widgets.ts`

### `SensorReading` (Core Fields):
-   `id`: string (Unique sensor identifier, e.g., `/librehardwaremonitor/nvidiagpu/0/load/0`)
-   `name`: string (Human-readable name, e.g., "GPU Core Load")
-   `value`: number | string
-   `unit`: string (e.g., "°C", "%", "MHz", "V")
-   `category`: `SensorCategory` (enum: "temperature", "load", "clock", etc.)
-   `hardware_type`: `HardwareType` (enum: "cpu", "gpu", "memory", etc.)
-   `source`: string (ID of the source, e.g., "librehardwaremonitor")
-   `timestamp`: string (ISO 8601 datetime)
-   `status`: `SensorStatus` (enum: "active", "inactive", "error")
-   `quality`: `DataQuality` (enum: "excellent", "good", "fair")
-   `min_value`, `max_value`: optional numbers
-   `parent_hardware`: optional string (path to parent hardware component)
-   `metadata`: optional dictionary for additional info.

### `WidgetConfig` (Core Fields):
-   `id`: string (Unique widget ID)
-   `sensor_id`: string (ID of the sensor this widget displays)
-   `gauge_type`: `ExtendedGaugeType` (enum: "text", "radial", "linear", "graph", "image", "glassmorphic", "system_status")
-   `pos_x`, `pos_y`, `width`, `height`, `rotation`, `z_index`: number (Layout properties)
-   `is_locked`, `is_visible`: boolean
-   `gauge_settings`: object (Specific settings for the chosen `gauge_type`. See `SystemStatusConfig` in `client/src/lib/types/widgets.ts` for an example of extended settings.)
-   `style_settings`: object (General styling: background, border, font, etc.)
-   `animation_settings`: object (Animation configurations)

### `DashboardPreset` (Core Fields):
-   `id`: optional string
-   `name`: string
-   `description`: optional string
-   `widgets`: `List[WidgetConfig]`
-   `widget_groups`: `List[WidgetGroup]`
-   `layout`: `DashboardLayout` (canvas size, background, grid settings)
-   `visual_settings`: `VisualSettings` (theme, fonts, effects)
-   `version`: string (e.g., "2.0")

## 4. Custom Widget API (Frontend)

While not a backend HTTP/WebSocket API, the frontend has an internal API for registering and using custom widgets.

### Widget Registration (`client/src/lib/components/widgets/index.ts`):
Custom widgets are registered in the `widgetTypes` object. Each entry defines:
-   `id`: Unique string identifier for the widget type.
-   `name`: Display name.
-   `description`: Brief description.
-   `category`: Grouping category.
-   `component`: The Svelte component for rendering the widget.
-   `inspector`: The Svelte component for the widget's settings panel in the `WidgetInspector`.
-   `defaultConfig`: Default configuration object for new instances of this widget.
-   `icon`: Emoji or SVG icon.

Example:
\`\`\`typescript
// client/src/lib/components/widgets/index.ts
import MyCustomWidget from './MyCustomWidget.svelte';
import MyCustomWidgetInspector from './MyCustomWidgetInspector.svelte';

export const widgetTypes: Record<ExtendedGaugeType, WidgetTypeDefinition> = {
// ... other widgets
"my_custom_widget": {
id: "my_custom_widget",
name: "My Custom Widget",
description: "A very special custom widget.",
category: "custom",
component: MyCustomWidget,
inspector: MyCustomWidgetInspector,
defaultConfig: { /* ... initial settings ... */ },
icon: "🌟",
}
};
\`\`\`

### Widget Component Interface (`WidgetComponentProps`):
-   `widget: WidgetConfig`: The current configuration of the widget instance.
-   `isSelected: boolean`: Whether the widget is currently selected.
-   `onUpdate?: (updates: Partial<WidgetConfig>) => void`: Callback to update the widget's configuration.

### Widget Inspector Interface (`WidgetInspectorProps`):
-   `widget: WidgetConfig`: The current configuration of the widget being inspected.
-   `updateWidget: (updates: Partial<WidgetConfig>) => void`: Function to apply updates to the widget's configuration.

### System Status Widget API (`SystemStatusConfig` and `SystemMetric`):
Defined in `client/src/lib/types/widgets.ts`.
-   `SystemStatusConfig`:
-   `layout`: "compact" | "detailed" | "minimal"
-   `columns`: number (1-4)
-   `metrics`: `SystemMetric[]`
-   `show_icons`, `show_labels`, `show_values`, `show_units`: boolean
-   `use_status_colors`: boolean
-   `warning_threshold`, `critical_threshold`: number (0-100, global for metrics without own)
-   `animate_changes`: boolean
-   `update_animation`: "fade" | "slide" | "pulse" | "none"
-   `SystemMetric`:
-   `id`: string
-   `sensor_id`: string
-   `label`: string
-   `icon?`: string (emoji)
-   `unit?`: string
-   `format?`: "number" | "percentage" | "temperature" | "frequency" | "bytes"
-   `warning_threshold?`, `critical_threshold?`: number (override global)

This API documentation should provide a solid foundation for interacting with and extending the Ultimate Sensor Monitor v2.0.0.
