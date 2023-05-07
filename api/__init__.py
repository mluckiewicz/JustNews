from typing import List
import importlib
from config import settings
from core.webpage_queue.queue import WebPageQueue
from core.network.downloader import AsyncDownloader


class JustNews:
    def __init__(self, urls: List[str] = None, queue: WebPageQueue = None) -> None:
        self.urls = urls or self.get_urls()
        self.queue = queue or WebPageQueue()
        
        self.add_subscribers()
        
    def add_subscribers(self):
        for extractor in settings.EXTRACTORS:
            self.queue.subscribe(create_instance(extractor), "item_added")
        
    def get_urls(self) -> List[str]:
        pass
        
    def collect_pages(self):
        downloader = AsyncDownloader()
        downloader.fetch(self.urls, self.queue)
    
    def process_content(self) -> None:
        pass
    
    
def create_instance(class_path: str) -> object:
    """Creates an instance of a class based on the given string that represents its absolute path.

    Args:
        class_path (str): Absolute path to the class declaration, using dot notation.

    Raises:
        AttributeError: If the class name is not found in the module.
        ModuleNotFoundError: If the module specified in the class path is not found.

    Returns:
        object: Instance of the found class.
    """
    try:
        module_path, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        class_obj = getattr(module, class_name)
        return class_obj()
    except (AttributeError, ModuleNotFoundError) as e:
        raise ModuleNotFoundError(f"Error creating instance of class '{class_path}': {e}")


