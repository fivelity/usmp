"""
Real-time sensor data broadcasting service.
Manages periodic sensor data collection and WebSocket broadcasting.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import json
from starlette.websockets import WebSocket
from ..models.websocket import WebSocketMessage

from ..core.config import AppSettings
from ..core.logging import get_logger
from ..websocket_manager import WebSocketManager
from .sensor_manager import SensorManager


class RealTimeService:
    """Service for real-time sensor data broadcasting via WebSocket."""

    def __init__(
        self, sensor_manager: SensorManager, websocket_manager: WebSocketManager
    ):
        self.sensor_manager = sensor_manager
        self.websocket_manager = websocket_manager
        self.logger = get_logger("realtime_service")

        # Configuration
        self.broadcast_interval = 2.0  # seconds
        self.is_running = False
        self.broadcast_task: Optional[asyncio.Task] = None

        # Statistics
        self.broadcasts_sent = 0
        self.last_broadcast_time: Optional[datetime] = None
        self.errors_count = 0

    async def start(self, app_settings: AppSettings) -> None:
        """Start the real-time broadcasting service."""
        if self.is_running:
            self.logger.warning("RealTimeService is already running")
            return

        # Update configuration from settings
        self.broadcast_interval = getattr(
            app_settings, "realtime_broadcast_interval", 2.0
        )

        self.logger.info(
            f"Starting RealTimeService with {self.broadcast_interval}s interval"
        )
        self.is_running = True

        # Start the broadcasting task
        self.broadcast_task = asyncio.create_task(self._broadcast_loop())

        self.logger.info("RealTimeService started successfully")

    async def stop(self) -> None:
        """Stop the real-time broadcasting service."""
        if not self.is_running:
            return

        self.logger.info("Stopping RealTimeService...")
        self.is_running = False

        if self.broadcast_task:
            self.broadcast_task.cancel()
            try:
                await self.broadcast_task
            except asyncio.CancelledError:
                pass
            self.broadcast_task = None

        self.logger.info("RealTimeService stopped")

    async def _broadcast_loop(self) -> None:
        """Main broadcasting loop."""
        self.logger.info("Starting sensor data broadcasting loop")

        while self.is_running:
            try:
                # Check if there are any connected WebSocket clients
                if not self.websocket_manager.active_connections:
                    # No clients connected, wait and continue
                    await asyncio.sleep(self.broadcast_interval)
                    continue

                # Get current sensor data from all sources
                sensor_data = await self.sensor_manager.get_all_sensor_data()

                if sensor_data:
                    # Convert SensorReading objects to dictionaries for JSON serialization
                    serializable_data = {}
                    for source_id, readings in sensor_data.items():
                        serializable_data[source_id] = [
                            reading.model_dump(mode="json")
                            if hasattr(reading, "model_dump")
                            else reading.dict()
                            for reading in readings
                        ]

                    # Prepare the broadcast message
                    broadcast_data = {
                        "sources": serializable_data,
                        "timestamp": datetime.now().isoformat(),
                        "total_sensors": sum(
                            len(readings) for readings in sensor_data.values()
                        ),
                        "active_sources": len(
                            [
                                source
                                for source, readings in sensor_data.items()
                                if readings
                            ]
                        ),
                    }

                    # Broadcast to all connected clients
                    await self.websocket_manager.broadcast_sensor_data(broadcast_data)

                    # Update statistics
                    self.broadcasts_sent += 1
                    self.last_broadcast_time = datetime.now()

                    if (
                        self.broadcasts_sent % 30 == 0
                    ):  # Log every 30 broadcasts (1 minute at 2s interval)
                        self.logger.debug(
                            f"Broadcast #{self.broadcasts_sent}: {broadcast_data['total_sensors']} sensors "
                            f"from {broadcast_data['active_sources']} sources to "
                            f"{len(self.websocket_manager.active_connections)} clients"
                        )
                else:
                    # No sensor data available
                    if self.broadcasts_sent % 15 == 0:  # Log every 15 attempts
                        self.logger.debug("No sensor data available for broadcasting")

            except Exception as e:
                self.errors_count += 1
                self.logger.error(f"Error in broadcast loop: {e}", exc_info=True)

                # If too many errors, increase the interval to avoid spam
                if self.errors_count > 10:
                    self.logger.warning(
                        "Too many broadcast errors, increasing interval"
                    )
                    await asyncio.sleep(self.broadcast_interval * 2)
                    self.errors_count = 0  # Reset error count

            # Wait for the next broadcast interval
            await asyncio.sleep(self.broadcast_interval)

    def get_stats(self) -> Dict[str, Any]:
        """Get real-time service statistics."""
        return {
            "is_running": self.is_running,
            "broadcast_interval": self.broadcast_interval,
            "broadcasts_sent": self.broadcasts_sent,
            "last_broadcast_time": self.last_broadcast_time.isoformat()
            if self.last_broadcast_time
            else None,
            "errors_count": self.errors_count,
            "connected_clients": len(self.websocket_manager.active_connections),
            "active_connections": [
                {
                    "client_id": metadata.get("client_id", "unknown"),
                    "connected_at": metadata.get("connected_at").isoformat()
                    if metadata.get("connected_at")
                    else None,
                    "messages_sent": metadata.get("messages_sent", 0),
                }
                for metadata in self.websocket_manager.connection_metadata.values()
            ],
        }

    async def force_broadcast(self) -> bool:
        """Force an immediate broadcast (for testing/debugging)."""
        try:
            self.logger.info(
                f"[FORCE] Force broadcast starting - connected clients: {len(self.websocket_manager.active_connections)}"
            )

            if not self.websocket_manager.active_connections:
                self.logger.info("No WebSocket clients connected for force broadcast")
                return False

            self.logger.info("Getting sensor data...")
            sensor_data = await self.sensor_manager.get_all_sensor_data()
            self.logger.info(f"   Retrieved data from {len(sensor_data)} sources")

            if sensor_data:
                # Convert SensorReading objects to dictionaries for JSON serialization
                self.logger.info(
                    "Converting sensor data to JSON-serializable format..."
                )
                serializable_data = {}
                for source_id, readings in sensor_data.items():
                    serializable_data[source_id] = [
                        reading.model_dump(mode="json")
                        if hasattr(reading, "model_dump")
                        else reading.dict()
                        for reading in readings
                    ]
                    self.logger.info(
                        f"   Converted {len(readings)} readings from {source_id}"
                    )

                total_sensors = sum(len(readings) for readings in sensor_data.values())
                active_sources = len(
                    [source for source, readings in sensor_data.items() if readings]
                )

                broadcast_data = {
                    "sources": serializable_data,
                    "timestamp": datetime.now().isoformat(),
                    "total_sensors": total_sensors,
                    "active_sources": active_sources,
                    "forced": True,
                }

                self.logger.info(
                    f"Broadcasting {total_sensors} sensors from {active_sources} sources..."
                )
                await self.websocket_manager.broadcast_sensor_data(broadcast_data)
                self.logger.info(f"[OK] Force broadcast completed successfully!")
                return True
            else:
                self.logger.warning("No sensor data available for force broadcast")
                return False

        except Exception as e:
            self.logger.error(f"Error in force broadcast: {e}", exc_info=True)
            return False

    # -------------------------------------------------------------
    # WebSocket helpers
    # -------------------------------------------------------------

    async def handle_incoming_ws_message(
        self, websocket: WebSocket, message_text: str
    ) -> None:
        """Process messages received from a WebSocket client.

        Current implementation supports a minimal protocol:

        {"event": "force_broadcast"}   -> triggers immediate sensor broadcast
        Any other message will be acknowledged back to the sender.
        """
        try:
            payload = json.loads(message_text)
            event = payload.get("event")

            if event == "force_broadcast":
                success = await self.force_broadcast()
                await self.websocket_manager.send_to_client(
                    websocket,
                    WebSocketMessage(
                        event="force_broadcast_ack",
                        data={"success": success},
                    ),
                )
            else:
                # Generic echo/ack for unsupported events
                await self.websocket_manager.send_to_client(
                    websocket,
                    WebSocketMessage(
                        event="ack",
                        data={"received": True, "echo": payload},
                    ),
                )

        except json.JSONDecodeError:
            # Non-JSON message: just echo raw text
            await self.websocket_manager.send_to_client(
                websocket,
                WebSocketMessage(event="ack", data={"received": True}),
            )
        except Exception as e:
            self.logger.error("Error handling WS message: %s", e, exc_info=True)
            await self.websocket_manager.send_to_client(
                websocket,
                WebSocketMessage(
                    event="error",
                    data={"message": "Error processing message"},
                ),
            )
