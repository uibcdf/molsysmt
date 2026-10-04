"""Checking validated manual mechanical charges independently of calculation."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

puw = msm.pyunitwizard


@pytest.fixture
def source():
    return msm.convert(
        msm.systems["caffeine"]["caffeine.sdf"], to_form="molsysmt.MolSys"
    )


def test_public_set_creates_and_replaces_atom_aligned_mechanical_charges(source):
    before = source.chemical_states._states[0].atom_attributes.copy()
    values = np.linspace(-0.3, 0.3, source.get_n_atoms())
    with puw.context(standard_units=["coulomb", "angstrom"]):
        msm.set(
            source,
            element="atom",
            partial_charge=puw.quantity(values, "elementary_charge"),
        )
    np.testing.assert_allclose(
        np.asarray(source.molecular_mechanics.partial_charge, dtype=float), values
    )
    msm.set(source, element="atom", selection=[3, 1], partial_charge=[0.15, -0.25])
    # Setter values follow the explicit index order, independent of atom IDs.
    values[[3, 1]] = [0.15, -0.25]
    np.testing.assert_allclose(
        np.asarray(source.molecular_mechanics.partial_charge, dtype=float), values
    )
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes, before
    )
    msm.set(source, element="atom", partial_charge=None)
    assert source.molecular_mechanics.partial_charge is None


def test_partial_assignment_keeps_unassigned_atoms_unknown(source):
    msm.set(source, selection=[5], partial_charge=[0.125])
    stored = source.molecular_mechanics.atoms_ff["partial_charge"]
    assert stored.iloc[5] == 0.125
    assert stored.drop(index=5).isna().all()


@pytest.mark.parametrize(
    "value",
    [
        [float("nan")],
        [float("inf")],
        [True],
        [[0.1]],
        "0.1",
        [None],
        puw.quantity([0.1], "nm"),
        [0.1, 0.2],
    ],
)
def test_invalid_assignment_fails_before_modifying_mechanics(source, value):
    with pytest.raises(ArgumentError):
        msm.set(source, selection=[0], partial_charge=value)
    assert source.molecular_mechanics.atoms_ff is None


def test_empty_selection_does_not_change_a_known_assignment(source):
    values = np.zeros(source.get_n_atoms())
    msm.set(source, partial_charge=values)
    msm.set(source, selection=[], partial_charge=[])
    np.testing.assert_array_equal(source.molecular_mechanics.partial_charge, values)


def test_direct_mechanical_subset_does_not_invent_an_atom_axis():
    from molsysmt.form.molsysmt_MolecularMechanics.set import set_partial_charge_to_atom
    from molsysmt.native.molecular_mechanics import MolecularMechanics

    mechanics = MolecularMechanics()
    with pytest.raises(ArgumentError, match="atom axis"):
        set_partial_charge_to_atom(mechanics, atom_indices=[5], value=[0.1])
    assert mechanics.atoms_ff is None
