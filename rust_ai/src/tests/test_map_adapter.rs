use crate::map_adapter::MapAdapter;

#[test]
fn test_map_adapter_constructor() {
    let lst = vec![1, 2, 3];
    let adapter = MapAdapter::new(lst.clone());
    assert_eq!(adapter.lst(), &lst);
}

#[test]
fn test_map_adapter_getitem() {
    let adapter = MapAdapter::new(vec![1, 2, 3]);
    assert_eq!(adapter[0], 1);
    assert_eq!(adapter[2], 3);
}

#[test]
#[should_panic(expected = "index out of bounds")]
fn test_map_adapter_getitem_out_of_bounds() {
    let adapter = MapAdapter::new(vec![1, 2, 3]);
    let _ = adapter[3];
}

#[test]
fn test_map_adapter_setitem() {
    let mut adapter = MapAdapter::new(vec![1, 2, 3]);
    adapter[1] = 5;
    assert_eq!(adapter[1], 5);
}

#[test]
#[should_panic(expected = "index out of bounds")]
fn test_map_adapter_setitem_out_of_bounds() {
    let mut adapter = MapAdapter::new(vec![1, 2, 3]);
    adapter[3] = 6;
}

#[test]
fn test_map_adapter_iter() {
    let adapter = MapAdapter::new(vec![1, 2, 3]);
    let result: Vec<i32> = adapter.into_iter().collect();
    assert_eq!(result, vec![1, 2, 3]);
}

#[test]
fn test_map_adapter_len() {
    let adapter = MapAdapter::new(vec![1, 2, 3]);
    // Note: MapAdapter doesn't implement len() in Rust version
    // We can check by counting items
    let count = adapter.items().count();
    assert_eq!(count, 3);
}

#[test]
fn test_map_adapter_values() {
    let adapter = MapAdapter::new(vec![1, 2, 3]);
    let result: Vec<&i32> = adapter.values().collect();
    assert_eq!(result, vec![&1, &2, &3]);
}

#[test]
fn test_map_adapter_items() {
    let adapter = MapAdapter::new(vec![1, 2, 3]);
    let result: Vec<(usize, &i32)> = adapter.items().collect();
    assert_eq!(result, vec![(0, &1), (1, &2), (2, &3)]);
}

#[test]
fn test_map_adapter_keys() {
    let adapter = MapAdapter::new(vec![1, 2, 3]);
    let result: Vec<usize> = adapter.keys().collect();
    assert_eq!(result, vec![0, 1, 2]);
}
