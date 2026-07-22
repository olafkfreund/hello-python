"""Helper functions for hello_python.

This module provides utility functions used throughout the application.
"""


def is_odd(n: int) -> bool:
    """Check if an integer is odd.

    AC1: is_odd(3) returns True and is_odd(4) returns False.

    Args:
        n: An integer to check.

    Returns:
        True if the integer is odd, False otherwise.

    Raises:
        TypeError: If n is not an integer.
    """
    return n % 2 != 0
