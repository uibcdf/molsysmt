"""Copy the native molecular graph without migration or ownership transfer."""

import copy
import pickle

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolecularMechanics, MolSys, Structures, Topology
from tests.native.test_molsys import build_minimal_molsys


def _native_deferred(source):
    return source.copy(deep=False)


def _copy_system():
    result = build_minimal_molsys(n_structures=3)
    result.structures.box = puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0), "nm")
    result.chemical_states.append_state()
    result._set_structure_chemical_state_indices([0, 1, None])
    result.molecular_mechanics.partial_charge = [0.1, 0.2, 0.3, 0.4]
    result.molecular_mechanics.atom_ff_type = ["A", "B", "C", "D"]
    records = [
        {
            "structure_index": structure,
            "interaction_type": "synthetic",
            "participants": [
                {"role": "donor", "atom_indices": [0]},
                {"role": "hydrogen", "atom_indices": [1]},
                {"role": "acceptor", "atom_indices": [2]},
            ],
            "measurements": {"distance": distance},
        }
        for structure, distance in [(0, 0.2), (2, 0.3), (2, 0.4)]
    ]
    analysis = msm.Interactions.from_records(
        records,
        n_atoms=4,
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="synthetic",
        measure_units={"distance": "nm"},
        software={"producer": "0.1"},
        atom_source_indices=[7, 6, 5, 4],
        structure_source_indices=[8, 3, 5],
        source_n_atoms=8,
        source_n_structures=9,
    )
    result.interactions = {
        "full": analysis,
        "masked": analysis.invalidate_structures([0]),
        "patched": analysis.replace_structures(analysis),
    }
    result.notes = {"items": [1]}
    return result


@pytest.fixture
def source():
    return _copy_system()


@pytest.fixture(
    params=[copy.copy, copy.deepcopy, _native_deferred, MolSys.copy, msm.copy]
)
def copier(request):
    return request.param


def test_copy_owns_domains_chemistry_and_canonical_tables(source, copier):
    duplicate = copier(source)
    assert duplicate is not source
    assert duplicate.topology is not source.topology
    assert source.topology._molsys_owner_ref() is source
    assert duplicate.topology._molsys_owner_ref() is duplicate
    assert duplicate.chemical_states._molsys_owner_ref() is duplicate
    assert duplicate.chemical_states is not source.chemical_states
    assert duplicate.structures is not source.structures
    assert duplicate.molecular_mechanics is not source.molecular_mechanics
    assert duplicate._interactions is not source._interactions
    for name in ("atoms", "groups", "molecules", "entities", "chains"):
        first, second = (
            getattr(source.topology, name),
            getattr(duplicate.topology, name),
        )
        pd.testing.assert_frame_equal(first, second)
        assert first is not second
        second.iloc[0, 0] = "changed"
        assert first.iloc[0, 0] != "changed"
    for original, cloned in zip(
        source.chemical_states._states, duplicate.chemical_states._states
    ):
        assert original is not cloned
        for name in ("bonds", "components", "atom_attributes"):
            first, second = getattr(original, name), getattr(cloned, name)
            pd.testing.assert_frame_equal(first, second)
            assert first is not second
    duplicate.chemical_states.get_bonds(chemical_state=0).at[0, "bond_order"] = 2
    assert source.chemical_states.get_bonds(chemical_state=0).at[0, "bond_order"] == 1
    duplicate._structure_chemical_state_indices[0] = 1
    assert source._structure_chemical_state_indices[0] == 0
    assert pd.isna(duplicate._structure_chemical_state_indices[2])
    duplicate.molecular_mechanics.atoms_ff.at[0, "partial_charge"] = 0.9
    assert source.molecular_mechanics.partial_charge[0] == 0.1
    duplicate.notes["items"].append(2)
    assert source.notes == {"items": [1]}


