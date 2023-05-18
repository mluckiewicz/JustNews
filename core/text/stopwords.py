from __future__ import annotations
from typing import List
import os
from config import settings
from .utils import StringHelper


class Stopwords:
    def __init__(self, lang: str) -> None:
        self.lang = lang or settings.LANGUAGE.lower()
        self.current_path = os.path.dirname(os.path.abspath(" "))
        self.stopwords = None

    @property
    def lang(self) -> str:
        return self._lang       
    
    @lang.setter
    def lang(self, lang: str) -> None:
        self._lang = lang

    @property
    def stopwords(self) -> List[str]:
        return self._stopwords
    
    @stopwords.setter
    def stopwords(self, _):
        
        # TODO Refactor
        resource_path = os.path.join(
            os.path.dirname(self.current_path),
            "news_extractor",
            "src",
            "stopwords",
            f"stopwords_{self.lang}.txt"
            )

        with open(resource_path, encoding='utf-8') as f:
            self._stopwords = [word.strip() for word in f.readlines()]
        
    def count(self, text: str) -> int:
        """ It is responsible for counting the number of stopwords in the submitted text

        Args:
            text (str): text to be searched

        Returns:
            stopwords_count (int): number of words detected 
        """
        stripped_text = StringHelper.remove_punctuation(''.join(text))
        tokkens = stripped_text.strip().split(' ')
        stopwords_count = len([w for w in tokkens if w.lower() in self.stopwords])
        return stopwords_count
        
        
if __name__ == '__main__':
    print(os.path.dirname(os.path.abspath(" ")))