use crate::robin::Robin;

#[test]
fn test_robin_constructor() {
    let mut r = Robin::new(5);
    // We can't directly access cycle in tests due to private field
    // But we can test iteration
    let result: Vec<i32> = r.exclude(0).collect();
    assert_eq!(result, vec![1, 2, 3, 4]);
}

#[test]
fn test_robin_exclude() {
    let mut r = Robin::new(5);
    let iterator = r.exclude(3);
    // Just verify we got an iterator
    let _count = iterator.count();
}

#[test]
fn test_robin_iteration() {
    let mut r = Robin::new(5);
    
    // Test starting from 0
    let result: Vec<i32> = r.exclude(0).collect();
    assert_eq!(result, vec![1, 2, 3, 4]);

    // Test starting from 3
    let mut r = Robin::new(5);
    let result: Vec<i32> = r.exclude(3).collect();
    assert_eq!(result, vec![4, 0, 1, 2]);

    // Test starting from the last element
    let mut r = Robin::new(5);
    let result: Vec<i32> = r.exclude(4).collect();
    assert_eq!(result, vec![0, 1, 2, 3]);
}

#[test]
fn test_robin_one_part() {
    let mut r = Robin::new(1);
    let result: Vec<i32> = r.exclude(0).collect();
    assert_eq!(result, Vec::<i32>::new());
}

#[test]
#[should_panic(expected = "Cannot exclude from an empty cycle.")]
fn test_robin_zero_parts() {
    let mut r = Robin::new(0);
    let _ = r.exclude(0);
}