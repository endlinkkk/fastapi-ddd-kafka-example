from uuid import UUID
from fastapi import Depends, WebSocket
from fastapi.routing import APIRouter
from punq import Container

from application.api.messages.decorators import handle_exceptions
from infra.message_brokers.base import BaseMessageBroker
from logic.init import init_container
from settings.config import Config


router = APIRouter(tags=['chats'])

@router.websocket('/{chat_oid}')
@handle_exceptions
async def messages_handlers(
    chat_oid: UUID, 
    websocket: WebSocket,
    container: Container = Depends(init_container)
    ):
    await websocket.accept()

    config: Config = container.resolve(Config)

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)


    async for consumed_message in  message_broker.start_consuming(
        topic=config.new_message_received_topic):
        await websocket.send_json(consumed_message)
    
    message_broker.stop_consuming()
    websocket.close()