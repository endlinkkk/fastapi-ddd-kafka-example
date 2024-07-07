from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True)
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"Text too long {self.text[:255]}..."


@dataclass(frozen=True)
class EmptyTextException(ApplicationException):

    @property
    def message(self):
        return f"Text is not be empty"
