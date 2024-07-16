from functools import lru_cache
from infra.repositories.messages.base import BaseMessageRepository
from infra.repositories.messages.memory import BaseChatRepository
from infra.repositories.messages.mongo import (
    MongoDBChatRepository,
    MongoDBMessageRepository,
)
from logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from logic.mediator import Mediator
from punq import Container, Scope
from motor.motor_asyncio import AsyncIOMotorClient

from logic.queries.messages import GetChatDetailQuery, GetChatDetailQueryHandler
from settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    config: Config = container.resolve(Config)

    def create_mongodb_client():
        return AsyncIOMotorClient(
            config.mongodb_connection_uri, serverSelectionTimeoutMS=3000
        )

    container.register(
        AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton
    )

    client = container.resolve(AsyncIOMotorClient)

    def init_chat_mongodb_repository() -> MongoDBChatRepository:

        return MongoDBChatRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    def init_message_mongodb_repository() -> MongoDBMessageRepository:

        return MongoDBMessageRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    container.register(
        BaseChatRepository, factory=init_chat_mongodb_repository, scope=Scope.singleton
    )

    container.register(
        BaseMessageRepository,
        factory=init_message_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(GetChatDetailQueryHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        mediator.register_command(
            CreateChatCommand,
            [
                container.resolve(CreateChatCommandHandler),
            ],
        )

        mediator.register_command(
            CreateMessageCommand,
            [
                container.resolve(CreateMessageCommandHandler),
            ],
        )
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatDetailQueryHandler),
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
