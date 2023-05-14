import sys
import os
import unittest
from unittest.mock import Mock
from typing import List
from threading import Thread

sys.path.append(os.path.abspath(os.curdir))

from core.webpage_queue.queue import WebPageQueue
from core.network.downloader import AsyncDownloader
from core.extractors import Extractor
from api import JustNews


class TestJustNews(unittest.TestCase):
    def setUp(self):
        self.urls = ["https://example.com", "https://example.org"]
        self.queue = WebPageQueue()
        self.producer = AsyncDownloader()
        self.mock_consumer = Mock()
        self.mock_consumer.update.return_value = None
        self.mock_consumer_instance = Mock()
        self.mock_consumer_instance.return_value = self.mock_consumer

    def test_create_consumers(self):
        just_news = JustNews()
        just_news.create_instance = self.mock_consumer_instance
        consumers = just_news.create_consumers()
        self.assertEqual(len(consumers), 8)  # assuming settings.THREADS = 8
        for consumer in consumers:
            self.assertIsInstance(consumer, Extractor)

    def test_create_threads(self):
        just_news = JustNews()
        just_news._consumers = [self.mock_consumer for _ in range(4)]
        threads = just_news.create_threads()
        self.assertEqual(len(threads), 4)
        for thread in threads:
            self.assertIsInstance(thread, Thread)

    def test_boot_threads(self):
        just_news = JustNews()
        just_news._treads = [Thread(target=lambda: None) for _ in range(1)]
        just_news._queue.subscribe = Mock()
        just_news.boot_threads()
        for thread in just_news._treads:
            self.assertTrue(thread.daemon)
            just_news._queue.subscribe.assert_called_once_with(thread, "item_added")

    @unittest.skip
    def test_process_urls(self):
        just_news = JustNews(urls=self.urls, queue=self.queue, producer=self.producer)
        self.producer.fetch = Mock()
        just_news.process_urls()
        self.producer.fetch.assert_called_once_with(self.urls, self.queue)
        
        
if __name__ == "__main__":
    unittest.main()