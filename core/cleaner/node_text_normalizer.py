from __future__ import annotations
from typing import List, Callable
from abc import ABC, abstractmethod
from lxml.html import HtmlElement
from ..parser.parser import Parser
from core.text.text_cleaner import clean_string


class Normalizer(ABC):
    
    @abstractmethod
    def set_next(self, normalizer: Normalizer) -> Normalizer:
        pass

    @abstractmethod
    def normalize(self, node: HtmlElement, parser: Parser):
        pass


class AbstractNormalizer(Normalizer):
    def __init__(self):
        self.next = None

    def get_normalizer(self):
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


class TextTailNormalizer(AbstractNormalizer):
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
    """ Gets the text of the entire subtree if the parent has its own text. 
    If it doesn't, it doesn't perform any operation. 
    """
    def normalize(self, node: HtmlElement, parser: Parser):
        #node_text = parser.get_text_value(node)
        if parser.have_childs(node):
            subtree_text = clean_string(
                parser.get_subtree_text(node)
            )
            parser.set_text_value(node, subtree_text)
            parser.remove_all_childerns(node)
        return super().normalize(node, parser)


class NodeTextNormalizingChain:
    def __init__(self, *normalizers: List[Normalizer]):
        self.chain = list(normalizers)

    def append(self, normalizer: Normalizer) -> None:
        self.chain.append(normalizer)

    def create_normalizing_chain(self) -> AbstractNormalizer:
        first = self.chain[0]
        while len(self.chain) > 0:
            current = self.chain.pop(0)
            if len(self.chain) >= 1:
                next = self.chain[0]
            elif len(self.chain) == 0:
                next = None
                
            current.set_next(next)
        return first
