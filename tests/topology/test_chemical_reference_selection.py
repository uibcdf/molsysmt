"""Keeping default-reference semantics in shared chemical-graph selections."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

READERS = [
    (msm.chemical_states.get_rings, "selection_atom_indices"),
    (msm.physchem.get_aromatic_rings, "selection_atom_indices"),
    (msm.physchem.get_aromaticity, "atom_indices"),
    (msm.chemical_states.get_rotatable_bonds, "atom_indices"),
    (msm.interactions.hbonds.get_hbond_sites, "selected_atom_indices"),
    (msm.physchem.get_cip_stereochemistry, "atom_indices"),
]


@pytest.mark.parametrize("reader,key", READERS)
@pytest.mark.parametrize("form", ["native", "complementary", "h5msm"])
@pytest.mark.parametrize("chemical_state", [None, "reference"])
@pytest.mark.parametrize(
    "query,expected", [("all and all", list(range(6))), ("name ZZZX", [])]
)
def test_default_reference_external_selector_matches_intended_population(
    aromatic_system, reader, key, form, chemical_state, query, expected, tmp_path
):
    pytest.importorskip("mdtraj")
    source = aromatic_system
    if form == "complementary":
        source = [source.topology, source.chemical_states, source.structures]
    elif form == "h5msm":
        source = tmp_path / "source.h5msm"
        msm.convert(aromatic_system, to_form=source)
    before = msm.convert(
        aromatic_system.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    file_bytes = source.read_bytes() if form == "h5msm" else None
    kwargs = dict(structure_indices=[2, 0, 2], chemical_state=chemical_state)
    numeric = reader(source, selection=list(reversed(expected)) + expected, **kwargs)
    symbolic = reader(source, selection=query, syntax="MDTraj", **kwargs)
    np.testing.assert_array_equal(symbolic[key], expected)
    assert symbolic[key].dtype == np.int64
    for name, value in numeric.items():
        if isinstance(value, np.ndarray):
            np.testing.assert_equal(symbolic[name], value)
    assert symbolic["chemical_state_index"] == 0
    np.testing.assert_equal(
        before,
        msm.convert(
            aromatic_system.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
    )
    if form == "h5msm":
        assert source.read_bytes() == file_bytes
    if symbolic[key].size:
        symbolic[key][:] = -1
        assert numeric[key].tolist() == expected


@pytest.mark.parametrize("reader,key", READERS)
@pytest.mark.parametrize("state_request", [0, 1, "structure"])
def test_explicit_and_associated_states_keep_external_syntax_restriction(
    aromatic_system, reader, key, state_request
):
    pytest.importorskip("mdtraj")
    states = aromatic_system.chemical_states
    states._append_state(deepcopy(states._states[0]), set_as_reference=True)
    msm.set(aromatic_system, structure_chemical_state_index=[0, 1, 0])
    with pytest.raises(ArgumentError):
        reader(
            aromatic_system,
            selection="all and all",
            syntax="MDTraj",
            chemical_state=state_request,
            structure_indices=[0],
        )
    assert states.reference_chemical_state_index == 1
    assert msm.get(aromatic_system, structure_chemical_state_index=True) == [0, 1, 0]


@pytest.mark.parametrize("reader,key", READERS)
def test_default_reference_is_not_replaced_by_structure_association(
    aromatic_system, reader, key
):
    pytest.importorskip("mdtraj")
    states = aromatic_system.chemical_states
    states._append_state(deepcopy(states._states[0]), set_as_reference=True)
    msm.set(aromatic_system, structure_chemical_state_index=[0, 0, 0])
    result = reader(
        aromatic_system, selection="all and all", syntax="MDTraj", structure_indices=[2]
    )
    assert result["chemical_state_index"] == 1
    assert result[key].tolist() == list(range(6))
    assert states.reference_chemical_state_index == 1


@pytest.mark.parametrize(
    "reader", [msm.chemical_states.get_rings, msm.physchem.get_aromatic_rings]
)
def test_external_selection_still_requires_complete_ring_participants(
    aromatic_system, reader
):
    pytest.importorskip("mdtraj")
    with pytest.raises(ArgumentError, match="cuts a perceived ring"):
        reader(aromatic_system, selection="name C0", syntax="MDTraj")
