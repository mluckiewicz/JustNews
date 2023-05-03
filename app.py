from core.webpage_queue.queue import WebPageQueue, Subscriber
from core.network.downloader import AsyncDownloader


class TestSub(Subscriber):
    def update(self, subject, item) -> None:
        print(f"coś się zadziało w kolejce {item}")
        
        
concrete_sub = TestSub()

queue = WebPageQueue()
queue.subscribe(concrete_sub, "item_added")

downloader = AsyncDownloader()

url = [
    "http://quotes.toscrape.com/random",
    "https://webscraper.io/test-sites/e-commerce/allinone",
] 

downloader.fetch(url, queue)

print(queue.get())