def test_geometry_allocation_mode_and_edits_are_independent(source, copier):
    duplicate = copier(source)
    deferred = copier in (copy.copy, _native_deferred)
    for name in ("_coordinates", "_box"):
        first = getattr(source.structures, name)._blocks[0]
        second = getattr(duplicate.structures, name)._blocks[0]
        assert first is not second
        assert np.shares_memory(first, second) == deferred
    snapshot = source.structures.get_coordinates()
    old_result = duplicate.interactions["full"]
    old_query = old_result.query(structure_indices=[1, 2])
    msm.set(
        duplicate,
        element="atom",
        selection=[3],
        structure_indices=[1],
        coordinates=puw.quantity([[[10.0, 20.0, 30.0]]], "angstrom"),
    )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.get_coordinates(), to_unit="nm"),
        puw.get_value(snapshot, to_unit="nm"),
    )
    np.testing.assert_allclose(
        puw.get_value(
            duplicate.structures.get_coordinates(indices=[3], structure_indices=[1]),
            to_unit="nm",
        ),
        [[[1.0, 2.0, 3.0]]],
    )
    np.testing.assert_array_equal(
        source.interactions["full"].evaluated_structure_indices, [0, 1, 2]
    )
    np.testing.assert_array_equal(
        duplicate.interactions["full"].evaluated_structure_indices, [0, 2]
    )
    np.testing.assert_array_equal(old_result.evaluated_structure_indices, [0, 1, 2])
    np.testing.assert_array_equal(
        old_query.to_dict()["evaluated_structure_indices"], [1, 2]
    )
    source.structures.set_coordinates(
        indices=[0],
        structure_indices=[0],
        value=puw.quantity([[[-1.0, -2.0, -3.0]]], "nm"),
    )
    np.testing.assert_array_equal(
        puw.get_value(
            duplicate.structures.get_coordinates(indices=[0], structure_indices=[0]),
            to_unit="nm",
        ),
        [[[0.0, 1.0, 2.0]]],
    )


