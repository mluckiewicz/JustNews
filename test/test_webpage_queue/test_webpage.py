import os
import sys
import unittest
from unittest.mock import MagicMock, patch
from queue import Empty

sys.path.append(os.path.abspath(os.curdir))

from webpage_queue.webpage import WebPage


class TestWebPage(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.web_page = WebPage()
        
    def test_init(self) -> None:
        self.assertIsNone(self.web_page.url)
        self.assertIsNone(self.web_page.status_code)
        self.assertIsNone(self.web_page.raw_html)
        self.assertIsNone(self.web_page.article)
        
    def test_repr(self) -> None:
        self.web_page.url = 'https://example.com'
        self.web_page.status_code = 200
        self.assertEqual(repr(self.web_page), "Page(url=https://example.com), status_code=200")
        
    @patch('webpage_queue.webpage.WebPage.get_page', new_callable=MagicMock)
    async def test_get_page(self, mock_get_page) -> None:
        mock_get_page.return_value = self.web_page
        page = self.web_page.get_page()
        self.assertIs(page, self.web_page)
        mock_get_page.assert_called_once()
        
if __name__ == '__main__':
    unittest.main()