"""Integration tests for REST API endpoints using AsyncClient.

These tests rely on the in-memory stores defined in the endpoint modules.
They do not require hardware sensors; the SensorManager is started via
FastAPI lifespan but its async initialization is mocked implicitly by
the default configuration (it falls back to mock sensors when no
hardware is available).
"""

# pylint: disable=redefined-outer-name
import json
import pytest
from httpx import AsyncClient

from datetime import datetime

from app.models.sensor import SensorReading

pytestmark = pytest.mark.anyio  # Enable async tests with anyio/pytest-asyncio


async def test_health_check(async_client: AsyncClient):
    resp = await async_client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"


async def test_preset_crud(async_client: AsyncClient):
    # Create preset
    payload = {
        "name": "Test Preset",
        "widgets": [],
        "widget_groups": [],
    }
    resp = await async_client.post("/api/v1/presets/", json=payload)
    assert resp.status_code == 201
    created = resp.json()
    preset_id = created["id"]

    # List presets
    resp = await async_client.get("/api/v1/presets/")
    assert resp.status_code == 200
    presets = resp.json()
    assert any(p["id"] == preset_id for p in presets)

    # Retrieve preset
    resp = await async_client.get(f"/api/v1/presets/{preset_id}")
    assert resp.status_code == 200
    retrieved = resp.json()
    assert retrieved["name"] == "Test Preset"

    # Delete preset
    resp = await async_client.delete(f"/api/v1/presets/{preset_id}")
    assert resp.status_code == 204

    # Ensure deletion
    resp = await async_client.get(f"/api/v1/presets/{preset_id}")
    assert resp.status_code == 404


async def test_widget_crud(async_client: AsyncClient):
    # Create widget
    payload = {
        "id": "widget-test-1",
        "sensor_id": "cpu_temp",
        "gauge_type": "text",
    }
    resp = await async_client.post("/api/v1/widgets/", json=payload)
    assert resp.status_code == 201
    created = resp.json()
    widget_id = created["id"]

    # List widgets
    resp = await async_client.get("/api/v1/widgets/")
    assert resp.status_code == 200
    widgets = resp.json()
    assert any(w["id"] == widget_id for w in widgets)

    # Retrieve widget
    resp = await async_client.get(f"/api/v1/widgets/{widget_id}")
    assert resp.status_code == 200
    retrieved = resp.json()
    assert retrieved["sensor_id"] == "cpu_temp"

    # Delete widget
    resp = await async_client.delete(f"/api/v1/widgets/{widget_id}")
    assert resp.status_code == 204

    # Ensure deletion
    resp = await async_client.get(f"/api/v1/widgets/{widget_id}")
    assert resp.status_code == 404


async def test_websocket_connect(async_client: AsyncClient):
    """Ensure WebSocket connects and closes cleanly."""
    async with async_client.websocket_connect("/ws") as ws:
        # Immediately close connection; server should handle gracefully
        await ws.close()


# ---------------------------------------------------------------------------
# Sensor endpoints & broadcast verification
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_sensor_data():
    """Create deterministic mock sensor data for tests."""
    now = datetime.utcnow()
    reading = SensorReading(
        sensor_id="cpu_temp",
        source_id="mock_source",
        value=42.0,
        unit="°C",
        timestamp=now,
        category="temperature",
        hardware_type="cpu",
        quality="good",
    )
    return {"mock_source": [reading]}


async def test_sensor_routes_and_broadcast(
    async_client: AsyncClient, sample_sensor_data, monkeypatch
):
    """Patch SensorManager to return mock data, exercise endpoints and broadcast."""

    sensor_manager = async_client.app.state.sensor_manager  # type: ignore

    # Patch async methods to return sample data
    async def _mock_get_all_sensor_data():
        return sample_sensor_data

    async def _mock_get_sensor_definitions():
        # Derive basic definition from reading
        return []

    def _mock_get_available_sources():
        return [
            {"source_id": "mock_source", "available": True},
        ]

    monkeypatch.setattr(sensor_manager, "get_all_sensor_data", _mock_get_all_sensor_data)
    monkeypatch.setattr(sensor_manager, "get_sensor_definitions", _mock_get_sensor_definitions)
    monkeypatch.setattr(sensor_manager, "get_available_sources", _mock_get_available_sources)

    # ---- Sensor HTTP endpoints ----

    # /sensors/data/all
    resp = await async_client.get("/api/v1/sensors/data/all")
    assert resp.status_code == 200
    assert resp.json() == {
        "mock_source": [reading.model_dump(mode="json") for reading in sample_sensor_data["mock_source"]]
    }

    # /sensors/status
    resp = await async_client.get("/api/v1/sensors/status")
    assert resp.status_code == 200
    status_payload = resp.json()
    assert status_payload[0]["source_id"] == "mock_source"

    # ---- WebSocket broadcast verification ----
    async with async_client.websocket_connect("/ws") as ws:
        # Trigger force broadcast
        await ws.send_text(json.dumps({"event": "force_broadcast"}))

        # Collect two messages: ack and sensor_data
        received = [json.loads(await ws.receive_text()) for _ in range(2)]

        ack = next(msg for msg in received if msg.get("event") == "force_broadcast_ack")
        assert ack["data"]["success"] is True

        sensor_msg = next(msg for msg in received if msg.get("type") == "sensor_data")
        assert sensor_msg["data"]["mock_source"][0]["sensor_id"] == "cpu_temp"
