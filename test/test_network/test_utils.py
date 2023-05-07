import unittest
import os
import sys
import re
from typing import List

sys.path.append(os.path.abspath(os.curdir))

from core.network.utils import url_validator, get_random_useragent



class TestURLValidator(unittest.TestCase):
    
    def test_valid_urls(self):
        self.assertTrue(url_validator("http://www.google.com"))
        self.assertTrue(url_validator("https://www.google.com"))
        self.assertTrue(url_validator("ftp://ftp.google.com"))
        self.assertTrue(url_validator("ftps://ftp.google.com"))
        self.assertTrue(url_validator("http://localhost:8000"))
        self.assertTrue(url_validator("https://example.com/foo/bar?a=b&c=d"))
        self.assertTrue(url_validator("https://example.com/foo/bar#baz"))
        
    def test_invalid_urls(self):
        # Missing scheme
        with self.assertRaises(Exception):
            url_validator("example.com")
        # Invalid scheme
        with self.assertRaises(Exception):
            url_validator("ssh://example.com")
        # Missing netlock
        with self.assertRaises(Exception):
            url_validator("http://")
        # Invalid netlock
        with self.assertRaises(Exception):
            url_validator("http://example.com:port")
        # URL too long
        with self.assertRaises(Exception):
            url_validator("http://" + "a" * 2048)
        # Missing URL address
        with self.assertRaises(Exception):
            url_validator("")
            

class TestGetRandomUserAgent(unittest.TestCase):
    
    def test_single_useragent(self):
        user_agent = get_random_useragent(k=1)
        self.assertIsInstance(user_agent[0], str)
        self.assertTrue(re.match(r"^Mozilla/5\.0 \(.*\) AppleWebKit/\d+\.\d+ \(KHTML, like Gecko\) Chrome/\d+\.\d+\.\d+\.\d+ Safari/\d+\.\d+$", user_agent[0]))
    

if __name__ == "__main__":
    unittest.main()