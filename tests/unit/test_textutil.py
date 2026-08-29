"""Unit tests for :mod:`hello_python.textutil` (slugify and truncate_words).

These tests exercise the pure library functions directly, covering every
acceptance criterion from the spec: slug formatting, empty/all-punctuation
input, word truncation with and without ellipsis, and the ValueError/TypeError
error paths for both functions.
"""

import pytest

from hello_python.textutil import slugify, truncate_words


@pytest.mark.parametrize(
    "text,expected",
    [
        ("  Hello, World!  ", "hello-world"),  # AC – canonical example
        ("Hello World", "hello-world"),  # spaces collapse to a hyphen
        ("already-slug", "already-slug"),  # idempotent on a clean slug
        ("Foo___Bar", "foo-bar"),  # run of non-alnum -> single hyphen
        ("MixEd CaSe 123", "mixed-case-123"),  # lowercasing + digits kept
    ],
)
def test_slugify_basic(text: str, expected: str) -> None:
    """slugify lowercases, hyphenates, and strips edge hyphens."""
    assert slugify(text) == expected


@pytest.mark.parametrize("text", ["", "!!!", "   ", "@#$%^&*"])
def test_slugify_empty_or_all_punctuation(text: str) -> None:
    """Empty or all-non-alphanumeric input returns "" (never a bare hyphen)."""
    assert slugify(text) == ""


@pytest.mark.parametrize("bad_input", [123, None, 12.5, ["a"], {"a": 1}])
def test_slugify_rejects_non_str(bad_input: object) -> None:
    """slugify raises TypeError when text is not a str."""
    with pytest.raises(TypeError):
        slugify(bad_input)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "text,limit,expected",
    [
        ("a b", 2, "a b"),  # AC – word count == limit, no ellipsis
        ("a b", 5, "a b"),  # word count < limit, no ellipsis
        ("  a   b  ", 2, "a b"),  # whitespace normalized, no ellipsis
        ("", 3, ""),  # no words, no ellipsis
    ],
)
def test_truncate_words_no_truncation(text: str, limit: int, expected: str) -> None:
    """When word count <= limit, text is normalized with no ellipsis."""
    assert truncate_words(text, limit) == expected


@pytest.mark.parametrize(
    "text,limit,expected",
    [
        ("a b c d", 2, "a b …"),  # AC – drops words, appends " …"
        ("one two three", 1, "one …"),
        ("  lots   of   spacing   here  ", 2, "lots of …"),
    ],
)
def test_truncate_words_truncation_with_ellipsis(
    text: str, limit: int, expected: str
) -> None:
    """When words are dropped, the ellipsis " …" is appended."""
    assert truncate_words(text, limit) == expected


@pytest.mark.parametrize("limit", [0, -1, -100])
def test_truncate_words_rejects_limit_below_one(limit: int) -> None:
    """truncate_words raises ValueError when limit < 1."""
    with pytest.raises(ValueError):
        truncate_words("a b c", limit)


@pytest.mark.parametrize("bad_input", [123, None, 12.5, ["a"], {"a": 1}])
def test_truncate_words_rejects_non_str(bad_input: object) -> None:
    """truncate_words raises TypeError when text is not a str."""
    with pytest.raises(TypeError):
        truncate_words(bad_input, 2)  # type: ignore[arg-type]
