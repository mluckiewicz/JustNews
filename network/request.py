from __future__ import annotations
from typing import List, Text
import asyncio
from aiohttp import ClientSession
from .utils import url_validator, get_random_useragent
from .page import Page


class AsyncDownloader:
    def __init__(self):
        self.cookies = {"CONSENT": "YES+1"}
        self.loop = asyncio.new_event_loop()
        self.pages = None
        self.pages_content = None
        self.headers = get_random_useragent()[0]
        asyncio.set_event_loop(self.loop)

    async def download_site(self, session: ClientSession, url: Text, queue) -> Page:
        """
        Downloads a single webpage using the aiohttp library and returns an instance of
        the Page class.

        Args:
            session (ClientSession): An instance of the aiohttp ClientSession class used
            to make HTTP requests.
            url (Text): A string representing the URL of the webpage to download.

        Returns:
            _type_: An instance of the Page class containing the downloaded webpage's
            information, including the URL, HTTP status code, and raw HTML.
        """

        async with session.get(
            url,
            headers={"User-Agent": f"{self.headers}"},
            ssl=False,
            cookies=self.cookies,
        ) as response:
            page = Page()
            page.url = url
            page.status_code = response.status
            page.raw_html = await response.text(errors="ignore")
            queue.put(page)
            return await page.get_page()

    async def download_all_sites(self, sites: List[Text], queue) -> asyncio.Future[list]:
        """
        Downloads multiple webpages using the aiohttp library and returns a future 
        object that resolves to a list of instances of the Page class.

        Args:
            sites (List[Text]): A list of URLs representing the webpages to download.

        Returns:
            asyncio.Future[list]: A future object that resolves to a list of instances 
            of the Page class, where each instance contains the downloaded webpage's 
            information, including the URL, HTTP status code, and raw HTML.
        """
        async with ClientSession() as session:
            tasks = []
            for url in sites:
                if url_validator(url):
                    task = asyncio.ensure_future(self.download_site(session, url, queue))
                    tasks.append(task)
            return await asyncio.gather(*tasks, return_exceptions=True)

    def fetch(self, sites: List[Text], queue) -> AsyncDownloader:
        """
        Downloads multiple webpages using the aiohttp library and returns an instance of 
        the AsyncRequest class with downloaded webpage information.

        Args:
            sites (List[Text]): A list of URLs representing the webpages to download.

        Returns:
            AsyncRequest: An instance of the AsyncRequest class containing the 
            downloaded webpage information.
        """
        self.pages = self.loop.run_until_complete(self.download_all_sites(sites, queue))
        self.loop.stop()
        return self

    def get_pages(self) -> List[Page]:
        return self.pages
