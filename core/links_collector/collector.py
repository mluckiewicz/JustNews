from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from core.parser.lxml_parser import LXMLParser
from core.network.utils import get_random_useragent
from core.webpage_queue.webpage import WebPage
from config import settings


class LinksCollectorInterface(ABC):
    pass


class GoogleEngineCollector(LinksCollectorInterface):
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
        The method is responsible for sending the request to the search engine.
        The request contains specific parameters set when the instance object
        was initialized.
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

    def read_html_file(self):
        with open("test.html", "r") as file:
            content = file.readlines()
        return content

    def extract_links(self):
        raw_html = self.send_query()
        n, m = 0, 4  # index values to slice subxpath resault
        root = LXMLParser.fromstring(raw_html)
        links = LXMLParser.xpath(root, '//*[@id="rso"]/descendant::a')

        for link in links:
            page = WebPage()

            url = LXMLParser.get_element_attr_value(link, "href")

            heading = LXMLParser.xpath(
                link,
                'descendant::div[normalize-space(text())][contains(@role,"heading")]',
            )[0].text

            lead = LXMLParser.xpath(
                link,
                'descendant::div[normalize-space(text())][not(contains(@role,"heading"))]',
            )[0].text

            pub_date = LXMLParser.xpath(
                link,
                'descendant::span[normalize-space(text())]',
            )[2].text

            print(heading)
            print(lead)
            print(pub_date)

    def collect_links(self):
        """
        The method is responsible for sending the request to the search engine.
        The request contains specific parameters set when the instance object
        was initialized.
        """

        # Make request
        self._request()

        # Collect search result
        soup = BeautifulSoup(self.response.text, "html.parser")

        # Find all links in div id=search
        anchors = soup.find("div", attrs={"id": "search"}).find_all("a")

        # Process links
        for anchor in anchors:
            # ?
            # Czy nie lepiej by było aby collector zwracał obiekt Page?

            link = anchor.attrs["href"]
            title = anchor.find("div", attrs={"role": "heading"}).text.replace("\n", "")
            date = anchor.find("div", attrs={"style": "bottom:0px"}).text.replace(
                "\xa0", " "
            )

            self.articles.append(
                {
                    "title": title,
                    "link": link,
                    "date": date,
                }
            )
        return self

    def get_news(self):
        """Return all founded articles as list(dict)"""
        if self._check_if_articles():
            return self.articles

    def get_links(self):
        """returns links of collected articles"""
        if self._check_if_articles():
            return [article["link"] for article in self.articles]

    def get_anchors(self):
        return self.articles


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
