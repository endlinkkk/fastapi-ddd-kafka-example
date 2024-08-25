from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass()
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"Text too long {self.text[:255]}..."


@dataclass()
class EmptyTextException(ApplicationException):
    @property
    def message(self):
        return "Text is not be empty"


@dataclass
class ListenerAlreadyExistsException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"Listener already exists {self.text}"
