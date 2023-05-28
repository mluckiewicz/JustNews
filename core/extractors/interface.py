from __future__ import annotations
from abc import ABC, abstractmethod


class ExtractorInterface(ABC):
    @abstractmethod
    def extract(self):
        pass
    