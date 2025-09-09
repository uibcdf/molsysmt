# Unit Tests

- Use `pytest` for all unit tests.
- Tests go in `molsysmt/tests/` using `test_<function>.py` naming.
- Use `@pytest.mark.parametrize` when testing over multiple forms.
- Track test coverage via Codecov: <https://app.codecov.io/github/uibcdf/MolSysMT>
- Validate tutorials optionally using `nbval` or `pytest + papermill`.

Las opciones '+ELLIPSIS' y 'NORMALIZE_WHITESPACE' fueron incluidas por defecto en el fichero `pytest.ini` (no es necesario repetirlas en el docstring).

