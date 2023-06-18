from __future__ import annotations
from typing import List
from concurrent.futures import ThreadPoolExecutor
from config import settings
from config.utils import create_instance
from core.webpage_queue import WebPageQueue
from core.network.downloader import AsyncDownloader


class JustNews:
    def __init__(
        self,
        urls: List[str] = None,
        queue: WebPageQueue = None,
        producer: AsyncDownloader = None,
        sync=True,
        parser_name: str = None,
    ) -> None:
        self._sync = sync
        self._urls = urls
        self._queue = queue or WebPageQueue()
        self._producer = producer or AsyncDownloader()
        self._consumers = None
        self._treads = None
        self._parser = create_instance(
            settings.PARSAERS.get(parser_name, settings.DEFAULT_PARSER)
        )

    def run(self) -> None:
        """Runs the application using either synchronous or threaded mode.

        If the application is set to run in synchronous mode, it calls the
        `_run_sync()` method. If the application is set to run in threaded mode,
        it calls the `_run_threading()` method.mit

        Returns:
            None.

        Raises:
            None.
        """
        if self._sync:
            self.synchronous_mode()
        else:
            self.threading_mode()

    def synchronous_mode(self) -> None:
        """Runs the application in synchronous mode.

        Returns:
            None.

        Raises:
            None.
        """
        pass

    def threading_mode(self) -> None:
        """
        The threading_mode method initializes a thread pool and subscribes a subscriber
        to a queue.

        It then proceeds to process URLs using the specified threading mode.
        """
        with ThreadPoolExecutor(max_workers=settings.THREADS) as thread_pool:
            subscriber = create_instance(settings.EXTRACTOR, thread_pool, self._parser)
            self._queue.subscribe(subscriber, "item_added")
            self.process_urls()

    def process_urls(self) -> None:
        """Fetches the URLs using the producer and puts them in the queue.

        The method loops while there are URLs left to process. It calls the
        producer's `fetch()` method to fetch the URLs and put them in the queue.
        """

        while len(self._urls) > 0:
            self._producer.fetch(self._urls, self._queue)
