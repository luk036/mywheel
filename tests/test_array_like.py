import pytest
from hypothesis import given, strategies as st

from mywheel.array_like import RepeatArray, ShiftArray


class TestRepeatArray:
    def test_constructor(self) -> None:
        ra = RepeatArray(10, 5)
        assert ra.value == 10
        assert ra.size == 5

    def test_getitem(self) -> None:
        ra = RepeatArray(10, 5)
        assert ra[0] == 10
        assert ra[4] == 10
        # The index is ignored, so any index should work
        assert ra[100] == 10

    def test_len(self) -> None:
        ra = RepeatArray(10, 5)
        assert len(ra) == 5

    def test_iter(self) -> None:
        ra = RepeatArray(10, 3)
        assert list(ra) == [10, 10, 10]

    def test_get(self) -> None:
        ra = RepeatArray(10, 5)
        assert ra.get(0) == 10
        assert ra.get(100) == 10


class TestShiftArray:
    def test_constructor(self) -> None:
        sa = ShiftArray([1, 2, 3])
        assert sa.start == 0
        assert list(sa) == [1, 2, 3]

    def test_set_start(self) -> None:
        sa = ShiftArray([1, 2, 3])
        sa.set_start(5)
        assert sa.start == 5

    def test_getitem(self) -> None:
        sa = ShiftArray([1, 2, 3])
        sa.set_start(5)
        assert sa[5] == 1
        assert sa[7] == 3
        with pytest.raises(IndexError):
            sa[4]
        with pytest.raises(IndexError):
            sa[8]

    def test_setitem(self) -> None:
        sa = ShiftArray([1, 2, 3])
        sa.set_start(5)
        sa[6] = 10
        assert sa[6] == 10
        assert list(sa) == [1, 10, 3]
        with pytest.raises(IndexError):
            sa[8] = 5

    def test_len(self) -> None:
        sa = ShiftArray([1, 2, 3])
        assert len(sa) == 3

    def test_items(self) -> None:
        sa = ShiftArray([1, 2, 3])
        sa.set_start(5)
        assert list(sa.items()) == [(5, 1), (6, 2), (7, 3)]


class TestRepeatArrayProperties:
    """Property-based tests for RepeatArray using Hypothesis."""

    @given(
        st.integers(min_value=-1000, max_value=1000),
        st.integers(min_value=0, max_value=100),
    )
    def test_repeat_array_all_elements_equal(self, value, size):
        """All elements in RepeatArray should be equal to the initial value."""
        ra = RepeatArray(value, size)
        for i in range(size):
            assert ra[i] == value

    @given(
        st.integers(min_value=-1000, max_value=1000),
        st.integers(min_value=0, max_value=100),
    )
    def test_repeat_array_length_property(self, value, size):
        """Length should match the size parameter."""
        ra = RepeatArray(value, size)
        assert len(ra) == size

    @given(
        st.integers(min_value=-1000, max_value=1000),
        st.integers(min_value=0, max_value=100),
    )
    def test_repeat_array_iteration_property(self, value, size):
        """Iteration should produce size copies of the value."""
        ra = RepeatArray(value, size)
        result = list(ra)
        assert result == [value] * size

    @given(
        st.integers(min_value=-1000, max_value=1000),
        st.integers(min_value=0, max_value=100),
        st.integers(min_value=-1000, max_value=1000),
    )
    def test_repeat_array_index_ignored_property(self, value, size, index):
        """Any index should return the same value."""
        ra = RepeatArray(value, size)
        assert ra[index] == value

    @given(
        st.integers(min_value=-1000, max_value=1000),
        st.integers(min_value=0, max_value=100),
        st.integers(min_value=-1000, max_value=1000),
    )
    def test_repeat_array_get_method_property(self, value, size, key):
        """Get method should ignore the key parameter."""
        ra = RepeatArray(value, size)
        assert ra.get(key) == value


