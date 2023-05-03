import os
import sys
import unittest
import asyncio
from unittest.mock import MagicMock, patch
from aiohttp import ClientSession

sys.path.append(os.path.abspath(os.curdir))

from network.downloader import AsyncDownloader

class TestAsyncRequest(unittest.TestCase):
    def setUp(self):
        self.async_request = AsyncDownloader()
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.loop.close()

    @patch('network.utils.url_validator')
    def test_download_all_sites(self, url_validator_mock):
        url_validator_mock.return_value = True

        expected_pages = [
            MagicMock(url='https://www.example.com', status_code=200, raw_html='<html>Example</html>'),
            MagicMock(url='https://www.example.net', status_code=200, raw_html='<html>Another example</html>')
        ]

        async def mock_download_site(*args):
            return expected_pages.pop()

        with patch.object(ClientSession, 'get', new=mock_download_site):
            pages = self.loop.run_until_complete(self.async_request.download_all_sites(['https://www.example.com', 'https://www.example.net']))
            self.assertEqual(len(pages), 2)
            self.assertEqual(pages[0], expected_pages[0])
            self.assertEqual(pages[1], expected_pages[1])

    @patch('network.request.AsyncRequest.download_all_sites')
    def test_fetch(self, download_all_sites_mock):
        expected_pages = [
            MagicMock(url='https://www.example.com', status_code=200, raw_html='<html>Example</html>'),
            MagicMock(url='https://www.example.net', status_code=200, raw_html='<html>Another example</html>')
        ]

        async def mock_download_all_sites(*args):
            return expected_pages

        download_all_sites_mock.return_value = asyncio.Future()
        download_all_sites_mock.return_value.set_result(expected_pages)

        async_request = AsyncDownloader()
        fetched_async_request = async_request.fetch(['https://www.example.com', 'https://www.example.net'])

        self.assertEqual(async_request, fetched_async_request)
        self.assertEqual(async_request.get_pages(), expected_pages)

if __name__ == '__main__':
    unittest.main()
