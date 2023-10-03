from mywheel.dllist import Dllink, Dllist


def test_dllink() -> None:
    """
    The `test_dllink` function tests the `Dllink` class by creating a new `Dllink` object with a given data value,
    and then checking if the `data` attribute of the `Dllink` object is equal to the data value passed to the function.

    :return: None
    """
    a = Dllink(3)
    assert a.data == 3
    assert a.next is a
    assert a.prev is a
    assert a.is_locked() is True
    a.lock()
    assert a.is_locked() is True


def test_dllist():
    a = Dllist(3)
    b = Dllink(4)
    a.append(b)
    c = a.pop()
    assert b == c
    assert a.is_empty()
    a.clear()
    assert a.is_empty()
    a.append(b)
    assert not a.is_empty()
    a.clear()
    assert a.is_empty()
    a.appendleft(b)
    assert not a.is_empty()
    a.clear()
    assert a.is_empty()


def test_dllist2():
    L1 = Dllist(99)
    L2 = Dllist(99)
    d = Dllink(1)
    e = Dllink(2)
    f = Dllink(3)

    L1.appendleft(e)
    assert not L1.is_empty()

    L1.appendleft(f)
    L1.append(d)
    L2.append(L1.pop())
    L2.append(L1.popleft())
    assert not L1.is_empty()
    assert not L2.is_empty()
    e.detach()
    assert L1.is_empty()

    count = 0
    for _ in L2:
        count += 1
    assert count == 2
