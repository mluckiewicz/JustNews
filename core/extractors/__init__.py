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


        #TODO
        # If i want add new extractor i shouldnt add it directly to and extractor.
        # Maybe there is a way to create concrete extractors in diffrent way.
        # Each one need to know to what article attribiute return value.
        content_extractor = create_instance(
            settings.EXTRACTORS["content_extractor"]["extractor"], root, self.parser
        )
        try:
            title_extractor = create_instance(
            settings.EXTRACTORS["title_extractor"]["extractor"], root, self.parser
            )
        except Exception as e:
            print(e)

        canonical_extractor = create_instance(
            settings.EXTRACTORS["canonical_extractor"]["extractor"], root, self.parser
        )

        page.article.canonical = canonical_extractor.extract()
        page.article.title = title_extractor.extract()
        page.article.content = content_extractor.extract()