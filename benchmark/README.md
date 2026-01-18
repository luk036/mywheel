# mywheel Benchmarks

This directory contains performance comparison benchmarks between `mywheel` data structures and Python's standard library.

## Running Benchmarks

```bash
# Run all benchmarks
python benchmark/benchmark.py

# Specific benchmark (edit script to run individual functions)
python benchmark/benchmark.py
```

## Benchmark Results

### Dllist vs collections.deque

| Operation | Items | Dllist (sec) | deque (sec) | Ratio |
|------------|---------|---------------|-------------|---------|
| Append     | 10,000  | 0.00093       | 0.00009    | 10.3x |
| Pop        | 1,000   | 0.00475       | 0.00157    | 3.0x  |

### Robin Iteration

| Operation | Items | Time (sec) |
|------------|---------|------------|
| Full cycle | 1,000  | 0.03413      |

## Interpreting Results

- **Dllist**: Designed for O(1) operations but with overhead from Dllink wrapper. deque is ~10x faster for simple append operations but Dllist provides node control for reuse.
- **Robin**: Efficient round-robin iteration with minimal overhead.
- **BPQueue**: Skipped in benchmarks - designed for specific use cases with bounded integer keys and node reuse (see documentation).

Note: Results vary based on hardware, Python version, and system load.
Run benchmarks multiple times for stable measurements.
