from api import JustNews
from core.links_collector.collector import GoogleEngineCollector

query = "wypadek"
#collected_links = GoogleEngineCollector(query=query).get_webpages()
collected_links = [
    "https://swidnica24.pl/2023/07/#wypadek-na-krajowej-piatce-pod-mielecinem-trzy-osoby-trafily-do-szpitala/"
]


jn = JustNews(urls=collected_links, sync=False, parser_name="lxml")
jn.run()

for article in jn.resaults:
    print(article.url)
    print(article.article.content)
    print('\n')
