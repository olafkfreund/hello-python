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


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, False),  # AC#2 – zero is even
        (-1, True),  # AC#3 – negative odd
        (-2, False),  # AC#3 – negative even
        (-3, True),  # AC#3 – canonical negative odd
        (-99, True),  # AC#3 – larger negative odd
        (-100, False),  # AC#3 – larger negative even
    ],
)
def test_is_odd_zero_and_negative(n: int, expected: bool) -> None:
    """Test is_odd with zero and negative integers (AC#2, AC#3)."""
    assert is_odd(n) == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "3",  # AC#4 – string
        3.0,  # AC#4 – float
        None,  # AC#4 – None
        [3],  # AC#4 – list
        {"n": 3},  # AC#4 – dict
        (3,),  # AC#4 – tuple
        True,  # AC#4 – bool
    ],
)
def test_is_odd_type_error(invalid_input) -> None:
    """Test that is_odd raises TypeError for non-integer inputs (AC#4)."""
    with pytest.raises(TypeError):
        is_odd(invalid_input)
