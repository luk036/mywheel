import pytest
from hypothesis import given
from hypothesis import strategies as st

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


class TestBPQueueCoverage:
    """Additional tests to improve coverage for BPQueue."""

    def test_set_key(self) -> None:
        """Test the set_key method."""
        bpq = BPQueue(-3, 3)
        a = Dllink([0, 3])
        bpq.set_key(a, 0)
        assert a.data[0] == 4  # gain - offset

    def test_appendleft_direct(self) -> None:
        """Test the appendleft_direct method."""
        bpq = BPQueue(-3, 3)
        a = Dllink([0, 3])  # Following the example in the docstring
        bpq.appendleft_direct(a)
        assert not bpq.is_empty()
        # The appendleft_direct passes the internal key (0) to appendleft
        # appendleft treats it as an external key, so external key 0
        # corresponds to internal key 4 (0 - offset)
        assert bpq.get_max() == 0

    def test_decrease_key_with_return(self) -> None:
        """Test decrease_key when it returns early."""
        bpq = BPQueue(-3, 3)
        a = Dllink([0, 3])
        bpq.append(a, -1)
        bpq.decrease_key(a, 1)  # This should trigger the early return
        assert bpq.get_max() == -2

    def test_iterator_next(self) -> None:
        """Test the iterator's __next__ method directly."""
        bpq = BPQueue(-3, 3)
        a = Dllink([0, 3])
        b = Dllink([0, 4])
        bpq.append(a, 0)
        bpq.append(b, 1)

        it = iter(bpq)
        assert next(it) is b
        assert next(it) is a
        with pytest.raises(StopIteration):
            next(it)

    def test_increase_key_updates_max(self) -> None:
        """Test increase_key when it updates max."""
        bpq = BPQueue(-3, 3)
        a = Dllink([0, 3])
        bpq.append(a, -1)
        # Increase key to a value higher than current max
        bpq.increase_key(a, 3)
        assert bpq.get_max() == 2

    def test_modify_key_unlocked(self) -> None:
        """Test modify_key when item is not locked."""
        bpq = BPQueue(-3, 3)
        a = Dllink([0, 3])
        bpq.append(a, 0)
        # Item is not locked (next is not itself)
        assert a.next is not a
        bpq.modify_key(a, 1)
        assert bpq.get_max() == 1

    def test_modify_key_locked(self) -> None:
        """Test modify_key when item is locked."""
        bpq = BPQueue(-3, 3)
        a = Dllink([0, 3])
        # Lock the item by setting next to itself
        a.next = a
        assert a.next is a
        bpq.modify_key(a, 1)
        # Max should remain at initial value since modify_key returns early
        assert bpq.get_max() == -4

    def test_decrease_key_asserts(self) -> None:
        """Test decrease_key with boundary conditions to trigger asserts."""
        bpq = BPQueue(-3, 3)
        a = Dllink([0, 3])
        bpq.append(a, 0)

        # This should trigger the assert it.data[0] > 0
        # Use pytest.raises to ensure the assert is triggered
        with pytest.raises(AssertionError):
            bpq.decrease_key(a, 5)  # This would make it negative

    def test_iterator_next_direct(self) -> None:
        """Test BPQueueIterator.__next__ directly."""
        bpq = BPQueue(-3, 3)
        a = Dllink([0, 3])
        b = Dllink([0, 4])
        bpq.append(a, 0)
        bpq.append(b, 1)

        # Get the iterator and call __next__ directly
        it = iter(bpq)
        # Call __next__ method directly
        item1 = it.__next__()
        item2 = it.__next__()
        assert item1 is b
        assert item2 is a
        with pytest.raises(StopIteration):
            it.__next__()


