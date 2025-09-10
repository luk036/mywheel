# Project Overview

`mywheel` is a Python library that appears to provide various data structures and utility functions, as indicated by modules like `array_like`, `bpqueue`, `dllist`, `map_adapter`, and `robin`. The project uses `setuptools` and `setuptools_scm` for packaging and version management.

# Building and Running

## Building the Package

The project can be built into a distributable package (wheel and sdist) using `tox` or `build`:

```bash
tox -e build
# or
python -m build
```

The built packages will be located in the `dist/` directory.

## Testing

Tests are run using `pytest` via `tox`.

To run all tests:

```bash
tox
# or
tox -e default
```

To run specific tests or pass arguments to `pytest`:

```bash
tox -- <pytest_args>
# Example: tox -- -k "test_my_feature"
```

## Running the Project

As `mywheel` is a Python library, it is not directly "runnable" as an application. Instead, its modules and functions are intended to be imported and used within other Python projects.

# Development Conventions

## Code Formatting and Linting

The project enforces code style and quality using `pre-commit` hooks with `isort`, `black`, and `flake8`.

*   **`isort`**: Used for sorting imports, configured with the `black` profile.
*   **`black`**: Used for code formatting.
*   **`flake8`**: Used for linting.

To install and run pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

## Type Checking

`mypy` is used for static type checking to ensure type consistency and catch potential errors. The configuration is in `mypy.ini`.

## Contribution Guidelines

The `CONTRIBUTING.md` file provides comprehensive guidelines for contributing to the project, including:

*   Reporting issues.
*   Improving documentation (using Sphinx).
*   Code contributions:
    *   Creating an isolated virtual environment.
    *   Forking and cloning the repository.
    *   Installing development dependencies and pre-commit hooks.
    *   Implementing changes in a new branch.
    *   Writing descriptive commit messages.
    *   Running tests with `tox`.
    *   Submitting pull requests.
