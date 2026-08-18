# Unit Tests

MolSysMT uses `pytest` for automated test execution across all modules, forms, and calculation engines.

---

## 1. Running Tests

Run the test suite from the repository root:

```bash
# Run the complete test suite
pytest

# Run tests in a specific module
pytest tests/structure/test_get_distances.py

# Run tests matching an expression
pytest -k "test_convert"

# Run tests in parallel across multiple CPU cores
pytest -n auto

# Stop immediately upon the first failure
pytest -x
```

---

## 2. Test Organization and Conventions

- **Mirrored Paths**: Tests live in `tests/` mirroring the package structure (e.g. tests for `molsysmt/structure/get_distances.py` reside in `tests/structure/test_get_distances.py`).
- **File Naming**: All test files must be prefixed with `test_*.py`.
- **Parametrization**: Use `@pytest.mark.parametrize` to test operations across multiple supported forms and syntaxes.
- **Bundled Demo Systems**: Rely on demo datasets from `molsysmt.systems` for deterministic, lightweight, and fast testing rather than generating heavy synthetic systems.
- **Doctest Validation**: Doctests in docstrings are verified automatically via `pytest --doctest-modules molsysmt`.
