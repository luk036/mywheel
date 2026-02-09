# Contributing to mywheel

Thank you for your interest in contributing to `mywheel`! This document provides guidelines and instructions for contributing to this project.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. Check if the issue already exists in [GitHub Issues](https://github.com/luk036/mywheel/issues)
2. Use an appropriate issue template
3. Include:
   - Python version
   - Operating system
   - Minimal reproducible example
   - Expected vs actual behavior

### Submitting Pull Requests

We welcome pull requests! Here's the process:

1. **Fork** the repository
2. **Create a branch** for your changes: `git checkout -b feature/your-feature`
3. **Make your changes** following the guidelines below
4. **Test thoroughly** (see Testing section)
5. **Submit a PR** with a clear description

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/mywheel.git
cd mywheel

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with testing dependencies
pip install -e ".[testing]"

# Install pre-commit hooks
pre-commit install
```

### Project Structure

```
mywheel/
├── src/mywheel/       # Source code
│   ├── __init__.py
│   ├── robin.py        # Round-robin implementation
│   ├── dllist.py       # Doubly-linked list
│   ├── bpqueue.py      # Bounded priority queue
│   ├── map_adapter.py  # List-to-map adapter
│   └── array_like.py  # Array-like utilities
├── tests/             # Test suite
│   ├── conftest.py
│   └── test_*.py
├── docs/              # Sphinx documentation
└── AGENTS.md          # Guidelines for agentic contributors
```

## 📝 Code Style Guidelines

### General Principles

- **Follow existing patterns**: The codebase uses consistent patterns (see `AGENTS.md`)
- **Type hints required**: All public APIs must have type hints
- **Memory efficiency**: Use `__slots__` for classes with fixed attributes
- **Docstrings**: Google/NumPy-style with doctest examples

### Specific Rules

1. **Imports**: Standard → Third-party → Local package
   ```python
   from typing import Generic, TypeVar
   from hypothesis import given
   from mywheel import Dllist
   ```

2. **Naming**:
   - Classes: `PascalCase`
   - Functions/Methods: `snake_case`
   - Private: `_leading_underscore`

3. **Error Handling**:
   - Use `assert` for invariants and preconditions
   - Raise specific exceptions (`IndexError`, `NotImplementedError`, `StopIteration`)
   - Use `id()` for object identity comparisons

4. **Circular References**:
   ```python
   # Self-referential initialization
   self.next = self

   # Identity checks
   if id(self.next) == id(self):
   ```

### Before Committing

```bash
# Format code
black .
isort .

# Run linters
flake8 src/mywheel

# Type check
mypy src/mywheel

# Run tests
pytest tests/

# Run all checks at once
pre-commit run --all-files
```

## 🧪 Testing

### Running Tests

```bash
# All tests with coverage
pytest

# Specific test file
pytest tests/test_dllist.py

# Specific test
pytest tests/test_robin.py::test_slnode

# Verbose output
pytest -v

# Pattern matching
pytest -k "test_dllist"

# In isolated environment (tox)
tox
```

### Writing Tests

- **Unit tests**: Use `pytest` for specific functionality
- **Property tests**: Use `hypothesis` for data structure invariants
- **Coverage**: Maintain 100% coverage for new code
- **Test structure**:
  ```python
  # Standard pytest test
  def test_feature():
      assert expected == actual

  # Property-based test
  @given(st.integers(min_value=1, max_value=100))
  def test_property(value):
      assert invariant_holds(value)
  ```

### Test Naming

- Test classes: `Test<ClassName>`, `Test<ClassName>Properties`
- Test functions: `test_<feature>`, `test_<behavior>`

## 📚 Documentation

### Docstrings

Use Google/NumPy-style docstrings for all public APIs:

```python
def method(self, param: int) -> str:
    """
    Brief description.

    Detailed description of what the method does.

    Args:
        param: Description of param

    Returns:
        Description of return value

    Raises:
        IndexError: When param is out of range

    Examples:
        >>> obj.method(5)
        'result'
    """
```

### Module Documentation

Each module should have a module-level docstring explaining:
- Purpose of the implementation
- Key algorithms used
- Performance characteristics
- Usage examples

## 🔄 Code Review Process

### Before Submitting PR

1. ✅ All tests pass locally
2. ✅ Type checking passes (`mypy`)
3. ✅ Linting passes (`flake8`)
4. ✅ Code formatted with `black` and `isort`
5. ✅ New code has tests
6. ✅ Docstrings updated
7. ✅ `AGENTS.md` updated if adding new patterns

### During Review

- **Be responsive**: Address review feedback promptly
- **Explain changes**: Provide rationale for significant decisions
- **Be patient**: Reviewers volunteer their time

### After Merge

- Your contribution will be credited in release notes
- Thank you for helping improve `mywheel`!

## 🚀 Release Process

Releases are managed by maintainers:

1. Version updated via `setuptools_scm` (git tags)
2. Changelog updated in `CHANGELOG.md`
3. Built and published to PyPI via CI

## 💬 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussions
- **Documentation**: Read <AGENTS.md> for codebase patterns

## 📄 License

By contributing, you agree that your contributions will be licensed under the <LICENSE>.

---

Thank you for contributing to `mywheel`! 🎉
