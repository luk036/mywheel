<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/mywheel.svg?branch=main)](https://cirrus-ci.com/github/<USER>/mywheel)
[![ReadTheDocs](https://readthedocs.org/projects/mywheel/badge/?version=latest)](https://mywheel.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/mywheel/main.svg)](https://coveralls.io/r/<USER>/mywheel)
[![PyPI-Server](https://img.shields.io/pypi/v/mywheel.svg)](https://pypi.org/project/mywheel/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/mywheel.svg)](https://anaconda.org/conda-forge/mywheel)
[![Monthly Downloads](https://pepy.tech/badge/mywheel/month)](https://pepy.tech/project/mywheel)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/mywheel)
-->

[![Python Version](https://img.shields.io/pypi/pyversions/mywheel.svg)](https://pypi.org/project/mywheel/)
[![PyPI-Server](https://img.shields.io/pypi/v/mywheel.svg)](https://pypi.org/project/mywheel/)
[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![Documentation Status](https://readthedocs.org/projects/mywheel/badge/?version=latest)](https://mywheel.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/luk036/mywheel/badge.svg?branch=main)](https://coveralls.io/github/luk036/mywheel?branch=main)
[![License](https://img.shields.io/github/license/luk036/mywheel.svg)](https://github.com/luk036/mywheel/blob/main/LICENSE.txt)

![logo](./reinventing-my-wheel.svg)

# 🛞 mywheel

> High-performance data structures and algorithms in Python

`mywheel` provides efficient implementations of fundamental data structures optimized for specific use cases in graph algorithms, EDA (Electronic Design Automation), and network optimization. All implementations prioritize memory efficiency and time complexity over Python's standard library alternatives.

## 🚀 Quick Start

### Installation

```bash
pip install mywheel
```

### Usage Examples

#### Doubly Linked List with O(1) Operations

```python
from mywheel import Dllist, Dllink

# Create list
dlist = Dllist(0)  # sentinel node
dlist.append(Dllink("A"))
dlist.append(Dllink("B"))

# O(1) operations
node = dlist.popleft()  # Remove first
dlist.appendleft(Dllink("C"))  # Add to front
```

#### Bounded Priority Queue for Small Integer Keys

```python
from mywheel import BPQueue, Dllink

# Efficient for keys in range [-5, 5]
bpq = BPQueue(-5, 5)

# Add items with integer keys
bpq.append(Dllink("task1"), 3)
bpq.append(Dllink("task2"), 5)

# Extract highest priority item
item = bpq.popleft()
```

#### Round-Robin Iteration

```python
from mywheel import Robin

# Create 5-part cycle
robin = Robin(5)

# Iterate excluding starting position
for part in robin.exclude(2):
    print(part)  # Prints: 3, 4, 0, 1
```

#### Array-Like Utilities

```python
from mywheel import MapAdapter

# Adapt list to dict-like interface
lst = [10, 20, 30, 40]
mapping = MapAdapter(lst)

mapping[0] = 99
assert mapping[0] == 99
```

## 📊 Performance Characteristics

| Data Structure | Insert | Delete | Lookup | Memory | Best For |
|---------------|---------|---------|---------|---------|-----------|
| `Dllist` | O(1) | O(1) | N/A | Minimal | Frequent front/back operations |
| `BPQueue` | O(1)* | O(k) | O(1) | O(b-a) | Small bounded integer keys |
| `Robin` | O(n) | N/A | O(1) | O(n) | Round-robin scheduling |
| `MapAdapter` | O(1) | N/A | O(1) | O(n) | Dict-like list access |

\* O(1) amortized for bounded keys

## 🎯 Used In

- [digraphx](https://luk036.github.io/digraphx) - Graph algorithms and data structures
- [netlistx](https://luk036.github.io/netlistx) - VLSI netlist partitioning
- [ckpttnpy](https://luk036.github.io/ckpttnpy) - Multi-level circuit partitioning

## ✨ Features

- **Memory Efficient**: Uses `__slots__` and sentinel nodes to minimize overhead
- **Type Safe**: Full type hints with mypy support
- **Well Tested**: 100% coverage with pytest and hypothesis
- **Zero Dependencies**: Pure Python, no external runtime dependencies
- **Python 3.8+**: Supports all modern Python versions

## 🔧 Development

```bash
# Clone and install
git clone https://github.com/luk036/mywheel.git
cd mywheel
pip install -e ".[testing]"

# Run tests
pytest

# Run type checking
mypy src/mywheel

# Run linting
pre-commit run --all-files
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

<!-- pyscaffold-notes -->

## 👉 Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
