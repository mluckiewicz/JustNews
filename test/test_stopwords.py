import sys
import os
import unittest

sys.path.append(os.path.abspath(os.curdir))

from core.text.stopwords import Stopwords


class TestStopwords(unittest.TestCase):

    def test_setting_lang(self):
        
        " Testing default language default value "
        
        sw = Stopwords('pl')
        self.assertEqual(sw.lang, 'pl')
        
    def test_setting_stopwords(self):
        sw_pl = Stopwords('pl')
        sw_en = Stopwords('en')
        self.assertEqual(len(sw_pl.stopwords), 350)
        self.assertEqual(len(sw_en.stopwords), 358)
        
    def test_init_method_setting_lang(self):
        
        " Testing raseing error after passing language name "
        
        self.assertRaises(FileNotFoundError, Stopwords, 'hr')
        self.assertRaises(FileNotFoundError, Stopwords, '')
        self.assertRaises(FileNotFoundError, Stopwords, 'jaja')
        
    def test_count(self):
        
        " Testing count method"
        
        sw_pl = Stopwords('pl')
        self.assertEqual(sw_pl.count("Że, że, że"), 3)
        self.assertEqual(sw_pl.count("To jest testowe zdanie."), 2)
        self.assertEqual(sw_pl.count("Jan Nowak"), 0)
        self.assertEqual(sw_pl.count("Owoc był nader słodki."), 1)


if __name__ == "__main__":
    unittest.main()
