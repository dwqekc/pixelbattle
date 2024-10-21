from fastapi import WebSocket

class ConnectionManager:

    @classmethod
    async def connect(cls,websocket: WebSocket):
        await websocket.accept()

    @classmethod
    async def disconnect(cls,websocket:WebSocket):
        await websocket.close()

    @classmethod
    async def send_message(cls, message:dict, websocket: WebSocket):
        await websocket.send_json(message)