import pytest

from mywheel.map_adapter import MapAdapter


class TestMapAdapter:
    def test_constructor(self):
        lst = [1, 2, 3]
        adapter = MapAdapter(lst)
        assert adapter.lst is lst

    def test_getitem(self):
        adapter = MapAdapter([1, 2, 3])
        assert adapter[0] == 1
        assert adapter[2] == 3
        with pytest.raises(IndexError):
            adapter[3]

    def test_setitem(self):
        adapter = MapAdapter([1, 2, 3])
        adapter[1] = 5
        assert adapter[1] == 5
        with pytest.raises(IndexError):
            adapter[3] = 6

    def test_delitem(self):
        adapter = MapAdapter([1, 2, 3])
        with pytest.raises(NotImplementedError):
            del adapter[0]

    def test_iter(self):
        adapter = MapAdapter([1, 2, 3])
        assert list(iter(adapter)) == [0, 1, 2]

    def test_contains(self):
        adapter = MapAdapter([1, 2, 3])
        assert 0 in adapter
        assert 2 in adapter
        assert 3 not in adapter
        assert -1 not in adapter

    def test_len(self):
        adapter = MapAdapter([1, 2, 3])
        assert len(adapter) == 3

    def test_values(self):
        adapter = MapAdapter([1, 2, 3])
        assert list(adapter.values()) == [1, 2, 3]

    def test_items(self):
        adapter = MapAdapter([1, 2, 3])
        assert list(adapter.items()) == [(0, 1), (1, 2), (2, 3)]

    def test_keys(self):
        adapter = MapAdapter([1, 2, 3])
        assert list(adapter.keys()) == [0, 1, 2]
