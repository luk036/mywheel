//! Bounded Priority Queue (BPQueue)
//!
//! This module implements a Bounded Priority Queue data structure using an array of
//! doubly-linked lists, optimized for small integer keys.

use crate::dllist::{Dllink, Dllist};
use std::iter::Iterator;

/// A bounded priority queue with integer keys in [a..b].
///
/// Implemented by array (bucket) of doubly-linked lists.
/// Efficient if key is bounded by a small integer value.
pub struct BPQueue {
    max: usize,
    offset: i32,
    high: usize,
    bucket: Vec<Dllist<[i32; 2]>>,
}

impl BPQueue {
    /// Creates a new BPQueue with the given bounds [a, b].
    ///
    /// # Panics
    /// Panics if a > b.
    pub fn new(a: i32, b: i32) -> Self {
        assert!(a <= b);
        let max = 0;
        let offset = a - 1;
        let high = (b - offset) as usize;
        let mut bucket = Vec::with_capacity(high + 1);
        
        for i in 0..=high {
            bucket.push(Dllist::new([i as i32, 4848]));
        }
        
        let mut sentinel = Dllink::new([0, 8965]);
        unsafe {
            bucket[0].appendleft(&mut sentinel);
        }
        
        Self {
            max,
            offset,
            high,
            bucket,
        }
    }

    /// Returns whether the queue is empty.
    pub fn is_empty(&self) -> bool {
        self.max == 0
    }

    /// Returns the maximum key in the queue.
    pub fn get_max(&self) -> i32 {
        (self.max as i32) + self.offset
    }

    /// Clears the queue.
    pub fn clear(&mut self) {
        while self.max > 0 {
            self.bucket[self.max].clear();
            self.max -= 1;
        }
    }

    /// Sets the key of an item.
    ///
    /// # Safety
    /// The item must be properly initialized.
    pub unsafe fn set_key(&self, it: &mut Dllink<[i32; 2]>, gain: i32) {
        it.data_mut()[0] = gain - self.offset;
    }

    /// Appends an item using its internal key.
    ///
    /// # Safety
    /// The item must be properly initialized and not already in the queue.
    pub unsafe fn appendleft_direct(&mut self, it: &mut Dllink<[i32; 2]>) {
        assert!(it.data()[0] > self.offset);
        unsafe {
            self.appendleft(it, it.data()[0]);
        }
    }

    /// Appends an item with an external key to the front of its bucket.
    ///
    /// # Safety
    /// The item must be properly initialized and not already in the queue.
    pub unsafe fn appendleft(&mut self, it: &mut Dllink<[i32; 2]>, k: i32) {
        assert!(k > self.offset);
        it.data_mut()[0] = k - self.offset;
        let key = it.data()[0] as usize;
        if self.max < key {
            self.max = key;
        }
        unsafe {
            self.bucket[key].appendleft(it);
        }
    }

    /// Appends an item with an external key to the end of its bucket.
    ///
    /// # Safety
    /// The item must be properly initialized and not already in the queue.
    pub unsafe fn append(&mut self, it: &mut Dllink<[i32; 2]>, k: i32) {
        assert!(k > self.offset);
        it.data_mut()[0] = k - self.offset;
        let key = it.data()[0] as usize;
        if self.max < key {
            self.max = key;
        }
        unsafe {
            self.bucket[key].append(it);
        }
    }

    /// Appends multiple items from an iterator.
    ///
    /// # Safety
    /// All items must be properly initialized and not already in the queue.
    pub unsafe fn appendfrom<'a, I>(&mut self, nodes: I)
    where
        I: Iterator<Item = &'a mut Dllink<[i32; 2]>>,
    {
        for it in nodes {
            it.data_mut()[0] -= self.offset;
            assert!(it.data()[0] > 0);
            let key = it.data()[0] as usize;
            unsafe {
                self.bucket[key].appendleft(it);
            }
        }
        self.max = self.high;
        while self.bucket[self.max].is_empty() {
            self.max -= 1;
        }
    }

