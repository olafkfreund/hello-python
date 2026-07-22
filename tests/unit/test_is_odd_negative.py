"""Unit tests for the is_odd helper function with negative integers (AC#3).

AC#3: is_odd(-3) returns True for negative odd integers.

These tests verify that the is_odd function correctly identifies negative odd
integers, ensuring the modulo operation works correctly for negative numbers.
"""

import pytest

from hello_python import is_odd


@pytest.mark.parametrize(
    "n,expected",
    [
        (-3, True),   # AC#3 – canonical negative odd
        (-1, True),   # AC#3 – smallest negative odd
        (-99, True),  # AC#3 – larger negative odd
        (-2, False),  # Negative even (control)
        (-4, False),  # Negative even (control)
        (-100, False),  # Larger negative even (control)
    ],
)
def test_is_odd_negative_integers(n: int, expected: bool) -> None:
    """Test is_odd returns correct value for negative integers (AC#3).

    Verifies that is_odd(-3) returns True and correctly distinguishes
    negative odd from negative even integers.
    """
    assert is_odd(n) == expected


def test_is_odd_negative_three_returns_true() -> None:
    """Explicit test: is_odd(-3) returns True (AC#3)."""
    assert is_odd(-3) is True


def test_is_odd_negative_one_returns_true() -> None:
    """Explicit test: is_odd(-1) returns True (AC#3)."""
    assert is_odd(-1) is True


def test_is_odd_negative_two_returns_false() -> None:
    """Explicit test: is_odd(-2) returns False (boundary case)."""
    assert is_odd(-2) is False
