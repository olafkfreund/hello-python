"""Unit tests for the clamp utility function."""

import pytest

from hello_python.utils import clamp


class TestClamp:
    """Test suite for the clamp() helper function."""

    def test_clamp_value_within_range(self) -> None:
        """clamp() returns the value unchanged if it's within [min, max]."""
        assert clamp(5, 0, 10) == 5
        assert clamp(0, 0, 10) == 0
        assert clamp(10, 0, 10) == 10

    def test_clamp_value_below_min(self) -> None:
        """clamp() returns min_value if value < min_value."""
        assert clamp(-5, 0, 10) == 0
        assert clamp(-100, -50, 50) == -50

    def test_clamp_value_above_max(self) -> None:
        """clamp() returns max_value if value > max_value."""
        assert clamp(15, 0, 10) == 10
        assert clamp(100, -50, 50) == 50

    def test_clamp_with_floats(self) -> None:
        """clamp() works with floating-point values."""
        assert clamp(5.5, 0.0, 10.0) == 5.5
        assert clamp(-1.5, 0.0, 10.0) == 0.0
        assert clamp(15.5, 0.0, 10.0) == 10.0

    def test_clamp_with_negative_range(self) -> None:
        """clamp() works with negative ranges."""
        assert clamp(-5, -10, -1) == -5
        assert clamp(-15, -10, -1) == -10
        assert clamp(0, -10, -1) == -1

    def test_clamp_min_equals_max(self) -> None:
        """clamp() returns min/max when they are equal."""
        result = clamp(5, 3, 3)
        assert result == 3

    def test_clamp_invalid_range_raises_error(self) -> None:
        """clamp() raises ValueError if min_value > max_value."""
        with pytest.raises(ValueError, match="min_value.*must be.*max_value"):
            clamp(5, 10, 0)


class TestClampImportability:
    """Test that clamp is properly exported from the hello_python package."""

    def test_clamp_importable_from_utils(self) -> None:
        """clamp should be importable from hello_python.utils."""
        from hello_python.utils import clamp as imported_clamp  # noqa: PLC0415

        assert callable(imported_clamp)

    def test_clamp_importable_from_package_root(self) -> None:
        """clamp should be importable from hello_python package root."""
        from hello_python import clamp as imported_clamp  # noqa: PLC0415

        assert callable(imported_clamp)

    def test_clamp_in_all_export(self) -> None:
        """clamp should be listed in hello_python.__all__."""
        import hello_python  # noqa: PLC0415

        assert hasattr(hello_python, "__all__")
        assert "clamp" in hello_python.__all__
