# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Performance
- **Identity checks use `is`**: Replaced `id(x) == id(y)` with `x is y` in `Dllink.is_locked`, `Dllist.is_empty`, and `DllIterator.__next__`, and switched the node/bucket identity comparisons in `BPQueue` from `==` to `is`. This removes a `builtins.id` call from every hot-path check. Public API unchanged.
- **`BPQueue` skips redundant max scans**: `increase_key` only calls `_update_max_key()` when the raised key does not exceed the current max, and `detach` only calls it when the detached item was in the max bucket. Neither can leave `_max` pointing at an empty bucket. Public API unchanged.

## [0.6.0] - 2026-09-04

### Code Cleanup
- **Removed AI slop**: Stripped boilerplate from docstrings and comments across `array_like`, `bpqueue`, `dllist`, `map_adapter` and `robin`. (#4f8adb1)

### Build & CI
- **Updated GitHub Actions**: checkout→v4, setup-python→v5. (#cb993a9)
- **Removed stale `.bak` workflow**: Deleted `python-app.bak`. (#f8799c1)

## [0.5.0] - 2026-07-16

### Performance
- **`__slots__` on core classes**: Added `__slots__` to `MapAdapter`, `RepeatArray`, and `SlNode`, saving ~176 bytes per instance for each. (#f4d6f8c)
- **Compact BPQueue buckets**: Replaced per-bucket `Dllist([i, 4848])` with bare `Dllink` sentinels, eliminating the per-bucket `Dllist` wrapper object + list — saving ~168 bytes per bucket (~150 MB for large circuits with pmax=50K). (#f4d6f8c)

### Documentation
- **svgbob doubly-linked list diagram**: Added ASCII-to-SVG diagram to `dllist.py` module docstring. (#b275f30)

### Fixed
- **mypy errors**: Resolved type annotation errors in config and `bpqueue`. (#69e04ae)
- **Robin precondition**: Enforced `num_parts >= 2` precondition, replaced empty-cycle guard with assertion. (#5411bce)
- **Python 3.9 compat**: Added `from __future__ import annotations` for PEP 604 syntax. (#f99e33d)

### Testing
- **Coverage raised 95%→98%**: Deduped redundant tests, added slice and iterator coverage tests. (#71de094)

### Code Cleanup
- **Removed PyScaffold boilerplate**: Deleted `skeleton.py`/`test_skeleton.py`, dropped Python < 3.9 compat, removed dead entry points and duplicate `LICENSE`. (#bde6f85)

### Build & CI
- **CI repair**: Fixed broken entry_points and remaining skeleton imports. (#551afd2)
