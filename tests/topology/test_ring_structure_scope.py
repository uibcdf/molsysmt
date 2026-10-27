"""Checking explicit ring structure scopes before coordinate-free chemistry reads."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys

READERS = [msm.topology.get_rings, msm.physchem.get_aromatic_rings]


def _source(molsys, form, tmp_path):
    if form == "complementary":
        return [molsys.topology, molsys.structures]
    if form == "h5msm":
        path = tmp_path / "ring.h5msm"
        msm.convert(molsys, to_form=path)
        return path
    return molsys


@pytest.mark.parametrize("reader", READERS)
@pytest.mark.parametrize("form", ["native", "complementary", "h5msm"])
@pytest.mark.parametrize("indices", [[-1], [3], [999]])
@pytest.mark.parametrize("selection", ["all", [5, 4, 3, 2, 1, 0]])
def test_ring_readers_reject_invalid_structure_scope(
    aromatic_system, reader, form, indices, selection, tmp_path
):
    source = _source(aromatic_system, form, tmp_path)
    with pytest.raises(ArgumentError):
        reader(source, structure_indices=indices, selection=selection)


@pytest.mark.parametrize("reader", READERS)
@pytest.mark.parametrize("form", ["native", "complementary", "h5msm"])
def test_valid_repeated_nonconsecutive_scope_needs_no_coordinate_read(
    aromatic_system, reader, form, tmp_path, monkeypatch
):
    source = _source(aromatic_system, form, tmp_path)
    before = aromatic_system.structures.coordinates
    reference = reader(source)
    if form == "h5msm":
        import molsysmt.form._h5msm05_modular as modular

        def reject(*args, **kwargs):
            raise AssertionError(
                "Pure ring recognition must not read structural payloads"
            )

        monkeypatch.setattr(modular, "read_independent_structures", reject)
    result = reader(source, structure_indices=[2, 0, 2])
    np.testing.assert_array_equal(result["atom_indices"], reference["atom_indices"])
    np.testing.assert_array_equal(result["atom_offsets"], [0, 6])
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(aromatic_system.structures.coordinates),
        msm.pyunitwizard.get_value(before),
    )
    assert result["chemical_state_index"] == 0


@pytest.mark.parametrize("reader", READERS)
@pytest.mark.parametrize("kind", ["topology", "states", "partial"])
def test_chemistry_without_structure_axis_accepts_default_and_rejects_explicit(
    aromatic_system, reader, kind
):
    if kind == "topology":
        source = aromatic_system.topology
    elif kind == "states":
        source = aromatic_system.chemical_states
    else:
        topology = msm.copy(aromatic_system.topology)
        source = MolSys._from_partial_domains(
            topology=topology, chemical_states=topology._chemical_states_domain
        )
    result = reader(source)
    np.testing.assert_array_equal(result["atom_offsets"], [0, 6])
    for indices in ([0], []):
        with pytest.raises(ArgumentError):
            reader(source, structure_indices=indices)


@pytest.mark.parametrize("reader", READERS)
def test_structure_state_selection_still_rejects_ambiguous_states(
    aromatic_system, reader
):
    aromatic_system.chemical_states.append_state()
    msm.set(aromatic_system, structure_chemical_state_index=[0, 1, None])
    with pytest.raises(StructuralInconsistencyError):
        reader(aromatic_system, structure_indices=[0, 1], chemical_state="structure")
    with pytest.raises(StructuralInconsistencyError):
        reader(aromatic_system, structure_indices=[2], chemical_state="structure")
