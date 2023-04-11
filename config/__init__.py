from __future__ import annotations
from typing import Any
import threading
import importlib


class Settings:
    """
    Singleton class that loads settings from a module.
    """

    _INSTANCE = None
    _SEMAPHORE = threading.Semaphore(value=1)

    def __new__(cls, settings_module) -> Settings:
        """
        Method in the Settings class checks if an instance already exists, and if so, 
        the instance is already visible. If it doesn't exist, there is a new instance of 
        the Settings class and they are loaded into multiple settings with the settings 
        module.
        """
        if not cls._INSTANCE:
            cls._SEMAPHORE.acquire()
            if not cls._INSTANCE:
                cls._INSTANCE = super().__new__(cls)
                cls._INSTANCE.__load_config(settings_module)
            cls._SEMAPHORE.release()
        return cls._INSTANCE

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value

    def __load_config(self, settings_module) -> None:
        _settings = importlib.import_module(settings_module)

        for setting in dir(_settings):
            if setting.isupper():
                setattr(self, setting, getattr(_settings, setting))


class SettingsProxy:
    """
    A proxy class for accessing Settings Singelton instance.
    """
    _SETTINGS = None

    def __init__(self, settings_module: str = None) -> SettingsProxy:
        if self._SETTINGS is None:
            if settings_module is not None:
                self._SETTINGS = Settings(settings_module)
            self._SETTINGS = Settings("settings")

    def __getattr__(self, name):
        value = self._SETTINGS.__dict__.get(name)
        self.__dict__[name] = value
        return value


if __name__ == "__main__":
    s1 = SettingsProxy()
    s2 = SettingsProxy()

    if id(s1._settings) == id(s2._settings):
        print("Singleton działa, obie zmienne mają tę samą instancję.")
    else:
        print("Singleton nie działa, obie zmienne mają różne instancje.")

    print(s1.CONSTANT_ONE)
    print(s1.CONSTANT_TWO)
