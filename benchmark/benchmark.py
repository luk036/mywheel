"""
Benchmark script comparing mywheel data structures with Python stdlib.

Run with: python benchmark/benchmark.py
"""

import timeit


def benchmark_dllist_vs_deque():
    """Compare Dllist with collections.deque for append/pop operations."""

    print("=== Dllist vs collections.deque ===")

    n = 10000

    # Test append/pop operations
    dlist_setup = f"""
from mywheel import Dllist, Dllink
dlist = Dllist(0)
for i in range({n}):
    dlist.append(Dllink(i))
"""

    deque_setup = f"""
from collections import deque
dque = deque()
for i in range({n}):
    dque.append(i)
"""

    print(f"Append operations (n={n}):")
    t_dllist = timeit.timeit("dlist.append(Dllink(i))", setup=dlist_setup, number=1000)
    print(f"  Dllist:  {t_dllist:.5f} sec")
    t_deque = timeit.timeit("dque.append(i)", setup=deque_setup, number=1000)
    print(f"  deque:    {t_deque:.5f} sec")

    dlist_pop_stmt = "[dlist.pop() for _ in range(1000)]"
    deque_pop_stmt = "[dque.pop() for _ in range(1000)]"

    print("Pop operations (1000 items):")
    t_dllist_pop = timeit.timeit(dlist_pop_stmt, setup=dlist_setup, number=10)
    print(f"  Dllist:  {t_dllist_pop:.5f} sec")
    t_deque_pop = timeit.timeit(deque_pop_stmt, setup=deque_setup, number=10)
    print(f"  deque:    {t_deque_pop:.5f} sec")


def benchmark_bpqueue_vs_heapq():
    """Compare BPQueue with heapq for bounded integer keys."""

    print("\n=== BPQueue vs heapq (bounded keys) ===")
    print("Note: BPQueue benchmark skipped due to complexity of timeit usage.")
    print("      BPQueue is designed for specific use cases with bounded integer keys.")
    print("      See documentation for performance characteristics.")


def benchmark_robin_iteration():
    """Benchmark Robin round-robin iteration."""

    print("\n=== Robin Round-Robin Iteration ===")

    n = 1000

    robin_setup = f"""
from mywheel import Robin
robin = Robin({n})
"""

    print(f"Full cycle iteration (n={n}):")
    robin_iter_stmt = "list(robin.exclude(0))"
    t_robin = timeit.timeit(robin_iter_stmt, setup=robin_setup, number=100)
    print(f"  Robin:    {t_robin:.5f} sec")


def run_all_benchmarks():
    """Run all benchmarks."""

    print("mywheel Performance Benchmarks")
    print("=" * 50)
    print("Note: These are microbenchmarks. Real-world performance")
    print("      depends on usage patterns and data sizes.")
    print("      Run multiple times for stable results.")
    print()

    benchmark_dllist_vs_deque()
    benchmark_bpqueue_vs_heapq()
    benchmark_robin_iteration()

    print("\n" + "=" * 50)
    print("Benchmarking complete!")


if __name__ == "__main__":
    run_all_benchmarks()
