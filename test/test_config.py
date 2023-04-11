import sys
import os
import unittest

sys.path.append(os.path.abspath(os.curdir))

from config import SettingsProxy


class TestSettings(unittest.TestCase):
    
    def test_singleton(self):
        """
        Test if the class is a singleton.
        """
        s1 = SettingsProxy()
        s2 = SettingsProxy()
        self.assertEqual(id(s1._SETTINGS), id(s2._SETTINGS))



if __name__ == "__main__":
    unittest.main()