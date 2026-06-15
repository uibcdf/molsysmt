"""Dummy residues (``DUM``) are treated as chemically neutral by the ``physchem``
group functions instead of raising ``KeyError``, so the functions can run over
whole systems that contain dummy/placeholder atoms (coarse beads, alchemical
placeholders, synthetic probe catalogs)."""

import os
import tempfile

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.physchem.groups._lookup import group_table_value


def _dummy_molsys():
    # Atoms named DUM, neutral dummy element 'Du', residue named DUM.
    pdb = (
        "HETATM    1 DUM  DUM A   1       0.000   0.000   0.000  1.00  0.00          Du\n"
        "HETATM    2 DUM  DUM A   2       3.000   0.000   0.000  1.00  0.00          Du\n"
        "END\n"
    )
    fd, path = tempfile.mkstemp(suffix=".pdb")
    try:
        os.write(fd, pdb.encode())
    finally:
        os.close(fd)
    try:
        return msm.convert(path, to_form="molsysmt.MolSys")
    finally:
        os.remove(path)


def test_dummy_atom_is_neutral_first_class_element():
    molsys = _dummy_molsys()
    assert list(msm.get(molsys, element="atom", atom_type=True)) == ["Du", "Du"]
    mass = puw.get_value(msm.physchem.get_mass(molsys, element="atom"), to_unit="amu")
    assert np.allclose(mass, [0.0, 0.0])
    for definition in ("vdw", "protor"):
        radius = puw.get_value(
            msm.physchem.get_atomic_radius(
                molsys, element="atom", definition=definition
            ),
            to_unit="nm",
        )
        assert np.allclose(radius, [0.0, 0.0])


def _x_molsys():
    # The other common dummy convention: atom name X, element X, residue X.
    pdb = (
        "HETATM    1 X    X   A   1       0.000   0.000   0.000  1.00  0.00           X\n"
        "HETATM    2 X    X   A   2       3.000   0.000   0.000  1.00  0.00           X\n"
        "END\n"
    )
    fd, path = tempfile.mkstemp(suffix=".pdb")
    try:
        os.write(fd, pdb.encode())
    finally:
        os.close(fd)
    try:
        return msm.convert(path, to_form="molsysmt.MolSys")
    finally:
        os.remove(path)


def test_group_table_value_neutral_for_dummy_and_raises_for_unknown():
    table = {"ALA": 0.0, "ARG": 1.0}
    assert group_table_value(table, "arg") == 1.0   # real residue, case-insensitive
    assert group_table_value(table, "DUM") == 0.0   # DUM dummy residue -> neutral
    assert group_table_value(table, "X") == 0.0     # X dummy residue -> neutral
    assert group_table_value(table, "DUM", neutral=np.nan) != group_table_value(
        table, "DUM", neutral=np.nan
    )  # neutral override propagates (NaN != NaN)
    with pytest.raises(KeyError):
        group_table_value(table, "XYZ")             # genuine unknown still raises


def test_x_dummy_atom_and_group_are_neutral():
    molsys = _x_molsys()
    assert list(msm.get(molsys, element="atom", atom_type=True)) == ["X", "X"]
    mass = puw.get_value(msm.physchem.get_mass(molsys, element="atom"), to_unit="amu")
    assert np.allclose(mass, [0.0, 0.0])
    radius = puw.get_value(
        msm.physchem.get_atomic_radius(molsys, element="atom", definition="vdw"),
        to_unit="nm",
    )
    assert np.allclose(radius, [0.0, 0.0])
    charge = puw.get_value(
        msm.physchem.get_charge(molsys, element="group", definition="physical_pH7"),
        to_unit="elementary_charge",
    )
    assert np.allclose(charge, [0.0, 0.0])


def test_get_charge_neutral_on_dummy_system():
    molsys = _dummy_molsys()
    charge = puw.get_value(
        msm.physchem.get_charge(molsys, element="group", definition="physical_pH7"),
        to_unit="elementary_charge",
    )
    assert np.allclose(charge, [0.0, 0.0])


def test_get_hydrophobicity_neutral_on_dummy_system():
    molsys = _dummy_molsys()
    hydrophobicity = puw.get_value(
        msm.physchem.get_hydrophobicity(molsys, element="group")
    )
    assert np.allclose(hydrophobicity, [0.0, 0.0])


def test_dummy_groups_are_typed_as_ion():
    # DUM / X carry no covalent bonds: standalone single-atom 'ion' groups.
    for molsys in (_dummy_molsys(), _x_molsys()):
        assert list(msm.get(molsys, element="group", group_type=True)) == ["ion", "ion"]
