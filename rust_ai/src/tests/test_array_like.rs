use crate::array_like::{RepeatArray, ShiftArray};

#[test]
fn test_repeat_array_constructor() {
    let ra = RepeatArray::new(10, 5);
    assert_eq!(ra.value, 10);
    assert_eq!(ra.size, 5);
}

#[test]
fn test_repeat_array_getitem() {
    let ra = RepeatArray::new(10, 5);
    assert_eq!(ra[0], 10);
    assert_eq!(ra[4], 10);
    // The index is ignored, so any index should work
    assert_eq!(ra[100], 10);
}

#[test]
fn test_repeat_array_len() {
    let ra = RepeatArray::new(10, 5);
    // Note: RepeatArray doesn't implement len() in Rust version
    // We can check size directly
    assert_eq!(ra.size, 5);
}

#[test]
fn test_repeat_array_iter() {
    let ra = RepeatArray::new(10, 3);
    let result: Vec<i32> = ra.into_iter().collect();
    assert_eq!(result, vec![10, 10, 10]);
}

#[test]
fn test_repeat_array_get() {
    let ra = RepeatArray::new(10, 5);
    assert_eq!(ra.get(0), &10);
    assert_eq!(ra.get(100), &10);
}

#[test]
fn test_shift_array_constructor() {
    let sa = ShiftArray::from(vec![1, 2, 3]);
    assert_eq!(sa.start(), 0);
    let result: Vec<i32> = sa.into_iter().collect();
    assert_eq!(result, vec![1, 2, 3]);
}

#[test]
fn test_shift_array_set_start() {
    let mut sa = ShiftArray::from(vec![1, 2, 3]);
    sa.set_start(5);
    assert_eq!(sa.start(), 5);
}

#[test]
fn test_shift_array_getitem() {
    let mut sa = ShiftArray::from(vec![1, 2, 3]);
    sa.set_start(5);
    assert_eq!(sa[5], 1);
    assert_eq!(sa[7], 3);
}

#[test]
#[should_panic(expected = "Index out of range")]
fn test_shift_array_getitem_out_of_range_low() {
    let mut sa = ShiftArray::from(vec![1, 2, 3]);
    sa.set_start(5);
    let _ = sa[4];
}

#[test]
#[should_panic(expected = "Index out of range")]
fn test_shift_array_getitem_out_of_range_high() {
    let mut sa = ShiftArray::from(vec![1, 2, 3]);
    sa.set_start(5);
    let _ = sa[8];
}

#[test]
fn test_shift_array_setitem() {
    let mut sa = ShiftArray::from(vec![1, 2, 3]);
    sa.set_start(5);
    sa[6] = 10;
    assert_eq!(sa[6], 10);
    let result: Vec<i32> = sa.into_iter().collect();
    assert_eq!(result, vec![1, 10, 3]);
}

#[test]
#[should_panic(expected = "Index out of range")]
fn test_shift_array_setitem_out_of_range() {
    let mut sa = ShiftArray::from(vec![1, 2, 3]);
    sa.set_start(5);
    sa[8] = 5;
}

#[test]
fn test_shift_array_len() {
    let sa = ShiftArray::from(vec![1, 2, 3]);
    // Note: ShiftArray doesn't implement len() in Rust version
    // We can check by iterating
    let count = sa.into_iter().count();
    assert_eq!(count, 3);
}

#[test]
fn test_shift_array_items() {
    let mut sa = ShiftArray::from(vec![1, 2, 3]);
    sa.set_start(5);
    let items: Vec<(usize, &i32)> = sa.items().collect();
    assert_eq!(items, vec![(5, &1), (6, &2), (7, &3)]);
}
