import sys
import os
import unittest
from unittest.mock import Mock
from typing import List
from threading import Thread

sys.path.append(os.path.abspath(os.curdir))

from core.webpage_queue.queue import WebPageQueue
from core.network.downloader import AsyncDownloader
from core.parser.parser import Parser
from core.parser.lxml_parser import LXMLParser
from api import JustNews


class TestJustNews(unittest.TestCase):
    def setUp(self):
        self.urls = ["https://example.com", "https://example.org"]
        self.producer = AsyncDownloader()

    def test_justnews_initialization(self):
        just_news = JustNews(self.urls)
        self.assertIsInstance(just_news._queue, WebPageQueue)
        self.assertIsInstance(just_news._producer, AsyncDownloader)
        self.assertEqual(just_news._urls, self.urls)
        self.assertIsInstance(just_news._parser, Parser)


    @unittest.skip
    def test_create_threads(self):
        just_news = JustNews()
        just_news._consumers = [self.mock_consumer for _ in range(4)]
        threads = just_news.create_threads()
        self.assertEqual(len(threads), 4)
        for thread in threads:
            self.assertIsInstance(thread, Thread)

    @unittest.skip
    def test_boot_threads(self):
        just_news = JustNews()
        just_news._treads = [Thread(target=lambda: None) for _ in range(1)]
        just_news._queue.subscribe = Mock()
        just_news.boot_threads()
        for thread in just_news._treads:
            self.assertTrue(thread.daemon)
            just_news._queue.subscribe.assert_called_once_with(thread, "item_added")

    def test_process_urls(self):

        self.producer.fetch = Mock()
        just_news = JustNews(urls=self.urls, producer=self.producer)
        just_news.process_urls()
        self.producer.fetch.assert_called_once_with(self.urls, self.queue)


if __name__ == "__main__":
    unittest.main()