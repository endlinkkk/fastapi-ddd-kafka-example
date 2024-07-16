from dataclasses import dataclass
from typing import Generic

from domain.entities.messages import Chat
from infra.repositories.messages.base import BaseChatRepository, BaseMessageRepository
from logic.exceptions.messages import ChatNotFoundException
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler, Generic[QR, QT]):
    chats_repository: BaseChatRepository
    messages_repository: BaseMessageRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chats_repository.get_chat_by_oid(oid=query.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        return chat
