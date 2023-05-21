import re
import logging
import string
from abc import ABC
from typing import List, Dict, Text
from html import unescape
import lxml
from lxml.html import soupparser, HtmlElement
from .parser import Parser
from ..text.utils import StringHelper 


class LXMLParser(Parser):
    @classmethod
    def clean_html(cls, html: str) -> str:
        """Wykonuje konwersję na potrzeby prawidłowego odczytania znaków
        https://stackoverflow.com/questions/8733233/filtering-out-certain-bytes-in-python
        """
        cleaned_html = StringHelper.adjust_string_to_xml(html)
        cleaned_html = re.sub(r"\<\?.*?\?\>", "", cleaned_html, flags=re.DOTALL)
        return cleaned_html

    @classmethod
    def fromstring(cls, html: str) -> HtmlElement:
        """ The method is responsible parse the html and returning root element.
        lxml.html.soupparser.fromstring was choosen because the lxml.html.fromstring 
        method does not handle some pages.

        Args:
            html (str): raw response content

        Returns:
            HtmlElement: Root element
        """
        error = None
        try:
            html = cls.clean_html(html)
            root = soupparser.fromstring(html)
            return root
        except Exception:
            #Invalid HTML tag name
            root = lxml.html.fromstring(html)
            return root

    @classmethod
    def get_elements_by_tag(
        cls,
        node: HtmlElement,
        tag: str = None,
        attr: str = None,
        value: str = None,
        use_regex: bool = False,
    ) -> List[HtmlElement]:
        NS = None
        selector = "descendant-or-self::%s" % (tag or "*")
        if attr and value:
            if use_regex:
                NS = {"re": "http://exslt.org/regular-expressions"}
                selector = '%s[re:test(@%s, "%s", "i")]' % (selector, attr, value)
            else:
                trans = 'translate(@%s, "%s", "%s")' % (
                    attr,
                    string.ascii_uppercase,
                    string.ascii_lowercase,
                )
                selector = '%s[contains(%s, "%s")]' % (selector, trans, value.lower())
        elems = node.xpath(selector, namespaces=NS)
        return elems

    @classmethod
    def get_element_attr_content(
        cls, node: HtmlElement, attr: str = None, content_attr: str = None
    ) -> str | None:
        """Is responsible for extracting the value from the content key from the node's
        attrib dictionary.

        Args:
            node : DOM tree
            attr (str, optional): attribiute name. Defaults to None.

        Returns:
            str | None: if attr in node.attrib returns node.attrib['content']
                        value. Else None
        """
        content = None
        if attr is not None and len(node.attrib) > 0:
            if node.attrib.has_key(attr) and node.attrib.has_key(content_attr):
                content = node.attrib[content_attr]
        return content

    @classmethod
    def get_comments(cls, node: HtmlElement) -> List[HtmlElement]:
        """It is responsible for running the xpath query for comment nodes.

        Args:
            node (Element):

        Returns:
            list : List of found nodes
        """
        return node.xpath("//comment()")

    @classmethod
    def remove(cls, node: HtmlElement, keep_tail: bool=False) -> None:
        parent = node.getparent()
        if parent is not None:
            if node.tail:
                prev = node.getprevious()
                if prev is None:
                    if not parent.text:
                        parent.text = ""
                    parent.text += " " + node.tail
                else:
                    if not prev.tail:
                        prev.tail = ""
                    prev.tail += " " + node.tail
            node.clear(keep_tail)
            parent.remove(node)

    @classmethod
    def remove_child(cls, node: HtmlElement) -> None:
        parent = node.getparent()
        if parent is not None:
            node.clear()
            parent.remove(node)
            
    @classmethod
    def remove_all_childerns(cls, node: HtmlElement) -> None:
        for child in list(node):
            cls.remove_child(child)

    @classmethod
    def get_nodes_with_text(cls, node: HtmlElement) -> List[HtmlElement]:
        """The method retrieves all nodes containing text from the sub tree.

        Args:
            node (HtmlElement): Root of the subtree.

        Returns:
            List[HtmlElement]: List of nodes with text from the sub tree.
        """
        nodes = node.xpath("//body//*[normalize-space(text())]")
        return nodes
    
    @classmethod
    def generate_node_with_text(cls, node):
        for node in node.xpath("//body//*[normalize-space(text())]"):
            yield node

    @classmethod
    def get_nodes_without_text(cls, node: HtmlElement) -> List[HtmlElement]:
        nodes = node.xpath("//body//*[not(.//text()[normalize-space()])]")
        return nodes

    @classmethod
    def get_subtree_text(cls, node: HtmlElement):
        """returns node text. If node have children with then chltren text is pulled in
        parrent text."""
        inner_text = " ".join([word.strip() for word in node.itertext()])
        return inner_text
    
    @classmethod
    def get_tail_value(cls, node: HtmlElement) -> str:
        return node.tail
    
    @classmethod
    def get_text_value(cls, node: HtmlElement) -> str:
        return node.text
    
    @classmethod
    def set_tail_value(cls, node: HtmlElement, value) -> str:
        node.tail = value
    
    @classmethod
    def set_text_value(cls, node: HtmlElement, value) -> str:
        node.text = value

    @classmethod
    def get_attribute(cls, node: HtmlElement, attr=None):
        if attr:
            attr = node.attrib.get(attr, None)
        if attr:
            attr = unescape(attr)
        return attr

    @classmethod
    def set_attribute(cls, node: HtmlElement, attr=None, value=None):
        if attr and value:
            node.set(attr, value)
            
    @classmethod
    def del_attribute(cls, node: HtmlElement, attr=None):
        if attr:
            _attr = node.attrib.get(attr, None)
            if _attr:
                del node.attrib[attr]

    @classmethod
    def get_children(cls, node: HtmlElement) -> List[HtmlElement] | None:
        "Returns all chlidrens of given node"
        return list(node)

    @classmethod
    def get_parent(cls, node: HtmlElement) -> HtmlElement:
        "Return parent of given node"
        return node.getparent()

    @classmethod
    def get_tag(cls, node: HtmlElement):
        return node.tag

    @classmethod
    def replace_tag(cls, node: HtmlElement, tag: str) -> None:
        node.tag = tag

    @classmethod
    def xpath(cls, root: HtmlElement, expression: Text) -> List[HtmlElement]:
        """Method performs xpath query against th root node.

        Args:
            root (HtmlElement): root node.
            expression (Text): regex expression to ran againts root node

        Returns:
            List[HtmlElement]: list of HtmlElement's.
        """
        regexp_namespace = "http://exslt.org/regular-expressions"
        items = root.xpath(expression, namespaces={"re": regexp_namespace})
        return items

    @classmethod
    def map_children(cls, nodes: List[HtmlElement]) -> Dict[Text, List[HtmlElement]]:
        """The method is responsible for mapping leaves to internal nodes.

        Returns a dictionary where the key is a node and the assigned value is
        a list consisting of the descendants of this node

        Args:
            nodes (List[HtmlElement]): _description_

        Returns:
            Dict[Text, List[HtmlElement]]: _description_
        """

        parents = {}
        for node in nodes:
            parent = cls.get_parent(node)
            if parent is not None:
                if parent not in parents:
                    parents[parent] = []
                if node not in parents.get(parent):
                    parents[parent].append(node)
        return parents

    @classmethod
    def have_childs(cls, node: HtmlElement) -> bool:
        """ Returns True if given node have descedents in first degree.

        Args:
            node (HtmlElement): node for wich che

        Returns:
            bool: _description_
        """
        childs = list(node)
        if childs:
            return True
        return False
            