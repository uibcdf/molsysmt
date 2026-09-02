import inspect
import pytest
from devtools.scripts.validate_docstrings import (
    find_vacuous_docstring_content,
    parse_docstring_parameters,
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


def test_parse_docstring_parameters_includes_type_and_description():
    doc = """
    Example function summary.

    Parameters
    ----------
    item : molecular system
        Molecular system to analyze, in any supported form.
    """
    assert parse_docstring_parameters(doc)["item"] == {
        "type": "molecular system",
        "default": "<no_default>",
        "description": "Molecular system to analyze, in any supported form.",
    }


@pytest.mark.parametrize(
    "replacement, expected_error",
    [
        ("", "empty description"),
        ("Argument item.", "only restates its name"),
        ("The item argument.", "only restates its name"),
    ],
)
def test_vacuity_check_rejects_mutated_parameter_descriptions(replacement, expected_error):
    doc = f"""
    Example function summary.

    Parameters
    ----------
    item : molecular system
        {replacement}

    Returns
    -------
    int
        Number of atoms in the molecular system.
    """
    assert any(expected_error in error for error in find_vacuous_docstring_content(doc))


def test_vacuity_check_rejects_object_parameter_type():
    doc = """
    Example function summary.

    Parameters
    ----------
    item : object
        Molecular system to analyze, in any supported form.
    """
    assert any(
        "non-informative type 'object'" in error
        for error in find_vacuous_docstring_content(doc)
    )


def test_vacuity_check_rejects_generated_returns_description():
    doc = """
    Example function summary.

    Returns
    -------
    object
        Resulting object in object form.
    """
    assert find_vacuous_docstring_content(doc) == [
        "The Returns section uses the generated placeholder description."
    ]


def test_vacuity_check_accepts_informative_content():
    doc = """
    Example function summary.

    Parameters
    ----------
    item : molecular system
        Molecular system to analyze, in any supported form.

    Returns
    -------
    int
        Number of atoms in the molecular system.
    """
    assert find_vacuous_docstring_content(doc) == []


def test_normalize_default_repr():
    assert normalize_default_repr("'MolSysMT'") == "'MolSysMT'"
    assert normalize_default_repr("False") == "False"
    assert normalize_default_repr("[0, 0, 1]") == "[0, 0, 1]"
    assert normalize_default_repr("(0, 0, 1)") == "(0, 0, 1)"
    assert normalize_default_repr("[0, 0, 1]") != normalize_default_repr("(0, 0, 1)")


def test_validate_docstrings_passes_on_codebase():
    """Verify that all public functions pass bidirectional and default validation."""
    assert validate() == 0
