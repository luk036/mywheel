# AGENTS.md

This file guides agentic coding agents working in the `mywheel` repository.

## Build / Test / Lint Commands

### Building
```bash
python -m build               # Build package (sdist + wheel)
python -m build --wheel      # Build wheel only
tox -e build                 # Build using tox
tox -e clean                # Clean build artifacts
```

### Testing
```bash
pytest                        # Run all tests with coverage
pytest tests/test_robin.py      # Run single test file
pytest tests/test_robin.py::test_slnode  # Run specific test
pytest -v                     # Verbose output
pytest -k "test_robin"        # Run tests matching pattern
tox                          # Run tests in isolated environment
```

### Linting / Formatting
```bash
pre-commit run --all-files    # Run all pre-commit hooks
black .                       # Format code
isort .                       # Sort imports
flake8 .                      # Lint code
```

## Code Style Guidelines

### Imports
- Group imports in this order:
  1. Standard library imports
  2. Third-party imports
  3. Local package imports (`from mywheel.xxx import ...`)
- Use absolute imports for local packages
- Type hints: `from typing import TypeVar, Generic, List, Iterator, Mapping`

### Formatting
- **Black**: 100 character default, but flake8 allows 256 (configured in setup.cfg)
- **isort**: Standard PEP8 ordering
- **Line endings**: Auto-detected (LF on Linux/Mac, CRLF on Windows)

### Type Hints
- **Mandatory**: All public APIs must have type hints
- Use TypeVar for generic classes: `T = TypeVar("T")`
- Forward references with quotes: `"Dllink[T]"`
- Return types on all methods

### Naming Conventions
- **Classes**: PascalCase (`Dllink`, `Dllist`, `BPQueue`, `RobinIterator`)
- **Functions/Methods**: snake_case (`appendleft`, `decrease_key`, `is_empty`)
- **Constants**: UPPER_CASE (`sentinel`, `_max`, `_offset`)
- **Private members**: Prefix with `_` (`_max`, `_bucket`, `_update_max_key`)
- **Instance attributes**: snake_case (`self.data`, `self.next`, `self.head`)

### Documentation
- **Docstrings**: Google/NumPy-style for all public classes/methods
- **Examples**: Include doctest examples in docstrings
- **Sphinx directives**: Use `.. svgbob::` for ASCII art diagrams
- **Sections**: `param`, `return`, `type`, `Examples` sections

### Error Handling
- Use `assert` for invariant checks and preconditions
- Raise specific exceptions: `IndexError`, `NotImplementedError`, `StopIteration`
- Use `id()` for object identity comparisons: `id(self.next) == id(self)`
- No bare `except:` clauses (use specific exceptions)

### Testing Patterns
- **pytest** for unit tests
- **hypothesis** for property-based testing (especially data structures)
- Test class naming: `Test<ClassName>`, `Test<ClassName>Properties`
- Property tests should cover invariants, roundtrips, and edge cases
- Use `pytest.raises(StopIteration)` for expected exceptions

### Special Patterns

#### Memory Optimization
```python
__slots__ = ("next", "prev", "data")  # Use __slots__ for fixed attributes
```

#### Iterators
```python
def __iter__(self) -> "SelfType":
    return self

def __next__(self) -> ReturnType:
    if condition:
        return value
    else:
        raise StopIteration()
```

#### Circular Data Structures
- Sentinel nodes for linked lists (`head` points to itself)
- Self-referential initialization: `self.next = self`
- Use `id()` for equality checks on circular references

#### Generic Types
```python
from typing import Generic, TypeVar

T = TypeVar("T")

class MyClass(Generic[T]):
    def method(self, item: T) -> T:
        ...
```

## Project Structure

```
mywheel/
├── src/mywheel/       # Source code (no package __init__ in tests)
│   ├── __init__.py     # Version management only
│   ├── robin.py        # Round-robin implementation
│   ├── dllist.py       # Doubly-linked list
│   ├── bpqueue.py      # Bounded priority queue
│   ├── map_adapter.py  # List-to-map adapter
│   └── array_like.py  # Array-like utilities
├── tests/             # Tests (pytest, hypothesis)
│   ├── conftest.py     # Pytest configuration
│   └── test_*.py      # Test files
├── docs/              # Sphinx documentation
├── setup.cfg          # Metadata, pytest config
├── pyproject.toml     # Build system (setuptools_scm)
└── tox.ini            # Test environments
```

## Key Dependencies

- **Testing**: pytest, pytest-cov, hypothesis
- **Linting**: black, isort, flake8 (via pre-commit)
- **Build**: setuptools, setuptools_scm, wheel

## Notes for Agents

1. **Never use `as any` or `@ts-ignore`** - this is Python, not TypeScript
2. **Follow existing patterns** - codebase is disciplined, PyScaffold-generated
3. **Add tests** - use pytest + hypothesis for data structures
4. **Docstring examples** - ensure they pass with doctest
5. **Pre-commit** - run hooks before committing
6. **Version** - managed by setuptools_scm (don't edit version manually)
