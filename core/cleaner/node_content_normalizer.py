"""
Module for creating a chain of responsibility to normalize node text and tail.
The goal is to return a flattened node with only the text value, removing any tail value and any children with text or tail.

Classes:
    Normalizer (ABC):
        Abstract base class for defining a normalizer in the chain of responsibility.

    AbstractNormalizer (Normalizer):
        Abstract class that provides a default implementation for setting the next normalizer and normalizing an HTML element.

    NodeTextNormalizer (AbstractNormalizer):
        Concrete normalizer responsible for sanitizing the text value of a node.

    NodeTailNormalizer (AbstractNormalizer):
        Concrete normalizer responsible for transferring a node's tail to its text value.

    TextTailJoiner (AbstractNormalizer):
        Concrete normalizer responsible for joining the text and tail values of a node.

    NodeFlatteningNormalizer (AbstractNormalizer):
        Concrete normalizer responsible for flattening the node by extracting the text of the entire subtree.

    NodeContentNormalizer:
        Class responsible for creating and managing the normalization chain.

"""

from __future__ import annotations
from typing import List, Callable
from abc import ABC, abstractmethod
from lxml.html import HtmlElement
from config import settings
from config.utils import create_instance
from core.parser.parser import Parser
from core.text.text_cleaner import clean_string


class Normalizer(ABC):
    @abstractmethod
    def set_next(self, normalizer: Normalizer) -> Normalizer:
        pass

    @abstractmethod
    def normalize(self, node: HtmlElement, parser: Parser):
        pass


class AbstractNormalizer(Normalizer):
    def __init__(self) -> None:
        self.next = None

    def get_normalizer(self) -> Normalizer:
        return self

    def set_next(self, normalizer: Normalizer) -> Normalizer:
        """Set the next normalizer in the chain.

        Args:
            normalizer (Normalizer): The next normalizer in the chain.

        Returns:
            Normalizer: The next normalizer.
        """

        self.next = normalizer
        return normalizer

    @abstractmethod
    def normalize(self, node: HtmlElement, parser: Parser):
        """Normalize the HTML element.

        Args:
            node (HtmlElement): The HTML element to normalize.
            parser (Parser): The LXML parser.

        Returns:
            None: If the normalization is done and no further action is required.
            Callable: The next normalization function to call if additional normalization is needed.
        """
        if self.next is not None:
            return self.next.normalize(node, parser)
        return None


class NodeTextNormalizer(AbstractNormalizer):
    def _sanitize_text_value(self, node: HtmlElement, parser: Parser) -> None:
        "Its resposobile for sanitizing concrete node text value"
        
        node_text = parser.get_text_value(node)
        if node_text is not None:
            node_text = clean_string(node_text)
            parser.set_text_value(node, node_text)

    def normalize(self, node: HtmlElement, parser: Parser) -> None | Callable:
        "Its responsible for removing all whitespace from the text of the node"
        self._sanitize_text_value(node, parser)
        return super().normalize(node, parser)


class NodeTailNormalizer(AbstractNormalizer):
    "Transfer nodes tail to node text"

    def _sanitize_tail_value(self, node: HtmlElement, parser: Parser) -> None:
        node_tail = parser.get_tail_value(node)
        if node_tail is not None:
            node_tail = clean_string(node_tail)
            parser.set_tail_value(node, node_tail)

    def normalize(self, node: HtmlElement, parser: Parser) -> None | Callable:
        """Resposible for transfer tail to node text and change value of tail to text"""
        self._sanitize_tail_value(node, parser)
        return super().normalize(node, parser)


class TextTailJoiner(AbstractNormalizer):
    def normalize(self, node: HtmlElement, parser: Parser):
        node_text = parser.get_text_value(node)
        node_tail = parser.get_tail_value(node)

        # In some casess tail or text are NoneType. To prevent TypeError if so their
        # value will be set to zero len string.
        if not isinstance(node_text, str):
            node_text = ""

        if not isinstance(node_tail, str):
            node_tail = ""

        joined_text = " ".join([node_text, node_tail])
        parser.set_text_value(node, joined_text)
        parser.set_tail_value(node, None)
        return super().normalize(node, parser)


class NodeFlatteningNormalizer(AbstractNormalizer):
    """Gets the text of the entire subtree if the parent has its own text.
    If it doesn't, it doesn't perform any operation.
    """

    def normalize(self, node: HtmlElement, parser: Parser):
        if parser.have_childs(node):
            subtree_text = clean_string(parser.get_subtree_text(node))
            parser.set_text_value(node, subtree_text)
            parser.remove_all_childerns(node)
        return super().normalize(node, parser)


class NodeContentNormalizer:
    """
    Responsible for creating a normalization chain.

    Args:
        links (List[str] | List[Normalizer], optional):
            A list of links or normalizers for creating the normalization chain.
            Defaults to None.

    Attributes:
        first_link: The first link in the normalization chain.

    Methods:
        create_chain(links: List[str] | List[Normalizer] = None) -> None:
            Creates a normalization chain from the given links or normalizers.

    """

    def __init__(self, links: List[str] | List[Normalizer] = None) -> None:
        self.first_link = None
        self.create_chain(links)

    def create_chain(self, links: List[str] | List[Normalizer] = None) -> None:
        """
        Creates a normalization chain from the given links or normalizers.
        If links arent passed method will access to settings constant and create list of links based on it.
        Next first element of this list will by assigned to self.first.
        After that next elements of links list will by join to create real chain.

        Args:
            links (List[str] | List[Normalizer], optional):
                A list of links or normalizers for creating the normalization chain.
                Defaults to None.

        """

        # creates list of non conected links
        _links = links or [
            create_instance(link) for link in settings.NODE_CONTENT_NORMALIZERS
        ]

        # set first link in node normalizer. It will be called as first
        self.first_link = _links[0]

        # Set the next links
        for i in range(len(_links) - 1):
            _links[i].set_next(_links[i + 1])
