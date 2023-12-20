from mywheel.lict import Lict


def test_lict():
    a = Lict([1, 4, 3, 6])
    assert a[2] == 3
    assert 3 in a
    assert len(a) == 4
    assert list(a.values()) == [1, 4, 3, 6]
    assert list(a.items()) == [(0, 1), (1, 4), (2, 3), (3, 6)]
    assert list(a.keys()) == [0, 1, 2, 3]

    a[2] = 7
    assert a[2] == 7
