"""Unit tests for the is_odd helper function.

AC#1: is_odd(3) returns True and is_odd(4) returns False.

These tests exercise the is_odd function for basic positive integers.
"""

import pytest

from hello_python import is_odd


def test_is_odd_returns_true_for_odd_number() -> None:
    """Test that is_odd(3) returns True (AC#1)."""
    assert is_odd(3) is True


def test_is_odd_returns_false_for_even_number() -> None:
    """Test that is_odd(4) returns False (AC#1)."""
    assert is_odd(4) is False
