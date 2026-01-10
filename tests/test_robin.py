import pytest
from hypothesis import given
from hypothesis import strategies as st

from mywheel.robin import Robin, RobinIterator, SlNode


def test_slnode() -> None:
    """Test the SlNode class."""
    node = SlNode(5)
    assert node.data == 5
    assert node.next is node


def test_robin_iterator_constructor() -> None:
    """Test the RobinIterator constructor."""
    node = SlNode(1)
    iterator = RobinIterator(node)
    assert iterator.cur is node
    assert iterator.stop is node


def test_robin_iterator_iter() -> None:
    """Test the RobinIterator's __iter__ method."""
    node = SlNode(1)
    iterator = RobinIterator(node)
    assert iter(iterator) is iterator


def test_robin_iterator_next() -> None:
    """Test the RobinIterator's next method."""
    r = Robin(3)
    iterator = r.exclude(0)
    assert next(iterator) == 1
    assert next(iterator) == 2
    with pytest.raises(StopIteration):
        next(iterator)


def test_robin_constructor() -> None:
    """Test the Robin constructor."""
    r = Robin(5)
    assert len(r.cycle) == 5
    for i, node in enumerate(r.cycle):
        assert node.data == i
        assert r.cycle[(i - 1) % 5].next is node


def test_robin_exclude() -> None:
    """Test the Robin's exclude method."""
    r = Robin(5)
    iterator = r.exclude(3)
    assert isinstance(iterator, RobinIterator)
    assert iterator.cur.data == 3


def test_robin_iteration() -> None:
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


def test_robin_one_part() -> None:
    """Test Robin with one part."""
    r = Robin(1)
    result = list(r.exclude(0))
    assert result == []


def test_robin_zero_parts() -> None:
    """Test Robin with zero parts."""
    r = Robin(0)
    with pytest.raises(IndexError):
        r.exclude(0)


class TestRobinProperties:
    """Property-based tests for Robin using Hypothesis."""

    @given(st.integers(min_value=1, max_value=20))
    def test_robin_cycle_structure_property(self, num_parts):
        """Cycle should have correct structure and connections."""
        r = Robin(num_parts)
        assert len(r.cycle) == num_parts

        # Verify each node has correct data
        for i, node in enumerate(r.cycle):
            assert node.data == i

        # Verify circular connections
        for i in range(num_parts):
            current_node = r.cycle[i]
            next_node = r.cycle[(i + 1) % num_parts]
            assert current_node.next is next_node

    @given(
        st.integers(min_value=1, max_value=20), st.integers(min_value=0, max_value=19)
    )
    def test_robin_exclude_completeness_property(self, num_parts, from_part):
        """Excluding a part should iterate through all other parts exactly once."""
        if from_part < num_parts:
            r = Robin(num_parts)
            result = list(r.exclude(from_part))

            # Should contain exactly num_parts - 1 elements
            assert len(result) == num_parts - 1

            # Should contain all parts except the excluded one
            expected = list(range(num_parts))
            expected.remove(from_part)
            assert sorted(result) == sorted(expected)

    @given(
        st.integers(min_value=2, max_value=20), st.integers(min_value=0, max_value=19)
    )
    def test_robin_exclude_order_property(self, num_parts, from_part):
        """Exclusion should iterate in correct circular order."""
        if from_part < num_parts:
            r = Robin(num_parts)
            result = list(r.exclude(from_part))

            # Verify circular order
            expected = []
            for i in range(1, num_parts):
                expected.append((from_part + i) % num_parts)
            assert result == expected

    @given(st.integers(min_value=1, max_value=20))
    def test_robin_all_exclusions_property(self, num_parts):
        """Excluding each part should give complementary results."""
        r = Robin(num_parts)
        all_results = {}

        for from_part in range(num_parts):
            result = set(r.exclude(from_part))
            all_results[from_part] = result

        # Each exclusion should be the complement of the excluded part
        for from_part in range(num_parts):
            expected = set(range(num_parts)) - {from_part}
            assert all_results[from_part] == expected

    @given(st.integers(min_value=1, max_value=20))
    def test_robin_iterator_consistency_property(self, num_parts):
        """Multiple iterators from the same Robin should work independently."""
        r = Robin(num_parts)

        # Create multiple iterators
        iters = [r.exclude(i % num_parts) for i in range(num_parts)]

        # Each should produce correct results
        for i, iterator in enumerate(iters):
            result = list(iterator)
            expected = list(range(i + 1, i + num_parts))
            expected = [x % num_parts for x in expected]
            assert result == expected


class TestSlNodeProperties:
    """Property-based tests for SlNode using Hypothesis."""

    @given(st.integers(min_value=-100, max_value=100))
    def test_slnode_initial_state_property(self, data):
        """New node should point to itself."""
        node = SlNode(data)
        assert node.data == data
        assert node.next is node

    @given(
        st.integers(min_value=-100, max_value=100),
        st.integers(min_value=-100, max_value=100),
    )
    def test_slnode_linking_property(self, data1, data2):
        """Linking nodes should maintain correct connections."""
        node1 = SlNode(data1)
        node2 = SlNode(data2)

        # Link node1 to node2
        node1.next = node2

        assert node1.next is node2
        assert node2.next is node2  # node2 still points to itself


class TestRobinIteratorProperties:
    """Property-based tests for RobinIterator using Hypothesis."""

    @given(
        st.integers(min_value=1, max_value=20), st.integers(min_value=0, max_value=19)
    )
    def test_robin_iterator_initialization_property(self, num_parts, from_part):
        """Iterator should initialize with correct current and stop nodes."""
        if from_part < num_parts:
            r = Robin(num_parts)
            iterator = r.exclude(from_part)

            assert iterator.cur is r.cycle[from_part]
            assert iterator.stop is r.cycle[from_part]

    @given(
        st.integers(min_value=1, max_value=20), st.integers(min_value=0, max_value=19)
    )
    def test_robin_iterator_self_iterable_property(self, num_parts, from_part):
        """Iterator should be self-iterable."""
        if from_part < num_parts:
            r = Robin(num_parts)
            iterator = r.exclude(from_part)

            assert iter(iterator) is iterator

    @given(
        st.integers(min_value=3, max_value=20), st.integers(min_value=0, max_value=19)
    )
    def test_robin_iterator_multiple_next_calls_property(self, num_parts, from_part):
        """Multiple next calls should produce correct sequence."""
        if from_part < num_parts:
            r = Robin(num_parts)
            iterator = r.exclude(from_part)

            # Collect all values
            values = []
            for _ in range(num_parts - 1):
                values.append(next(iterator))

            # Verify sequence
            expected = [(from_part + i + 1) % num_parts for i in range(num_parts - 1)]
            assert values == expected

            # Next call should raise StopIteration
            with pytest.raises(StopIteration):
                next(iterator)
