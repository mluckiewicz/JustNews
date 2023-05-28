from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
import threading
from core.parser.parser import Parser
from core.extractors.content import ContentExtractor
from core.webpage_queue.queue import WebPageQueue, Subscriber
from core.webpage_queue.webpage import WebPage
from core.cleaner.dom_cleaner import DocumentCleaner


class Extractor(Subscriber):
    def __init__(self, thread_pool: ThreadPoolExecutor, parser: Parser) -> None:
        self.thread_pool = thread_pool
        self.parser = parser
        
    def update(self, web_queue: WebPageQueue) -> None:
        self.thread_pool.submit(self.extract, web_queue.get())
        
    def extract(self, page: WebPage) -> object:
        print(f"Przetwarzam element: {page} wątkiem o identyfikatorze: {threading.get_ident()}")
        cleaner = DocumentCleaner()
        root = self.parser.fromstring(page.raw_html)
        cleaned = cleaner.execute(root, self.parser)
        page.article.content = ContentExtractor().extract(cleaned, self.parser)
        print(page.article.content)
        print('\n')