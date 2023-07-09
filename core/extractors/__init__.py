from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
import threading
from core.parser.parser import Parser
from core.webpage_queue.queue import WebPageQueue, Subscriber
from core.webpage_queue.webpage import WebPage
from config import settings
from config.utils import create_instance


class Extractor(Subscriber):
    def __init__(self, thread_pool: ThreadPoolExecutor, parser: Parser, resaults_container: list) -> None:
        self.thread_pool = thread_pool
        self.parser = parser
        # use list reference
        self.resaults_container = resaults_container

    def update(self, web_queue: WebPageQueue) -> None:
        future = self.thread_pool.submit(self.extract, web_queue.get())
        self.resaults_container.append(future.result())

    def extract(self, page: WebPage) -> object:
        root = self.parser.fromstring(page.raw_html)

        # mapping extractor to article attr
        for extractor_name, extractor_settings in settings.EXTRACTORS.items():
            # check if extractor settings ar ok
            if not (
                "extractor" in extractor_settings
                and "article_attr" in extractor_settings
            ):
                raise AttributeError(
                    f"Extractor: {extractor_name} dont implement extracor or article_attr setting."
                )

            # assign name of article property to return data after extraction
            article_attr = extractor_settings["article_attr"]

            # check if article has correct property
            if hasattr(page.article, article_attr):
                extractor = create_instance(
                    settings.EXTRACTORS[extractor_name]["extractor"], root, self.parser
                )
                setattr(page.article, article_attr, extractor.extract())

        return page
