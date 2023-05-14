from abc import ABC, abstractmethod
import threading
from ..webpage_queue.queue import Subscriber


class ExtractorInterface(ABC):
    @abstractmethod
    def extract(self):
        pass


class Extractor(Subscriber):
    def __init__(self):
        self.running = False
        
    def update(self, queue) -> None:
        while True:
            page = queue.get()
            print(f"{threading.current_thread().name} przetwarza: {page.article}")

    def run_extraction(self, root):
        return
        
    def handle_result(self, future):
        return