use crate::bpqueue::BPQueue;
use crate::dllist::Dllink;

#[test]
fn test_bpqueue_constructor() {
    let bpq = BPQueue::new(-3, 3);
    assert!(bpq.is_empty());
    assert_eq!(bpq.get_max(), -4); // a - 1
}

#[test]
fn test_bpqueue_append_and_pop() {
    let mut bpq = BPQueue::new(-5, 5);
    let mut a = Dllink::new([0, 1]);
    let mut b = Dllink::new([0, 2]);
    let mut c = Dllink::new([0, 3]);
    a.lock();
    b.lock();
    c.lock();

    unsafe {
        bpq.append(&mut a, 3);
        bpq.append(&mut b, -2);
        bpq.append(&mut c, 5);
    }

    assert!(!bpq.is_empty());
    assert_eq!(bpq.get_max(), 5);

    unsafe {
        bpq.popleft();
        assert_eq!(bpq.get_max(), 3);

        bpq.popleft();
        assert_eq!(bpq.get_max(), -2);

        bpq.popleft();
    }
    assert!(bpq.is_empty());
}

#[test]
fn test_bpqueue_appendleft() {
    let mut bpq = BPQueue::new(-5, 5);
    let mut a = Dllink::new([0, 1]);
    let mut b = Dllink::new([0, 2]);

    unsafe {
        bpq.appendleft(&mut a, 3);
        bpq.appendleft(&mut b, 3);
    }

    unsafe {
        bpq.popleft();
        bpq.popleft();
    }
}

#[test]
fn test_bpqueue_clear() {
    let mut bpq = BPQueue::new(-5, 5);
    let mut a = Dllink::new([0, 1]);

    unsafe {
        bpq.append(&mut a, 3);
    }
    bpq.clear();
    assert!(bpq.is_empty());
}

#[test]
fn test_bpqueue_key_manipulation() {
    let mut bpq = BPQueue::new(-5, 5);
    let mut a = Dllink::new([0, 1]);

    unsafe {
        bpq.append(&mut a, 0);
        assert_eq!(bpq.get_max(), 0);

        bpq.increase_key(&mut a, 2);
        assert_eq!(bpq.get_max(), 2);

        bpq.decrease_key(&mut a, 3);
        assert_eq!(bpq.get_max(), -1);

        bpq.modify_key(&mut a, 4);
        assert_eq!(bpq.get_max(), 3);

        bpq.modify_key(&mut a, -5);
        assert_eq!(bpq.get_max(), -2);
    }
}

#[test]
fn test_bpqueue_detach() {
    let mut bpq = BPQueue::new(-5, 5);
    let mut a = Dllink::new([0, 1]);
    let mut b = Dllink::new([0, 2]);

    unsafe {
        bpq.append(&mut a, 3);
        bpq.append(&mut b, 5);

        bpq.detach(&mut a);
        assert_eq!(bpq.get_max(), 5);

        bpq.popleft();
    }
    assert!(bpq.is_empty());
}

#[test]
fn test_bpqueue_locked_item() {
    let mut bpq = BPQueue::new(-5, 5);
    let mut a = Dllink::new([0, 1]);

    unsafe {
        bpq.append(&mut a, 0);
        a.lock();
        bpq.modify_key(&mut a, 3); // Should have no effect
        assert_eq!(bpq.get_max(), 0);
    }
}
