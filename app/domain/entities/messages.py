from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.events.messages import (
    ChatDeletedEvent,
    ListenerAddedEvent,
    ListenerDeletedEvent,
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from domain.exceptions.messages import (
    ListenerAlreadyDeletedException,
    ListenerAlreadyExistsException,
)
from domain.values.messages import Text, Title


@dataclass(eq=False)
class Message(BaseEntity):
    chat_oid: str
    text: Text


@dataclass(eq=False)
class ChatListener(BaseEntity): ...


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: set[Message] = field(default_factory=set, kw_only=True)
    listeners: set[ChatListener] = field(default_factory=set, kw_only=True)
    is_deleted: bool = field(default=False, kw_only=True)

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(
            NewMessageReceivedEvent(
                message_text=message.text.as_generic_type(),
                chat_oid=self.oid,
                message_oid=message.oid,
            )
        )

    @classmethod
    def create_chat(cls, title: Title) -> "Chat":
        new_chat = cls(title=title)
        new_chat.register_event(
            NewChatCreatedEvent(
                chat_oid=new_chat.oid, chat_title=new_chat.title.as_generic_type()
            )
        )
        return new_chat

    def delete(self):
        self.is_deleted = True
        self.register_event(ChatDeletedEvent(chat_oid=self.oid))

    def add_listener(self, listener: ChatListener):
        if listener in self.listeners:
            raise ListenerAlreadyExistsException(listener.oid)
        self.listeners.add(listener)
        self.register_event(ListenerAddedEvent(listener_oid=listener.oid))

    def delete_listener(self, listener: ChatListener):
        if listener not in self.listeners:
            raise ListenerAlreadyDeletedException(listener_id=listener.oid)
        self.listeners.remove(listener)
        self.register_event(ListenerDeletedEvent(listener_oid=listener.oid))
