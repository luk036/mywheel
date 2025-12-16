//! Array-like data structures
//!
//! This module provides array-like data structures with special indexing behavior.

use std::ops::{Index, IndexMut};

/// A list-like object that repeats a given value for a specified number of times.
///
/// # Examples
///
/// ```
/// use mywheel::array_like::RepeatArray;
///
/// let repeat_array = RepeatArray::new(1, 5);
/// assert_eq!(repeat_array.value, 1);
/// assert_eq!(repeat_array.size, 5);
/// assert_eq!(repeat_array[0], 1);
/// assert_eq!(repeat_array[4], 1);
/// ```
pub struct RepeatArray<T> {
    /// The value to repeat
    pub value: T,
    /// The number of times to repeat the value
    pub size: usize,
}

impl<T> RepeatArray<T> {
    /// Creates a new RepeatArray with the given value and size.
    pub fn new(value: T, size: usize) -> Self {
        Self { value, size }
    }

    /// Returns the value at any index (index is ignored).
    pub fn get(&self, _item: usize) -> &T {
        &self.value
    }
}

impl<T> Index<usize> for RepeatArray<T> {
    type Output = T;

    fn index(&self, _index: usize) -> &Self::Output {
        &self.value
    }
}

impl<T> IntoIterator for RepeatArray<T>
where
    T: Clone,
{
    type Item = T;
    type IntoIter = std::iter::Take<std::iter::Repeat<T>>;

    fn into_iter(self) -> Self::IntoIter {
        std::iter::repeat(self.value).take(self.size)
    }
}

impl<'a, T> IntoIterator for &'a RepeatArray<T>
where
    T: Clone,
{
    type Item = T;
    type IntoIter = std::iter::Take<std::iter::Repeat<T>>;

    fn into_iter(self) -> Self::IntoIter {
        std::iter::repeat(self.value.clone()).take(self.size)
    }
}

/// A list with arbitrary starting index.
///
/// # Examples
///
/// ```
/// use mywheel::array_like::ShiftArray;
///
/// let mut shift_array = ShiftArray::from(vec![1, 2, 3]);
/// shift_array.set_start(5);
/// assert_eq!(shift_array[5], 1);
/// assert_eq!(shift_array[7], 3);
/// ```
pub struct ShiftArray<T> {
    data: Vec<T>,
    start: usize,
}

impl<T> ShiftArray<T> {
    /// Creates a new ShiftArray from a vector.
    pub fn from(data: Vec<T>) -> Self {
        Self { data, start: 0 }
    }

    /// Sets the starting index for the array.
    pub fn set_start(&mut self, start: usize) {
        self.start = start;
    }

    /// Returns the current starting index.
    pub fn start(&self) -> usize {
        self.start
    }

    /// Returns an iterator over (index, value) pairs.
    pub fn items(&self) -> impl Iterator<Item = (usize, &T)> {
        self.data
            .iter()
            .enumerate()
            .map(move |(i, v)| (i + self.start, v))
    }

    /// Returns a mutable iterator over (index, value) pairs.
    pub fn items_mut(&mut self) -> impl Iterator<Item = (usize, &mut T)> {
        let start = self.start;
        self.data
            .iter_mut()
            .enumerate()
            .map(move |(i, v)| (i + start, v))
    }
}

impl<T> Index<usize> for ShiftArray<T> {
    type Output = T;

    fn index(&self, index: usize) -> &Self::Output {
        if index < self.start || index - self.start >= self.data.len() {
            panic!("Index out of range");
        }
        &self.data[index - self.start]
    }
}

impl<T> IndexMut<usize> for ShiftArray<T> {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        if index < self.start || index - self.start >= self.data.len() {
            panic!("Index out of range");
        }
        &mut self.data[index - self.start]
    }
}

impl<T> IntoIterator for ShiftArray<T> {
    type Item = T;
    type IntoIter = std::vec::IntoIter<T>;

    fn into_iter(self) -> Self::IntoIter {
        self.data.into_iter()
    }
}

impl<'a, T> IntoIterator for &'a ShiftArray<T> {
    type Item = &'a T;
    type IntoIter = std::slice::Iter<'a, T>;

    fn into_iter(self) -> Self::IntoIter {
        self.data.iter()
    }
}

impl<T> From<Vec<T>> for ShiftArray<T> {
    fn from(data: Vec<T>) -> Self {
        Self::from(data)
    }
}