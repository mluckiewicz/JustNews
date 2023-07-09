from abc import ABC, abstractmethod
import requests
from core.parser.lxml_parser import LXMLParser
from core.network.utils import get_random_useragent
from core.webpage_queue.webpage import WebPage
from core.text.utils import StringHelper
from config import settings


class LinksCollectorInterface(ABC):
    pass


class GoogleEngineCollector(LinksCollectorInterface):
    """
    A class for collecting webpages using the Google search engine.

    Args:
        query (str): The query string for the search.
        search_engine (str, optional): The URL of the Google search engine. Defaults to "https://www.google.com/search".
        google_domain (str, optional): The Google domain to use. Defaults to "google.pl".
        location_requested (str, optional): The location requested for the search. Defaults to "Poland".
        tbm (str, optional): The type of search results to retrieve. Defaults to "nws".
        num (int, optional): The number of results to return. Defaults to 20.
        start (int, optional): The starting index of the results. Defaults to 0.
        lang (str, optional): The language for the search. Defaults to None.
        gl (str, optional): The Google host for the search. Defaults to None.
        tbs (str, optional): Additional search parameters. Defaults to "qdr:h12,sbd:1".
        proxy (dict, optional): Proxy settings for the requests. Defaults to None.
    """

    __slots__ = [
        "query",
        "search_engine",
        "google_domain",
        "location_requested",
        "tbm",
        "num_results",
        "start",
        "lang",
        "gl",
        "tbs",
        "proxy",
    ]

    def __init__(
        self,
        query: str,
        search_engine: str = "https://www.google.com/search",
        google_domain: str = "google.pl",
        location_requested: str = "Poland",
        tbm: str = "nws",
        num: int = 20,
        start: int = 0,
        lang: str = None,
        gl: str = None,
        tbs: str = "qdr:h12,sbd:1",
        proxy: dict = None,
    ):
        """
        Initializes a GoogleEngineCollector object.

        Args:
            query (str): The query string for the search.
            search_engine (str, optional): The URL of the Google search engine. Defaults to "https://www.google.com/search".
            google_domain (str, optional): The Google domain to use. Defaults to "google.pl".
            location_requested (str, optional): The location requested for the search. Defaults to "Poland".
            tbm (str, optional): The type of search results to retrieve. Defaults to "nws".
            num (int, optional): The number of results to return. Defaults to 20.
            start (int, optional): The starting index of the results. Defaults to 0.
            lang (str, optional): The language for the search. Defaults to None.
            gl (str, optional): The Google host for the search. Defaults to None.
            tbs (str, optional): Additional search parameters. Defaults to "qdr:h12,sbd:1".
            proxy (dict, optional): Proxy settings for the requests. Defaults to None.
        """

        self.user_agent = {"User-Agent": get_random_useragent()[0]}
        self.cookies = settings.COOKIES_CONSENT  # allows to accept policies
        self.q = query.replace(" ", "+")  # query string
        self.search_engine = search_engine
        self.google_domain = google_domain
        self.location_requested = location_requested
        self.tbm = tbm
        self.num = num  # numer of resaults to return
        self.start = start
        self.lang = lang or settings.LANGUAGE
        self.gl = gl or settings.LANGUAGE  # googlehost
        self.tbs = tbs
        self.proxy = proxy
        self.pages = []

    def setup_proxy(self):
        """
        Set up proxy settings for requests.

        Returns:
            dict: Proxy settings.
        """
        proxies = None
        if self.proxy:
            if self.proxy[:5] == "https":
                proxies = {"https": self.proxy}
            else:
                proxies = {"http": self.proxy}
        else:
            proxies = {"http": None, "https": None}
        return proxies

    def send_query(self):
        """
        Send the search query to the Google search engine.

        Returns:
            str: The response text.
        """
        response = requests.get(
            url=self.search_engine,
            headers=self.user_agent,
            params=dict(
                q=self.q,
                google_domain=self.google_domain,
                location_requested=self.location_requested,
                tbm=self.tbm,
                num=self.num,
                start=self.start,
                gl=self.gl,
                hl=self.lang,
                tbs=self.tbs,
            ),
            proxies=self.setup_proxy(),
            cookies=self.cookies,
            timeout=None,
        )
        # Raise Error when response code is not valid
        response.raise_for_status()

        return response.text

    def extract_webpages(self):
        """
        Extract webpages from the search results and store them in the `pages` list.
        For each a tag descendant in container with id equal rso will create WebPage instance.
        In next step will extract href value, tile, description and pubdate.
        """
        raw_html = self.send_query()
        n, m = 0, 4  # index values to slice subxpath resault
        root = LXMLParser.fromstring(raw_html)
        links = LXMLParser.xpath(root, '//*[@id="rso"]/descendant::a')

        for link in links:
            page = WebPage()

            # extraction
            url = LXMLParser.get_element_attr_value(link, "href")

            title = LXMLParser.xpath(
                link,
                'descendant::div[normalize-space(text())][contains(@role,"heading")]',
            )[0].text

            description = LXMLParser.xpath(
                link,
                'descendant::div[normalize-space(text())][not(contains(@role,"heading"))]',
            )[0].text

            pub_date = LXMLParser.xpath(
                link,
                'descendant::span[normalize-space(text())]',
            )[2].text

            # assigment
            page.url = url
            page.article.google_title = title
            page.article.google_description = description
            page.article.google_pubdate = StringHelper.calculate_pubtime(pub_date)
            self.pages.append(page)

    def get_webpages(self):
        self.extract_webpages()
        return self.pages


class GoogleNewsRSSCollector(LinksCollectorInterface):
    def __init__(
        self,
        q: str,
        search_engine: str = "https://news.google.com/rss/search?q",
        num: int = 20,
        start: int = 0,
        hl: str = None,
        gl: str = None,
        ceid: str = None,
        when: str = "1d",
        proxy: dict = None,
    ):
        self.user_agent = {"User-Agent": get_random_useragent()[0]}
        self.cookies = settings.COOKIES_CONSENT  # allows to accept policies
        self.q = q.replace(" ", "+")  # query string
        self.search_engine = search_engine
        self.num = num  # numer of resaults to return
        self.start = start
        self.hl = hl or settings.LANGUAGE
        self.gl = (gl or settings.LANGUAGE).upper()  # googlehost
        self.ceid = ceid or ":".join([(settings.LANGUAGE).upper(), settings.LANGUAGE])
        self.when = when
        self.proxy = proxy
        self.pages = []

    # https://news.google.com/rss/search?q=allintext:(wypadek|zderzenie|kolizja)+when:1d&hl=pl&gl=PL&ceid=PL:pl

    # https://newscatcherapi.com/blog/google-news-rss-search-parameters-the-missing-documentaiton
