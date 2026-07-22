"""Unit tests for is_odd with zero input (AC#2).

AC#2: is_odd(0) returns False

This test verifies that the is_odd function correctly identifies zero as an
even number, returning False.
"""

import pytest

from hello_python import is_odd


def test_is_odd_zero_returns_false() -> None:
    """Test that is_odd(0) returns False (AC#2)."""
    assert is_odd(0) is False


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, False),  # AC#2 – zero is even
        (-2, False),  # Negative even for comparison
        (2, False),  # Positive even for comparison
    ],
    ids=[
        "zero",
        "negative_even",
        "positive_even",
    ],
)
def test_is_odd_even_numbers_return_false(n: int, expected: bool) -> None:
    """Test that is_odd returns False for even numbers including zero (AC#2)."""
    assert is_odd(n) is expected
