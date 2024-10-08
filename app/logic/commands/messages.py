from dataclasses import dataclass

from domain.entities.messages import Chat, ChatListener, Message
from domain.values.messages import Text, Title
from infra.repositories.messages.base import BaseMessagesRepository
from infra.repositories.messages.memory import BaseChatsRepository
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
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chats_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)
        chat = Chat.create_chat(title=title)

        await self.chats_repository.add_chat(chat)

        await self._mediator.publish(chat.pull_events())

        return chat


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass(frozen=True)
class CreateMessageCommandHandler(BaseCommandHandler[CreateMessageCommand, Message]):
    chats_repository: BaseChatsRepository
    message_repository: BaseMessagesRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat = await self.chats_repository.get_chat_by_oid(oid=command.chat_oid)
        if not chat:
            raise ChatNotFoundException(chat_oid=command.chat_oid)

        message = Message(text=Text(value=command.text), chat_oid=command.chat_oid)
        chat.add_message(message)
        await self.message_repository.add_message(message=message)

        await self._mediator.publish(chat.pull_events())

        return message


@dataclass(frozen=True)
class DeleteChatCommand(BaseCommand):
    chat_oid: str


@dataclass(frozen=True)
class DeleteChatCommandHandler(BaseCommandHandler[DeleteChatCommand, None]):
    chats_repository: BaseChatsRepository

    async def handle(self, command: DeleteChatCommand) -> None:
        chat = await self.chats_repository.get_chat_by_oid(oid=command.chat_oid)
        if not chat:
            raise ChatNotFoundException(chat_oid=command.chat_oid)

        await self.chats_repository.delete_chat_by_oid(oid=command.chat_oid)
        chat.delete()
        await self._mediator.publish(chat.pull_events())


@dataclass(frozen=True)
class AddTelegramListenerCommand(BaseCommand):
    chat_oid: str
    telegram_chat_id: str


@dataclass(frozen=True)
class AddTelegramListenerCommandHandler(
    BaseCommandHandler[AddTelegramListenerCommand, ChatListener]
):
    chats_repository: BaseChatsRepository

    async def handle(self, command: AddTelegramListenerCommand) -> None:
        chat = await self.chats_repository.get_chat_by_oid(oid=command.chat_oid)
        if not chat:
            raise ChatNotFoundException(chat_oid=command.chat_oid)

        listener = ChatListener(oid=command.telegram_chat_id)
        chat.add_listener(listener)
        await self.chats_repository.add_telegram_listener(
            chat_oid=command.chat_oid, telegram_chat_id=command.telegram_chat_id
        )

        await self._mediator.publish(chat.pull_events())
        return listener


@dataclass(frozen=True)
class DeleteTelegramListenerCommand(BaseCommand):
    chat_oid: str
    telegram_chat_id: str


@dataclass(frozen=True)
class DeleteChatListenerCommandHandler(
    BaseCommandHandler[DeleteTelegramListenerCommand, None]
):
    chats_repository: BaseChatsRepository

    async def handle(self, command: DeleteTelegramListenerCommand) -> None:
        chat = await self.chats_repository.get_chat_by_oid(oid=command.chat_oid)
        if not chat:
            raise ChatNotFoundException(chat_oid=command.chat_oid)

        listener = ChatListener(oid=command.telegram_chat_id)
        chat.delete_listener(listener)

        await self.chats_repository.delete_telegram_listener(
            chat_oid=command.chat_oid, telegram_chat_id=command.telegram_chat_id
        )
        await self._mediator.publish(chat.pull_events())
