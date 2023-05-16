import sys
import unittest
from unittest.mock import MagicMock
import lxml
import os

sys.path.append(os.path.abspath(os.curdir))

from core.text.sanitizer import (
    TrimHandler,
    WhiteSpaceHandler,
    MultipleSpaceHandler,
    BoundsHandler,
    BeforePunctuationHandler,
    clean_string
)

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class TestTrimHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.handler = TrimHandler()
        
    def test_trimhandler_clean_removed(self):
        to_clean = "   test Case   string   , to clean    "
        self.assertEqual(
            self.handler.clean(to_clean), 
            "test Case string , to clean"
            )
        
    def test_trimhandler_clean_none(self):
        to_clean = None
        self.assertEqual(
            self.handler.clean(to_clean), 
            None
            )
        
    def test_trimhandler_clean_zero_len(self):
        to_clean = ""
        self.assertEqual(
            self.handler.clean(to_clean), 
            ""
            )
        

class TestWhitespacesHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.maxdiff = None
        self.handler = WhiteSpaceHandler()
        
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
            
            
class TestWhitespacesHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.maxdiff = None
        self.handler = MultipleSpaceHandler()
        
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
        

class TestBoundsHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.maxdiff = None
        self.handler = BoundsHandler()
        
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
        

class TestBeforePunctuationHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.maxdiff = None
        self.handler = BeforePunctuationHandler()
        
    def test_replace_before_punct_at_end_positive(self):
        to_clean = "this is test case string ."
        self.assertEqual(
            self.handler.clean(to_clean),
            "this is test case string."
        )
        
 
class TestCleaningChain(unittest.TestCase):
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
        