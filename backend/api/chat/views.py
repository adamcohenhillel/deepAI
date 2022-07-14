"""Deeper 2022, All Rights Reserved
"""
from fastapi import APIRouter, WebSocket

chat_router = APIRouter()


@chat_router.websocket('/ws')
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")