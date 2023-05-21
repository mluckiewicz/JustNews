from typing import List, Text, Literal
from abc import ABC, abstractmethod
import queue
from lxml.html import HtmlElement
from ..parser.parser import Parser
from .node_text_normalizer import (
    AbstractNormalizer,
    NormalizingChain,
    NodeFlatteningNormalizer,
    NodeTailNormalizer,
    NodeTextNormalizer,
    TextTailConnNormalizer,
)
from ..text.utils import StringHelper
from core.utils import compare_lists


class BasicCleaner(ABC):
    @abstractmethod
    def __init__(self, parser: Parser):
        pass

    @abstractmethod
    def execute(self):
        pass


class RemoverStrategy(ABC):
    @abstractmethod
    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        pass


class CompoundRemover(RemoverStrategy):
    def __init__(self, *cleaning_strattegies: List[RemoverStrategy]) -> None:
        self.cleaning_strattegies = list(cleaning_strattegies)

    def add_strategy(self, startegy: RemoverStrategy) -> None:
        "Add cleaning strategy to strategies"
        if isinstance(startegy, RemoverStrategy):
            self.cleaning_strattegies.append(startegy)
        else:
            raise TypeError(
                f"Object of {type(startegy)} passed. Should be CleaningStrategy"
            )

    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        for cleaning_startegy in self.cleaning_strattegies:
            root = cleaning_startegy.execute(root, parser)
        if root is not None:
            return root


class AttribiuteRemover(RemoverStrategy):
    "Strategy removes attrs class and id values in given tags"

    def __init__(self, tags: List[Text] | None) -> None:
        self.tags = tags

    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        for tag in self.tags:
            nodes = parser.get_elements_by_tag(root, tag)
            if len(nodes) > 0:
                for node in nodes:
                    if "class" in node.attrib:
                        parser.del_attribute(node, "class")

                    if "id" in node.attrib:
                        parser.del_attribute(node, "id")
        return root


class TagRemover(RemoverStrategy):
    def __init__(self, tags: List[Text]) -> None:
        self.tags = tags

    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        for tag in self.tags:
            nodes = parser.get_elements_by_tag(root, tag=tag)
            if len(nodes) > 0:
                for node in nodes:
                    parser.remove(node)
        return root


class CommentsRemover(RemoverStrategy):
    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        comments = parser.get_comments(root)
        for comment in comments:
            parser.remove(comment)
        return root


class TextNormalizer(RemoverStrategy):
    def __init__(self) -> None:
        self.normalizer: AbstractNormalizer = self.set_normalizer()

    def set_normalizer(self):
        _chain = NormalizingChain()
        _chain.append(NodeTextNormalizer())
        _chain.append(NodeTailNormalizer())
        _chain.append(NodeFlatteningNormalizer())
        _chain.append(TextTailConnNormalizer())
        return _chain.create_normalizing_chain()

    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        text_nodes = parser.get_nodes_with_text(root)
        for node in text_nodes:
            self.normalizer.normalize(node, parser)
        return root


class ByAttrValueRemover(RemoverStrategy):
    "Removes nodes from tree based on finding match in passed attr value"

    def __init__(self, attr_name: Text, attr_values: Literal) -> None:
        self.attr_name = attr_name
        self.attr_values = attr_values

    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        re_pattern = f"//*[re:test(@{self.attr_name}, '{self.attr_values}', 'i')]"
        regex_resault = parser.xpath(root, re_pattern)
        for node in regex_resault:
            parser.remove(node)
        return root


class NoTextRemover(RemoverStrategy):
    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        nodes = parser.get_nodes_without_text(root)
        for node in nodes:
            parser.remove(node)
        return root


class NonArticleSubtreeRemover(RemoverStrategy):
    """Removes nodes that are not part of article tag subtree. It assumes only one
    article node exist in tree"""

    def __init__(self, subtree_root_tag: Text) -> None:
        self.subtree_root_tag = subtree_root_tag

    def mark_subtree_nodes(
        self,
        subtree_node: HtmlElement,
        parser: Parser,
        traversing_up: bool = False,
    ) -> None:
        """
        If traversing_up = False
        Traverses up or down over tree from given root node and mark any nodes if it is part of subbtree . Traverses down by default.
        You can change direction by keyword 'traversing_up'.

        Args:
            subtree_node (HtmlElement): _description_
            parser (Parser): _description_
            traversing_up (bool): _description_
        """
        if traversing_up:
            for i in subtree_node.iterancestors():
                parser.set_attribute(i, "is_article_subtree", "True")
        for i in subtree_node.iter():
            parser.set_attribute(i, "is_article_subtree", "True")

    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        """_summary_

        Args:
            root (HtmlElement): _description_
            parser (Parser): _description_

        Returns:
            HtmlElement: _description_
        """
        article_root = parser.get_elements_by_tag(root, self.subtree_root_tag)

        # check if only one article tag exist
        if len(article_root) == 1:
            # traverse up to tree root and mark as part of subtree
            self.mark_subtree_nodes(article_root[0], parser, traversing_up=True)

            # traverse down form subtree root and mark as part of subtree
            self.mark_subtree_nodes(article_root[0], parser)

            # removing nodes that are not part of sub tree
            for node in list(root.iter()):
                if parser.get_attribute(node, "is_article_subtree") is None:
                    parser.remove(node)

        return root


