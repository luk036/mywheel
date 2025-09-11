import pytest

from mywheel.array_like import RepeatArray, ShiftArray


class TestRepeatArray:
    def test_constructor(self):
        ra = RepeatArray(10, 5)
        assert ra.value == 10
        assert ra.size == 5

    def test_getitem(self):
        ra = RepeatArray(10, 5)
        assert ra[0] == 10
        assert ra[4] == 10
        # The index is ignored, so any index should work
        assert ra[100] == 10

    def test_len(self):
        ra = RepeatArray(10, 5)
        assert len(ra) == 5

    def test_iter(self):
        ra = RepeatArray(10, 3)
        assert list(ra) == [10, 10, 10]

    def test_get(self):
        ra = RepeatArray(10, 5)
        assert ra.get(0) == 10
        assert ra.get(100) == 10


class TestShiftArray:
    def test_constructor(self):
        sa = ShiftArray([1, 2, 3])
        assert sa.start == 0
        assert list(sa) == [1, 2, 3]

    def test_set_start(self):
        sa = ShiftArray([1, 2, 3])
        sa.set_start(5)
        assert sa.start == 5

    def test_getitem(self):
        sa = ShiftArray([1, 2, 3])
        sa.set_start(5)
        assert sa[5] == 1
        assert sa[7] == 3
        with pytest.raises(IndexError):
            sa[4]
        with pytest.raises(IndexError):
            sa[8]

    def test_setitem(self):
        sa = ShiftArray([1, 2, 3])
        sa.set_start(5)
        sa[6] = 10
        assert sa[6] == 10
        assert list(sa) == [1, 10, 3]
        with pytest.raises(IndexError):
            sa[8] = 5

    def test_len(self):
        sa = ShiftArray([1, 2, 3])
        assert len(sa) == 3

    def test_items(self):
        sa = ShiftArray([1, 2, 3])
        sa.set_start(5)
        assert list(sa.items()) == [(5, 1), (6, 2), (7, 3)]
