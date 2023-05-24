import sys
import unittest
import os

sys.path.append(os.path.abspath(os.curdir))

from core.text.text_cleaner import (
    TrimTokens,
    RemoveWhiteSpaces,
    RemoveMultipleSpaces,
    TrimString,
    RemoveSpacesBeforePunctuation,
    clean_string
)

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class TestTrimTokens(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.handler = TrimTokens()
        
    def test_clean_removed(self):
        to_clean = "   test Case   string   , to clean    "
        self.assertEqual(
            self.handler.clean(to_clean), 
            "test Case string , to clean"
            )
        
    def test_clean_none(self):
        to_clean = None
        self.assertEqual(
            self.handler.clean(to_clean), 
            None
            )
        
    def test_clean_zero_len(self):
        to_clean = ""
        self.assertEqual(
            self.handler.clean(to_clean), 
            ""
            )
        

class TestRemoveWhiteSpaces(unittest.TestCase):
    def setUp(self) -> None:
        self.maxdiff = None
        self.handler = RemoveWhiteSpaces()
        
    def test_replace_n_single_positive(self):
        to_clean = "this is test\n case string"
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test  case string"
        )
        
    def test_replace_n_multiple_test_replace_n_single_positive(self):
        to_clean =  "this is test\n case\n\n string"
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test  case   string"
        )
        
    def test_replace_t_single_positive(self):
        to_clean = "this is test\t case string"
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test  case string"
        )
        
    def test_replace_rn_positive(self):
        to_clean = "this is test\r\n case string"
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test   case string"
        )
        
    def test_replace_nbsp_positive(self):
        to_clean = "this is test&nbsp; case string"
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test  case string"
        )     
            
            
class TestRemoveMultipleSpaces(unittest.TestCase):
    def setUp(self) -> None:
        self.maxdiff = None
        self.handler = RemoveMultipleSpaces()
        
    def test_replace_front_positive(self):
        to_clean = "    this is test case string"
        self.assertEqual(
            self.handler.clean(to_clean),
            " this is test case string"
        )
        
    def test_replace_middle_positive(self):
        to_clean = "this   is test case string"
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test case string"
        )
        
    def test_replace_rear_positive(self):
        to_clean = "this is test case string     "
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test case string "
        )
        
    def test_replace_multiple_indexes_positive(self):
        to_clean = "this   is test   case string  "
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test case string "
        )
        

class TestTrimString(unittest.TestCase):
    def setUp(self) -> None:
        self.maxdiff = None
        self.handler = TrimString()
        
    def test_replace_multiplespace_front_positive(self):
        to_clean = "    this is test case string"
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test case string"
        )
        
    def test_replace_multiplespace_rear_positive(self):
        to_clean = "this is test case string     "
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test case string"
        )
        
    def test_replace_single_front_rear_positive(self):
        to_clean = " this is test case string "
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test case string"
        )
        

class TestRemoveSpacesBeforePunctuation(unittest.TestCase):
    def setUp(self) -> None:
        self.maxdiff = None
        self.handler = RemoveSpacesBeforePunctuation()
        
    def test_replace_before_punct_at_end_positive(self):
        to_clean = "this is test case string ."
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test case string."
        )
        
 
class TestCleaningTextContext(unittest.TestCase):
    def setUp(self) -> None:
        self.maxdiff = None
        
    def test_clean_string(self):
        to_clean = "this is test    case string ."
        self.assertEqual(
            clean_string(to_clean),
            "this is test case string."
        )
                
if __name__ == '__main__':
    unittest.main()
        