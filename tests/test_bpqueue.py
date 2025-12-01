import pytest

from mywheel.bpqueue import BPQueue
from mywheel.dllist import Dllink


class TestBPQueue:
    def test_constructor(self) -> None:
        bpq = BPQueue(-3, 3)
        assert bpq.is_empty()
        assert bpq.get_max() == -4  # a - 1

    def test_append_and_pop(self) -> None:
        bpq = BPQueue(-5, 5)
        a = Dllink([0, 1])
        b = Dllink([0, 2])
        c = Dllink([0, 3])

        bpq.append(a, 3)
        bpq.append(b, -2)
        bpq.append(c, 5)

        assert not bpq.is_empty()
        assert bpq.get_max() == 5

        item = bpq.popleft()
        assert item is c
        assert bpq.get_max() == 3

        item = bpq.popleft()
        assert item is a
        assert bpq.get_max() == -2

        item = bpq.popleft()
        assert item is b
        assert bpq.is_empty()

    def test_appendleft(self) -> None:
        bpq = BPQueue(-5, 5)
        a = Dllink([0, 1])
        b = Dllink([0, 2])

        bpq.appendleft(a, 3)
        bpq.appendleft(b, 3)

        assert bpq.popleft() is b
        assert bpq.popleft() is a

    def test_appendfrom(self) -> None:
        bpq = BPQueue(-10, 10)
        nodes = [Dllink([2 * i - 10, i]) for i in range(10)]
        bpq.appendfrom(nodes)
        assert bpq.get_max() == 8
        count = 0
        for _ in bpq:
            count += 1
        assert count == 10

    def test_clear(self) -> None:
        bpq = BPQueue(-5, 5)
        bpq.append(Dllink([0, 1]), 3)
        bpq.clear()
        assert bpq.is_empty()

    def test_key_manipulation(self) -> None:
        bpq = BPQueue(-5, 5)
        a = Dllink([0, 1])

        bpq.append(a, 0)
        assert bpq.get_max() == 0

        bpq.increase_key(a, 2)
        assert bpq.get_max() == 2

        bpq.decrease_key(a, 3)
        assert bpq.get_max() == -1

        bpq.modify_key(a, 4)
        assert bpq.get_max() == 3

        bpq.modify_key(a, -5)
        assert bpq.get_max() == -2

    def test_detach(self) -> None:
        bpq = BPQueue(-5, 5)
        a = Dllink([0, 1])
        b = Dllink([0, 2])

        bpq.append(a, 3)
        bpq.append(b, 5)

        bpq.detach(a)
        assert bpq.get_max() == 5
        assert bpq.popleft() is b
        assert bpq.is_empty()

    def test_locked_item(self) -> None:
        bpq = BPQueue(-5, 5)
        a = Dllink([0, 1])
        bpq.append(a, 0)
        a.lock()
        bpq.modify_key(a, 3)  # Should have no effect
        assert bpq.get_max() == 0


class TestBPQueueIterator:
    def test_iteration(self) -> None:
        bpq = BPQueue(-5, 5)
        a = Dllink([0, 1])
        b = Dllink([0, 2])
        c = Dllink([0, 3])

        bpq.append(a, 3)
        bpq.append(b, -2)
        bpq.append(c, 5)

        items = [item.data[1] for item in bpq]
        assert items == [3, 1, 2]

    def test_empty_iteration(self) -> None:
        bpq = BPQueue(-5, 5)
        items = list(bpq)
        assert items == []

    def test_iterator_invalidation(self) -> None:
        bpq = BPQueue(-5, 5)
        a = Dllink([0, 1])
        bpq.append(a, 3)

        it = iter(bpq)
        next(it)
        bpq.popleft()  # This invalidates the iterator

        with pytest.raises(StopIteration):
            next(it)
