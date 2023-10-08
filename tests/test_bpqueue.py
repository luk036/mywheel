from mywheel.bpqueue import BPQueue, BPQueueIterator
from mywheel.dllist import Dllink


def test_bpqueue():
    bpq = BPQueue(-3, 3)
    a = Dllink([0, 3])
    bpq.append(a, 0)
    it = BPQueueIterator(bpq)
    b = next(it)
    bpq.decrease_key(a, 1)
    assert b.data[0] == 3
    bpq.increase_key(a, 1)
    assert b.data[0] == 4
    bpq.modify_key(a, 1)
    assert b.data[0] == 5
    bpq.detach(a)
    assert bpq._max == 0
    bpq.clear()
    assert bpq._max == 0
    bpq.append(a, 1)


def test_bpqueue1():
    try:
        _ = BPQueue(-10.4, 10.4)
    except TypeError:
        print("ok")

    bpq1 = BPQueue(-10, 10)
    bpq2 = BPQueue(-10, 10)

    assert bpq1._max == 0  # is_empty()

    d = Dllink([0, 0])
    e = Dllink([0, 1])
    f = Dllink([0, 2])

    assert d.data[0] == 0

    bpq1.append(e, 3)
    bpq1.append(f, -10)
    bpq1.append(d, 5)

    bpq2.append(bpq1.popleft(), -6)  # d
    bpq2.append(bpq1.popleft(), 3)
    bpq2.append(bpq1.popleft(), 0)

    bpq2.modify_key(d, 15)
    bpq2.modify_key(d, -3)
    bpq2.detach(f)
    assert bpq1._max == 0  # is_empty()
    assert bpq2.get_max() == 6
    bpq1.clear()
    nodelist = list(Dllink([0, i]) for i in range(10))

    for i, it in enumerate(nodelist):
        it.data[0] = 2 * i - 10
    bpq1.appendfrom(nodelist)

    count = 0
    for _ in bpq1:
        count += 1
    assert count == 10

    bpq1.clear()
    assert bpq1._max == 0  # is_empty()
