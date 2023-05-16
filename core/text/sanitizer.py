from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
import re
from config import settings
from config.utils import create_instance


__all__ = ["clean_string"]


class Sanitizer(ABC):
    """
    Default chain behaviour can be implemented inside a base handler class
    """

    @abstractmethod
    def set_next(self, cleaner: Sanitizer) -> Sanitizer:
        pass

    @abstractmethod
    def clean(self, text: str) -> str | None:
        pass


class AbstractTextSanitizer(Sanitizer):
    def __init__(self) -> None:
        self.next: Sanitizer = None

    def set_next(self, cleaner: Sanitizer) -> Sanitizer:
        """_summary_

        Args:
            cleaner (Sanitizer): concrete Sanitizer

        Returns:
            Sanitizer: _description_
        """
        self.next = cleaner

    def clean(self, text: str) -> str | None:
        if self.next is not None:
            return self.next.clean(text)
        return text


class TrimHandler(AbstractTextSanitizer):
    """
    Chain link which is resposible for trim tokkens with spaces
    """

    def clean(self, text: str):
        if text is not None:
            text = " ".join(text.split())
        return super().clean(text)


class WhiteSpaceHandler(AbstractTextSanitizer):
    """
    Chsin link which replace all whitespaces with single space
    """

    def clean(self, text: str) -> str | None:
        if text is not None:
            pattern = r"[\f\n\r\t\v]|&nbsp;"
            text = re.sub(pattern, " ", text)
        return super().clean(text)


class MultipleSpaceHandler(AbstractTextSanitizer):
    """
    Chain link which replace multiple spaces in row with single space
    """

    def clean(self, text: str) -> str:
        if text is not None:
            pattern = r"[ ]{2,}"
            text = re.sub(pattern, " ", text)
        return super().clean(text)


class BoundsHandler(AbstractTextSanitizer):
    """
    Chain link which is resposible for replace with zero len string multiple spaces
    at start and end of string
    """

    def clean(self, text: str) -> str | None:
        if text is not None:
            pattern = r"^[\s]*|[\s]*$"
            text = re.sub(pattern, "", text)
        return super().clean(text)


class BeforePunctuationHandler(AbstractTextSanitizer):
    """
    Chain link which is responsible for replace with zero len string spaces before
    punctuation
    """

    def clean(self, text: str) -> str | None:
        if text is not None:
            pattern = r"[\s]+(?=[!,.:;?])"
            text = re.sub(pattern, "", text)
        return super().clean(text)


class StringSanitizer:
    def __init__(self, handlers: List[str] | List[Sanitizer] = None) -> None:
        self.handlers = handlers or list(
            map(create_instance, list(settings.SANITIZATION_ORDER))
        )

    def append(self, handler: Sanitizer) -> None:
        """Add Sanitizer to list of handlers

        Args:
            handler (Sanitizer): Concrete String Handler
        """
        self.handlers.append(handler)

    def create_chain(self) -> Sanitizer:
        """Creating chain of handlers created in order of element in self.handlers lsit

        Returns:
            Sanitizer | None: First link of chain or None
        """
        first = self.handlers[0]
        while len(self.handlers) > 0:
            current = self.handlers.pop(0)
            if len(self.handlers) >= 1:
                next = self.handlers[0]
            elif len(self.handlers) == 0:
                next = None

            current.set_next(next)
        return first


def get_chain() -> Sanitizer:
    return StringSanitizer().create_chain()


def clean_string(text: str) -> str:
    chain = StringSanitizer()
    cleaning_chain = chain.create_chain()
    cleaned_text = cleaning_chain.clean(text)
    return cleaned_text
