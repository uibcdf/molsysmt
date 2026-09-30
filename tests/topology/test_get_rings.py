"""Checking sparse cycle-basis membership and source/state semantics."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt.native import Topology


def _topology(n_atoms, pairs):
    molsys = Topology(n_atoms=n_atoms)
    molsys.atoms["atom_id"] = [f"atom-{100 + i}" for i in range(n_atoms)]
    if len(pairs):
        molsys.bonds = pd.DataFrame({
            "atom1_index": [a for a, _ in pairs], "atom2_index": [b for _, b in pairs],
            "bond_type": ["covalent"] * len(pairs),
        })
    molsys._reference_chemical_state.connectivity_completeness = "complete"
    return molsys


def _memberships(result):
    return [tuple(result["atom_indices"][a:b]) for a, b in zip(
        result["atom_offsets"][:-1], result["atom_offsets"][1:],
    )]


def test_two_fused_cycles_do_not_expand_to_all_cycles():
    pairs = [(0, 1), (1, 2), (2, 3), (3, 0), (2, 4), (4, 5), (5, 3)]
    molsys = _topology(6, pairs)
    result = msm.topology.get_rings(molsys)
    assert _memberships(result) == [(0, 1, 2, 3), (2, 3, 4, 5)]
    np.testing.assert_array_equal(result["source_atom_indices"], np.arange(6))
    assert result["software"]["molsysmt"] == msm.__version__
    assert result["chemical_state_index"] == 0
    assert result["method"] == "minimum_cycle_basis"


def test_ring_memberships_are_independent_of_bond_row_order_and_orientation():
    pairs = [(0, 1), (1, 2), (2, 3), (3, 0), (2, 4), (4, 5), (5, 3)]
    first = msm.topology.get_rings(_topology(6, pairs))
    second = msm.topology.get_rings(_topology(6, [(b, a) for a, b in reversed(pairs)]))
    assert _memberships(first) == _memberships(second)


def test_complete_selection_preserves_original_indices_and_repeated_indices():
    pairs = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
    result = msm.topology.get_rings(_topology(6, pairs), selection=[5, 3, 4, 3])
    assert _memberships(result) == [(3, 4, 5)]
    assert result["selection_atom_indices"].tolist() == [3, 4, 5]
    assert result["examined_atom_indices"].tolist() == list(range(6))


def test_partial_selection_and_shared_fused_atom_fail():
    molsys = _topology(6, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)])
    for selected in ([0], [0, 1, 2]):
        with pytest.raises(ArgumentError, match="cuts a perceived ring"):
            msm.topology.get_rings(molsys, selection=selected)


def test_dative_edges_cannot_close_a_covalent_ring():
    molsys = _topology(3, [(0, 1), (1, 2), (2, 0)])
    molsys.bonds.loc[2, "bond_type"] = "dative"
    result = msm.topology.get_rings(molsys)
    assert result["atom_indices"].shape == (0,)
    assert result["atom_indices"].dtype == np.int64
    assert result["atom_offsets"].tolist() == [0]


def test_explicit_assumption_does_not_change_source_metadata():
    molsys = _topology(3, [(0, 1), (1, 2), (2, 0)])
    molsys._reference_chemical_state.connectivity_completeness = "unavailable"
    with pytest.raises(StructuralInconsistencyError, match="declared complete"):
        msm.topology.get_rings(molsys)
    result = msm.topology.get_rings(molsys, assume_complete_connectivity=True)
    assert result["evidence"]["assume_complete_connectivity"] is True
    assert molsys._reference_chemical_state.connectivity_completeness == "unavailable"


def test_explicit_nonreference_state_changes_cycles_without_changing_reference():
    molsys = _topology(3, [(0, 1), (1, 2), (2, 0)])
    second = molsys._append_chemical_state(state_id="open")
    molsys._append_chemical_state_bonds([(0, 1), (1, 2)], types="covalent", state_index=second)
    molsys._chemical_states[second].connectivity_completeness = "complete"
    before = msm.topology.get_rings(molsys)
    after = msm.topology.get_rings(molsys, chemical_state=second)
    assert len(_memberships(before)) == 1
    assert not _memberships(after)
    assert after["chemical_state_index"] == second
    assert molsys._reference_chemical_state_index == 0


@pytest.mark.parametrize("limit", [True, False, 2, 3.5, "256", None])
def test_block_limit_requires_an_explicit_integer_at_least_three(limit):
    with pytest.raises(ArgumentError):
        msm.topology.get_rings(_topology(0, []), max_cyclic_block_size=limit)


def test_block_limit_applies_to_cycles_instead_of_acyclic_component_size():
    pairs = [(i, i + 1) for i in range(999)] + [(0, 2)]
    result = msm.topology.get_rings(_topology(1000, pairs), max_cyclic_block_size=3)
    assert _memberships(result) == [(0, 1, 2)]
    with pytest.raises(UnsupportedHeavyOperationError, match="max_cyclic_block_size"):
        msm.topology.get_rings(_topology(4, [(0, 1), (1, 2), (2, 3), (3, 0)]), max_cyclic_block_size=3)


@pytest.mark.parametrize("defect", ["missing_type", "unknown_type", "duplicate", "self", "out_of_range"])
def test_invalid_connectivity_cannot_masquerade_as_an_evaluated_empty_result(defect):
    molsys = _topology(3, [(0, 1), (1, 2), (2, 0)])
    if defect == "missing_type":
        molsys._reference_chemical_state.bonds = molsys.bonds.drop(columns="bond_type")
    elif defect == "unknown_type":
        molsys.bonds.loc[0, "bond_type"] = pd.NA
    elif defect == "duplicate":
        molsys.bonds.loc[1, ["atom1_index", "atom2_index"]] = [1, 0]
    else:
        molsys.bonds.loc[0, "atom2_index"] = 0 if defect == "self" else 3
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_rings(molsys, selection=[])


def test_unsupported_method_does_not_silently_use_another_basis():
    with pytest.raises(ArgumentError):
        msm.topology.get_rings(_topology(0, []), method="symmsssr")


def test_empty_atom_domain_has_typed_empty_membership():
    result = msm.topology.get_rings(_topology(0, []))
    assert result["atom_indices"].dtype == np.int64
    assert result["atom_offsets"].dtype == np.int64
    assert result["atom_offsets"].tolist() == [0]
