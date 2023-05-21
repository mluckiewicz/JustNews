from abc import ABC, abstractmethod
import threading
from ..webpage_queue.queue import Subscriber
from core.text.text_cleaner import clean_string


class ExtractorInterface(ABC):
    @abstractmethod
    def extract(self):
        pass


class Extractor(Subscriber):
    def __init__(self) -> None:
        pass

    def update(self, queue) -> None:
        while True:
            page = queue.get()
            text = " text  "
            print(
                f"{threading.current_thread().name} przetwarza: {clean_string(text)}"
            )

    def run_extraction(self, root):
        return

    def handle_result(self, future):
        return
