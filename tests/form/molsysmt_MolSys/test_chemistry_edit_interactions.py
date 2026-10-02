"""Prevent attached observations from surviving controlled chemistry edits."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys


@pytest.fixture
def ionic_system():
    molsys = MolSys(n_atoms=4)
    molsys.topology.atoms["atom_type"] = ["Na", "Cl", "C", "C"]
    msm.set(molsys, element="atom", formal_charge=[1, -1, 0, 0])
    molsys.topology._append_chemical_state_bonds(
        [[2, 3]], orders=1, types="covalent", evidence="explicit"
    )
    molsys.topology._reference_chemical_state.connectivity_completeness = "complete"
    xyz = np.tile([[0, 0, 0], [0.3, 0, 0], [2, 0, 0], [2.1, 0, 0]], (4, 1, 1))
    xyz[1, 1, 0] = 1
    molsys.structures.append(coordinates=msm.pyunitwizard.quantity(xyz, "nm"))
    molsys.structures.structure_id = np.array(["a", "b", "c", "d"])
    result = msm.interactions.ionic.get_ionic_interactions(
        molsys, "0.4 nm", structure_indices=[2, 0, 1], pbc=False
    )
    molsys.interactions = {"ionic": result, "second": result.remap()}
    return molsys


def _assert_unevaluated(molsys):
    for result in molsys.interactions.values():
        assert result.n_interactions == 0
        assert result.evaluated_structure_indices.shape == (0,)


def test_neutralizing_ion_invalidates_observations_and_empty_coverage(
    ionic_system, tmp_path
):
    molsys = ionic_system
    originals = dict(molsys.interactions)
    old_view = originals["ionic"].query(structure_indices=[0])
    assert old_view.n_interactions == 1
    with msm.pyunitwizard.context(
        standard_units=["angstrom", "fs", "elementary_charge"]
    ):
        msm.set(
            molsys,
            element="atom",
            selection=[0],
            formal_charge=msm.pyunitwizard.quantity([0], "elementary_charge"),
        )
    _assert_unevaluated(molsys)
    assert msm.get(molsys, element="atom", formal_charge=True) == [0, -1, 0, 0]
    assert old_view.n_interactions == 1
    assert originals["ionic"].n_interactions == 2
    for name, result in molsys.interactions.items():
        assert result.parameters == originals[name].parameters
        assert result.software == originals[name].software
        assert result.measure_units == originals[name].measure_units
        np.testing.assert_array_equal(
            result.atom_source_indices, originals[name].atom_source_indices
        )
        np.testing.assert_array_equal(
            result.structure_source_indices, originals[name].structure_source_indices
        )
    fresh = msm.interactions.ionic.get_ionic_interactions(molsys, "0.4 nm", pbc=False)
    assert fresh.n_interactions == 0
    assert fresh.evaluated_structure_indices.tolist() == [0, 1, 2, 3]
    path = tmp_path / "chemical-edit.h5msm"
    msm.convert(molsys, to_form="file:h5msm", output_filename=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    _assert_unevaluated(restored)


@pytest.mark.parametrize(
    ("attribute", "value"),
    [
        ("atom_is_aromatic", True),
        ("n_unpaired_electrons", 1),
        ("n_implicit_hydrogens", 1),
        ("n_explicit_hydrogens", 1),
        ("allows_implicit_hydrogens", False),
        ("atom_stereochemistry", "R"),
    ],
)
def test_atom_state_edits_invalidate_all_named_analyses(ionic_system, attribute, value):
    msm.set(ionic_system, element="atom", selection=[2], **{attribute: value})
    _assert_unevaluated(ionic_system)


@pytest.mark.parametrize(
    ("attribute", "value"),
    [
        ("bond_order", 2),
        ("fractional_bond_order", 1.5),
        ("bond_type", "covalent"),
        ("bond_is_aromatic", True),
        ("bond_is_conjugated", True),
        ("bond_joins_components", False),
        ("bond_evidence", "user_defined"),
        ("bond_stereochemistry", None),
        ("bond_stereo_atom_indices", None),
        ("bond_donor_atom_index", None),
        ("bond_acceptor_atom_index", None),
    ],
)
def test_bond_state_edits_invalidate_all_named_analyses(ionic_system, attribute, value):
    msm.set(ionic_system, element="bond", selection=[0], **{attribute: value})
    _assert_unevaluated(ionic_system)


def test_empty_selections_and_identifiers_preserve_analyses(ionic_system):
    molsys = ionic_system
    original = molsys.interactions["ionic"]
    msm.set(molsys, element="atom", selection=[], formal_charge=[])
    msm.set(molsys, element="bond", selection=[], bond_order=[])
    msm.set(molsys, element="bond", selection=[0], bond_id="new-label")
    msm.set(molsys, element="atom", selection=[0], atom_id=["renamed"])
    msm.set(molsys, structure_indices=[0], structure_id=["new-frame-label"])
    assert molsys.interactions["ionic"] is original


def test_domain_replacement_invalidates_without_mutating_old_snapshot(ionic_system):
    molsys = ionic_system
    previous = molsys.interactions["ionic"]
    replacement = molsys.chemical_states.copy()
    replacement._states[0].set_atom_attribute("formal_charge", [0, -1, 0, 0])
    molsys.chemical_states = replacement
    assert molsys.chemical_states is replacement
    assert molsys.topology._chemical_states_domain is replacement
    _assert_unevaluated(molsys)
    assert previous.n_interactions == 2


def test_invalid_domain_replacement_preserves_chemistry_and_analyses(ionic_system):
    molsys = ionic_system
    previous_states = molsys.chemical_states
    previous = molsys.interactions["ionic"]
    with pytest.raises(msm.StructuralInconsistencyError):
        molsys.chemical_states = msm.ChemicalStates(n_atoms=3)
    assert molsys.chemical_states is previous_states
    assert molsys.interactions["ionic"] is previous


def test_editing_a_nonreference_state_invalidates_conservatively(ionic_system):
    molsys = ionic_system
    states = molsys.chemical_states.copy()
    states._append_state(states._states[0].copy())
    # Establish the expanded chemical context before declaring the analysis current.
    originals = dict(molsys.interactions)
    molsys.chemical_states = states
    molsys.interactions = originals
    msm.set(
        molsys,
        element="atom",
        selection=[0],
        chemical_state=1,
        structure_indices=[0],
        formal_charge=0,
    )
    assert msm.get(
        molsys, element="atom", selection=[0], chemical_state=0, formal_charge=True
    ) == [1]
    assert msm.get(
        molsys, element="atom", selection=[0], chemical_state=1, formal_charge=True
    ) == [0]
    _assert_unevaluated(molsys)


@pytest.mark.parametrize(
    ("frames", "value", "remaining"),
    [
        ([2, 0, 2], 0, [1]),
        ([1], pd.NA, [0, 2]),
        ("all", None, []),
        ([], [], [0, 1, 2]),
    ],
)
def test_state_association_assignment_invalidates_only_selected_frames(
    ionic_system, frames, value, remaining
):
    molsys = ionic_system
    msm.set(molsys, structure_indices=frames, structure_chemical_state_index=value)
    for result in molsys.interactions.values():
        assert sorted(result.evaluated_structure_indices.tolist()) == remaining
        assert set(result.occurrence_structures.tolist()) <= set(remaining)


def test_invalid_state_assignment_preserves_association_and_analyses(ionic_system):
    molsys = ionic_system
    previous = molsys.interactions["ionic"]
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.set(molsys, structure_indices=[0], structure_chemical_state_index=3)
    assert molsys._structure_chemical_state_indices is None
    assert molsys.interactions["ionic"] is previous


def test_chemical_invalidation_allocation_failure_precedes_write(
    ionic_system, monkeypatch
):
    molsys = ionic_system
    originals = dict(molsys.interactions)
    original_invalidate = msm.Interactions.invalidate_structures
    calls = []

    def fail_second(result, frames):
        calls.append(result)
        if len(calls) == 2:
            raise MemoryError("Second analysis cannot be staged")
        return original_invalidate(result, frames)

    monkeypatch.setattr(msm.Interactions, "invalidate_structures", fail_second)
    with pytest.raises(MemoryError, match="cannot be staged"):
        msm.set(molsys, element="atom", selection=[0], formal_charge=0)
    assert len(calls) == 2
    assert msm.get(molsys, element="atom", formal_charge=True) == [1, -1, 0, 0]
    assert all(
        molsys.interactions[name] is result for name, result in originals.items()
    )


def test_failed_delegate_conservatively_invalidates_chemical_evidence(
    ionic_system, monkeypatch
):
    molsys = ionic_system
    original_setter = molsys.topology._set_chemical_state_atom_attribute

    def partially_failing_setter(*args, **kwargs):
        original_setter(*args, **kwargs)
        raise RuntimeError("Failure after chemistry write")

    monkeypatch.setattr(
        molsys.topology, "_set_chemical_state_atom_attribute", partially_failing_setter
    )
    with pytest.raises(RuntimeError, match="after chemistry write"):
        msm.set(molsys, element="atom", selection=[0], formal_charge=0)
    _assert_unevaluated(molsys)
    assert msm.get(molsys, element="atom", formal_charge=True) == [0, -1, 0, 0]
