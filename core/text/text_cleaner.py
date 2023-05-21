from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
import re
from config import settings
from config.utils import create_instance
from core.exceptions import NotImplementedInterface


__all__ = ["clean_string"]


class TextCleaningStrategy(ABC):
    "Text cleaning startegy interface"

    @abstractmethod
    def clean(self, text: str) -> str:
        pass


class TrimTokens(TextCleaningStrategy):
    "Strategy responsibile for trim each tokken from passed text."

    def clean(self, text: str) -> str:
        if text is not None:
            text = " ".join(text.split())
        return text


class RemoveWhiteSpaces(TextCleaningStrategy):
    "Strategy responsibile for repleacing whitespaces with single space."

    def clean(self, text: str) -> str | None:
        if text is not None:
            pattern = r"[\f\n\r\t\v]|&nbsp;"
            text = re.sub(pattern, " ", text)
        return text


class RemoveMultipleSpaces(TextCleaningStrategy):
    "Strategy responsibile for repleacing more the one space in row with single one."

    def clean(self, text: str) -> str:
        if text is not None:
            pattern = r"[ ]{2,}"
            text = re.sub(pattern, " ", text)
        return text


class TrimString(TextCleaningStrategy):
    "Strategy resposible for replace with zero len string multiple spaces at start and end of string."

    def clean(self, text: str) -> str | None:
        if text is not None:
            pattern = r"^[\s]*|[\s]*$"
            text = re.sub(pattern, "", text)
        return text


class RemoveSpacesBeforePunctuation(TextCleaningStrategy):
    "Strategy resposible for replace with zero len string spaces beforepunctuation from list `[!,.:;?]`"

    def clean(self, text: str) -> str | None:
        if text is not None:
            pattern = r"[\s]+(?=[!,.:;?])"
            text = re.sub(pattern, "", text)
        return text


class CleaningTextContext:
    """Context for cleaning text using various strategies.

    Args:
        text (str): The text to be cleaned.
        cleaning_strategies (List[str] or List[TextCleaningStrategy], optional):
            The list of cleaning strategies to be applied to the text.
            Defaults to None, in which case the strategies from `settings.SANITIZATION_ORDER`
            will be used.

    Methods:
        append(cleaning_strategy: TextCleaningStrategy) -> None:
            Appends a cleaning strategy to the list of cleaning strategies.

        clean() -> str:
            Applies all the cleaning strategies to the text and returns the cleaned text.
    """

    def __init__(
        self,
        text: str,
        cleaning_strategies: List[str] | List[TextCleaningStrategy] = None,
    ) -> None:
        self.text = text
        self.cleaning_strategies = cleaning_strategies or list(
            map(create_instance, list(settings.SANITIZATION_ORDER))
        )

    def append(self, cleaning_strategies: TextCleaningStrategy) -> None:
        """Appends a cleaning strategy to the list of strategies.

        Args:
            cleaning_strategy (TextCleaningStrategy): The cleaning strategy object to append.

        Raises:
            NotImplementedInterface: If the given cleaning strategy object does not implement
                the `TextCleaningStrategy` interface.
        """
        if not isinstance(cleaning_strategies, TextCleaningStrategy):
            raise NotImplementedInterface(
                "Given object is not implementing TextCleaningStrategy interface."
            )
        self.cleaning_strategies.append(cleaning_strategies)

    def clean(self) -> str:
        """Applies all the cleaning strategies to the text and returns the cleaned text.

        Returns:
            str: The cleaned text.
        """
        for strategy in self.cleaning_strategies:
            self.text = strategy.clean(self.text)
        return self.text


# TODO Add cleaning_strategies in call. Now client cant chage order with this cunction.
# TODO It must call CleaningTextContent directly
def clean_string(text: str) -> str:
    """Function is creating context instance and passing text to it. Context will run cleaning strategies in given order. Order of cleaning is define in config.Settings.

    Args:
        text (str): some text that will by processed with strategies

    Returns:
        str: cleaned text
    """
    cleaner = CleaningTextContext(text)
    return cleaner.clean()