class TestShiftArrayProperties:
    """Property-based tests for ShiftArray using Hypothesis."""

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-50, max_value=50),
    )
    def test_shift_array_index_mapping_property(self, values, start):
        """Index mapping should be consistent with start offset."""
        sa = ShiftArray(values)
        sa.set_start(start)

        for i, value in enumerate(values):
            assert sa[start + i] == value

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-50, max_value=50),
    )
    def test_shift_array_items_property(self, values, start):
        """Items should return (index, value) pairs with correct indices."""
        sa = ShiftArray(values)
        sa.set_start(start)

        items = list(sa.items())
        expected = [(start + i, value) for i, value in enumerate(values)]
        assert items == expected

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-50, max_value=50),
    )
    def test_shift_array_length_preserved_property(self, values, start):
        """Length should be preserved regardless of start value."""
        sa = ShiftArray(values)
        sa.set_start(start)
        assert len(sa) == len(values)

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-50, max_value=50),
        st.integers(min_value=0, max_value=19),
    )
    def test_shift_array_setitem_property(self, values, start, index):
        """Setting an item should update the underlying list correctly."""
        if index < len(values):
            sa = ShiftArray(values.copy())
            sa.set_start(start)
            new_value = 999  # Use a distinctive value

            sa[start + index] = new_value
            assert sa[start + index] == new_value
            assert list(sa)[index] == new_value

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-50, max_value=50),
        st.integers(min_value=-100, max_value=100),
    )
    def test_shift_array_out_of_bounds_property(self, values, start, invalid_index):
        """Accessing indices outside the valid range should raise IndexError for getitem."""
        sa = ShiftArray(values)
        sa.set_start(start)

        # Calculate the adjusted index that ShiftArray uses internally
        adjusted_index = invalid_index - start

        # Test indices that are out of bounds after adjustment
        if adjusted_index < 0 or adjusted_index >= len(values):
            with pytest.raises(IndexError):
                _ = sa[invalid_index]
            # Note: __setitem__ doesn't have bounds checking, so we don't test it here


class TestRepeatArrayCoverage:
    """Additional tests to improve coverage for RepeatArray."""

    def test_init_assignment(self):
        """Test that __init__ properly assigns value and size attributes."""
        ra = RepeatArray("test", 42)
        assert hasattr(ra, "value")
        assert hasattr(ra, "size")
        assert ra.value == "test"
        assert ra.size == 42

    def test_getitem_ignored_key(self):
        """Test that __getitem__ ignores the key parameter."""
        ra = RepeatArray(5, 3)
        # Test with various key types to ensure they're all ignored
        assert ra[0] == 5
        assert ra[100] == 5
        assert ra[-5] == 5

    def test_len_returns_size(self):
        """Test that __len__ returns the size attribute."""
        ra = RepeatArray(None, 7)
        assert len(ra) == 7

    def test_iter_returns_iterator(self):
        """Test that __iter__ returns a proper iterator."""
        ra = RepeatArray(9, 4)
        it = ra.__iter__()
        # Check that we got an iterator
        assert hasattr(it, "__iter__")
        assert hasattr(it, "__next__")
        # Check that it yields the correct values
        assert list(it) == [9, 9, 9, 9]

    def test_get_ignored_item(self):
        """Test that get ignores the item parameter."""
        ra = RepeatArray("value", 5)
        # Test with various item types to ensure they're all ignored
        assert ra.get(0) == "value"
        assert ra.get(100) == "value"
        assert ra.get("key") == "value"
        assert ra.get(None) == "value"


class TestShiftArrayCoverage:
    """Additional tests to improve coverage for ShiftArray."""

    def test_init_with_args_kwargs(self):
        """Test that __init__ properly handles args and kwargs."""
        # Test with positional arguments
        sa1 = ShiftArray([1, 2, 3])
        assert list(sa1) == [1, 2, 3]
        assert sa1.start == 0

        # Test with empty arguments
        sa2 = ShiftArray()
        assert list(sa2) == []
        assert sa2.start == 0

    def test_set_start_assignment(self):
        """Test that set_start properly assigns the start attribute."""
        sa = ShiftArray([1, 2, 3])
        sa.set_start(10)
        assert hasattr(sa, "start")
        assert sa.start == 10

    def test_getitem_bounds_check(self):
        """Test that __getitem__ performs bounds checking."""
        sa = ShiftArray([1, 2, 3])
        sa.set_start(10)

        # Test valid indices
        assert sa[10] == 1
        assert sa[11] == 2
        assert sa[12] == 3

        # Test invalid indices
        with pytest.raises(IndexError):
            _ = sa[9]  # Below range

        with pytest.raises(IndexError):
            _ = sa[13]  # Above range

    def test_setitem_adjusts_index(self):
        """Test that __setitem__ adjusts the index correctly."""
        sa = ShiftArray([1, 2, 3])
        sa.set_start(5)

        # Test setting values
        sa[5] = 10
        sa[6] = 20
        sa[7] = 30

        # Verify the values were set correctly
        assert list(sa) == [10, 20, 30]
        assert sa[5] == 10
        assert sa[6] == 20
        assert sa[7] == 30

    def test_items_returns_iterator(self):
        """Test that items returns a proper iterator."""
        sa = ShiftArray([1, 2, 3])
        sa.set_start(10)

        items = sa.items()
        # Check that we got an iterator
        assert hasattr(items, "__iter__")
        assert hasattr(items, "__next__")

        # Check that it yields the correct (index, value) pairs
        expected = [(10, 1), (11, 2), (12, 3)]
        assert list(items) == expected
