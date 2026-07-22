"""Unit tests for is_odd TypeError handling (AC#4).

AC#4: is_odd called with a non-int (e.g. a string) raises TypeError

These tests verify that is_odd properly rejects non-integer inputs with a TypeError.
"""

import pytest

from hello_python import is_odd


class TestIsOddTypeError:
    """Test suite for is_odd TypeError handling."""

    @pytest.mark.parametrize(
        "invalid_input,type_name",
        [
            ("3", "str"),  # String
            (3.14, "float"),  # Float
            (None, "NoneType"),  # None
            ([3], "list"),  # List
            ((3,), "tuple"),  # Tuple
            ({3}, "set"),  # Set
            ({"n": 3}, "dict"),  # Dictionary
            (True, "bool"),  # Boolean (also excluded by isinstance check)
            (False, "bool"),  # Boolean False
        ],
        ids=[
            "string",
            "float",
            "none",
            "list",
            "tuple",
            "set",
            "dict",
            "bool_true",
            "bool_false",
        ],
    )
    def test_is_odd_raises_type_error_for_non_int(self, invalid_input, type_name) -> None:
        """is_odd raises TypeError when called with a non-int type.

        This verifies AC#4 for each relevant non-integer type.
        """
        with pytest.raises(TypeError, match=f"Expected an integer, got {type_name}"):
            is_odd(invalid_input)

    def test_is_odd_type_error_message_content(self) -> None:
        """Verify the TypeError message includes the actual type name."""
        with pytest.raises(TypeError) as exc_info:
            is_odd("not an int")
        assert "Expected an integer" in str(exc_info.value)
        assert "str" in str(exc_info.value)

    def test_is_odd_type_error_with_float(self) -> None:
        """Float input raises TypeError (not converted to int)."""
        with pytest.raises(TypeError):
            is_odd(3.0)

    def test_is_odd_accepts_valid_positive_int(self) -> None:
        """Valid positive int does not raise TypeError (sanity check)."""
        # Verify the function works for valid input
        assert is_odd(3) is True
        assert is_odd(4) is False

    def test_is_odd_accepts_valid_negative_int(self) -> None:
        """Valid negative int does not raise TypeError (sanity check)."""
        # Verify the function works for valid input
        assert is_odd(-3) is True
        assert is_odd(-4) is False

    def test_is_odd_accepts_zero(self) -> None:
        """Zero (valid int) does not raise TypeError (sanity check)."""
        # Verify zero is handled correctly
        assert is_odd(0) is False
