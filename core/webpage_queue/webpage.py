from __future__ import annotations
from typing import Text
from ..article import Article


class WebPage:
    """
    Represents a web page and its properties.

    Attributes:
        url (str): The URL of the web page.
        status_code (int): The HTTP status code returned by the server when accessing the page.
        raw_html (str): The raw HTML content of the page.

    Methods:
        __init__(self): Initializes a new Page object with default properties.
        __repr__(self): Returns a string representation of the Page object.
        get_page(self): Returns a Page object with updated properties.
    """
    def __init__(self):
        self.url: str = None
        self.status_code: int = None
        self.raw_html: str = None
        self.article: object = None
        
    @property
    def raw_html(self) -> str:
        return self._raw_html
    
    @raw_html.setter
    def raw_html(self, value: str) -> None:
        self._raw_html = value
        
    @property
    def status_code(self) -> int:
        return self._status_code
    
    @status_code.setter
    def status_code(self, value: int) -> None:
        self._status_code = value
        
    @property
    def article(self) -> None:
        return self._article
    
    @article.setter
    def article(self, value):
        self._article = value or Article()
        
    def __repr__(self) -> str:
        return f'Page(url={self.url}), status_code={self.status_code}'
                
    async def get_page(self) -> WebPage:
        return self