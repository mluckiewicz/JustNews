from __future__ import annotations
from lxml.html import HtmlElement
from config import settings
from core.extractors.interface import ExtractorInterface
from core.parser.parser import Parser


class PublishdateExtractor(ExtractorInterface):

    PATTERNS = settings.EXTRACTORS["publishdate_extractor"]["patterns"]

    def __init__(self, root: HtmlElement, parser: Parser):
        """
        Initializes the CanonicalExtractor.

        Args:
            root (HtmlElement): The root element to search for canonical URLs.
            parser (Parser): The parser object used to extract URLs.
        """
        self.root = root
        self.parser = parser

    def extract(self) -> str | None:
        """
        Extracts the canonical URL using the defined patterns. Patterns will be checked in loop. Method will return first found match.

        Returns:
            str | None: The extracted canonical URL, or None if not found.

        Raises:
            IndexError: If any of pattenrs will not apply method will throw IndexError wen try to acces first position of empty list.
        """
        for pattern in self.PATTERNS:
            try:
                extracted_urls = self.parser.xpath(self.root, pattern)
                if extracted_urls:
                    return extracted_urls[0]
            except IndexError:  # if any pattern will not match
                pass
        return None