class TestBPQueueProperties:
    """Property-based tests for BPQueue using Hypothesis."""

    @given(
        st.integers(min_value=-10, max_value=-1), st.integers(min_value=1, max_value=10)
    )
    def test_bpqueue_initial_empty_property(self, a, b):
        """New BPQueue should be empty."""
        bpq = BPQueue(a, b)
        assert bpq.is_empty()
        assert bpq.get_max() == a - 1

    @given(
        st.integers(min_value=-5, max_value=0),
        st.integers(min_value=1, max_value=5),
        st.lists(
            st.tuples(
                st.integers(min_value=1, max_value=100),
                st.integers(min_value=-5, max_value=5),
            ),
            min_size=1,
            max_size=20,
        ),
    )
    def test_bpqueue_priority_ordering_property(self, a, b, items_data):
        """Items should be returned in descending priority order."""
        bpq = BPQueue(a, b)
        items = []

        # Create items and add them to queue
        for item_id, priority in items_data:
            if a <= priority <= b:  # Only add items within valid range
                item = Dllink([item_id, priority])
                items.append(item)
                bpq.append(item, priority)

        if items:
            # Extract items in order and verify descending priority
            priorities = []
            while not bpq.is_empty():
                item = bpq.popleft()
                priorities.append(item.data[1])

            # Verify priorities are in descending order
            for i in range(len(priorities) - 1):
                assert priorities[i] >= priorities[i + 1]

    @given(
        st.integers(min_value=-5, max_value=0), st.integers(min_value=1, max_value=5)
    )
    def test_bpqueue_append_appendleft_order_property(self, a, b):
        """appendleft should reverse order compared to append for same priority."""
        bpq1 = BPQueue(a, b)
        bpq2 = BPQueue(a, b)

        items = [Dllink([i, i]) for i in range(3)]
        priority = 0  # Use same priority for all items

        # Test append vs appendleft
        for item in items:
            bpq1.append(item, priority)
            bpq2.appendleft(item, priority)

        # Extract items and compare order
        append_order = [bpq1.popleft().data[0] for _ in range(len(items))]
        appendleft_order = [bpq2.popleft().data[0] for _ in range(len(items))]

        assert append_order == appendleft_order[::-1]  # Should be reversed

    @given(
        st.integers(min_value=-5, max_value=0),
        st.integers(min_value=1, max_value=5),
        st.integers(min_value=-3, max_value=3),
        st.integers(min_value=1, max_value=3),
    )
    def test_bpqueue_increase_key_property(self, a, b, initial_key, delta):
        """Increasing key should move item to higher priority bucket."""
        if a <= initial_key <= b and a <= initial_key + delta <= b:
            bpq = BPQueue(a, b)
            item = Dllink([1, 1])

            bpq.append(item, initial_key)
            old_max = bpq.get_max()

            bpq.increase_key(item, delta)
            new_max = bpq.get_max()

            # New max should be at least as high as old max
            assert new_max >= old_max

    @given(
        st.integers(min_value=-5, max_value=0),
        st.integers(min_value=1, max_value=5),
        st.integers(min_value=-3, max_value=3),
        st.integers(min_value=1, max_value=3),
    )
    def test_bpqueue_decrease_key_property(self, a, b, initial_key, delta):
        """Decreasing key should move item to lower priority bucket."""
        if a <= initial_key <= b and a <= initial_key - delta <= b:
            bpq = BPQueue(a, b)
            item = Dllink([1, 1])

            bpq.append(item, initial_key)
            bpq.decrease_key(item, delta)

            # The item should still be in the queue
            found = False
            while not bpq.is_empty():
                if bpq.popleft() is item:
                    found = True
                    break
            assert found

    @given(
        st.integers(min_value=-5, max_value=0), st.integers(min_value=1, max_value=5)
    )
    def test_bpqueue_clear_property(self, a, b):
        """Clear should empty the queue."""
        bpq = BPQueue(a, b)

        # Add some items
        for i in range(5):
            if a <= i <= b:
                bpq.append(Dllink([i, i]), i)

        bpq.clear()
        assert bpq.is_empty()
        assert bpq.get_max() == a - 1

    @given(
        st.integers(min_value=-5, max_value=0),
        st.integers(min_value=1, max_value=5),
        st.lists(
            st.tuples(
                st.integers(min_value=1, max_value=100),
                st.integers(min_value=-5, max_value=5),
            ),
            min_size=1,
            max_size=10,
        ),
    )
    def test_bpqueue_detach_property(self, a, b, items_data):
        """Detaching an item should remove it from the queue."""
        bpq = BPQueue(a, b)
        items = []

        # Add items to queue
        for item_id, priority in items_data:
            if a <= priority <= b:
                item = Dllink([item_id, priority])
                items.append(item)
                bpq.append(item, priority)

        if items:
            # Remove a random item
            import random

            item_to_remove = random.choice(items)
            bpq.detach(item_to_remove)

            # Verify the item is no longer in the queue
            found = False
            while not bpq.is_empty():
                if bpq.popleft() is item_to_remove:
                    found = True
                    break
            assert not found
