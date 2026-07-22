"""Palindrome checking utilities.

This module provides functions to check if strings are palindromes.
Pure functions with no side effects, no secrets, no external access.
"""


def is_palindrome(text: str) -> bool:
    """Check if a string is a palindrome.

    Palindromes are checked case-insensitively and ignoring whitespace.

    Args:
        text: The string to check.

    Returns:
        True if the string is a palindrome, False otherwise.

    Raises:
        TypeError: If text is not a string.

    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("hello")
        False
    """
    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")

    # Remove whitespace and convert to lowercase for comparison
    cleaned = text.replace(" ", "").lower()

    # Check if the cleaned string is equal to its reverse
    return cleaned == cleaned[::-1]
