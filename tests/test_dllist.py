import pytest

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
        dlist = Dllist("head")
        assert dlist.head.data == "head"
        assert dlist.is_empty()

    def test_clear(self) -> None:
        dlist = Dllist("head")
        dlist.append(Dllink(1))
        dlist.clear()
        assert dlist.is_empty()

    def test_append_and_pop(self) -> None:
        dlist = Dllist("head")
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
        dlist = Dllist("head")
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
        dlist = Dllist("head")
        link1 = Dllink(1)
        link2 = Dllink(2)
        link3 = Dllink(3)

        dlist.append(link1)
        dlist.append(link2)
        dlist.append(link3)

        items = [item.data for item in dlist]
        assert items == [1, 2, 3]

    def test_empty_iteration(self) -> None:
        dlist = Dllist("head")
        items = [item.data for item in dlist]
        assert items == []


class TestDllIterator:
    def test_constructor(self) -> None:
        dlist = Dllist("head")
        iterator = DllIterator(dlist.head)
        assert iterator.link is dlist.head
        assert iterator.cur is dlist.head.next

    def test_next(self) -> None:
        dlist = Dllist("head")
        link1 = Dllink(1)
        link2 = Dllink(2)
        dlist.append(link1)
        dlist.append(link2)

        iterator = iter(dlist)
        assert next(iterator) is link1
        assert next(iterator) is link2
        with pytest.raises(StopIteration):
            next(iterator)
