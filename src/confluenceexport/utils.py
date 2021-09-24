#! python3

"""
Utilities functions.
"""

from typing import Any


def force_list(value: Any) -> list:
    """
    Convert `value` to list or return `value` if it is already a list.

    :param value: Value to convert to list.
    """
    return list(value) if isinstance(value, (list, tuple)) else [value]


def keys_exists(element: dict, *keys) -> bool:
    """
    Check if *keys (nested) exists in `element` (dict).

    :param element: Dictionary to check.
    :param keys: Dictionary keys to search.
    :return: True if all nested keys found or False in other cases.
    :raises Exception: if input element or keys are invalid.
    """
    if not isinstance(element, dict):
        raise AttributeError("keys_exists() expects dict as first argument.")
    if len(keys) == 0:
        raise AttributeError(
            "keys_exists() expects at least two arguments, one given."
        )

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True
