from __future__ import annotations
from typing import Text
from lxml.html import HtmlElement
from config import settings
from core.extractors.interface import ExtractorInterface
from core.parser.parser import Parser

class TitleExtractor(ExtractorInterface):
    SPPLITERS = ["|", "-", "»", ":"]

    def __init__(self, root: HtmlElement, parser: Parser):
        """
        Initializes the CanonicalExtractor.

        Args:
            root (HtmlElement): The root element to search for canonical URLs.
            parser (Parser): The parser object used to extract URLs.
        """
        self.root = root
        self.parser = parser

    def fetch_meta_opengraf(self) -> Text|None:
        # opengraph
        title = ""
        title_nodes = self.parser.get_elements_by_tag(
            self.root, tag="meta", attr="property", value="og:title"
        )
        for element in title_nodes:
            title = self.parser.get_element_attr_content(
                element, "property", "content"
            )
            if title is not None:
                return title
        return None

    def fetch_tag_title(self, root: HtmlElement) -> Text|None:
        # title tag
        title_nodes = self.parser.get_elements_by_tag(root, "title")
        if title_nodes is not None and len(title_nodes) > 0:
            title = title_nodes[0].text
            return title
        return None

    def get_title(self) -> Text|None:
        """ Method is respon

        Args:
            root (HtmlElement): root node

        Returns:
            HtmlElement: _description_
        """
        if self.root is not None:
            title = self.fetch_meta_opengraf()
            if title is None:
                title = self.fetch_tag_title()
            return title
        return None

    def remove_sitename(self, title: Text|None) -> Text|None:
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
            # check if title contains any sppliter
            # TODO
            # Sprawdzana jest faktycznie obecność spllitera a nie faktycznej nazwy portalu
            # Jak przekazać nazwę portalu tak aby sprawdzić czy faktycznie istnieje w tytule
            sppliter = [item for item in self.SPPLITERS if item in title]
            if len(sppliter) > 0:
                # title without portal name
                content_words = title.split(sppliter[0])

            if content_words:
                clened_title = content_words[0].strip()
            else:
                clened_title = title
        return clened_title

    def extract(self) -> Text|None:
        """Extraction method

        Args:
            root (HtmlElement): _description_
            parser (Parser): _description_

        Returns:
            Text: article title
        """
        if self.root is not None:
            title = self.get_title()
            cleaned_title = self.remove_sitename(title)
            return cleaned_title
        return None