class SubtreeMergingStrategy(RemoverStrategy):
    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        """The method only processes internal nodes whose children are nodes
        containing text.
        The nodes are processed in the reverse order than in the document, as
        this allows to exclude the transfer of the node containing the lead of
        the article.
        If all text nodes in the document are children of a given node, the
        method does not call inner function ``move_nodes``.
        Otherwise, it is checked if the node has other children than those with
        text. If not, the children will be moved to the parent of that node
        recursively.
        Args:
            root (HtmlElement): _description_
        Returns:
            HtmlElement: _description_
        """

        def move_nodes(node: HtmlElement) -> None:
            """The method is responsible for moving the leaves up the tree until the
            parent has more children than the nodes being moved
            Args:
                node (HtmlElement): _description_
            Returns:
                _type_: _description_
            """
            while True:
                parent = parser.get_parent(node)
                if parent is not None:
                    parent_childs = parser.get_children(parent)
                    parent_childs.remove(node)
                    if not parent_childs:
                        parent.extend(parent_childs_with_text)
                        parser.remove(node)
                        return move_nodes(parent)
                break

        get_nodes_with_text = parser.get_nodes_with_text(root)
        parents = parser.map_children(
            get_nodes_with_text
        )  # if parent is text node and have content chlidren falls in infinite loop
        for parent in reversed(parents.keys()):
            parent_childs_all = parser.get_children(parent)
            parent_childs_with_text = parents.get(parent)
            # Jeżeli wszyskie węzły z tekstem są dziećmi rodzica nie ma sensu
            # przetwarzać je dalej.
            if get_nodes_with_text != parent_childs_with_text:
                # Sprawdzenie czy węzeł ma inne dzieci niż te z tekstem
                compare = compare_lists(parent_childs_all, parent_childs_with_text)
                if not compare:
                    move_nodes(parent)
        return root


class NonSentenceRemover(RemoverStrategy):
    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        text_nodes = parser.get_nodes_with_text(root)
        try:
        
            avg = sum(
                [len(parser.get_text_value(node)) for node in text_nodes]
                ) / len(text_nodes)
        except ZeroDivisionError:
            avg = 50
        for node in text_nodes:
            node_text = parser.get_text_value(node)
            # Some times picture description is pulled tu content. To not lose whole
            # content node it wil be skiped
            if len(node_text) >= avg:
                continue
            if not StringHelper.is_sentance(node_text.strip()):
                parser.remove(node)
        return root


class ReplaceTags(RemoverStrategy):
    def __init__(self, starting_tag: str, target_tag: str) -> HtmlElement:
        self.starting_tag = starting_tag
        self.target_tag = target_tag

    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        for node in parser.generate_node_with_text(root):
            node_tag = parser.get_tag(node)
            if node_tag == self.starting_tag:
                parser.replace_tag(node, self.target_tag)
        return root


class TransferUpTree(RemoverStrategy):
    """Responsible for moving nodes with text up the tree if the current node is the only
    child of its parent."""

    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        q = queue.Queue()
        for node in reversed(parser.get_nodes_with_text(root)):
            q.put(node)

        if q.qsize() > 1:  # prevent to run transfer if only one text node left in tree
            while not q.empty():
                try:
                    current = q.get(0)
                    parent = parser.get_parent(current)
                    if len(parser.get_children(parent)) == 1:
                        current_text = parser.get_text_value(current)
                        parser.set_text_value(parent, current_text)
                        parser.remove_child(current)
                        grandparent = parser.get_parent(parent)
                        if len(parser.get_children(grandparent)) > 1:
                            continue
                        q.put(parent)
                except TypeError:  # if parent or grandparent are NoneType
                    continue
        return root


class DocumentCleaner(BasicCleaner):
    "Concrete Cleaner"

    def __init__(self) -> None:
        self.composite = CompoundRemover()
        self.redundant_tags = [
            "script",
            "style",
            "aside",
            "noscript",
            "figure",
            "nav",
            "footer",
            "iframe",
            "picture",
            "img",
            "form",
            "button",
            "svg",
            "header",
            "svg",
            "label",
            "select",
            "amp-sidebar",
            "a",
            "title",
            "h1",
            "h2",
            "h3",
            "h4",
        ]
        self.non_removable_tags = ["body", "article"]
        self.bad_attrs = "|".join(
            [
                "facebook",
                "tweet",
                "google",
                "social",
                "payu",
                "cookie",
                "comment",
                "OpenDiscussionBox",
                "Discussion",
                "question",
                "komentarz",
                "reklama",
                "ogloszenia",
                "announcements",
                "Promotions",
                "advertisement",
                "ads",
                "foot",
                "poster",
                "links",
                "footer-holder",
                "footer",
                "copyright",
                "author",
                "widget",
                "photo",
                "date",
                "^slider",
                "image120x90",
                "upgradebrowser",
                "msccBanner",
                "login",
                "menu",
                "aside",
                "popup",
                "am-article__description",
                "topbar",
                "RadioStream",
                "^share",
                "video_player",
                "bannergroup",
                "spotligh",
                "itemRelated",
                "Image",
                "blocker",
                "upprev_box",
                "claim",
                "author",
                "title",
                "plus18",
                "reglog",
            ]
        )

    def execute(self, root: HtmlElement, parser: Parser) -> HtmlElement:
        if root is not None:
            # phase 1 cleaning - Tags
            self.composite.add_strategy(
                self.remove_attribiutes(self.non_removable_tags)
            )
            self.composite.add_strategy(self.remove_by_tag_match(self.redundant_tags))
            self.composite.add_strategy(self.remove_comments())
            self.composite.add_strategy(
                self.remove_by_attr_match("class", self.bad_attrs)
            )

            
            self.composite.add_strategy(self.remove_by_attr_match("id", self.bad_attrs))
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
