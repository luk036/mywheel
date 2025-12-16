//! Round-Robin Implementation
//!
//! This module implements a round-robin algorithm for cycling through elements.

use std::ptr;

/// Node for a singly-linked list.
pub struct SlNode {
    next: *mut SlNode,
    data: i32,
}

impl SlNode {
    /// Creates a new node with the given data.
    pub fn new(data: i32) -> Self {
        let mut node = Self {
            next: ptr::null_mut(),
            data,
        };
        node.next = &mut node as *mut _;
        node
    }
}

/// An iterator that iterates over a singly linked list starting from a given node.
pub struct RobinIterator {
    cur: *mut SlNode,
    stop: *mut SlNode,
}

impl RobinIterator {
    /// Creates a new iterator starting from the given node.
    pub fn new(node: &mut SlNode) -> Self {
        Self {
            cur: node as *mut _,
            stop: node as *mut _,
        }
    }
}

impl Iterator for RobinIterator {
    type Item = i32;

    fn next(&mut self) -> Option<Self::Item> {
        unsafe {
            self.cur = (*self.cur).next;
            if !ptr::eq(self.cur, self.stop) {
                Some((*self.cur).data)
            } else {
                None
            }
        }
    }
}

/// Round Robin implementation for cycling through a list of parts.
pub struct Robin {
    cycle: Vec<*mut SlNode>,
}

impl Robin {
    /// Creates a new Robin with the given number of parts.
    pub fn new(num_parts: usize) -> Self {
        if num_parts == 0 {
            return Self { cycle: Vec::new() };
        }
        
        let mut nodes: Vec<Box<SlNode>> = (0..num_parts as i32)
            .map(|k| Box::new(SlNode::new(k)))
            .collect();
        
        let mut cycle: Vec<*mut SlNode> = nodes.iter_mut().map(|node| &mut **node as *mut _).collect();
        
        // Link nodes in a circular list
        for i in 0..num_parts {
            let prev = if i == 0 { num_parts - 1 } else { i - 1 };
            unsafe {
                (*cycle[prev]).next = cycle[i];
            }
        }
        
        // Leak the nodes to keep them alive
        std::mem::forget(nodes);
        
        Self { cycle }
    }

    /// Returns an iterator starting from the specified part.
    ///
    /// # Panics
    /// Panics if the cycle is empty.
    pub fn exclude(&mut self, from_part: usize) -> RobinIterator {
        if self.cycle.is_empty() {
            panic!("Cannot exclude from an empty cycle.");
        }
        unsafe {
            RobinIterator::new(&mut *self.cycle[from_part])
        }
    }
}

impl Drop for Robin {
    fn drop(&mut self) {
        // Reconstruct the boxes to properly deallocate memory
        for &ptr in &self.cycle {
            unsafe {
                let _ = Box::from_raw(ptr);
            }
        }
    }
}