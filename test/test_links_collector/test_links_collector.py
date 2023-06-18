import os
import sys

sys.path.append(os.path.abspath(os.curdir))

from core.links_collector.collector import GoogleEngineCollector


s = GoogleEngineCollector("wypadek").extract_links()
