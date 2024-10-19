from fastapi import WebSocket

class ConnectionManager:
    active_connections: list[WebSocket] = []

    @classmethod
    async def preconnect(cls,websocket: WebSocket):
        await websocket.accept()

    @classmethod
    async def predisconnect(cls,websocket:WebSocket):
        await websocket.close()

    @classmethod
    async def connect(cls, websocket: WebSocket):
        cls.active_connections.append(websocket)

    @classmethod
    def disconnect(cls, websocket: WebSocket):
        cls.active_connections.remove(websocket)

    @classmethod
    async def send_personal_message(cls, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    @classmethod
    async def broadcast(cls, message: dict):
        for connection in cls.active_connections:
            await connection.send_json(message)