import os
import sys
import unittest
from unittest.mock import Mock

sys.path.append(os.path.abspath(os.curdir))

from core.webpage_queue.queue import WebPageQueue


class MockSubscriber():
    def __init__(self):
        self.update = Mock() 


class WebPageQueueTestCase(unittest.TestCase):
    def setUp(self):
        self.queue = WebPageQueue()

    def test_subscribe(self):
        subscriber = MockSubscriber()
        self.queue.subscribe(subscriber)
        self.assertIn(subscriber, self.queue.subscribers)

    def test_unsubscribe(self):
        subscriber = MockSubscriber()
        self.queue.subscribe(subscriber)
        self.queue.unsubscribe(subscriber)
        self.assertNotIn(subscriber, self.queue.subscribers)

    def test_notify_no_event(self):
        subscriber1 = MockSubscriber()
        subscriber2 = MockSubscriber()
        self.queue.subscribe(subscriber1)
        self.queue.subscribe(subscriber2)
        self.queue.notify()
        subscriber1.update.assert_called_with(self.queue)
        subscriber2.update.assert_called_with(self.queue)

    def test_notify_with_event(self):
        subscriber1 = MockSubscriber()
        subscriber2 = MockSubscriber()
        self.queue.subscribe(subscriber1, "item_added")
        self.queue.subscribe(subscriber2, "item_removed")
        self.queue.notify(event="item_added", item="example.com")
        subscriber1.update.assert_called_once_with(self.queue, item="example.com")
        subscriber2.update.assert_not_called()

    def test_put(self):
        subscriber = MockSubscriber()
        self.queue.subscribe(subscriber, "item_added")
        self.queue.put("example.com")
        subscriber.update.assert_called_once_with(self.queue, item="example.com")

    def test_get(self):
        item = "example.com"
        self.queue.put(item)
        self.assertEqual(self.queue.get(), item)


if __name__ == '__main__':
    unittest.main()