def test_copy_preserves_lazy_analyses_and_producer_without_reconstruction(
    source, copier, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Molecular copying crossed a constructor or interchange boundary")

    classes = (
        MolSys,
        Topology,
        Structures,
        MolecularMechanics,
        msm.ChemicalStates,
        msm.Interactions,
    )
    with monkeypatch.context() as patch:
        from molsysmt.native._structure_array import _StructureArray

        patch.setattr(_StructureArray, "_dense", forbidden)
        for cls in classes:
            patch.setattr(cls, "__init__", forbidden)
            if hasattr(cls, "__setstate__"):
                patch.setattr(cls, "__setstate__", forbidden)
        patch.setattr(msm.Interactions, "remap", forbidden)
        for result in source.interactions.values():
            if hasattr(result, "_packed"):
                patch.setattr(type(result), "_packed", forbidden)
        duplicate = copier(source)
    for name, result in duplicate.interactions.items():
        original = source.interactions[name]
        assert result is not original
        assert type(result) is type(original)
        if hasattr(original, "_packed_result"):
            assert original._packed_result is None
            assert result._packed_result is None
        assert result.software == {"producer": "0.1"}
        np.testing.assert_array_equal(result.atom_source_indices, [7, 6, 5, 4])
        np.testing.assert_array_equal(result.structure_source_indices, [8, 3, 5])
        np.testing.assert_array_equal(
            result.query(structure_indices=[2, 0]).to_dict()["occurrence_indices"],
            original.query(structure_indices=[2, 0]).to_dict()["occurrence_indices"],
        )
    duplicate.interactions = {"retained": duplicate.interactions["full"]}
    assert set(source.interactions) == {"full", "masked", "patched"}


def test_replacing_copied_chemistry_invalidates_only_the_copied_analyses(source):
    duplicate = source.copy(deep=False)
    replacement = duplicate.chemical_states.copy()
    duplicate.chemical_states = replacement
    assert duplicate.chemical_states is replacement
    assert duplicate.chemical_states is not source.chemical_states
    assert duplicate.interactions["full"].evaluated_structure_indices.size == 0
    np.testing.assert_array_equal(
        source.interactions["full"].evaluated_structure_indices, [0, 1, 2]
    )


@pytest.mark.parametrize(
    "domains",
    ["structures", "chemistry", "topology", "interactions", "topology_chemistry"],
)
def test_copy_preserves_absent_domains(source, copier, domains):
    topology = (
        None
        if domains not in ("topology", "topology_chemistry")
        else Topology(n_atoms=4)
    )
    chemistry = source.chemical_states if domains == "chemistry" else None
    if domains == "topology_chemistry":
        chemistry = source.chemical_states.copy()
    partial = MolSys._from_partial_domains(
        topology=topology,
        chemical_states=chemistry,
        structures=source.structures if domains == "structures" else None,
        interactions=source.interactions if domains == "interactions" else None,
    )
    duplicate = copier(partial)
    assert (duplicate.structures is None) == (partial.structures is None)
    assert (duplicate.topology is None) == (partial.topology is None)
    assert (duplicate.chemical_states is None) == (partial.chemical_states is None)
    if topology is not None:
        assert topology._molsys_owner_ref() is partial
        assert duplicate.topology._molsys_owner_ref() is duplicate
    assert set(duplicate.interactions) == set(partial.interactions)


@pytest.mark.parametrize("root", ["system", "topology", "chemistry", "mechanics"])
def test_deepcopy_propagates_memo_and_explicit_owner_cycles(source, root):
    source.topology.extension_owner = source
    source.molecular_mechanics.extension_owner = source
    source.chemical_states.extension_owner = source
    original = {
        "system": source,
        "topology": source.topology,
        "chemistry": source.chemical_states,
        "mechanics": source.molecular_mechanics,
    }[root]
    graph = copy.deepcopy(
        [
            original,
            source,
            source.topology,
            source.chemical_states,
            source.structures,
            source.interactions["masked"],
            source.notes,
        ]
    )
    duplicate = graph[1]
    assert duplicate.topology is graph[2]
    assert duplicate.chemical_states is graph[3]
    assert duplicate.structures is graph[4]
    assert duplicate.interactions["masked"] is graph[5]
    assert duplicate.notes is graph[6]
    assert duplicate.chemical_states._molsys_owner_ref() is duplicate
    assert duplicate.topology.extension_owner is duplicate
    assert duplicate.chemical_states.extension_owner is duplicate
    assert duplicate.molecular_mechanics.extension_owner is duplicate
    assert duplicate.topology._molsys_owner_ref() is duplicate
    assert source.topology._molsys_owner_ref() is source


class _ExtendedMolSys(MolSys):
    __slots__ = ("extra",)


@pytest.mark.parametrize(
    "copier", [copy.copy, copy.deepcopy, _native_deferred, MolSys.copy]
)
def test_copy_preserves_concrete_subclass_slots_and_self_cycle(copier):
    source = _ExtendedMolSys(n_atoms=2)
    source.extra = {"owner": source, "values": [1]}
    source.again = source
    duplicate = copier(source)
    assert type(duplicate) is _ExtendedMolSys
    assert duplicate.again is duplicate
    assert duplicate.extra["owner"] is duplicate
    duplicate.extra["values"].append(2)
    assert source.extra["values"] == [1]


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_standalone_topology_copy_does_not_retain_or_clone_weak_owner(source, copier):
    duplicate = copier(source.topology)
    assert getattr(duplicate, "_molsys_owner_ref", None) is None
    assert source.topology._molsys_owner_ref() is source
    independent = MolSys(n_atoms=4)
    independent.topology = duplicate
    assert duplicate._molsys_owner_ref() is independent
    assert source.topology._molsys_owner_ref() is source


def test_failed_molecular_copy_leaves_original_owner_and_analyses_intact(source):
    class CannotCopy:
        def __deepcopy__(self, memo):
            raise MemoryError("deliberate metadata allocation failure")

    source.notes["failure"] = CannotCopy()
    original = vars(source).copy()
    with pytest.raises(MemoryError):
        source.copy(deep=False)
    assert all(vars(source)[name] is value for name, value in original.items())
    assert source.topology._molsys_owner_ref() is source
    np.testing.assert_array_equal(
        source.interactions["full"].evaluated_structure_indices, [0, 1, 2]
    )


@pytest.mark.parametrize("deep", [None, 1, "false", np.bool_(False)])
def test_native_copy_rejects_non_boolean_allocation_mode(source, deep):
    from molsysmt._private.smonitor import ArgumentError

    with pytest.raises(ArgumentError):
        source.copy(deep=deep)


def test_copied_system_h5msm_and_pickle_keep_one_chemical_authority(source, tmp_path):
    duplicate = source.copy(deep=False)
    duplicate.molecular_mechanics = MolecularMechanics()
    path = tmp_path / "copied.h5msm"
    msm.convert(duplicate, to_form=path)
    for restored in (
        msm.convert(path, to_form="molsysmt.MolSys"),
        pickle.loads(pickle.dumps(duplicate)),
    ):
        assert restored.chemical_states._molsys_owner_ref() is restored
        assert restored.topology._molsys_owner_ref() is restored
        assert restored.chemical_states.n_chemical_states == 2
        assert pd.isna(restored._structure_chemical_state_indices[2])
        np.testing.assert_array_equal(
            restored.interactions["full"].to_dict()["occurrence_indices"], [0, 1, 2]
        )
        assert restored.interactions["full"].software == {"producer": "0.1"}
    assert source.topology._molsys_owner_ref() is source
