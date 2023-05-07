from abc import ABC, abstractmethod
from ..webpage_queue.queue import Subscriber


class ExtractorInterface(ABC):
    @abstractmethod
    def extract(self):
        pass


class Extractor(Subscriber):
    def update(self, subject, item) -> None:
        print(f"Extractor: coś się zadziało w kolejce {item}")