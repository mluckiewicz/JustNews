from __future__ import annotations
from typing import List
from concurrent.futures import ThreadPoolExecutor
from config import settings
from config.utils import create_instance
from core.webpage_queue import WebPageQueue, WebPage
from core.network.downloader import AsyncDownloader


class JustNews:
    def __init__(
        self,
        urls: List[str] | List[WebPage] = None,
        queue: WebPageQueue = None,
        producer: AsyncDownloader = None,
        sync: bool = True,
        parser_name: str = None,
    ) -> None:
        self.sync = sync
        self.urls = urls  # rename variable to be more specific
        self.queue = queue or WebPageQueue()
        self.producer = producer or AsyncDownloader()
        self.parser = create_instance(
            settings.PARSAERS.get(parser_name, settings.DEFAULT_PARSER)
        )
        self.resaults = []

    @property
    def resaults(self):
        return self._resaults

    @resaults.setter
    def resaults(self, value):
        self._resaults = value

    @property
    def urls(self):
        return self._urls

    @urls.setter
    def urls(self, value):
        if any([isinstance(item, str) for item in value]):
            # Conversion urls to an Webpage
            self._urls = [WebPage(url=url) for url in value]
        else:
            self._urls = value

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

        if self.sync:
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
        raise NotImplementedError("Sync mode is in development stage")

    def threading_mode(self) -> None:
        """
        The threading_mode method initializes a thread pool and subscribes a subscriber
        to a queue.

        It then proceeds to process URLs using the specified threading mode.
        """
        with ThreadPoolExecutor(max_workers=settings.THREADS) as thread_pool:
            subscriber = create_instance(
                settings.EXTRACTOR, thread_pool, self.parser, self.resaults
            )
            self.queue.subscribe(subscriber, "item_added")
            self.process_urls()

    def process_urls(self) -> None:
        """Fetches the URLs using the producer and puts them in the queue.

        The method loops while there are URLs left to process. It calls the
        producer's `fetch()` method to fetch the URLs and put them in the queue.
        """

        while len(self.urls) > 0:
            self.producer.fetch(self.urls, self.queue)
