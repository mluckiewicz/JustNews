from __future__ import annotations
from typing import List
from config import settings
from .utils import StringHelper, ResourceLoader


class Stopwords:
    def __init__(self, lang: str) -> None:
        self.lang = lang or settings.LANGUAGE.lower()
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
        _file = f"stopwords_{self.lang}.txt"
        _content = ResourceLoader.load_resoruce_file(_file)
        self._stopwords = [word.strip() for word in _content]
        
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
