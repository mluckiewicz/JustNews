from __future__ import annotations
from typing import List, Text
from queue import Queue
import asyncio
from aiohttp import ClientSession
from config import settings
from core.webpage_queue.webpage import WebPage
from core.network.utils import url_validator, get_random_useragent


class AsyncDownloader:
    def __init__(self):
        self.cookies = settings.COOKIES_CONSENT
        self.loop = asyncio.new_event_loop()
        self.headers = get_random_useragent()[0]
        asyncio.set_event_loop(self.loop)

    async def download_single_site(
        self, session: ClientSession, url: Text, queue: Queue
    ) -> None:
        """Downloads a single webpage using the aiohttp library and returns an instance
        of the Page class.

        Args:
            session (ClientSession): An instance of the aiohttp ClientSession class used
            to make HTTP requests.
            url (Text): A string representing the URL of the webpage to download.

        Returns:
            None
        """

        async with session.get(
            url,
            headers={"User-Agent": f"{self.headers}"},
            ssl=True,
            cookies=self.cookies,
        ) as response:
            page = WebPage()
            page.url = url
            page.status_code = response.status
            page.raw_html = await response.text(errors="ignore")
            await queue.put(page) #send notification to queue subscribers

    async def download_all_sites(self, sites: List[str], queue: Queue) -> None:
        """ Downloads the contents of a list of sites using asyncio and adds them to a 
        queue.
        
        In each iteration pops one url form given list.

        Args:
            sites (List[str]): A list of URLs to download.
            queue (Queue): A queue to add the downloaded site contents to.

        Returns:
            None.

        Raises:
            None.
        """

        async with ClientSession() as session:
            tasks = []
            while len(sites) > 0:
                url = sites.pop()
                if url_validator(url):
                    task = asyncio.ensure_future(
                        self.download_single_site(session, url, queue)
                    )
                    tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)

    def fetch(self, sites: List[Text], queue: Queue) -> None:
        """Downloads multiple webpages using the aiohttp library and returns an instance 
        of the AsyncRequest class with downloaded webpage information.

        Args:
            sites (List[Text]): A list of URLs representing the webpages to download.

        Returns:
            None
        """

        self.loop.run_until_complete(self.download_all_sites(sites, queue))
