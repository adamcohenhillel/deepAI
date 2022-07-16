"""Deeper 2022, All Rights Reserved
"""
import asyncio
import logging

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Depends
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis.client import PubSub

from db.session import get_db_session
from db.models.rooms import Room


rooms_router = APIRouter()


@rooms_router.websocket('/{room_uuid}')
async def room_websocket(
    room_uuid: int,
    websocket: WebSocket,
    ) -> None:
    """
    """
    await websocket.accept()
    # TODO: Add user <-> Room validation!
    session: AsyncSession = websocket.app.state.db_session_factory()
    with session.begin():
        query = await session.execute(select(Room).where(Room.id==room_uuid))
        room: Room = query.scalars().first()
        messages = room.messages
        print('**************')
        print(messages)
        print('**************')

    _, pending = await asyncio.wait(
        [_consumer(websocket, room_uuid), _producer(websocket, room_uuid)],
        return_when=asyncio.FIRST_COMPLETED,
    )
    [task.cancel() for task in pending]


async def _consumer(websocket: WebSocket, room_uuid: str) -> None:
    """
    """
    try:
        redis = websocket.app.state.redis
        while True:
            message = await websocket.receive_text()
            if message:
                await redis.publish(room_uuid, message)
    except WebSocketDisconnect as exc:
        logging.error(exc)


async def _producer(websocket: WebSocket, room_uuid: str) -> None:
    """
    """
    pubsub: PubSub = websocket.app.state.redis.pubsub()
    await pubsub.subscribe(room_uuid)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await websocket.send_text(message.get('data'))
    except Exception as e:
        logging.error(e)
