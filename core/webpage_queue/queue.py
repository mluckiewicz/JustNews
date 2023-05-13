from __future__ import annotations
from abc import ABC, abstractmethod
from queue import Queue


class Subscriber(ABC):
    @abstractmethod
    def update(self, subject) -> None:
        "Receive update from subject."
        pass


class Subject(ABC):
    "The Subject interface declares a set of methods for managing subscribers."

    @abstractmethod
    def subscribe(self, subscriber, event=None) -> None:
        "Attach an subscriber to the subject."
        pass

    @abstractmethod
    def unsubscribe(self, subscriber, event=None) -> None:
        "Detach an subscriber from the subject."
        pass

    @abstractmethod
    def notify(self, event=None, **kwargs) -> None:
        """
        Notify observers about an event.
        """
        pass


class WebPageQueue(Queue, Subject):
    """A queue that stores instances of WebPage class.
    Producers add items to the queue asynchronously, while consumers retrieve items from
    the queue and perform their operations on them.
    This class inherits from the `Queue` class from builtin module `queue` and
    implements the `Subject` interface for the subscriber pattern.

    Attributes:
        `subscribers (list)`: A list of subscribers to the queue.
        `event_subscribers (dict)`: A dictionary of subscribers for specific events.
        `queue (Queue)`: A queue object used to store WebPage instances.

    Methods:
        `subscribe(subscriber, event=None)`: Adds an subscriber to the list of
            subscribers. If an event is specified, the subscriber is added to the list
            of subscribers for that specific event.
        `unsubscribe(subscriber, event=None)`: Removes an subscriber from the list of
            subscribers. If an event is specified, the subscriber is removed from the
            list of subscribers for that specific event.
        `notify(event=None, **kwargs)`: Notifies all subscribers that an event has
            occurred. If an event is specified, only the subscribers for that specific
            event are notified.
        `put(item)`: Adds an item to the queue and notifies subscribers that an item has
            been added.
        `get()`: Retrieves an item from the queue and notifies subscribers that an item
            has been removed.
    
    Examples:
        >>> class ConcreteSubscriber(Subscriber):
        >>>    def update(self, subject, item) -> None:
        >>>        print(f"Add {item}")
    
        >>> q = WebPageQueue()
        >>> wp1 = Downloader(["https://www.google.com"])
        >>> q.put(wp1)
        >>> q.get()
        <Page(url='https://www.google.com')>
        >>> wp2 = Downloader(["https://www.wikipedia.org"])
        >>> q.subscribe(ConcreteSubscriber(), "item_added")
        >>> q.put(wp2)
        <Add Page(url='https://www.google.com')>
    
    """

    def __init__(self) -> None:
        "Initializes a WebPageQueue object"

        super().__init__()
        self.subscribers = []
        self.event_subscribers = {}

    def subscribe(self, subscriber, event=None) -> None:
        """Adds an observer to the list of subscribers. If an event is specified, the
        observer is added to the list of subscribers for that specific event.

        Args:
            observer (Observer): An observer object to be added to the list of
                subscribers.
            event (str): The name of the event that the observer will be subscribed to.

        Returns:
            None
        """

        if event is None:
            self.subscribers.append(subscriber)
        else:
            if event not in self.event_subscribers:
                self.event_subscribers[event] = []
            self.event_subscribers[event].append(subscriber)

    def unsubscribe(self, subscriber, event=None) -> None:
        """Removes an observer from the list of subscribers. If an event is specified, 
        the observer is removed from the list of subscribers for that specific event.

        Args:
            observer (Observer): An observer object to be removed from the list of
                subscribers.
            event (str): The name of the event that the observer will be unsubscribed from.

        Returns:
            None
        """

        if event is None:
            self.subscribers.remove(subscriber)
        else:
            self.event_subscribers[event].remove(subscriber)

    def notify(self, event=None, **kwargs) -> None:
        """Notifies all subscribers that an event has occurred. If an event is 
        specified, only the subscribers for that specific event are notified.

        Args:
            event (str): The name of the event that has occurred.
            **kwargs: Additional arguments to be passed to the subscribers.

        Returns:
            None
        """
        
        if event is None:
            for subscriber in self.subscribers:
                subscriber.update(self, **kwargs)
        else:
            if event in self.event_subscribers:
                for subscriber in self.event_subscribers[event]:
                    subscriber.update(self, **kwargs)

    def put(self, item) -> None:
        """Adds an item to the queue and notifies subscribers that an item has been 
        added.

        Args:
            item (WebPage): The item to be added to the queue.

        Returns:
            None
        """

        super().put(item)
        self.notify(event="item_added")

    def get(self) -> None:
        """Retrieves an item from the queue and notifies subscribers that an item has Sbeen removed.

        Returns:
            WebPage: The item retrieved from the queue.
        """
        item = super().get()
        self.notify(event="item_removed", item=item)
        return item
