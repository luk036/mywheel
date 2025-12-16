//! Doubly Linked List Implementation
//!
//! This module provides a doubly linked list data structure.

use std::cell::UnsafeCell;
use std::ptr;

/// A node in a doubly linked list.
///
/// # Safety
/// This struct uses raw pointers for performance and flexibility.
/// The caller must ensure proper memory management.
#[repr(C, align(8))]
pub struct Dllink<T> {
    next: *mut Dllink<T>,
    prev: *mut Dllink<T>,
    data: UnsafeCell<T>,
}

impl<T> Dllink<T> {
    /// Creates a new node with the given data.
    ///
    /// The node is initially locked (points to itself).
    pub fn new(data: T) -> Self {
        let mut node = Self {
            next: ptr::null_mut(),
            prev: ptr::null_mut(),
            data: UnsafeCell::new(data),
        };
        node.lock();
        node
    }

    /// Returns whether the node is locked (points to itself).
    pub fn is_locked(&self) -> bool {
        let self_ptr = std::ptr::from_ref(self) as *mut Dllink<T>;
        ptr::eq(self.next, self_ptr)
    }

    /// Locks the node (makes it point to itself).
    pub fn lock(&mut self) {
        let self_ptr = std::ptr::from_mut(self);
        self.next = self_ptr;
        self.prev = self_ptr;
    }

    /// Attaches another node after this node.
    ///
    /// # Safety
    /// The caller must ensure `node` is properly initialized and not already part of another list.
    pub unsafe fn attach(&mut self, node: &mut Dllink<T>) {
        node.next = self.next;
        node.prev = std::ptr::from_mut(self);
        if !self.next.is_null() {
            unsafe {
                (*self.next).prev = std::ptr::from_mut(node);
            }
        }
        self.next = std::ptr::from_mut(node);
    }

    /// Detaches this node from the list.
    ///
    /// # Safety
    /// The node must be part of a list.
    pub unsafe fn detach(&mut self) {
        unsafe {
            if !self.next.is_null() {
                (*self.next).prev = self.prev;
            }
            if !self.prev.is_null() {
                (*self.prev).next = self.next;
            }
        }
    }

    /// Returns a reference to the node's data.
    pub fn data(&self) -> &T {
        unsafe { &*self.data.get() }
    }

    /// Returns a mutable reference to the node's data.
    pub fn data_mut(&mut self) -> &mut T {
        unsafe { &mut *self.data.get() }
    }
}

impl<T> Drop for Dllink<T> {
    fn drop(&mut self) {
        if !self.is_locked() {
            unsafe {
                self.detach();
            }
        }
    }
}

/// An iterator over a doubly linked list.
pub struct DllIterator<'a, T> {
    link: &'a Dllink<T>,
    cur: *mut Dllink<T>,
}

impl<'a, T> DllIterator<'a, T> {
    /// Creates a new iterator starting from the given link.
    pub fn new(link: &'a Dllink<T>) -> Self {
        Self {
            link,
            cur: link.next,
        }
    }
}

impl<'a, T> Iterator for DllIterator<'a, T> {
    type Item = &'a Dllink<T>;

    fn next(&mut self) -> Option<Self::Item> {
        if ptr::eq(self.cur, self.link as *const _ as *mut _) {
            None
        } else {
            let result = unsafe { &*self.cur };
            self.cur = result.next;
            Some(result)
        }
    }
}

/// A doubly linked list with a sentinel head node.
pub struct Dllist<T> {
    head: Dllink<T>,
}

impl<T> Dllist<T> {
    /// Creates a new empty list with the given head data.
    pub fn new(data: T) -> Self {
        Self {
            head: Dllink::new(data),
        }
    }

    /// Returns whether the list is empty.
    pub fn is_empty(&self) -> bool {
        self.head.is_locked()
    }

    /// Clears the list.
    pub fn clear(&mut self) {
        self.head.lock();
    }

    /// Appends a node to the front of the list.
    ///
    /// # Safety
    /// The node must not be part of another list.
    pub unsafe fn appendleft(&mut self, node: &mut Dllink<T>) {
        unsafe {
            self.head.attach(node);
        }
    }

    /// Appends a node to the end of the list.
    ///
    /// # Safety
    /// The node must not be part of another list.
    pub unsafe fn append(&mut self, node: &mut Dllink<T>) {
        unsafe {
            (*self.head.prev).attach(node);
        }
    }

    /// Removes and returns the first node in the list.
    ///
    /// # Safety
    /// The list must not be empty.
    pub unsafe fn popleft(&mut self) -> &mut Dllink<T> {
        unsafe {
            let res = &mut *self.head.next;
            res.detach();
            res
        }
    }

    /// Removes and returns the last node in the list.
    ///
    /// # Safety
    /// The list must not be empty.
    pub unsafe fn pop(&mut self) -> &mut Dllink<T> {
        unsafe {
            let res = &mut *self.head.prev;
            res.detach();
            res
        }
    }

    /// Returns an iterator over the list.
    pub fn iter(&self) -> DllIterator<'_, T> {
        DllIterator::new(&self.head)
    }
}

impl<'a, T> IntoIterator for &'a Dllist<T> {
    type Item = &'a Dllink<T>;
    type IntoIter = DllIterator<'a, T>;

    fn into_iter(self) -> Self::IntoIter {
        self.iter()
    }
}