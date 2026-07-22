"""Unit tests for the is_palindrome helper function.

Tests cover all acceptance criteria:
- C1: Basic palindrome detection (racecar, "A man a plan a canal Panama")
- C2: Correctly identifies non-palindromes (hello)
- C3: Type validation (TypeError for non-str)
- C4: Pure function behavior (no side effects)
"""

import pytest

from hello_python import is_palindrome


class TestPalindromeDetection:
    """Test basic palindrome detection functionality."""

    def test_simple_palindrome(self) -> None:
        """Simple lowercase palindrome is correctly identified (C1)."""
        assert is_palindrome("racecar") is True

    def test_palindrome_with_spaces_and_case(self) -> None:
        """Palindrome with spaces and mixed case is correctly identified (C1)."""
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_non_palindrome(self) -> None:
        """Non-palindrome string is correctly identified as False (C2)."""
        assert is_palindrome("hello") is False

    def test_single_character(self) -> None:
        """Single character is a palindrome."""
        assert is_palindrome("a") is True

    def test_two_same_characters(self) -> None:
        """Two identical characters form a palindrome."""
        assert is_palindrome("aa") is True

    def test_two_different_characters(self) -> None:
        """Two different characters don't form a palindrome."""
        assert is_palindrome("ab") is False

    def test_empty_string(self) -> None:
        """Empty string is considered a palindrome."""
        assert is_palindrome("") is True

    def test_spaces_only(self) -> None:
        """String with only spaces is considered a palindrome (cleaned to empty)."""
        assert is_palindrome("   ") is True

    def test_case_insensitive(self) -> None:
        """Palindrome detection is case-insensitive."""
        assert is_palindrome("RaceCar") is True
        assert is_palindrome("RACECAR") is True

    def test_palindrome_with_multiple_spaces(self) -> None:
        """Palindrome with multiple spaces between words."""
        assert is_palindrome("A  man  a  plan  a  canal  Panama") is True


class TestTypeValidation:
    """Test type validation and error handling (C3)."""

    def test_integer_raises_typeerror(self) -> None:
        """Non-string argument (int) raises TypeError (C3)."""
        with pytest.raises(TypeError) as exc_info:
            is_palindrome(123)  # type: ignore
        assert "expected str" in str(exc_info.value).lower()

    def test_none_raises_typeerror(self) -> None:
        """Non-string argument (None) raises TypeError (C3)."""
        with pytest.raises(TypeError) as exc_info:
            is_palindrome(None)  # type: ignore
        assert "expected str" in str(exc_info.value).lower()

    def test_list_raises_typeerror(self) -> None:
        """Non-string argument (list) raises TypeError (C3)."""
        with pytest.raises(TypeError) as exc_info:
            is_palindrome(["racecar"])  # type: ignore
        assert "expected str" in str(exc_info.value).lower()

    def test_dict_raises_typeerror(self) -> None:
        """Non-string argument (dict) raises TypeError (C3)."""
        with pytest.raises(TypeError) as exc_info:
            is_palindrome({"text": "racecar"})  # type: ignore
        assert "expected str" in str(exc_info.value).lower()

    def test_float_raises_typeerror(self) -> None:
        """Non-string argument (float) raises TypeError (C3)."""
        with pytest.raises(TypeError) as exc_info:
            is_palindrome(3.14)  # type: ignore
        assert "expected str" in str(exc_info.value).lower()


class TestPureFunction:
    """Test that is_palindrome is a pure function with no side effects (C4)."""

    def test_pure_function_no_mutations(self) -> None:
        """Function doesn't mutate input or have side effects (C4)."""
        original = "RaceCar"
        text = original
        result = is_palindrome(text)
        # Input should not be mutated
        assert text == original
        assert result is True

    def test_pure_function_consistent_results(self) -> None:
        """Function returns consistent results for same input (C4)."""
        test_string = "A man a plan a canal Panama"
        result1 = is_palindrome(test_string)
        result2 = is_palindrome(test_string)
        assert result1 == result2
        assert result1 is True

    def test_pure_function_no_external_calls(self) -> None:
        """Function operates only on input, no external dependencies (C4)."""
        # This is verified by code inspection (no file/network access in implementation)
        # The function should work consistently regardless of external state
        assert is_palindrome("racecar") is True
        assert is_palindrome("racecar") is True  # Same result, no state changes


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_palindrome_with_punctuation_only(self) -> None:
        """String with only punctuation (treated as spaces)."""
        # Currently only removes spaces, so punctuation is not removed
        assert is_palindrome("!") is True  # Single char treated as palindrome

    def test_long_palindrome(self) -> None:
        """Long palindrome string."""
        long_palindrome = "a" * 100 + "b" + "a" * 100
        assert is_palindrome(long_palindrome) is True

    def test_long_non_palindrome(self) -> None:
        """Long non-palindrome string."""
        long_non_palindrome = "a" * 100 + "b" + "c" * 100
        assert is_palindrome(long_non_palindrome) is False

    def test_palindrome_numeric_string(self) -> None:
        """Numeric strings as palindromes."""
        assert is_palindrome("12321") is True
        assert is_palindrome("12345") is False

    def test_palindrome_with_numbers_and_letters(self) -> None:
        """Mixed alphanumeric palindrome."""
        assert is_palindrome("a1b1a") is True
        assert is_palindrome("a1b2a") is False
