from __future__ import annotations
import string
import re
import os
import codecs


__all__ = [
    "StringHelper", 
    "ResourceLoader"
]


class StringHelper:
    @staticmethod
    def is_sentance(paragraf: str) -> bool:
        "Sprawdza czy ostat znak tekstu to kropka"
        if isinstance(paragraf, str):
            pattern = re.compile(r"[?.!]$")
            if len(pattern.findall(paragraf)) > 0:
                return True
        return False

    @staticmethod
    def count_sentances(paragraf: str) -> tuple:
        """_summary_

        Args:
            paragraf (str): _description_

        Returns:
            tuple: _description_
        """
        sentences = re.split(r"((?<!\d)\.|\.(?!\d))|([!.?]+)[ $]+", paragraf)
        dots = [dot for dot in sentences if dot in [".", "!", "?"]]
        sentences = [
            sentence for sentence in sentences if sentence not in [".", None, ""]
        ]
        return len(sentences), len(dots)

    @staticmethod
    def remove_punctuation(text: str) -> str:
        """_summary_

        Args:
            text (str): _description_

        Returns:
            str: _description_
        """
        # code taken form
        # http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        trans_table = {ord(c): None for c in string.punctuation}
        if isinstance(text, str):
            text = text.encode("utf-8")
        stripped_input = text.decode("utf-8").translate(trans_table)
        sanitized_text = " ".join(stripped_input.split())

        return sanitized_text

    @staticmethod
    def valid_char_ordinal(c: str) -> bool:
        """The method is responsible for examining whether the byte value of
        the character is within the indicated ranges.
        Based on:
        http://stackoverflow.com/questions/8733233/filtering-out-certain-bytes-in-python
        Args:
            c (str): character to check
        Returns:
            bool: returns True if the value is within the specified range.
            Otherwise false
        """
        # conditions ordered by presumed frequency
        codepoint = ord(c)
        is_valid_char = (
            0x20 <= codepoint <= 0xD7FF
            or codepoint in (0x9, 0xA, 0xD)
            or 0xE000 <= codepoint <= 0xFFFD
            or 0x10000 <= codepoint <= 0x10FFFF
        )
        return is_valid_char

    @staticmethod
    def adjust_string_to_xml(text: str) -> str:
        """_summary_

        Args:
            text (str): _description_

        Returns:
            str: _description_
        """
        return "".join(c for c in text if __class__.valid_char_ordinal(c))


class ResourceLoader(object):
    @staticmethod
    def load_resoruce_file(filename):
        
        if not os.path.isabs(filename):
            dirpath = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(dirpath, 'resources', filename)
        else:
            path = filename
            
        try:
            with codecs.open(path, 'r', 'utf-8') as f:
                content = f.read()
            return content
        except IOError:
            raise IOError("Couldn't open file %s" % path)