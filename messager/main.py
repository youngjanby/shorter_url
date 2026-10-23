from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for ws in self.active_connections:
            await ws.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def ws_endpoint(webSocket: WebSocket):
    await manager.connect(webSocket)

    try:
        while True:
            data = await webSocket.receive_text()

            await manager.broadcast(f"Аноним: {data}")

    except Exception:
        manager.disconnect(webSocket)