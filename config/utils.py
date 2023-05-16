from __future__ import annotations
from typing import Type
import importlib


def create_instance(class_path: str) -> Type[object]:
    """Creates an instance of a class based on the given string that represents its absolute path.

    Args:
        class_path (str): Absolute path to the class declaration, using dot notation.

    Raises:
        AttributeError: If the class name is not found in the module.
        ModuleNotFoundError: If the module specified in the class path is not found.

    Returns:
        Type[object]: Instance of the found class.
    """

    try:
        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        class_obj = getattr(module, class_name)
        return class_obj()
    except (AttributeError, ModuleNotFoundError) as e:
        raise ModuleNotFoundError(
            f"Error creating instance of class '{class_path}': {e}"
        )