from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from domain.values.messages import Text, Title
from infra.repositories.messages.base import BaseMessageRepository
from infra.repositories.messages.memory import BaseChatRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.messages import (
    ChatNotFoundException,
    ChatWithThatTitleAlreadyExistsException,
)


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(BaseCommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)
        chat = Chat.create_chat(title=title)

        await self.chat_repository.add_chat(chat)

        return chat


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass(frozen=True)
class CreateMessageCommandHandler(BaseCommandHandler[CreateMessageCommand, Message]):
    chat_repository: BaseChatRepository
    message_repository: BaseMessageRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat = await self.chat_repository.get_chat_by_oid(oid=command.chat_oid)
        if not chat:
            raise ChatNotFoundException(chat_oid=command.chat_oid)

        message = Message(text=Text(value=command.text))
        chat.add_message(message)
        await self.message_repository.add_message(
            chat_oid=command.chat_oid, message=message
        )

        return message
