from faker import Faker
import pytest
from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.messages.memory import BaseChatsRepository
from logic.commands.messages import CreateChatCommand
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException
from logic.mediator.base import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chats_repository: BaseChatsRepository,
    mediator: Mediator,
    faker: Faker,
):
    chat: Chat = (
        await mediator.handle_command(
            CreateChatCommand(title=faker.text(max_nb_chars=10))
        )
    )[0]

    assert await chats_repository.check_chat_exists_by_title(
        title=chat.title.as_generic_type()
    )


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
    chats_repository,
    mediator,
    faker: Faker,
):
    fake_title = faker.text(max_nb_chars=10)

    chat = Chat(title=Title(fake_title))
    await chats_repository.add_chat(chat)

    with pytest.raises(ChatWithThatTitleAlreadyExistsException):
        chat: Chat = (
            await mediator.handle_command(CreateChatCommand(title=fake_title))
        )[0]

    assert len(chats_repository._saved_chats) == 1
