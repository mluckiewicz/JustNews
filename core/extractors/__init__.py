from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
import threading
from core.parser.parser import Parser
from core.webpage_queue.queue import WebPageQueue, Subscriber
from core.webpage_queue.webpage import WebPage
from config import settings
from config.utils import create_instance


class Extractor(Subscriber):
    def __init__(self, thread_pool: ThreadPoolExecutor, parser: Parser) -> None:
        self.thread_pool = thread_pool
        self.parser = parser

    def update(self, web_queue: WebPageQueue) -> None:
        self.thread_pool.submit(self.extract, web_queue.get())

    def extract(self, page: WebPage) -> object:
        print(
            f"Przetwarzam element: {page} wątkiem o identyfikatorze: {threading.get_ident()}"
        )

        root = self.parser.fromstring(page.raw_html)

        # mapping extractor to article attr
        for extractor_name, extractor_settings in settings.EXTRACTORS.items():
            # check if extractor settings ar ok
            if not ("extractor" in extractor_settings
                 and "article_attr" in extractor_settings):
                raise AttributeError(f"Extractor: {extractor_name} dont implement extracor or article_attr setting.")

            # assign name of article property to return data after extraction
            article_attr = extractor_settings["article_attr"]

            # check if article has correct property
            if hasattr(page.article, article_attr):
                extractor = create_instance(
                    settings.EXTRACTORS[extractor_name]["extractor"], root, self.parser
                )
                setattr(page.article, article_attr, extractor.extract())