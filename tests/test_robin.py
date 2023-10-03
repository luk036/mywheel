from mywheel.robin import Robin


def test_robin():
    r = Robin(5)
    for k in r.exclude(3):
        print(k)
    assert r.exclude(3).cur.data == 3
    assert r.exclude(3).stop.data == 3
    assert r.exclude(3).cur.next.data == 4
    assert r.exclude(3).cur.next.next.data == 0
    assert r.exclude(3).cur.next.next.next.data == 1

