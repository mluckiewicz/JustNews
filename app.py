from api import JustNews
urls = [
    "http://quotes.toscrape.com/random",
    "https://webscraper.io/test-sites/e-commerce/allinone",
] 

jn = JustNews(urls=urls)
jn.collect_pages()
