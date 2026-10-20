"""Protect useful native summaries against payload scans and diagnostic side effects."""

import io

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import (
    ChemicalStates,
    ChemicalStatesDict,
    GROAtomicCoordinateEntry,
    GROFileHandler,
    H5MSMFileHandler,
    InteractionsDict,
    MolecularMechanics,
    MolSys,
    MolSysBuilder,
    MolSysDict,
    PDBAtomicCoordinateEntry,
    PDBFileHandler,
    Simulation,
    Structures,
    Topology,
    TopologyDict,
    ViewerJSON,
)


def analysis():
    return msm.Interactions.from_records(
        [
            dict(
                structure_index=i,
                interaction_type="pair",
                participants=[
                    dict(role="a", atom_indices=[0]),
                    dict(role="b", atom_indices=[1]),
                ],
            )
            for i in [0, 2]
        ],
        n_atoms=3,
        n_structures=4,
        evaluated_structure_indices=[0, 1, 2],
        method="test",
    )


@pytest.mark.parametrize(
    "factory,fields",
    [
        (MolSys, ["n_atoms=0", "n_structures=0", "n_chemical_states=1"]),
        (Topology, ["n_atoms=0", "n_groups=0", "n_bonds=0"]),
        (Structures, ["n_atoms=None", "n_structures=0", "coordinates=False"]),
        (ChemicalStates, ["n_atoms=0", "n_chemical_states=0"]),
        (MolSysBuilder, ["n_atoms=0", "n_groups=0", "n_structures=0"]),
        (MolecularMechanics, ["n_atoms=None", "forcefield=False"]),
        (Simulation, ["integrator=None", "platform='CUDA'"]),
        (MolSysDict, ["n_atoms=0", "n_structures=None"]),
        (TopologyDict, ["n_atoms=0", "n_groups=0", "n_bonds=0"]),
        (
            lambda: ChemicalStatesDict(
                dict(n_atoms=5, states=[], reference_chemical_state_index=None)
            ),
            ["n_atoms=5", "n_chemical_states=0"],
        ),
        (
            lambda: msm.convert(analysis(), to_form="molsysmt.InteractionsDict"),
            ["n_atoms=3", "n_structures=4", "n_stored_relations=1", "n_occurrences=2"],
        ),
        (ViewerJSON, ["n_atoms=0", "n_structures=0", "compressed=False"]),
        (GROAtomicCoordinateEntry, ["n_atoms=0", "n_groups=0"]),
        (PDBAtomicCoordinateEntry, ["n_models=None", "format_version=None"]),
        (
            analysis,
            [
                "n_atoms=3",
                "n_structures=4",
                "n_occurrences=2",
                "n_evaluated_structures=3",
                "view=False",
            ],
        ),
    ],
)
def test_public_containers_report_actual_metadata_without_payloads(factory, fields):
    obj = factory()
    text = repr(obj)
    assert text.startswith(type(obj).__name__ + "(") and text.endswith(")")
    assert all(field in text for field in fields)
    assert len(text) < 300
    assert "object at 0x" not in text


def test_unknown_axes_are_distinct_from_empty_declared_axes():
    absent = MolSys._from_partial_domains(structures=Structures())
    assert "n_atoms=None" in repr(absent) and "n_structures=0" in repr(absent)
    assert "topology=False" in repr(absent) and "n_chemical_states=None" in repr(absent)
    assert "n_atoms=0" in repr(MolSys())
    empty = Structures(coordinates=msm.pyunitwizard.quantity(np.empty((2, 0, 3)), "nm"))
    assert "n_atoms=0" in repr(empty) and "n_structures=2" in repr(empty)
    partial = MolSys._from_partial_domains(structures=empty)
    assert "topology=False" in repr(partial) and "n_atoms=0" in repr(partial)
    chemistry_only = MolSys._from_partial_domains(chemical_states=ChemicalStates())
    assert "n_structures=None" in repr(chemistry_only)
    time_only = MolSysDict(dict(topology=dict(atoms=[]), structures=dict(time=[0, 1])))
    assert "n_structures=2" in repr(time_only)


def test_ambiguous_reference_does_not_select_a_state_or_raise():
    topology = Topology(n_atoms=5, n_groups=2)
    states = topology._chemical_states_domain
    states.append_state()
    states._reference_index = None
    assert "n_bonds=None" in repr(topology)
    assert "n_chemical_states=2" in repr(topology)
    assert "reference_chemical_state_index=None" in repr(states)
    assert states._reference_index is None


def test_summary_never_dispatches_validates_or_renders_data(monkeypatch):
    molsys = MolSys(n_atoms=3)
    molsys.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm")
    )
    builder = MolSysBuilder(molsys)
    before = molsys.structures._coordinates

    def forbidden(*args, **kwargs):
        raise AssertionError("repr must only inspect stored metadata")

    for name in ["get", "get_form", "select", "copy", "info"]:
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(Structures, "_validate_alignment", forbidden)
    monkeypatch.setattr(Topology, "_get_chemical_state_bonds", forbidden)
    monkeypatch.setattr(MolSys, "_validate_interactions", forbidden)
    monkeypatch.setattr(pd.DataFrame, "__repr__", forbidden)
    monkeypatch.setattr(msm.pyunitwizard, "get_value", forbidden)
    for obj in [
        molsys,
        builder,
        molsys.topology,
        molsys.chemical_states,
        molsys.structures,
        molsys.molecular_mechanics,
    ]:
        assert len(repr(obj)) < 300
    assert molsys.structures._coordinates is before
    assert molsys.chemical_states._reference_index == 0


class ShapeOnly:
    shape = (10_000, 100_000, 3)

    def __array__(self, *args, **kwargs):
        raise AssertionError("No materialization")

    def __len__(self):
        raise AssertionError("Use the stored shape")

    def __repr__(self):
        raise AssertionError("No payload rendering")


