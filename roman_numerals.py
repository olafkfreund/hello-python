"""
Roman numeral conversion utility.

Pure-Python module exposing two public functions:

    to_roman(n: int) -> str    Convert an integer 1..3999 to an uppercase
                               subtractive Roman numeral.
    from_roman(s: str) -> int  Parse an uppercase subtractive Roman numeral
                               back to an integer 1..3999.

Stdlib only, no third-party dependencies. No CLI, no I/O, no network access.
"""

# Greedy conversion table ordered from largest to smallest value, including
# the six subtractive pairs (CM, CD, XC, XL, IX, IV).
_ROMAN_TABLE: tuple[tuple[int, str], ...] = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

# Value of each single Roman numeral character, used for parsing.
_ROMAN_VALUES: dict[str, int] = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

_MIN_VALUE = 1
_MAX_VALUE = 3999


def to_roman(n: int) -> str:
    """Convert an integer to an uppercase subtractive Roman numeral.

    Args:
        n: An integer in the inclusive range 1..3999.

    Returns:
        The Roman numeral representation of ``n``.

    Raises:
        TypeError: If ``n`` is not an ``int`` (``bool`` is explicitly rejected
            even though it is a subclass of ``int``).
        ValueError: If ``n`` is outside the range 1..3999.
    """
    # bool subclasses int, so reject it explicitly before the int check.
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if not _MIN_VALUE <= n <= _MAX_VALUE:
        raise ValueError(f"n must be in range {_MIN_VALUE}..{_MAX_VALUE}, got {n}")

    parts: list[str] = []
    remainder = n
    for value, symbol in _ROMAN_TABLE:
        count, remainder = divmod(remainder, value)
        parts.append(symbol * count)
    return "".join(parts)


def from_roman(s: str) -> int:
    """Parse an uppercase subtractive Roman numeral into an integer.

    Validation is strict: the input is parsed and then re-encoded with
    :func:`to_roman`; any mismatch (e.g. ``"IIII"``, ``"VV"``, ``"IC"``) is
    rejected. This guarantees only canonical numerals are accepted.

    Args:
        s: An uppercase subtractive Roman numeral string.

    Returns:
        The integer value of ``s`` in the range 1..3999.

    Raises:
        TypeError: If ``s`` is not a ``str``.
        ValueError: If ``s`` is empty, contains characters outside ``IVXLCDM``,
            or is a malformed / non-canonical numeral.
    """
    if not isinstance(s, str):
        raise TypeError(f"s must be a str, got {type(s).__name__}")
    if not s:
        raise ValueError("s must be a non-empty Roman numeral string")

    invalid = {ch for ch in s if ch not in _ROMAN_VALUES}
    if invalid:
        raise ValueError(f"s contains invalid Roman numeral characters: {sorted(invalid)}")

    total = 0
    prev_value = 0
    for ch in reversed(s):
        value = _ROMAN_VALUES[ch]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    # Strict canonical validation: the parsed value must round-trip exactly.
    if not _MIN_VALUE <= total <= _MAX_VALUE or to_roman(total) != s:
        raise ValueError(f"malformed Roman numeral: {s!r}")

    return total
