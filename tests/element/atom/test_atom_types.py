"""Testing explicit element identity without atom-name or force-field guessing."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


def test_canonical_symbols_are_distinct_from_names_and_forcefield_types():
    values = [
        "C",
        "Ca",
        "Cl",
        "Og",
        "D",
        "T",
        "CA",
        "OA",
        "HD",
        "Du",
        "X",
        "UNK",
        "c",
        " C",
        "",
    ]
    result = msm.element.atom.is_atom_type(values)
    assert result.dtype == bool and result.shape == (len(values),)
    assert result.tolist() == [True] * 4 + [False] * 11
    assert msm.element.atom.is_atom_type("Ca") is True
    assert msm.element.atom.is_atom_type("CA") is False
    assert msm.element.atom.get_atom_type_from_atom_name("CA") == "C"


@pytest.mark.parametrize("container", [list, tuple, np.asarray])
def test_atom_type_empty_and_batch_containers(container):
    values = container(["N", "O"])
    assert msm.element.atom.is_atom_type(values).tolist() == [True, True]
    assert msm.element.atom.normalize_atom_types(values) == (["N", "O"], [None, None])
    assert msm.element.atom.is_atom_type(container([])).shape == (0,)
    assert msm.element.atom.normalize_atom_types(container([])) == ([], [])


@pytest.mark.parametrize(
    "bad", [None, 6, True, ["C", 6], [["C"]], np.array("C"), np.array([["C"]])]
)
@pytest.mark.parametrize("function", ["is_atom_type", "normalize_atom_types"])
def test_reject_malformed_type_containers(bad, function):
    with pytest.raises(ArgumentError):
        getattr(msm.element.atom, function)(bad)


@pytest.mark.parametrize(
    "atom_type,isotope,expected",
    [
        ("D", None, ("H", 2)),
        ("T", 3, ("H", 3)),
        ("H", None, ("H", None)),
        ("C", np.int64(13), ("C", 13)),
        ("D", pd.NA, ("H", 2)),
    ],
)
def test_normalize_scalar_aliases_and_explicit_mass_numbers(
    atom_type, isotope, expected
):
    assert msm.element.atom.normalize_atom_types(atom_type, isotope) == expected


def test_batch_isotope_alignment_does_not_mutate_inputs():
    atom_types = np.array(["C", "D", "T", "Cl"], dtype=object)
    isotopes = np.array([13, pd.NA, 3, None], dtype=object)
    before_types, before_isotopes = atom_types.copy(), isotopes.copy()
    assert msm.element.atom.normalize_atom_types(atom_types, isotopes) == (
        ["C", "H", "H", "Cl"],
        [13, 2, 3, None],
    )
    np.testing.assert_array_equal(atom_types, before_types)
    assert isotopes.tolist() == before_isotopes.tolist()


@pytest.mark.parametrize(
    "atom_type,isotope",
    [
        ("D", 3),
        ("T", 2),
        ("CA", None),
        ("OA", None),
        ("Du", None),
        ("C", 0),
        ("C", 65536),
        ("C", True),
        ("C", 13.0),
        ("C", [13]),
        (["C", "H"], 13),
        (["C", "H"], [13]),
        (["C"], [[13]]),
        ("C", np.array(13)),
        ("C", "13"),
        ("C", float("nan")),
    ],
)
def test_reject_conflicts_unknown_symbols_and_misaligned_isotopes(atom_type, isotope):
    with pytest.raises(ArgumentError):
        msm.element.atom.normalize_atom_types(atom_type, isotope)


def test_validated_delegation_preserves_normalization():
    values, isotopes = ["D", "O"], [None, 18]
    assert msm.element.atom.normalize_atom_types(
        values, isotopes, skip_digestion=True
    ) == (msm.element.atom.normalize_atom_types(values, isotopes))
    np.testing.assert_array_equal(
        msm.element.atom.is_atom_type(values, skip_digestion=True),
        msm.element.atom.is_atom_type(values),
    )


def test_all_real_elements_in_existing_mass_data_have_canonical_atom_types():
    from molsysmt.physchem.atoms.mass import physical

    real_elements = [symbol for symbol in physical if symbol not in {"Du", "X"}]
    assert len(real_elements) == 118
    assert msm.element.atom.is_atom_type(real_elements).all()
    assert msm.element.atom.normalize_atom_types(real_elements) == (
        real_elements,
        [None] * 118,
    )


def test_value_tool_validation_does_not_restrict_existing_isotope_setter():
    molsys = msm.convert(msm.systems["caffeine"]["caffeine.sdf"])
    isotopes = pd.Series([13] + [pd.NA] * (molsys.topology.n_atoms - 1), dtype="UInt16")
    msm.set(molsys, isotope=isotopes)
    assert molsys.topology.atoms.isotope.iloc[0] == 13
    assert molsys.topology.atoms.isotope.iloc[1:].isna().all()