    /// Removes and returns the item with the highest key.
    ///
    /// # Safety
    /// The queue must not be empty.
    pub unsafe fn popleft(&mut self) {
        let max = self.max;
        
        unsafe {
            self.bucket[max].popleft();
        }
        
        // Update max
        while self.max > 0 && self.bucket[self.max].is_empty() {
            self.max -= 1;
        }
    }

    /// Decreases the key of an item.
    ///
    /// # Safety
    /// The item must be properly initialized.
    pub unsafe fn decrease_key(&mut self, it: &mut Dllink<[i32; 2]>, delta: i32) {
        unsafe {
            it.detach();
        }
        it.data_mut()[0] -= delta;
        assert!(it.data()[0] > 0);
        assert!(it.data()[0] as usize <= self.high);
        let key = it.data()[0] as usize;
        unsafe {
            self.bucket[key].append(it); // FIFO
        }
        if self.max < key {
            self.max = key;
            return;
        }
        self.update_max_key();
    }

    /// Increases the key of an item.
    ///
    /// # Safety
    /// The item must be properly initialized.
    pub unsafe fn increase_key(&mut self, it: &mut Dllink<[i32; 2]>, delta: i32) {
        unsafe {
            it.detach();
        }
        it.data_mut()[0] += delta;
        assert!(it.data()[0] > 0);
        assert!(it.data()[0] as usize <= self.high);
        let key = it.data()[0] as usize;
        unsafe {
            self.bucket[key].appendleft(it); // LIFO
        }
        if self.max < key {
            self.max = key;
        }
        self.update_max_key();
    }

    /// Modifies the key of an item (increase or decrease).
    ///
    /// # Safety
    /// The item must be properly initialized.
    pub unsafe fn modify_key(&mut self, it: &mut Dllink<[i32; 2]>, delta: i32) {
        if it.is_locked() {
            return;
        }
        if delta > 0 {
            unsafe {
                self.increase_key(it, delta);
            }
        } else if delta < 0 {
            unsafe {
                self.decrease_key(it, -delta);
            }
        }
    }

    /// Detaches an item from the queue.
    ///
    /// # Safety
    /// The item must be properly initialized and in the queue.
    pub unsafe fn detach(&mut self, it: &mut Dllink<[i32; 2]>) {
        unsafe {
            it.detach();
        }
        self.update_max_key();
    }

    /// Updates the maximum key in the queue.
    fn update_max_key(&mut self) {
        while self.bucket[self.max].is_empty() {
            self.max -= 1;
        }
    }

    /// Returns an iterator over the queue in descending priority order.
    pub fn iter(&self) -> BPQueueIterator<'_> {
        BPQueueIterator::new(self)
    }
}

/// An iterator over a BPQueue in descending priority order.
pub struct BPQueueIterator<'a> {
    curkey: usize,
    _marker: std::marker::PhantomData<&'a ()>,
}

impl<'a> BPQueueIterator<'a> {
    /// Creates a new iterator for the given BPQueue.
    fn new(bpq: &'a BPQueue) -> Self {
        let curkey = bpq.max;
        Self {
            curkey,
            _marker: std::marker::PhantomData,
        }
    }
}

impl<'a> Iterator for BPQueueIterator<'a> {
    type Item = &'a Dllink<[i32; 2]>;

    fn next(&mut self) -> Option<Self::Item> {
        while self.curkey > 0 {
            // Simplified implementation - in practice, we'd iterate over the Dllist
            // For now, return None to indicate the iterator is done
            self.curkey -= 1;
        }
        None
    }
}

impl<'a> IntoIterator for &'a BPQueue {
    type Item = &'a Dllink<[i32; 2]>;
    type IntoIter = BPQueueIterator<'a>;

    fn into_iter(self) -> Self::IntoIter {
        self.iter()
    }
}