def test_large_coordinate_axes_need_only_shape_metadata():
    structures = Structures()
    partial = MolSys._from_partial_domains(structures=structures)
    partial.structures._coordinates = ShapeOnly()
    assert "n_atoms=100000" in repr(partial)
    assert "n_structures=10000" in repr(partial)
    assert "n_atoms=100000" in repr(partial.structures)
    assert len(repr(partial)) < 300


def test_sparse_views_report_selected_occurrences_without_building_indexes():
    result = analysis()
    selected = result.query(structure_indices=[1, 2])
    assert "n_stored_relations=1" in repr(selected)
    assert "n_occurrences=1" in repr(selected)
    assert "n_evaluated_structures=2" in repr(selected)
    assert "view=True" in repr(selected)
    assert result._atom_relation_offsets is None
    assert result._relation_occurrence_offsets is None
    empty = result.query(structure_indices=[1])
    unevaluated = result.query(structure_indices=[3])
    assert "n_evaluated_structures=1" in repr(empty)
    assert "n_evaluated_structures=0" in repr(unevaluated)


class LengthOnly:
    def __len__(self):
        return 100_000

    def __iter__(self):
        raise AssertionError("Do not scan payloads")

    def __repr__(self):
        raise AssertionError("Do not render payloads")


def test_dictionary_representations_do_not_expand_large_payloads():
    payload = LengthOnly()
    objects = [
        MolSysDict(
            dict(topology=dict(atoms=payload), structures=dict(coordinates=payload))
        ),
        TopologyDict(dict(atoms=payload, groups=[], bonds=payload)),
        ChemicalStatesDict(dict(n_atoms=100_000, states=payload)),
        InteractionsDict(
            dict(
                n_atoms=100_000,
                n_structures=10_000,
                relation_types=payload,
                occurrence_relations=payload,
            )
        ),
        ViewerJSON(dict(atoms=dict(atom_id=payload), structures=payload)),
    ]
    for obj in objects:
        assert "100000" in repr(obj)
        assert len(repr(obj)) < 300


def test_named_analyses_and_settings_remain_bounded_and_unchanged():
    result = analysis()
    molsys = MolSys(n_atoms=3)
    molsys.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((4, 3, 3)), "nm")
    )
    molsys.interactions = {f"private-analysis-{index}": result for index in range(1000)}
    before = molsys._interactions
    text = repr(molsys)
    assert "n_interaction_analyses=1000" in text
    assert "private-analysis" not in text
    assert molsys._interactions is before
    mechanics = MolecularMechanics(
        forcefield="sensitive-forcefield-name" * 1000, partial_charge=[0, 0, 0]
    )
    assert "n_atoms=3" in repr(mechanics)
    assert "sensitive-forcefield" not in repr(mechanics)
    simulation = Simulation(integrator="a" * 100_000)
    assert len(repr(simulation)) < 300


@pytest.mark.parametrize("factory", [PDBFileHandler, GROFileHandler])
def test_text_handler_summaries_do_not_read_or_seek_and_follow_close(factory):
    class Unreadable(io.StringIO):
        def read(self, *args):
            raise AssertionError("No I/O")

        readline = read
        readlines = read
        seek = read

    handler = object.__new__(factory)
    handler.file = Unreadable("private payload")
    handler.entry = None
    handler.format_version = "3.3"
    assert "is_open=True" in repr(handler)
    handler.close()
    assert "is_open=False" in repr(handler)
    assert "private payload" not in repr(handler)


def test_h5msm_handler_summary_does_not_read_datasets(tmp_path, monkeypatch):
    import h5py

    handler = H5MSMFileHandler(
        tmp_path / "summary.h5msm", io_mode="w", format_version="0.4"
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("No HDF5 data reads")

    monkeypatch.setattr(h5py.Group, "__getitem__", forbidden)
    monkeypatch.setattr(h5py.Dataset, "__getitem__", forbidden)
    assert "is_open=True" in repr(handler) and "format_version='0.4'" in repr(handler)
    handler.close()
    assert "is_open=False" in repr(handler)


@pytest.mark.parametrize(
    "cls",
    [
        MolSys,
        Topology,
        Structures,
        ChemicalStates,
        MolSysBuilder,
        MolecularMechanics,
        Simulation,
        MolSysDict,
        TopologyDict,
        ChemicalStatesDict,
        InteractionsDict,
        ViewerJSON,
        PDBFileHandler,
        H5MSMFileHandler,
        GROFileHandler,
        PDBAtomicCoordinateEntry,
        GROAtomicCoordinateEntry,
        msm.Interactions,
    ],
)
def test_initializing_objects_can_be_summarized_by_diagnostics(cls):
    # SMonitor can request repr(self) before a constructor has assigned its fields.
    obj = object.__new__(cls)
    try:
        assert len(repr(obj)) < 300
    finally:
        if isinstance(obj, (PDBFileHandler, GROFileHandler)):
            obj.file = None  # Their existing destructors expect this attribute.


def test_invalidated_and_patched_analyses_use_cached_counts_without_packing(
    monkeypatch,
):
    result = analysis()
    invalidated = result.invalidate_structures(structure_indices=[0])
    replacement = analysis().invalidate_structures([2])
    patched = result.replace_structures(replacement)

    def forbidden(*args, **kwargs):
        raise AssertionError("No packing during inspection")

    for obj, count in [(invalidated, 1), (patched, 2)]:
        monkeypatch.setattr(obj, "_packed", forbidden)
        assert repr(obj).startswith("Interactions(")
        assert f"n_occurrences={count}" in repr(obj)
        assert obj._packed_result is None
