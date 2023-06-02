from __future__ import annotations
from typing import Text
from lxml.html import HtmlElement
from config import settings
from core.extractors.interface import ExtractorInterface
from core.parser.parser import Parser


class TitleExtractor(ExtractorInterface):
    SPPLITERS = ["|", "-", "»", ":"]
    PATTERNS = settings.EXTRACTORS["title_extractor"]["patterns"]

    def __init__(self, root: HtmlElement, parser: Parser):
        """
        Initializes the CanonicalExtractor.

        Args:
            root (HtmlElement): The root element to search for canonical URLs.
            parser (Parser): The parser object used to extract URLs.
        """
        self.root = root
        self.parser = parser

    def remove_sitename(self, title: Text | None) -> Text | None:
        """Responsible for removing the name of the portal or
        publisher from the title of the article

        Args:
            node (HtmlElement): The node that holds the article tag

        Returns:
            Text: Returns the sanitized title
        """
        clened_title = ""
        content_words = None

        if title is not None:
            sppliter = [item for item in self.SPPLITERS if item in title]
            if len(sppliter) > 0:
                # title without portal name
                content_words = title.split(sppliter[0])
            if content_words:
                clened_title = " ".join(content_words[:-1]) #remove last tokken. Almost always it is site name
            else:
                clened_title = title
        return clened_title

    def extract(self) -> Text | None:
        """Method is respon

        Args:
            root (HtmlElement): root node

        Returns:
            HtmlElement: _description_
        """
        for pattern in self.PATTERNS:
            try:
                extracted_urls = self.parser.xpath(self.root, pattern)
                if extracted_urls:
                    raw_title = self.parser.get_text_value(extracted_urls[0])
                    clean_title = self.remove_sitename(raw_title)
                    return clean_title
            except IndexError:  # if any pattern will not match
                return None
