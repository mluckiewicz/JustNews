from __future__ import annotations
from typing import Text, List
import statistics
from lxml.html import HtmlElement
from core.parser.parser import Parser
from core.text.stopwords import Stopwords
from core.text.utils import StringHelper
from core.extractors import ExtractorInterface


class ContentExtractor(ExtractorInterface):
    INNER_TEXT_LEN = 25
    STOPWORDS_COUNT = 2

    def __init__(self) -> None:
        """ """
        self.tags = ["p", "pre", "td"]
        self.stopwords = Stopwords("pl")

    def get_nodes_with_text(self, root: HtmlElement) -> List[HtmlElement]:
        """The method is responsible for filtering nodes containing text
        that does meet the specified conditions.

        The text must be at least 25 characters long and contain a minimum of 2
        stop words and must be contained in p, pre, etc. tags.

        Args:
            root (HtmlElement): root node of the document.

        Returns:
            List[HtmlElement]: List of nodes meeting the criteria.
        """

        nodes_with_text = []
        nodes = self.parser.get_nodes_with_text(root)
        for node in nodes:
            if node.tag in self.tags:
                inner_text = self.parser.get_subtree_text(node)
                inner_text_len = len(inner_text)
                stopwords_count = self.stopwords.count(inner_text)
                if (
                    inner_text_len > self.INNER_TEXT_LEN
                    and stopwords_count > self.STOPWORDS_COUNT
                ):
                    nodes_with_text.append(node)
        return nodes_with_text

    def rate_paragraphs(self, nodes_with_text: List[HtmlElement]) -> List[HtmlElement]:
        """The method is responsible for evaluating the text contained in the
        paragraphs. The evaluation of a given text is the number of occurrences of stop
        words.

        Then the parent and grandparent of the processed node are evaluated. The result
        is transferred and summed up with the results of subsequent nodes. As a result,
        after processing all the nodes, the result of the initial nodes is the sum of
        the results of their descendants.

        Args:
            nodes_with_text (List[HtmlElement]): Nodes containing text with specific
            criteria.

        Returns:
            List[HtmlElement]: List of items that have been scored.
        """

        parents = []
        for node in nodes_with_text:
            # rate node
            inner_text = self.parser.get_text_value(node)
            if inner_text is not None:
                if StringHelper.is_sentance(inner_text):
                    stopwords_num = self.stopwords.count(inner_text)
                    self.update_attibiute_value(node, "score", stopwords_num)
                    self.update_attibiute_value(node, "nodes", 1)

                # rate node parent
                parent = self.parser.get_parent(node)
                score = self.parser.get_attribute(node, "score")
                self.update_attibiute_value(parent, "score", score)
                self.update_attibiute_value(parent, "nodes", 1)
                if parent not in parents:
                    parents.append(parent)

                # rate node grandparent
                grandparent = self.parser.get_parent(parent)
                score = self.parser.get_attribute(node, "score")
                self.update_attibiute_value(grandparent, "score", score)
                self.update_attibiute_value(grandparent, "nodes", 1)
                if grandparent not in parents:
                    parents.append(grandparent)
        return parents

    def normalize_nodes_score(
        self, rated_parents: List[HtmlElement]
    ) -> List[HtmlElement]:
        """The method is responsible for normalizing the results of parents of children
        containing text. Normalization involves taking the scores of all children of a
        given and calculating the median from the scores of the children.

        Then the median is multiplied by the position of the parent in the list
        reflecting the position of the family in the document.

        Args:
            rated_parents (List[HtmlElement]): List of parents whose children contain
            the text and have been reviewed.

        Returns:
            List[HtmlElement]: List of nodes whose score has been normalized.
        """

        parents = self.parser.map_children(rated_parents)
        num_of_parents = len(parents.items())

        for parent, childs in parents.items():
            tmp = [self.get_score(child) for child in childs]
            new_score = statistics.median(tmp) * num_of_parents
            num_of_parents -= 1
            self.update_attibiute_value(parent, "score", new_score)
        return list(parents.keys())

    def update_attibiute_value(self, node: HtmlElement, attr_name: str, value) -> None:
        """Method is responsible for updating the attribute value in the
        passed node.

        Args:
            node (HtmlElement): _description_
            attr_name (str): _description_
            value (_type_): _description_
        """

        current_value = self.parser.get_attribute(node, attr_name)
        if current_value:
            current_value = int(current_value)
        else:
            current_value = 0

        if not value:
            value = 0
        new_score = current_value + int(value)
        self.parser.set_attribute(node, attr_name, str(new_score))

    def get_top_node(self, nodes: List[HtmlElement]) -> HtmlElement:
        """Method is responsible for selecting the node with the highest score.

        Args:
            nodes (List[HtmlElement]): List of nodes that have been scored.

        Returns:
            HtmlElement: Noe with highest score.
        """

        top_node_score = 0
        top_node = None

        for node in nodes:
            score = self.get_score(node)

            if score > top_node_score:
                top_node = node
                top_node_score = score

            if top_node is None:
                top_node = node

        return top_node

    def get_score(self, node: HtmlElement) -> int | None:
        score = self.parser.get_attribute(node, "score")
        if score is None:
            return None
        return int(score)

    def calculate_nodes_scoring(self, node: HtmlElement) -> List[HtmlElement]:
        """The method is responsible for managing the process of evaluating paragraphs
        and their introductions.

        Args:
            node (HtmlElement): Root node of document.

        Returns:
            List[HtmlElement]: List of nodes that have been scored.
        """
        nodes_with_text = self.get_nodes_with_text(node)
        scored_parents = self.rate_paragraphs(nodes_with_text)
        normalized_score_parents = self.normalize_nodes_score(scored_parents)
        return normalized_score_parents

    def extract(self, root: HtmlElement, parser: Parser) -> Text:
        """External interface. It is responsible for calling individual methods, which in effect return the uncleaned text of the article.

        Args:
            node (HtmlElement): Root node of document
            parser (Parser):

        Returns:
            str: Uncleaned text of the article.
        """
        if root is not None:
            self.parser = parser
            scored_inner_nodes = self.calculate_nodes_scoring(root)
            self.top_node = self.get_top_node(scored_inner_nodes)

            if self.top_node is not None:
                article_text = self.parser.get_subtree_text(self.top_node)
                return article_text
            return "Error occured with geting top node. Probobly webpage is js-redner"
        return None
