"""
Text utility helpers.

Pure, stdlib-only functions for turning free text into URL-friendly slugs and
for truncating text to a fixed number of words. No third-party dependencies and
no I/O — these are in-process helpers with no trust boundary of their own.
"""

import re

_NON_ALNUM_RUN = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Return a lowercase, hyphen-separated slug of ``text``.

    Lowercases the input, collapses each run of non-alphanumeric characters into
    a single hyphen, and strips leading/trailing hyphens. Empty or
    all-non-alphanumeric input returns ``""`` (never a bare hyphen).

    Raises ``TypeError`` if ``text`` is not a ``str``.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    return _NON_ALNUM_RUN.sub("-", text.lower()).strip("-")


def truncate_words(text: str, limit: int) -> str:
    """Return the first ``limit`` whitespace-separated words of ``text``.

    Words are joined by single spaces. If the word count is less than or equal
    to ``limit``, the whitespace-normalized text is returned with no ellipsis.
    If words are dropped, ``" …"`` is appended after the last kept word.

    Raises ``TypeError`` if ``text`` is not a ``str``.
    Raises ``ValueError`` if ``limit`` is less than 1.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    if limit < 1:
        raise ValueError(f"limit must be >= 1, got {limit}")
    words = text.split()
    if len(words) <= limit:
        return " ".join(words)
    return " ".join(words[:limit]) + " …"
