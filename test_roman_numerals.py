"""Pytest suite for the Roman numeral conversion utility.

Covers:
    * Valid conversions in both directions.
    * Out-of-range ``ValueError`` for :func:`to_roman`.
    * ``TypeError`` for non-int / non-str inputs (including explicit
      ``bool`` rejection).
    * Invalid-character ``ValueError`` for :func:`from_roman`.
    * Malformed / non-canonical numeral ``ValueError``.
    * A full 1..3999 round-trip.
"""

import pytest

from roman_numerals import from_roman, to_roman

# Representative (integer, numeral) pairs spanning single symbols, the six
# subtractive pairs, and the numeric boundaries.
_KNOWN_PAIRS = [
    (1, "I"),
    (2, "II"),
    (3, "III"),
    (4, "IV"),
    (5, "V"),
    (9, "IX"),
    (10, "X"),
    (14, "XIV"),
    (40, "XL"),
    (49, "XLIX"),
    (50, "L"),
    (90, "XC"),
    (100, "C"),
    (400, "CD"),
    (500, "D"),
    (900, "CM"),
    (1000, "M"),
    (1984, "MCMLXXXIV"),
    (2024, "MMXXIV"),
    (3549, "MMMDXLIX"),
    (3999, "MMMCMXCIX"),
]


@pytest.mark.parametrize("value,numeral", _KNOWN_PAIRS)
def test_to_roman_valid(value: int, numeral: str) -> None:
    """``to_roman`` produces the expected canonical numeral."""
    assert to_roman(value) == numeral


@pytest.mark.parametrize("value,numeral", _KNOWN_PAIRS)
def test_from_roman_valid(value: int, numeral: str) -> None:
    """``from_roman`` parses the expected integer."""
    assert from_roman(numeral) == value


@pytest.mark.parametrize("value", [0, -1, -100, 4000, 4001, 10000])
def test_to_roman_out_of_range(value: int) -> None:
    """Values outside 1..3999 raise ``ValueError``."""
    with pytest.raises(ValueError):
        to_roman(value)


@pytest.mark.parametrize("value", ["10", 3.0, 3.5, None, [1], (1,)])
def test_to_roman_non_int_type(value: object) -> None:
    """Non-int inputs raise ``TypeError``."""
    with pytest.raises(TypeError):
        to_roman(value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [True, False])
def test_to_roman_rejects_bool(value: bool) -> None:
    """``bool`` is explicitly rejected even though it subclasses ``int``."""
    with pytest.raises(TypeError):
        to_roman(value)


@pytest.mark.parametrize("value", [1, 3999, None, 5.0, ["X"], ("I",)])
def test_from_roman_non_str_type(value: object) -> None:
    """Non-str inputs raise ``TypeError``."""
    with pytest.raises(TypeError):
        from_roman(value)  # type: ignore[arg-type]


def test_from_roman_empty_string() -> None:
    """An empty string raises ``ValueError``."""
    with pytest.raises(ValueError):
        from_roman("")


@pytest.mark.parametrize("numeral", ["A", "IIX?", "MMz", "iv", "1V", " X", "X "])
def test_from_roman_invalid_characters(numeral: str) -> None:
    """Characters outside ``IVXLCDM`` raise ``ValueError``."""
    with pytest.raises(ValueError):
        from_roman(numeral)


@pytest.mark.parametrize(
    "numeral",
    ["IIII", "VV", "IC", "IL", "XM", "VX", "IIV", "MMMM", "LL", "DD", "XXXX"],
)
def test_from_roman_malformed_numeral(numeral: str) -> None:
    """Non-canonical numerals raise ``ValueError``."""
    with pytest.raises(ValueError):
        from_roman(numeral)


def test_full_round_trip_1_to_3999() -> None:
    """Every integer in 1..3999 round-trips through both functions."""
    for value in range(1, 4000):
        numeral = to_roman(value)
        assert from_roman(numeral) == value
