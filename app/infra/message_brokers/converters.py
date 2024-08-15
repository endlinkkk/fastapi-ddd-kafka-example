from domain.events.base import BaseEvent
import orjson


def convert_event_to_broker_message(event: BaseEvent) -> bytes:
    return orjson.dumps(event)
