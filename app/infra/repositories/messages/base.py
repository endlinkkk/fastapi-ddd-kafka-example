from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.messages import Chat, Message
from infra.repositories.filters.messages import GetMessagesFilters


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    async def get_chat_by_oid(self, oid: str) -> Chat | None: ...

    @abstractmethod
    async def add_chat(self, chat: Chat): ...


@dataclass
class BaseMessageRepository(ABC):
    @abstractmethod
    async def add_message(self, chat_oid: str, message: Message) -> None: ...


    @abstractmethod
    async def get_messages(self, chat_oid: str, filters: GetMessagesFilters) -> tuple[Iterable[Message], int]: ...