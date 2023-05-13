from abc import ABC, abstractmethod
import time
from ..webpage_queue.queue import Subscriber
import threading


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
            print(f"{threading.current_thread().name} przetwarza: {page}")

    def process_page(self, page):
        # code to process the page
        #print(f"processing {page}")
        return
        
    def handle_result(self, future):
        # code to handle the result of the processed page
        #print("handle processing resault")
        return