from datetime import datetime
import pytest

from domain.entities.messages import Chat, Message
from domain.events.messages import NewMessageReceivedEvent
from domain.exceptions.messages import TitleTooLongException
from domain.values.messages import Text, Title
from faker import Faker


def test_create_message_success(faker: Faker):
    text = Text(faker.text(max_nb_chars=254))
    message = Message(text=text)

    assert message.text == text

    assert message.created_at.date() == datetime.today().date()


def test_create_chat_success():
    title = Title("title")
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_title_too_long():
    with pytest.raises(TitleTooLongException):
        title = Title("title" * 200)


def test_add_chat_to_message(faker: Faker):
    text = Text(faker.text(max_nb_chars=254))
    message = Message(text=text)

    title = Title("title")
    chat = Chat(title=title)

    chat.add_message(message=message)

    assert message in chat.messages


def test_new_message_events(faker: Faker):
    text = Text(faker.text(max_nb_chars=254))
    message = Message(text=text)

    title = Title("title")
    chat = Chat(title=title)

    chat.add_message(message=message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not chat.pull_events()
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewMessageReceivedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.message_text == text.as_generic_type()
    assert new_event.chat_oid == chat.oid
