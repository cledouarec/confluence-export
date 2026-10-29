#! python3

"""Utilities functions."""

from typing import Any


def force_list(value: Any) -> list:
    """Convert `value` to list or return `value` if it is already a list.

    Args:
        value: Value to convert to list.

    Returns:
        The `value` converted to list.
    """
    return list(value) if isinstance(value, (list, tuple)) else [value]


def keys_exists(element: dict, *keys) -> bool:
    """Check if *keys (nested) exists in `element` (dict).

    Args:
        element: Dictionary to check.
        *keys: Dictionary keys to search.

    Returns:
        True if all nested keys found or False in other cases.

    Raises:
        TypeError: If input element is not a dictionary.
        AttributeError: If no keys are given.
    """
    if not isinstance(element, dict):
        msg = "keys_exists() expects dict as first argument."
        raise TypeError(msg)
    if len(keys) == 0:
        msg = "keys_exists() expects at least two arguments, one given."
        raise AttributeError(msg)

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True
