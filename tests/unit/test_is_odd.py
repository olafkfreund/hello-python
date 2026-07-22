"""Unit tests for the is_odd helper function (AC#1).

These tests exercise the is_odd function behavior directly.
"""

import pytest

from hello_python import is_odd


@pytest.mark.parametrize(
    "n,expected",
    [
        (3, True),  # AC#1 – canonical odd number
        (4, False),  # AC#1 – canonical even number
        (1, True),  # Additional odd number
        (2, False),  # Additional even number
        (99, True),  # Larger odd number
        (100, False),  # Larger even number
    ],
)
def test_is_odd_basic(n: int, expected: bool) -> None:
    """Basic is_odd test for positive integers (AC#1)."""
    assert is_odd(n) == expected
