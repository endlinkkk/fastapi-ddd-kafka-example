from functools import lru_cache
from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator
from punq import Container, Scope


def init_mediator(
    container: Container,
    mediator: Mediator,
):
    mediator.register_command(
        CreateChatCommand,
        [
            container.resolve(CreateChatCommandHandler),
        ],
    )


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    container.register(CreateChatCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        mediator.register_command(
            CreateChatCommand,
            [
                container.resolve(CreateChatCommandHandler),
            ],
        )
        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
