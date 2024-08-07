from punq import Container

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from application.api.messages.decorators import handle_exceptions
from application.api.messages.filters import GetMessagesFilterss
from application.api.messages.schemas import (
    ChatDetailSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageResponseSchema,
    CreateMessageSchema,
    GetMessagesQueryResponseSchema,
    MessageDetailSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand, CreateMessageCommand
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.messages import GetChatDetailQuery, GetMessagesQuery, GetMessagesQueryHandler

router = APIRouter(
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Create new uniq chat",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
@handle_exceptions
async def create_chat_handler(
    schema: CreateChatRequestSchema, container: Container = Depends(init_container)
) -> CreateChatResponseSchema:
    """Create new chat"""
    mediator: Mediator = container.resolve(Mediator)

    chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))

    return CreateChatResponseSchema.from_entity(chat=chat)


@router.post(
    "/{chat_oid}/messages",
    status_code=status.HTTP_201_CREATED,
    description="Create new message",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
@handle_exceptions
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageSchema,
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    """Create new message"""
    mediator: Mediator = container.resolve(Mediator)

    message, *_ = await mediator.handle_command(
        CreateMessageCommand(text=schema.text, chat_oid=chat_oid)
    )

    return CreateMessageResponseSchema.from_entity(message=message)


@router.get(
    "/{chat_oid}",
    status_code=status.HTTP_200_OK,
    description="Get chat detail by chat_oid",
    responses={
        status.HTTP_200_OK: {"model": ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
@handle_exceptions
async def get_chat_detail_handler(
    chat_oid: str, container: Container = Depends(init_container)
) -> ChatDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    chat = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))

    return ChatDetailSchema.from_entity(chat)


@router.get(
    "/{chat_oid}/messages",
    status_code=status.HTTP_200_OK,
    description="Get all messages by chat_oid",
    responses={
        status.HTTP_200_OK: {"model": GetMessagesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
@handle_exceptions
async def get_chat_messages_handler(
    chat_oid: str, 
    filters: GetMessagesFilterss = Depends(),
    container: Container = Depends(init_container)
) -> GetMessagesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    messages, count = await mediator.handle_query(GetMessagesQuery(chat_oid=chat_oid, filters=filters.to_infra()))

    return GetMessagesQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[MessageDetailSchema.from_entity(message) for message in messages],
    )
