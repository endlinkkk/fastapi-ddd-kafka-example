from faker import Faker
import pytest
import pytest_asyncio
from domain.entities.messages import Chat
from infra.repositories.messages import BaseChatRepository
from logic.commands.messages import CreateChatCommand
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
        chat_repository: BaseChatRepository,
        mediator: Mediator,
):
    chat: Chat = (await mediator.handle_command(CreateChatCommand(title=Faker().text(max_nb_chars=10))))[0]
    print(chat)
    assert chat_repository.check_chat_exists_by_title(title=chat.title.as_generic_type())
