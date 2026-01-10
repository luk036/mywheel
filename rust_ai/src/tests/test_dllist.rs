use crate::dllist::{Dllink, Dllist};

#[test]
fn test_dllink_constructor() {
    let mut link = Dllink::new(1);
    link.lock();
    assert_eq!(link.data(), &1);
    assert!(link.is_locked());
}

#[test]
fn test_dllink_lock_and_is_locked() {
    let mut link = Dllink::new(1);
    assert!(link.is_locked());

    // Create another node to test attachment
    let mut link2 = Dllink::new(2);
    unsafe {
        link.attach(&mut link2);
    }
    assert!(!link.is_locked());

    link.lock();
    assert!(link.is_locked());
}

#[test]
fn test_dllink_attach_and_detach() {
    let mut a = Dllink::new("a");
    let mut b = Dllink::new("b");
    let mut c = Dllink::new("c");
    a.lock();
    b.lock();
    c.lock();

    // Attach b after a
    unsafe {
        a.attach(&mut b);
    }
    assert!(!a.is_locked());
    assert!(!b.is_locked());

    // Attach c after b
    unsafe {
        b.attach(&mut c);
    }
    assert!(!c.is_locked());

    // Detach b
    unsafe {
        b.detach();
    }
    // After detach, b should be locked
    assert!(b.is_locked());
}

#[test]
fn test_dllist_constructor() {
    let dlist = Dllist::new(0);
    // Can't access head directly since it's private
    // Just check that it's empty
    assert!(dlist.is_empty());
}

#[test]
fn test_dllist_clear() {
    let mut dlist = Dllist::new(0);
    let mut link1 = Dllink::new(1);
    unsafe {
        dlist.append(&mut link1);
    }
    assert!(!dlist.is_empty());
    dlist.clear();
    assert!(dlist.is_empty());
}

#[test]
fn test_dllist_append_and_pop() {
    let mut dlist = Dllist::new(0);
    let mut link1 = Dllink::new(1);
    let mut link2 = Dllink::new(2);

    unsafe {
        dlist.append(&mut link1);
    }
    assert!(!dlist.is_empty());

    unsafe {
        dlist.append(&mut link2);
    }

    unsafe {
        let popped = dlist.pop();
        assert_eq!(popped.data(), &2);

        let popped = dlist.pop();
        assert_eq!(popped.data(), &1);
    }
    assert!(dlist.is_empty());
}

#[test]
fn test_dllist_appendleft_and_popleft() {
    let mut dlist = Dllist::new(0);
    let mut link1 = Dllink::new(1);
    let mut link2 = Dllink::new(2);

    unsafe {
        dlist.appendleft(&mut link1);
    }
    assert!(!dlist.is_empty());

    unsafe {
        dlist.appendleft(&mut link2);
    }

    unsafe {
        let popped = dlist.popleft();
        assert_eq!(popped.data(), &2);

        let popped = dlist.popleft();
        assert_eq!(popped.data(), &1);
    }
    assert!(dlist.is_empty());
}

#[test]
fn test_dllist_iteration() {
    let mut dlist = Dllist::new(0);
    let mut link1 = Dllink::new(1);
    let mut link2 = Dllink::new(2);
    let mut link3 = Dllink::new(3);

    unsafe {
        dlist.append(&mut link1);
        dlist.append(&mut link2);
        dlist.append(&mut link3);
    }

    let items: Vec<&i32> = dlist.iter().map(|link| link.data()).collect();
    assert_eq!(items, vec![&1, &2, &3]);
}

#[test]
fn test_dllist_empty_iteration() {
    let dlist = Dllist::new(0);
    let items: Vec<&i32> = dlist.iter().map(|link| link.data()).collect();
    assert_eq!(items, Vec::<&i32>::new());
}
