import pytest
from hypothesis import given
from hypothesis import strategies as st

from mywheel.dllist import Dllink, Dllist, DllIterator


class TestDllink:
    def test_constructor(self) -> None:
        link = Dllink(1)
        assert link.data == 1
        assert link.next is link
        assert link.prev is link

    def test_lock_and_is_locked(self) -> None:
        link = Dllink(1)
        assert link.is_locked()
        link.next = Dllink(2)
        assert not link.is_locked()
        link.lock()
        assert link.is_locked()

    def test_attach_and_detach(self) -> None:
        a = Dllink("a")
        b = Dllink("b")
        c = Dllink("c")

        # Attach b after a
        a.attach(b)
        assert a.next is b
        assert b.prev is a
        assert b.next is a  # circular

        # Attach c after b
        b.attach(c)
        assert b.next is c
        assert c.prev is b
        assert c.next is a  # circular
        assert a.prev is c

        # Detach b
        b.detach()
        assert a.next is c
        assert c.prev is a


class TestDllist:
    def test_constructor(self) -> None:
        dlist = Dllist(0)
        assert dlist.head.data == 0
        assert dlist.is_empty()

    def test_clear(self) -> None:
        dlist = Dllist(0)
        dlist.append(Dllink(1))
        dlist.clear()
        assert dlist.is_empty()

    def test_append_and_pop(self) -> None:
        dlist = Dllist(0)  # Use int to match link types
        link1 = Dllink(1)
        link2 = Dllink(2)

        dlist.append(link1)
        assert not dlist.is_empty()
        assert dlist.head.next is link1
        assert dlist.head.prev is link1

        dlist.append(link2)
        assert dlist.head.next is link1
        assert dlist.head.prev is link2

        popped = dlist.pop()
        assert popped is link2
        assert dlist.head.prev is link1

        popped = dlist.pop()
        assert popped is link1
        assert dlist.is_empty()

    def test_appendleft_and_popleft(self) -> None:
        dlist = Dllist(0)  # Use int to match link types
        link1 = Dllink(1)
        link2 = Dllink(2)

        dlist.appendleft(link1)
        assert not dlist.is_empty()
        assert dlist.head.next is link1
        assert dlist.head.prev is link1

        dlist.appendleft(link2)
        assert dlist.head.next is link2
        assert dlist.head.prev is link1

        popped = dlist.popleft()
        assert popped is link2
        assert dlist.head.next is link1

        popped = dlist.popleft()
        assert popped is link1
        assert dlist.is_empty()

    def test_iteration(self) -> None:
        dlist = Dllist(0)  # Use int to match link types
        link1 = Dllink(1)
        link2 = Dllink(2)
        link3 = Dllink(3)

        dlist.append(link1)
        dlist.append(link2)
        dlist.append(link3)

        items = [item.data for item in dlist]
        assert items == [1, 2, 3]

    def test_empty_iteration(self) -> None:
        dlist = Dllist(0)  # Use int to match link types
        items = [item.data for item in dlist]
        assert items == []


class TestDllIterator:
    def test_constructor(self) -> None:
        dlist = Dllist("head")
        iterator = DllIterator(dlist.head)
        assert iterator.link is dlist.head
        assert iterator.cur is dlist.head.next

    def test_next(self) -> None:
        dlist = Dllist(0)  # Use int to match link types
        link1 = Dllink(1)
        link2 = Dllink(2)
        dlist.append(link1)
        dlist.append(link2)

        iterator = iter(dlist)
        assert next(iterator) is link1
        assert next(iterator) is link2
        with pytest.raises(StopIteration):
            next(iterator)

    def test_iterator_self(self) -> None:
        """Test that iterator returns self from __iter__."""
        dlist = Dllist(0)
        iterator = iter(dlist)
        assert iterator is iterator.__iter__()


