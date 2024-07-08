from faker import Faker
import pytest
import pytest_asyncio
from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.messages import BaseChatRepository
from logic.commands.messages import CreateChatCommand
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker,
):
    chat: Chat = (
        await mediator.handle_command(
            CreateChatCommand(title=faker.text(max_nb_chars=10))
        )
    )[0]

    assert await (chat_repository.check_chat_exists_by_title(
        title=chat.title.as_generic_type()
    ))


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker,
):
    fake_title = faker.text(max_nb_chars=10)

    chat = Chat(title=Title(fake_title))
    await chat_repository.add_chat(chat)

    with pytest.raises(ChatWithThatTitleAlreadyExistsException):
        
        chat: Chat = (
            await mediator.handle_command(
                CreateChatCommand(title=fake_title)
            )
        )[0]

    assert len(chat_repository._saved_chats) == 1

