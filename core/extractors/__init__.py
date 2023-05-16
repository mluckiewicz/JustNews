from abc import ABC, abstractmethod
import threading
from ..webpage_queue.queue import Subscriber
from core.text.sanitizer import get_chain


class ExtractorInterface(ABC):
    @abstractmethod
    def extract(self):
        pass


class Extractor(Subscriber):
    def __init__(self, text_sanitizer=None) -> None:
        self.text_sanitizer = text_sanitizer or get_chain()

    def update(self, queue) -> None:
        while True:
            page = queue.get()
            text = " text  "
            print(
                f"{threading.current_thread().name} przetwarza: {self.text_sanitizer.clean(text)}"
            )

    def run_extraction(self, root):
        return

    def handle_result(self, future):
        return
