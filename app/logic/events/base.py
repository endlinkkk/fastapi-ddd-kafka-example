from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.events.base import BaseEvent


ET = TypeVar(name="ET", bound=BaseEvent)
ER = TypeVar(name="ER", bound=Any)


@dataclass
class BaseEventHandler(ABC, Generic[ET, ER]):
    @abstractmethod
    def handle(self, event: ET) -> ER: ...
