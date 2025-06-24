# /server/app/services/websocket_service.py
import json
from datetime import datetime
from fastapi import WebSocket
from app.websocket_manager import WebSocketManager
from app.services.realtime_service import RealTimeService
from app.core.logging import get_logger

logger = get_logger(__name__)


class WebSocketService:
    def __init__(
        self, websocket_manager: WebSocketManager, realtime_service: RealTimeService
    ):
        self.websocket_manager = websocket_manager
        self.realtime_service = realtime_service
        self.command_handlers = {
            "get_stats": self.handle_get_stats,
            "force_broadcast": self.handle_force_broadcast,
        }

    async def handle_message(self, websocket: WebSocket, data: str):
        try:
            message = json.loads(data)
            command = message.get("command")
            if command in self.command_handlers:
                await self.command_handlers[command](websocket)
            else:
                await self.handle_unknown_command(websocket, command)
        except json.JSONDecodeError:
            await self.handle_plain_text(websocket, data)
        except Exception as e:
            await self.handle_error(websocket, e)

    async def handle_get_stats(self, websocket: WebSocket):
        stats = self.realtime_service.get_stats()
        response = {
            "type": "stats_response",
            "data": stats,
            "timestamp": datetime.now().isoformat(),
        }
        await self.websocket_manager.send_personal_message(
            json.dumps(response), websocket
        )

    async def handle_force_broadcast(self, websocket: WebSocket):
        success = await self.realtime_service.force_broadcast()
        response = {
            "type": "broadcast_response",
            "success": success,
            "timestamp": datetime.now().isoformat(),
        }
        await self.websocket_manager.send_personal_message(
            json.dumps(response), websocket
        )

    async def handle_unknown_command(self, websocket: WebSocket, command: str):
        response = {
            "type": "error",
            "message": f"Unknown command: {command}",
            "timestamp": datetime.now().isoformat(),
        }
        await self.websocket_manager.send_personal_message(
            json.dumps(response), websocket
        )

    async def handle_plain_text(self, websocket: WebSocket, data: str):
        logger.info(f"Received plain text message: {data}")
        await self.websocket_manager.send_personal_message(f"Echo: {data}", websocket)

    async def handle_error(self, websocket: WebSocket, error: Exception):
        logger.error(f"Error processing command: {error}")
        response = {
            "type": "error",
            "message": f"Error processing command: {str(error)}",
            "timestamp": datetime.now().isoformat(),
        }
        await self.websocket_manager.send_personal_message(
            json.dumps(response), websocket
        )
