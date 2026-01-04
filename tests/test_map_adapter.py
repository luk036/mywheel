import pytest
from hypothesis import given, strategies as st

from mywheel.map_adapter import MapAdapter


class TestMapAdapter:
    def test_constructor(self) -> None:
        lst = [1, 2, 3]
        adapter = MapAdapter(lst)
        assert adapter.lst is lst

    def test_getitem(self) -> None:
        adapter = MapAdapter([1, 2, 3])
        assert adapter[0] == 1
        assert adapter[2] == 3
        with pytest.raises(IndexError):
            adapter[3]

    def test_setitem(self) -> None:
        adapter = MapAdapter([1, 2, 3])
        adapter[1] = 5
        assert adapter[1] == 5
        with pytest.raises(IndexError):
            adapter[3] = 6

    def test_delitem(self) -> None:
        adapter = MapAdapter([1, 2, 3])
        with pytest.raises(NotImplementedError):
            del adapter[0]

    def test_iter(self) -> None:
        adapter = MapAdapter([1, 2, 3])
        assert list(iter(adapter)) == [0, 1, 2]

    def test_contains(self) -> None:
        adapter = MapAdapter([1, 2, 3])
        assert 0 in adapter
        assert 2 in adapter
        assert 3 not in adapter
        assert -1 not in adapter

    def test_len(self) -> None:
        adapter = MapAdapter([1, 2, 3])
        assert len(adapter) == 3

    def test_values(self) -> None:
        adapter = MapAdapter([1, 2, 3])
        assert list(adapter.values()) == [1, 2, 3]

    def test_items(self) -> None:
        adapter = MapAdapter([1, 2, 3])
        assert list(adapter.items()) == [(0, 1), (1, 2), (2, 3)]

    def test_keys(self) -> None:
        adapter = MapAdapter([1, 2, 3])
        assert list(adapter.keys()) == [0, 1, 2]


class TestMapAdapterProperties:
    """Property-based tests for MapAdapter using Hypothesis."""

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_map_adapter_length_property(self, values):
        """Length should match the underlying list length."""
        adapter = MapAdapter(values)
        assert len(adapter) == len(values)

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_map_adapter_iteration_property(self, values):
        """Iteration should produce valid indices."""
        adapter = MapAdapter(values)
        indices = list(adapter)
        expected_indices = list(range(len(values)))
        assert indices == expected_indices

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_map_adapter_contains_property(self, values):
        """Contains should be true for valid indices and false for invalid ones."""
        adapter = MapAdapter(values)

        # Test valid indices
        for i in range(len(values)):
            assert i in adapter

        # Test invalid indices
        assert len(values) not in adapter
        assert -1 not in adapter
        assert len(values) + 5 not in adapter

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_map_adapter_values_property(self, values):
        """Values should match the underlying list values."""
        adapter = MapAdapter(values)
        adapter_values = list(adapter.values())
        assert adapter_values == values

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_map_adapter_items_property(self, values):
        """Items should produce (index, value) pairs."""
        adapter = MapAdapter(values)
        adapter_items = list(adapter.items())
        expected_items = list(enumerate(values))
        assert adapter_items == expected_items

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=0, max_value=19),
        st.integers(min_value=-200, max_value=200),
    )
    def test_map_adapter_getitem_property(self, values, index, new_value):
        """Getting and setting items should work correctly."""
        if index < len(values):
            adapter = MapAdapter(values.copy())

            # Test getitem
            assert adapter[index] == values[index]

            # Test setitem
            adapter[index] = new_value
            assert adapter[index] == new_value
            assert adapter.lst[index] == new_value

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_map_adapter_keys_property(self, values):
        """Keys should match iteration result."""
        adapter = MapAdapter(values)
        keys = list(adapter.keys())
        expected_keys = list(range(len(values)))
        assert keys == expected_keys

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_map_adapter_reference_property(self, values):
        """Adapter should reference the original list."""
        adapter = MapAdapter(values)
        assert adapter.lst is values

        # Modifying the original list should be reflected in adapter
        if len(values) > 0:
            values[0] = 999
            assert adapter[0] == 999

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_map_adapter_delitem_not_implemented_property(self, values):
        """Delitem should always raise NotImplementedError."""
        adapter = MapAdapter(values)
        with pytest.raises(NotImplementedError):
            del adapter[0]
