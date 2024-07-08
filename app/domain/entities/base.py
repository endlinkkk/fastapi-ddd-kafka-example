from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.events.base import BaseEvent


@dataclass(eq=False)
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    _events: list[BaseEvent] = field(default_factory=list, kw_only=True)

    def pull_events(self) -> list[BaseEvent]:
        registered_events = copy(self._events)
        self._events.clear()

        return registered_events

    def register_event(self, event: BaseEvent):
        self._events.append(event)

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, value: "BaseEntity") -> bool:
        return self.oid == value.oid
