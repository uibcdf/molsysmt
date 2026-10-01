import pytest

import molsysmt as msm
from devtools.scripts.validate_docstrings import (
    find_vacuous_docstring_content,
    normalize_default_repr,
    parse_docstring_parameters,
    parse_docstring_params_and_defaults,
    validate,
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
def test_vacuity_check_rejects_mutated_parameter_descriptions(
    replacement, expected_error
):
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


@pytest.mark.parametrize(("family", "function"), [
    ("hbonds", "get_hbonds"),
    ("disulfides", "get_disulfide_candidates"),
    ("ionic", "get_ionic_interactions"),
    ("pi_pi", "get_pi_pi_interactions"),
    ("cation_pi", "get_cation_pi_interactions"),
    ("halogen_bonds", "get_halogen_bonds"),
    ("hydrophobic", "get_hydrophobic_interactions"),
])
def test_missing_exported_detector_docstring_fails_gate(monkeypatch, capsys, family, function):
    detector = getattr(getattr(msm.interactions, family), function)
    monkeypatch.setattr(detector, "__doc__", None)
    assert validate() == 1
    assert f"molsysmt.interactions.{family}.{function}: Missing docstring entirely." in capsys.readouterr().out


def test_wrong_detector_default_fails_gate(monkeypatch, capsys):
    detector = msm.interactions.hydrophobic.get_hydrophobic_interactions
    monkeypatch.setattr(detector, "__doc__", detector.__doc__.replace(
        "method : str, default='atom_pair_distance'", "method : str, default='invented'"))
    assert validate() == 1
    assert "Default mismatch for parameter 'method'" in capsys.readouterr().out


def test_new_public_family_is_checked_without_validator_edits(monkeypatch, capsys):
    from types import SimpleNamespace

    def undocumented_detector(molecular_system):
        return molecular_system

    namespace = SimpleNamespace(get_interactions=undocumented_detector)
    monkeypatch.setattr(msm.interactions, "test_family", namespace, raising=False)
    monkeypatch.setattr(msm.interactions, "__all__", [*msm.interactions.__all__, "test_family"])
    assert validate() == 1
    assert "molsysmt.interactions.test_family.get_interactions: Missing docstring entirely." in capsys.readouterr().out
