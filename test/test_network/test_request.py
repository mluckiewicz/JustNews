import os
import sys
import unittest
import asyncio
from unittest.mock import MagicMock, patch, Mock
from aiohttp import ClientSession

sys.path.append(os.path.abspath(os.curdir))

from core.network.downloader import AsyncDownloader
from core.webpage_queue.queue import WebPageQueue


class TestAsyncDownloader(unittest.TestCase):
    def setUp(self):
        self.async_downloader = AsyncDownloader()
        self.loop = asyncio.new_event_loop()
        self.queue = Mock(spec=WebPageQueue)

    def tearDown(self):
        self.loop.close()

    @patch("core.network.utils.url_validator")
    def test_download_all_sites(self, url_validator_mock):
        url_validator_mock.return_value = True

        expected_pages = [
            MagicMock(
                url="https://www.example.com",
                status_code=200,
                raw_html="<html>Example</html>",
            ),
            MagicMock(
                url="https://www.example.net",
                status_code=200,
                raw_html="<html>Another example</html>",
            ),
        ]

        async def mock_download_site(*args):
            return expected_pages.pop()

        with patch.object(ClientSession, "get", new=mock_download_site):
            self.loop.run_until_complete(
                self.async_downloader.download_all_sites(
                    ["https://www.example.net"],
                    self.queue
                )
            )
            self.queue.put.assert_called_once

    @unittest.skip("work in progres")
    @patch("core.network.downloader.AsyncDownloader.download_all_sites")
    def test_fetch(self, download_all_sites_mock):
        expected_pages = [
            MagicMock(
                url="https://www.example.com",
                status_code=200,
                raw_html="<html>Example</html>",
            ),
            MagicMock(
                url="https://www.example.net",
                status_code=200,
                raw_html="<html>Another example</html>",
            ),
        ]

        async def mock_download_all_sites(*args):
            return expected_pages

        download_all_sites_mock.return_value = asyncio.Future()
        download_all_sites_mock.return_value.set_result(expected_pages)

        async_request = AsyncDownloader()
        fetched_async_request = async_request.fetch(
            ["https://www.example.com", "https://www.example.net"], self.queue
        )

        self.assertEqual(async_request, fetched_async_request)
        self.assertEqual(async_request.get_pages(), expected_pages)


if __name__ == "__main__":
    unittest.main()
