"""Deeper 2022, All Rights Reserved
"""
import asyncio
import logging

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    HTTPException
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis.client import PubSub

from db.models.rooms import Room, RoomMessage


rooms_router = APIRouter()


@rooms_router.websocket('/{room_uuid}')
async def room_websocket(
    room_uuid: int,
    websocket: WebSocket,
    ) -> None:
    """Websocket API endpoint to connect a chat room

    :param room_uuid: 
    :param websocket: 
    """
    await websocket.accept()
    # TODO: Add user <-> Room validation!
    session: AsyncSession = websocket.app.state.db_session_factory()
    query = await session.execute(select(Room).where(Room.id==room_uuid))
    room: Room = query.scalars().first()
    if not room:
        raise HTTPException(status_code=404, detail='Room Not Found')

    # TODO: Add pagination, should we move this to a http endpoint?
    for room_message in room.messages:
        await websocket.send_text(room_message.message)

    _, pending = await asyncio.wait(
        [_consumer(websocket, room, 1, session),
        _producer(websocket, room)],
        return_when=asyncio.FIRST_COMPLETED,
    )
    # for task in pending:
    #     task.cancel()


async def _consumer(
    websocket: WebSocket,
    room: Room,
    user_id: int,
    session: AsyncSession
) -> None:
    """Coroutine to handle incoming data coming from the websocket

    This function is waiting for messages coming from the
    websocket (the user) and then when received, add it to the
    sql database and publish it to the redis channel (the "room")

    :param websocket: Websocket object of the
    :param room:
    :param user_id:
    :param session:
    """
    try:
        redis = websocket.app.state.redis
        while True:
            websocket_text = await websocket.receive_text()
            if websocket_text:
                new_room_message = RoomMessage(text=websocket_text, user_id=user_id)
                room.messages.append(new_room_message)
                session.add(room)
                await session.commit()
                await redis.publish(room.channel, new_room_message.message)
    except WebSocketDisconnect as exc:
        logging.error(exc)


async def _producer(websocket: WebSocket, room: Room) -> None:
    """Coroutine to handle incoming messages from the room's channel
    
    This function subscribe to a redis channel and wait for a message 
    from it, and then when received, pass it back to the websocket

    :param websocket:
    :param room:
    """
    pubsub: PubSub = websocket.app.state.redis.pubsub()
    await pubsub.subscribe(room.channel)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await websocket.send_text(message.get('data'))
    except Exception as e:
        logging.error(e)
