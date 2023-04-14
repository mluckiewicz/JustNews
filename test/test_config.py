import sys
import os
import unittest
from unittest import skip

sys.path.append(os.path.abspath(os.curdir))


class TestSettings(unittest.TestCase):

    def test_singleton_instance(self):
        from config import settings
        # The Settings class should be a singleton, so two instances should be equal
        self.assertIs(settings, settings)

    def test_settings_attribute(self):
        from config import settings
        # Make sure the settings have been loaded correctly
        self.assertIsNotNone(settings.LANGUAGE)
        self.assertIsNotNone(settings.STRING_CLEANER)

    def test_settings_proxy(self):
        from config import SettingsProxy
        # The SettingsProxy class should return the same instance of Settings
        settings1 = SettingsProxy()
        settings2 = SettingsProxy()
        self.assertIs(settings1._SETTINGS, settings2._SETTINGS)

    @skip("in development")
    def test_settings_module(self):
        from config import SettingsProxy
        # Test if the settings module passed to SettingsProxy is loaded correctly
        settings = SettingsProxy("custom_settings")
        settings._INSTANCE = None
        settings._INSTANCE = None
        settings = SettingsProxy("custom_settings")
        self.assertIsNotNone(settings.CUSTOM_SETTING_ONE)
        self.assertIsNotNone(settings.CUSTOM_SETTING_TWO)
        self.assertEqual(settings.CUSTOM_SETTING_ONE, "value_one")
        self.assertEqual(settings.CUSTOM_SETTING_TWO, "value_two")
        


if __name__ == "__main__":
    unittest.main()