"""Checking sparse ionic reduction across native and projected H5MSM blocks."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt.native import Structures

from .test_get_ionic_interactions import _calculate, _ions, _system


def _assert_same(first, second):
    # Execution provenance can differ, while every scientific/result field must match.
    for name in (
        "occurrence_structures",
        "occurrence_relations",
        "participant_atoms",
        "participant_atom_offsets",
        "relation_participant_offsets",
        "evaluated_structure_indices",
        "atom_source_indices",
        "structure_source_indices",
    ):
        np.testing.assert_array_equal(getattr(first, name), getattr(second, name))
    assert first.participant_roles == second.participant_roles
    assert first.relation_types == second.relation_types
    assert first.measure_units == second.measure_units
    assert first.software == second.software
    for name in first.measurements:
        np.testing.assert_allclose(first.measurements[name], second.measurements[name])
    if first.image_vectors is None:
        assert second.image_vectors is None
    else:
        np.testing.assert_array_equal(first.image_vectors, second.image_vectors)
        np.testing.assert_array_equal(
            first.occurrence_image_offsets, second.occurrence_image_offsets
        )
    np.testing.assert_array_equal(
        first.query().to_dict()["occurrence_indices"],
        second.query().to_dict()["occurrence_indices"],
    )


@pytest.mark.parametrize("file_source", [False, True])
@pytest.mark.parametrize("scope", ["internal", "incident", "between"])
def test_eager_chunked_scopes_and_empty_nonconsecutive_frames(
    file_source, scope, tmp_path
):
    molsys = _ions()
    if file_source:
        source = str(tmp_path / "ions.h5msm")
        msm.convert(molsys, to_form=source)
    else:
        source = molsys
    kwargs = dict(selection_mode=scope, structure_indices=[2, 0, 2, 1])
    if scope != "internal":
        kwargs["selection"] = [1]
    if scope == "between":
        kwargs["selection_2"] = [0, 2]
    with msm.configure.context(chunk_size=2):
        eager = _calculate(source, heavy_mode="off", **kwargs)
        chunked = _calculate(source, heavy_mode="force", **kwargs)
    _assert_same(eager, chunked)
    assert chunked.execution_records[0]["details"]["execution"] == "chunked"
    assert chunked.execution_records[0]["details"]["execution_chunks"] == 2
    assert eager.execution_records[0]["details"]["execution_chunks"] == 1
    assert chunked.query(structure_indices=1).n_interactions == 0
    assert chunked.query(structure_indices=1).to_dict()[
        "evaluated_structure_indices"
    ].tolist() == [1]


@pytest.mark.parametrize("file_source", [False, True])
def test_compound_triclinic_images_queries_and_named_roundtrip(file_source, tmp_path):
    box = np.array([[2, 0, 0], [0.4, 2, 0], [0.2, 0.3, 2.0]])
    xyz = np.array([[[0.1, 0, 0], [0.2, 0, 0], [0.2, 0.1, 0], [1.9, 0, 0]]])
    molsys = _system(
        ["C", "O", "O", "Na"],
        [0, -1, 0, 1],
        np.repeat(xyz, 5, axis=0),
        [(0, 1), (0, 2)],
        [1, 2],
        box=np.repeat(box[None], 5, axis=0),
    )
    source = molsys
    if file_source:
        source = str(tmp_path / "compound.h5msm")
        msm.convert(molsys, to_form=source)
    with msm.configure.context(chunk_size=2):
        eager = msm.interactions.ionic.get_ionic_interactions(
            source, ".4 nm", heavy_mode="off"
        )
        chunked = msm.interactions.ionic.get_ionic_interactions(
            source, ".4 nm", heavy_mode="force"
        )
    _assert_same(eager, chunked)
    assert chunked.execution_records[0]["details"]["execution_chunks"] == 3
    assert chunked.query(atom_indices=[0], structure_indices=[4, 1]).n_interactions == 2
    assert chunked.query(atom_indices=[0, 1, 2], mode="internal").n_interactions == 0
    molsys.interactions = {"ionic": chunked}
    path = str(tmp_path / "result.h5msm")
    msm.convert(molsys, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys").interactions["ionic"]
    _assert_same(chunked, restored)
    assert restored.parameters == chunked.parameters


def test_file_state_resolution_and_no_structural_materialization(tmp_path, monkeypatch):
    from molsysmt.form import _h5msm05_modular

    molsys = _ions()
    state = molsys.chemical_states.append_state()
    msm.set(molsys, element="atom", formal_charge=[2, -1, 1], chemical_state=state)
    molsys.topology._chemical_states[state].connectivity_completeness = "complete"
    molsys._set_structure_chemical_state_indices([state, 0, state])
    source = str(tmp_path / "states.h5msm")
    msm.convert(molsys, to_form=source)

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Projected calculation must not read whole structural or interaction domains."
        )

    monkeypatch.setattr(_h5msm05_modular, "read_independent_structures", forbidden)
    monkeypatch.setattr(_h5msm05_modular, "read_named_analyses", forbidden)
    monkeypatch.setattr(_h5msm05_modular, "read_molsys_file", forbidden)
    with msm.configure.context(chunk_size=1):
        result = _calculate(
            source,
            chemical_state="structure",
            structure_indices=[2, 0],
            heavy_mode="force",
        )
    assert result.parameters["chemical_state_index"] == state
    np.testing.assert_allclose(result.measurements["positive_charge"], [2, 1, 2])
    with pytest.raises(StructuralInconsistencyError):
        _calculate(source, chemical_state="structure", heavy_mode="force")


def test_file_rejects_nonidentity_atom_association_before_geometry(tmp_path):
    import h5py

    source = str(tmp_path / "mapping.h5msm")
    msm.convert(_ions(), to_form=source)
    with h5py.File(source, "r+") as file:
        for link in file["associations"].values():
            if link.attrs["source"] == "structures" and link.attrs["axis"] == "atom":
                link.attrs["mapping"] = "explicit"
                link.create_dataset("indices", data=[2, 1, 0])
    with pytest.raises(ValueError, match="identity atom-axis"):
        _calculate(source, heavy_mode="force")


def test_auto_coordinate_working_estimate_selects_small_blocks():
    molsys = _ions()
    molsys.structures = Structures(
        coordinates=puw.quantity(
            np.tile(
                puw.get_value(molsys.structures.coordinates, to_unit="nm"), (2, 1, 1)
            ),
            "nm",
        )
    )
    with msm.configure.context(max_ram_usage=6000, chunk_size=2):
        result = _calculate(molsys)
    assert result.execution_records[0]["details"]["execution"] == "chunked"
    assert result.execution_records[0]["details"]["execution_chunks"] == 3
    assert result.n_interactions == 6


def test_result_budget_failure_does_not_return_partial_coverage():
    molsys = _system(
        ["Na", "Cl"], [1, -1], np.tile([[[0.0, 0, 0], [0.2, 0, 0]]], (12, 1, 1))
    )
    with msm.configure.context(max_ram_usage=8000, chunk_size=2):
        with pytest.raises(MemoryBudgetExceededError, match="sparse-result"):
            _calculate(molsys, heavy_mode="force")


def test_later_invalid_block_propagates_without_finalizing(monkeypatch):
    from molsysmt.interactions.ionic._reducer import _IonicReducer

    molsys = _ions()
    xyz = puw.get_value(molsys.structures.coordinates, to_unit="nm").copy()
    xyz[2, 1, 0] = np.nan
    molsys.structures.coordinates = puw.quantity(xyz, "nm")

    def forbidden(self):
        raise AssertionError("A failed block must not finalize a partial analysis.")

    monkeypatch.setattr(_IonicReducer, "finalize", forbidden)
    with msm.configure.context(chunk_size=2):
        with pytest.raises(StructuralInconsistencyError):
            _calculate(molsys, heavy_mode="force")


@pytest.mark.parametrize("file_source", [False, True])
def test_missing_coordinates_are_not_evaluated_as_zero(file_source, tmp_path):
    molsys = _ions()
    molsys.structures = Structures(structure_id=np.arange(3))
    source = molsys
    if file_source:
        source = str(tmp_path / "no_coordinates.h5msm")
        msm.convert(molsys, to_form=source)
    with pytest.raises(StructuralInconsistencyError, match="Coordinates are required"):
        _calculate(source, heavy_mode="force")


def test_rich_selection_rejects_forced_chunking_but_keeps_eager():
    molsys = _ions()
    assert (
        _calculate(
            molsys, selection='atom_type=="Na" or atom_type=="Cl"', heavy_mode="off"
        ).n_interactions
        == 2
    )
    with pytest.raises(UnsupportedHeavyOperationError):
        _calculate(molsys, selection='atom_type=="Na"', heavy_mode="force")


def test_empty_selections_still_budget_the_resident_axis_arrays():
    with msm.configure.context(max_ram_usage=128):
        with pytest.raises(MemoryBudgetExceededError):
            _calculate(_ions(), selection=[], heavy_mode="force")
