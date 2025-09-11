import pytest

from mywheel.robin import Robin, RobinIterator, SlNode


def test_slnode():
    """Test the SlNode class."""
    node = SlNode(5)
    assert node.data == 5
    assert node.next is node


def test_robin_iterator_constructor():
    """Test the RobinIterator constructor."""
    node = SlNode(1)
    iterator = RobinIterator(node)
    assert iterator.cur is node
    assert iterator.stop is node


def test_robin_iterator_iter():
    """Test the RobinIterator's __iter__ method."""
    node = SlNode(1)
    iterator = RobinIterator(node)
    assert iter(iterator) is iterator


def test_robin_iterator_next():
    """Test the RobinIterator's next method."""
    r = Robin(3)
    iterator = r.exclude(0)
    assert next(iterator) == 1
    assert next(iterator) == 2
    with pytest.raises(StopIteration):
        next(iterator)


def test_robin_constructor():
    """Test the Robin constructor."""
    r = Robin(5)
    assert len(r.cycle) == 5
    for i, node in enumerate(r.cycle):
        assert node.data == i
        assert r.cycle[(i - 1) % 5].next is node


def test_robin_exclude():
    """Test the Robin's exclude method."""
    r = Robin(5)
    iterator = r.exclude(3)
    assert isinstance(iterator, RobinIterator)
    assert iterator.cur.data == 3


def test_robin_iteration():
    """Test the round-robin iteration logic."""
    r = Robin(5)
    # Test starting from 0
    result = list(r.exclude(0))
    assert result == [1, 2, 3, 4]

    # Test starting from 3
    result = list(r.exclude(3))
    assert result == [4, 0, 1, 2]

    # Test starting from the last element
    result = list(r.exclude(4))
    assert result == [0, 1, 2, 3]


def test_robin_one_part():
    """Test Robin with one part."""
    r = Robin(1)
    result = list(r.exclude(0))
    assert result == []


def test_robin_zero_parts():
    """Test Robin with zero parts."""
    r = Robin(0)
    with pytest.raises(IndexError):
        r.exclude(0)
