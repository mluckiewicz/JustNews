from typing import List, Type
import importlib
from threading import Thread
from config import settings
from core.webpage_queue.queue import WebPageQueue
from core.network.downloader import AsyncDownloader


class JustNews:
    def __init__(
        self,
        urls: List[str] = None,
        queue: WebPageQueue = None,
        producer: AsyncDownloader = None,
        sync=True,
    ) -> None:
        self._sync = sync
        self._urls = urls
        self._queue = queue or WebPageQueue()
        self._producer = producer or AsyncDownloader()

        self._consumers = None
        self._treads = None

    def run(self) -> None:
        """Runs the application using either synchronous or threaded mode.

        If the application is set to run in synchronous mode, it calls the
        `_run_sync()` method. If the application is set to run in threaded mode,
        it calls the `_run_threading()` method.

        Returns:
            None.

        Raises:
            None.
        """
        if self._sync:
            self._run_synchronous_mode()
        else:
            self._run_threading_mode()

    def _run_synchronous_mode(self) -> None:
        """Runs the application in synchronous mode.

        Returns:
            None.

        Raises:
            None.
        """    
    
        pass

    def _run_threading_mode(self) -> None:
        """Runs the application in threaded mode.

        Creates a list of consumers using the `create_consumers()` method,
        creates a list of threads using the `create_threads()` method, and
        boots the threads using the `boot_threads()` method. Finally, it
        processes the URLs using the `process_urls()` method.

        Returns:
            None.

        Raises:
            None.
        """
        
        self._consumers = JustNews.create_consumers()
        self._treads = self.create_threads()
        self.boot_threads()
        self.process_urls()

    @staticmethod
    def create_consumers() -> List[object]:
        """This method creates a list of consumer instances based on the `settings.EXTRACTOR` setting and the number of threads specified in `settings.THREADS`.

        Args:
            None

        Returns:
            A list of consumer instances.

        Raises:
            None
        """

        return [create_instance(settings.EXTRACTOR) for _ in range(settings.THREADS)]

    def create_threads(self) -> List[Thread]:
        """Creates a list of threads, each running a consumer's update method.

        The update method of each consumer is called in a separate thread,
        with a reference to the shared queue instance passed as a keyword argument.

        Returns:
            A list of `Thread` instances, each running a consumer's update method.

        Raises:
            None.
        """
        
        return [
            Thread(target=consumer.update, kwargs={"queue": self._queue})
            for consumer in self._consumers
        ]

    def boot_threads(self) -> None:
        """Starts all the threads and subscribes them to the queue's "item_added" event.

        For each thread in the list of threads, sets the `daemon` flag to `True`,
        starts the thread, and subscribes it to the queue's "item_added" event.
        This event will be triggered every time an item is added to the queue.

        Returns:
            None.

        Raises:
            None.
        """
        
        for thread in self._treads:
            thread.daemon = True
            thread.start()
            self._queue.subscribe(thread, "item_added")

    def process_urls(self) -> None:
        """Fetches the URLs using the producer and puts them in the queue.

        The method loops while there are URLs left to process. It calls the
        producer's `fetch()` method to fetch the URLs and put them in the queue.

        Returns:
            None.

        Raises:
            None.
        """
        
        while len(self._urls) > 0:
            self._producer.fetch(self._urls, self._queue)


def create_instance(class_path: str) -> Type[object]:
    """Creates an instance of a class based on the given string that represents its absolute path.

    Args:
        class_path (str): Absolute path to the class declaration, using dot notation.

    Raises:
        AttributeError: If the class name is not found in the module.
        ModuleNotFoundError: If the module specified in the class path is not found.

    Returns:
        Type[object]: Instance of the found class.
    """

    try:
        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        class_obj = getattr(module, class_name)
        return class_obj()
    except (AttributeError, ModuleNotFoundError) as e:
        raise ModuleNotFoundError(
            f"Error creating instance of class '{class_path}': {e}"
        )
