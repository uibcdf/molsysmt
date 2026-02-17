# Unit Tests

- Use `pytest` for all unit tests.
- Tests go in `tests/` following mirrored package paths and `test_*.py` naming.
- Use `@pytest.mark.parametrize` when testing over multiple forms.
- Track test coverage via Codecov: <https://app.codecov.io/github/uibcdf/MolSysMT>
- Validate tutorials optionally using `nbval` or `pytest + papermill`.
- `+ELLIPSIS` and `NORMALIZE_WHITESPACE` doctest flags are configured in
  `pytest.ini`, so they do not need to be repeated in each docstring.