class TestDllistProperties:
    """Property-based tests for Dllist using Hypothesis."""

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_dllist_append_pop_roundtrip_property(self, values):
        """Appending items and then popping them should preserve order."""
        dlist = Dllist(0)
        links = [Dllink(value) for value in values]

        # Append all items
        for link in links:
            dlist.append(link)

        # Pop all items and verify reverse order
        popped_values = []
        while not dlist.is_empty():
            popped = dlist.pop()
            popped_values.append(popped.data)

        assert popped_values == values[::-1]

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_dllist_appendleft_popleft_roundtrip_property(self, values):
        """Appending left and then popping left should preserve order."""
        dlist = Dllist(0)
        links = [Dllink(value) for value in values]

        # Append all items to the left
        for link in links:
            dlist.appendleft(link)

        # Pop all items from left and verify reverse order
        popped_values = []
        while not dlist.is_empty():
            popped = dlist.popleft()
            popped_values.append(popped.data)

        assert popped_values == values[::-1]

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_dllist_iteration_order_property(self, values):
        """Iteration should return items in insertion order for append."""
        dlist = Dllist(0)
        links = [Dllink(value) for value in values]

        # Append all items
        for link in links:
            dlist.append(link)

        # Iterate and verify order
        iterated_values = [item.data for item in dlist]
        assert iterated_values == values

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20)
    )
    def test_dllist_clear_property(self, values):
        """Clear should empty the list."""
        dlist = Dllist(0)
        links = [Dllink(value) for value in values]

        # Add all items
        for link in links:
            dlist.append(link)

        # Clear the list
        dlist.clear()
        assert dlist.is_empty()

        # Iteration should yield no items
        assert list(dlist) == []

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=2, max_size=10)
    )
    def test_dllist_mixed_operations_property(self, values):
        """Mixed append and appendleft operations should work correctly."""
        dlist = Dllist(0)
        links = [Dllink(value) for value in values]

        # Alternate between append and appendleft
        for i, link in enumerate(links):
            if i % 2 == 0:
                dlist.append(link)
            else:
                dlist.appendleft(link)

        # Extract all items
        remaining_items = []
        while not dlist.is_empty():
            remaining_items.append(dlist.popleft().data)

        # Verify all items are present (order may differ)
        assert sorted(remaining_items) == sorted(values)


class TestDllinkProperties:
    """Property-based tests for Dllink using Hypothesis."""

    @given(st.integers(min_value=-100, max_value=100))
    def test_dllink_initial_state_property(self, data):
        """New Dllink should point to itself."""
        link = Dllink(data)
        assert link.data == data
        assert link.next is link
        assert link.prev is link
        assert link.is_locked()

    @given(
        st.integers(min_value=-100, max_value=100),
        st.integers(min_value=-100, max_value=100),
    )
    def test_dllink_attach_detach_symmetry_property(self, data1, data2):
        """Attaching and detaching should be symmetric operations."""
        link1 = Dllink(data1)
        link2 = Dllink(data2)

        # Store original state
        original_next1 = link1.next
        original_prev1 = link1.prev

        # Attach link2 after link1
        link1.attach(link2)

        # Verify attachment
        assert link1.next is link2
        assert link2.prev is link1

        # Detach link2
        link2.detach()

        # Verify restoration of link1's connections
        assert link1.next is original_next1
        assert link1.prev is original_prev1

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=3, max_size=10)
    )
    def test_dllink_chain_property(self, values):
        """Chain of attached links should maintain correct connections."""
        links = [Dllink(value) for value in values]

        # Create chain: link0 -> link1 -> link2 -> ...
        for i in range(len(links) - 1):
            links[i].attach(links[i + 1])

        # Verify forward connections
        for i in range(len(links) - 1):
            assert links[i].next is links[i + 1]

        # Verify backward connections
        for i in range(1, len(links)):
            assert links[i].prev is links[i - 1]

        # Detach middle link and verify chain breaks correctly
        if len(links) >= 3:
            middle = len(links) // 2
            links[middle].detach()

            # Verify neighbors are now connected
            if middle > 0:
                assert (
                    links[middle - 1].next is links[middle + 1]
                    if middle + 1 < len(links)
                    else links[0]
                )
            if middle + 1 < len(links):
                assert (
                    links[middle + 1].prev is links[middle - 1]
                    if middle > 0
                    else links[-1]
                )
