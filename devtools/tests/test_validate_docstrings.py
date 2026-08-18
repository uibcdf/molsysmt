import inspect
import pytest
from devtools.scripts.validate_docstrings import (
    validate,
    parse_docstring_params_and_defaults,
    normalize_default_repr,
)


def test_parse_docstring_params_and_defaults():
    doc = """
    Example function summary.

    Parameters
    ----------
    a : int
        First argument without default.
    b : str, default='MolSysMT'
        Second argument with string default.
    c : bool, default=False
        Third argument with bool default.
    d : tuple, default=(0, 0, 1)
        Fourth argument with tuple default.

    Returns
    -------
    int
        Result.
    """
    params, defaults = parse_docstring_params_and_defaults(doc)
    assert params == ["a", "b", "c", "d"]
    assert defaults["a"] == "<no_default>"
    assert defaults["b"] == "'MolSysMT'"
    assert defaults["c"] == "False"
    assert defaults["d"] == "(0, 0, 1)"


def test_normalize_default_repr():
    assert normalize_default_repr("'MolSysMT'") == "'MolSysMT'"
    assert normalize_default_repr("False") == "False"
    assert normalize_default_repr("[0, 0, 1]") == "[0, 0, 1]"
    assert normalize_default_repr("(0, 0, 1)") == "(0, 0, 1)"
    assert normalize_default_repr("[0, 0, 1]") != normalize_default_repr("(0, 0, 1)")


def test_validate_docstrings_passes_on_codebase():
    """Verify that all public functions pass bidirectional and default validation."""
    assert validate() == 0
