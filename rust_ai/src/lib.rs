//! MyWheel Rust implementation
//! 
//! This is a Rust port of the Python mywheel library, containing various data structures
//! and utilities.

pub mod array_like;
pub mod dllist;
pub mod bpqueue;
pub mod map_adapter;
pub mod robin;

#[cfg(test)]
mod tests {
    mod test_array_like;
    mod test_dllist;
    mod test_bpqueue;
    mod test_map_adapter;
    mod test_robin;
}