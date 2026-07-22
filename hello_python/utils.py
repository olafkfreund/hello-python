"""Utility functions for the hello_python package."""

from typing import TypeVar

T = TypeVar("T", int, float)


def clamp(value: T, min_value: T, max_value: T) -> T:
    """Constrain a value to a given range.

    Args:
        value: The value to constrain.
        min_value: The minimum allowed value.
        max_value: The maximum allowed value.

    Returns:
        The value constrained to [min_value, max_value].

    Raises:
        ValueError: If min_value > max_value.
    """
    if min_value > max_value:
        raise ValueError(f"min_value ({min_value}) must be <= max_value ({max_value})")
    return max(min_value, min(value, max_value))
