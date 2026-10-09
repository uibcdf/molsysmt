"""Preserving prepared atom-aligned mechanics through public merging."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralAttributeDropWarning
from molsysmt.native import MolecularMechanics


@pytest.mark.parametrize("charges", [True, False])
def test_merge_preserves_prepared_mechanics_atom_axis(charges):
    left = MolecularMechanics(
        atom_ff_type=np.array(["C", "N"]),
        partial_charge=np.array([0.25, -0.5]) if charges else None,
    )
    right = MolecularMechanics(
        atom_ff_type=np.array(["OA"]),
        partial_charge=np.array([-0.75]) if charges else None,
    )
    originals = [item.atoms_ff.copy(deep=True) for item in (left, right)]

    merged = msm.merge([left, right])

    assert len(merged.atoms_ff) == 3
    assert merged.atom_ff_type.tolist() == ["C", "N", "OA"]
    if charges:
        np.testing.assert_allclose(merged.partial_charge.astype(float), [0.25, -0.5, -0.75])
    else:
        assert merged.partial_charge is None
    merged.atoms_ff.iloc[0, 0] = "changed"
    for item, original in zip((left, right), originals):
        pd.testing.assert_frame_equal(item.atoms_ff, original)


def test_merge_prepared_molsys_preserves_charge_units_and_selected_order():
    molsys = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"])
    charges = np.arange(molsys.topology.n_atoms, dtype=float) / 10
    msm.set(
        molsys,
        element="atom",
        partial_charge=puw.convert(puw.quantity(charges, "e"), to_unit="coulomb"),
    )
    molsys.molecular_mechanics.atom_ff_type = np.array(
        [f"type-{i}" for i in range(len(charges))]
    )

    with puw.context(standard_units=["angstrom", "coulomb"]):
        merged = msm.merge([molsys, molsys], selections=[[2, 0], [1]])
        observed = msm.get(merged, element="atom", partial_charge=True)
        # Native get returns the numerical column in elementary charge.
        np.testing.assert_allclose(np.asarray(observed, dtype=float), charges[[2, 0, 1]])

    assert merged.topology.n_atoms == 3
    assert len(merged.molecular_mechanics.atoms_ff) == 3
    assert merged.molecular_mechanics.atom_ff_type.tolist() == ["type-2", "type-0", "type-1"]
    np.testing.assert_allclose(molsys.molecular_mechanics.partial_charge.astype(float), charges)


def test_empty_selection_does_not_remove_other_prepared_columns():
    left = MolecularMechanics(atom_ff_type=np.array(["C", "N"]))
    right = MolecularMechanics(atom_ff_type=np.array(["O"]))
    merged = msm.merge([left, right], selections=[[], "all"])
    assert merged.atom_ff_type.tolist() == ["O"]
    assert len(merged.atoms_ff) == 1


def test_merge_invalidates_named_reports_without_mutating_input_provenance():
    left = MolecularMechanics(partial_charge=np.array([0.25]), atom_ff_type=np.array(["C"]))
    right = left.copy()
    left.partial_charge_assignment = {"producer": "original", "atom_indices": [0]}
    right.atom_type_assignment = {"producer": "other", "atom_indices": [0]}

    with pytest.warns(StructuralAttributeDropWarning):
        merged = msm.merge([left, right])

    assert merged.partial_charge_assignment is None
    assert merged.atom_type_assignment is None
    np.testing.assert_allclose(merged.partial_charge.astype(float), [0.25, 0.25])
    assert merged.atom_ff_type.tolist() == ["C", "C"]
    assert left.partial_charge_assignment == {"producer": "original", "atom_indices": [0]}
    assert right.atom_type_assignment == {"producer": "other", "atom_indices": [0]}


def test_single_full_input_preserves_detached_assignment_report():
    source = MolecularMechanics(partial_charge=np.array([0.25]))
    source.partial_charge_assignment = {"producer": "original", "atom_indices": [0]}
    merged = msm.merge([source])
    assert merged.partial_charge_assignment == source.partial_charge_assignment
    merged.partial_charge_assignment["atom_indices"].append(1)
    assert source.partial_charge_assignment["atom_indices"] == [0]


def test_missing_column_is_reported_and_other_columns_keep_the_combined_axis():
    left = MolecularMechanics(partial_charge=np.array([0.2]), atom_ff_type=np.array(["C"]))
    right = MolecularMechanics(atom_ff_type=np.array(["N", "O"]))
    with pytest.warns(StructuralAttributeDropWarning):
        merged = msm.merge([left, right])
    assert merged.partial_charge is None
    assert merged.atom_ff_type.tolist() == ["C", "N", "O"]
    np.testing.assert_allclose(left.partial_charge.astype(float), [0.2])


def test_selected_input_clears_reports_and_preserves_formal_charge_column():
    source = MolecularMechanics(formal_charge=np.array([0, -1]), partial_charge=np.array([0.1, -0.2]))
    source.partial_charge_assignment = {"producer": "original", "atom_indices": [0, 1]}
    with pytest.warns(StructuralAttributeDropWarning):
        selected = msm.merge([source], selections=[[1]])
    assert selected.formal_charge.tolist() == [-1]
    np.testing.assert_allclose(selected.partial_charge.astype(float), [-0.2])
    assert selected.partial_charge_assignment is None
    assert source.partial_charge_assignment["atom_indices"] == [0, 1]
