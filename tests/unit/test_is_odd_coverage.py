"""Unit tests for the is_odd helper function with comprehensive coverage.

AC#5: unit tests cover odd, even, zero, negative, and the TypeError case.

This test file demonstrates parametrized test coverage of all required cases.
"""

import pytest

from hello_python import is_odd


@pytest.mark.parametrize(
    "n,expected",
    [
        # Odd numbers
        (3, True),      # AC#5 – canonical odd number
        (1, True),      # AC#5 – small odd number
        (99, True),     # AC#5 – larger odd number
        # Even numbers
        (4, False),     # AC#5 – canonical even number
        (2, False),     # AC#5 – small even number
        (100, False),   # AC#5 – larger even number
        # Zero
        (0, False),     # AC#5 – zero is even
        # Negative numbers
        (-3, True),     # AC#5 – canonical negative odd number
        (-1, True),     # AC#5 – small negative odd number
        (-99, True),    # AC#5 – larger negative odd number
        (-2, False),    # AC#5 – negative even number
        (-4, False),    # AC#5 – negative even number
        (-100, False),  # AC#5 – larger negative even number
    ],
    ids=[
        "odd_3", "odd_1", "odd_99",
        "even_4", "even_2", "even_100",
        "zero",
        "negative_odd_minus3", "negative_odd_minus1", "negative_odd_minus99",
        "negative_even_minus2", "negative_even_minus4", "negative_even_minus100",
    ],
)
def test_is_odd_returns_correct_boolean_for_all_integer_types(n: int, expected: bool) -> None:
    """is_odd returns correct boolean for odd, even, zero, and negative integers (AC#5)."""
    assert is_odd(n) is expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "3",           # AC#5 – string
        3.0,           # AC#5 – float
        None,          # AC#5 – None
        [3],           # AC#5 – list
        {"n": 3},      # AC#5 – dict
        (3,),          # AC#5 – tuple
        True,          # AC#5 – bool (subclass of int, should raise TypeError)
        False,         # AC#5 – bool False (subclass of int, should raise TypeError)
    ],
    ids=[
        "string", "float", "none", "list", "dict", "tuple",
        "bool_true", "bool_false",
    ],
)
def test_is_odd_raises_type_error_for_non_integer_inputs(invalid_input) -> None:
    """is_odd raises TypeError for all non-integer inputs including bool (AC#5)."""
    with pytest.raises(TypeError):
        is_odd(invalid_input)
