from __future__ import annotations
from typing import Text


class Page:
    def __init__(self):
        self.url: Text = None
        self.status_code: int = None
        self.raw_html: Text = None
        
    @property
    def raw_html(self) -> Text:
        return self._raw_html
    
    @raw_html.setter
    def raw_html(self, value):
        self._raw_html = value
        
    @property
    def status_code(self) -> int:
        return self._status_code
    
    @status_code.setter
    def status_code(self, value):
        self._status_code = value
        
    def __repr__(self):
        return f'Page(url={self.url}), status_code={self.status_code}'
                
    async def get_page(self) -> Page:
        return self