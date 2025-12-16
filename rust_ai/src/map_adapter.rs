//! Map Adapter
//!
//! This module provides a MapAdapter that adapts a list to behave like a dictionary.

use std::collections::HashMap;
use std::ops::{Index, IndexMut};

/// A custom implementation of a mutable mapping with integer keys and generic values,
/// which adapts a list to behave like a dictionary.
pub struct MapAdapter<T> {
    lst: Vec<T>,
}

impl<T> MapAdapter<T> {
    /// Creates a new MapAdapter from a vector.
    pub fn new(lst: Vec<T>) -> Self {
        Self { lst }
    }

    /// Returns a reference to the underlying vector.
    pub fn lst(&self) -> &Vec<T> {
        &self.lst
    }

    /// Returns a mutable reference to the underlying vector.
    pub fn lst_mut(&mut self) -> &mut Vec<T> {
        &mut self.lst
    }

    /// Returns an iterator over the values.
    pub fn values(&self) -> std::slice::Iter<'_, T> {
        self.lst.iter()
    }

    /// Returns a mutable iterator over the values.
    pub fn values_mut(&mut self) -> std::slice::IterMut<'_, T> {
        self.lst.iter_mut()
    }

    /// Returns an iterator over (index, value) pairs.
    pub fn items(&self) -> impl Iterator<Item = (usize, &T)> {
        self.lst.iter().enumerate()
    }

    /// Returns a mutable iterator over (index, value) pairs.
    pub fn items_mut(&mut self) -> impl Iterator<Item = (usize, &mut T)> {
        self.lst.iter_mut().enumerate()
    }

    /// Returns an iterator over the keys (indices).
    pub fn keys(&self) -> impl Iterator<Item = usize> {
        0..self.lst.len()
    }
}

impl<T> Index<usize> for MapAdapter<T> {
    type Output = T;

    fn index(&self, index: usize) -> &Self::Output {
        &self.lst[index]
    }
}

impl<T> IndexMut<usize> for MapAdapter<T> {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        &mut self.lst[index]
    }
}

impl<T> IntoIterator for MapAdapter<T> {
    type Item = T;
    type IntoIter = std::vec::IntoIter<T>;

    fn into_iter(self) -> Self::IntoIter {
        self.lst.into_iter()
    }
}

impl<'a, T> IntoIterator for &'a MapAdapter<T> {
    type Item = &'a T;
    type IntoIter = std::slice::Iter<'a, T>;

    fn into_iter(self) -> Self::IntoIter {
        self.lst.iter()
    }
}

impl<T> From<Vec<T>> for MapAdapter<T> {
    fn from(lst: Vec<T>) -> Self {
        Self::new(lst)
    }
}

/// Extension trait for HashMap to provide MapAdapter-like functionality.
pub trait MapAdapterExt<K, V> {
    /// Returns an iterator over the keys.
    fn keys_iter(&self) -> std::collections::hash_map::Keys<'_, K, V>;
    
    /// Returns an iterator over the values.
    fn values_iter(&self) -> std::collections::hash_map::Values<'_, K, V>;
    
    /// Returns an iterator over (key, value) pairs.
    fn items_iter(&self) -> std::collections::hash_map::Iter<'_, K, V>;
}

impl<K, V> MapAdapterExt<K, V> for HashMap<K, V> {
    fn keys_iter(&self) -> std::collections::hash_map::Keys<'_, K, V> {
        self.keys()
    }
    
    fn values_iter(&self) -> std::collections::hash_map::Values<'_, K, V> {
        self.values()
    }
    
    fn items_iter(&self) -> std::collections::hash_map::Iter<'_, K, V> {
        self.iter()
    }
}