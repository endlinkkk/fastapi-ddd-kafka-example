from dataclasses import dataclass

from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.messages import BaseChatRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException


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
