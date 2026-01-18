# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI workflow with Python 3.8-3.12 testing
- mypy type checking configuration
- Improved README with quick start examples and performance characteristics
- Comprehensive CONTRIBUTING.md guide
- Explicit public API exports via `__all__` in all modules
- Additional PyPI classifiers for Python versions and audience

### Changed
- Enhanced documentation and developer experience

## [0.1.0] - TBD

### Added
- Initial release with core data structures:
  - `Dllist`: Doubly-linked list with O(1) operations
  - `BPQueue`: Bounded priority queue for small integer keys
  - `Robin`: Round-robin iterator
  - `MapAdapter`: List-to-map adapter
  - `RepeatArray`: Memory-efficient repeated value array
  - `ShiftArray`: Array with arbitrary start index
- Full type hints with mypy support
- Comprehensive test suite with pytest and hypothesis
- Pre-commit hooks for code quality
- Sphinx documentation

### Features
- Memory efficient implementations using `__slots__`
- Sentinel nodes for circular data structures
- Property-based testing with hypothesis
- Zero runtime dependencies
- Python 3.8+ support

---

## Notes for Maintainers

### Adding New Entries

When adding new entries to changelog:

1. Use categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
2. Link issue references: `[Unreleased]` or `[#123]`
3. Order entries logically (new features first, then fixes)
4. Keep entries concise but informative

### Version Bumping

This project uses `setuptools_scm` for versioning. To release:

1. Create git tag: `git tag -a v0.2.0 -m "Release v0.2.0"`
2. Push tag: `git push origin v0.2.0`
3. CI will automatically build and publish to PyPI
