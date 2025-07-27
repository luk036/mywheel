import pytest
from mywheel.map_adapter import MapAdapter


def test_map_adapter_legacy():
    a = MapAdapter([1, 4, 3, 6])
    assert a[2] == 3
    assert 3 in a
    assert len(a) == 4
    assert list(a.values()) == [1, 4, 3, 6]
    assert list(a.items()) == [(0, 1), (1, 4), (2, 3), (3, 6)]
    assert list(a.keys()) == [0, 1, 2, 3]

    a[2] = 7
    assert a[2] == 7

def test_map_adapter():
    a = MapAdapter([1, 2, 3])
    assert len(a) == 3
    assert a[0] == 1
    assert a[1] == 2
    assert a[2] == 3

    with pytest.raises(IndexError):
        a[3]

    a[1] = 4
    assert a[1] == 4

    assert 1 in a
    assert 3 not in a

    assert list(a.keys()) == [0, 1, 2]
    assert list(a.values()) == [1, 4, 3]
    assert list(a.items()) == [(0, 1), (1, 4), (2, 3)]

    with pytest.raises(NotImplementedError):
        del a[0]
