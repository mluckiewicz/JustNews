from typing import List, Text
from abc import ABC, abstractmethod
from lxml.html import HtmlElement
from config import settings
from ..parser.parser import Parser
from .dom_cleaning_strategies import (
    RemoverStrategy,
    CompoundRemover,
    AttribiuteRemover,
    TagRemover,
    CommentsRemover,
    TextNormalizer,
    ByAttrValueRemover,
    NoTextRemover,
    NonArticleSubtreeRemover,
    NonSentenceRemover,
    SubtreeMergingStrategy,
    ReplaceTags,
    TransferUpTree,
)


class BasicCleaner(ABC):
    @abstractmethod
    def __init__(self, parser: Parser):
        pass

    @abstractmethod
    def execute(self):
        pass


class DocumentCleaner(BasicCleaner):
    "Concrete Cleaner"

    def __init__(self) -> None:
        self.composite = CompoundRemover()
        self.tag_blacklist = settings.TAG_BLACKLIST
        self.tag_whitelist = settings.TAG_WHITELIST
        self.attribiutes_blacklist = "|".join(settings.ATTRIBIUTES_BLACKLIST)

    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        if root is not None:
            # phase 1 cleaning - Tags
            self.composite.add_strategy(self.remove_attribiutes(self.tag_whitelist))
            self.composite.add_strategy(self.remove_by_tag_match(self.tag_blacklist))
            self.composite.add_strategy(self.remove_comments())
            self.composite.add_strategy(
                self.remove_by_attr_match("class", self.attribiutes_blacklist)
            )
            self.composite.add_strategy(
                self.remove_by_attr_match("id", self.attribiutes_blacklist)
            )
            self.composite.add_strategy(self.remove_article_node_siblings("article"))

            # phase 2 cleaning - Text and Tail
            self.composite.add_strategy(self.normalize_text())
            self.composite.add_strategy(self.remove_no_sentences())
            self.composite.add_strategy(self.remove_nodes_without_text())

            # phase 3 cleaning - tree
            self.composite.add_strategy(self.merge_subree())
            self.composite.add_strategy(self.transfer_up_tree())

            self.composite.add_strategy(self.change_tag("div", "p"))
            self.composite.add_strategy(self.change_tag("span", "p"))
            self.composite.add_strategy(self.change_tag("h1", "p"))

            cleaned = self.composite.execute(root, parser)

        return cleaned

    def remove_attribiutes(self, tags: List[Text]) -> RemoverStrategy:
        return AttribiuteRemover(tags)

    def remove_by_tag_match(self, tags: List[Text]) -> RemoverStrategy:
        return TagRemover(tags)

    def remove_comments(self) -> RemoverStrategy:
        return CommentsRemover()

    def normalize_text(self) -> RemoverStrategy:
        return TextNormalizer()

    def remove_by_attr_match(self, attr, value) -> RemoverStrategy:
        return ByAttrValueRemover(attr, value)

    def remove_nodes_without_text(self) -> RemoverStrategy:
        return NoTextRemover()

    def remove_article_node_siblings(self, tag_name) -> RemoverStrategy:
        return NonArticleSubtreeRemover(tag_name)

    def remove_no_sentences(self) -> RemoverStrategy:
        return NonSentenceRemover()

    def merge_subree(self) -> RemoverStrategy:
        return SubtreeMergingStrategy()

    def change_tag(self, starting_tag, target_tag) -> RemoverStrategy:
        return ReplaceTags(starting_tag, target_tag)

    def transfer_up_tree(self) -> RemoverStrategy:
        return TransferUpTree()
