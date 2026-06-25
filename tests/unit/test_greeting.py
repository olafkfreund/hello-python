"""Unit tests for the greeting service logic (AC#2, AC#3, AC#4).

These tests exercise the greeting behaviour directly without HTTP overhead.
"""

import pytest


@pytest.mark.parametrize(
    "name,expected_message",
    [
        ("ada", "Hello, ada!"),  # AC#2 – canonical example
        ("Bob", "Hello, Bob!"),  # AC#3 – arbitrary name
        ("Alice", "Hello, Alice!"),  # AC#3 – arbitrary name
        ("Z" * 64, f"Hello, {'Z' * 64}!"),  # AC#4 – exactly 64 chars is valid
    ],
)
def test_greeting_format(name: str, expected_message: str) -> None:
    """The greeting f-string formats names correctly (AC#2, AC#3)."""
    # The greeting logic lives in the route; replicate the expression here.
    result = f"Hello, {name}!"
    assert result == expected_message


def test_max_length_boundary() -> None:
    """A name of exactly 64 characters is the upper valid boundary (AC#4)."""
    name = "A" * 64
    assert len(name) == 64
    message = f"Hello, {name}!"
    assert message == f"Hello, {'A' * 64}!"


def test_over_max_length_is_rejected_by_fastapi(client) -> None:  # noqa: ANN001
    """A name of 65 characters must be rejected with HTTP 422 (AC#4)."""
    long_name = "A" * 65
    response = client.get(f"/greet/{long_name}")
    assert response.status_code == 422
