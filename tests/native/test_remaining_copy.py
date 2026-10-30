"""Native convenience and Python copies preserve resident graph semantics."""

import copy
import json

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import (
    ChemicalStates,
    ChemicalStatesDict,
    InteractionsDict,
    MolecularMechanics,
    MolSysBuilder,
    MolSysDict,
    TopologyDict,
    ViewerJSON,
)
from tests.native.test_molsys import build_minimal_molsys
from tests.native.test_topology_operations import (
    build_minimal_chemical_molsys,
    build_minimal_topology,
)


def _resident(kind):
    if kind == "topology":
        return build_minimal_topology()
    if kind == "chemistry":
        return build_minimal_chemical_molsys().chemical_states
    if kind == "mechanics":
        return MolecularMechanics(forcefield="example", partial_charge=[0.1, 0.2])
    if kind == "builder":
        return MolSysBuilder(build_minimal_molsys(n_structures=3))
    classes = {
        "molsys_dict": MolSysDict,
        "topology_dict": TopologyDict,
        "chemistry_dict": ChemicalStatesDict,
        "interactions_dict": InteractionsDict,
        "viewer_json": ViewerJSON,
    }
    # These payload probes exercise copying, not schema admission or conversion.
    return classes[kind](data={"metadata": {"values": [1]}, "array": np.arange(6)})


KINDS = (
    "topology",
    "chemistry",
    "mechanics",
    "builder",
    "molsys_dict",
    "topology_dict",
    "chemistry_dict",
    "interactions_dict",
    "viewer_json",
)


@pytest.fixture(params=KINDS)
def source(request):
    result = _resident(request.param)
    result.extra = {"values": [1], "owner": result}
    result.alias = result.extra
    return result


@pytest.mark.parametrize(
    "operation", [copy.copy, copy.deepcopy, lambda item: item.copy()]
)
def test_every_entry_owns_mutable_state_and_preserves_aliases(source, operation):
    duplicate = operation(source)
    assert type(duplicate) is type(source)
    assert duplicate is not source
    assert duplicate.extra is duplicate.alias
    assert duplicate.extra["owner"] is duplicate
    duplicate.extra["values"].append(2)
    assert source.extra["values"] == [1]
    if hasattr(source, "data"):
        assert duplicate.data is not source.data
        duplicate.data["metadata"]["values"].append(2)
        duplicate.data["array"][0] = 99
        assert source.data["metadata"]["values"] == [1]
        np.testing.assert_array_equal(source.data["array"], np.arange(6))
    elif isinstance(source, ChemicalStates):
        duplicate.get_bonds().at[0, "bond_order"] = 2
        assert source.get_bonds().at[0, "bond_order"] == 1
    elif isinstance(source, MolecularMechanics):
        duplicate.atoms_ff.at[0, "partial_charge"] = 0.9
        assert source.partial_charge[0] == 0.1
    else:
        first = source.topology if isinstance(source, MolSysBuilder) else source
        second = (
            duplicate.topology if isinstance(duplicate, MolSysBuilder) else duplicate
        )
        second.atoms.at[0, "atom_name"] = "CHANGED"
        assert first.atoms.at[0, "atom_name"] == "N"


@pytest.mark.parametrize("kind", KINDS)
def test_native_copy_keeps_subclass_slots_and_avoids_construction(kind, monkeypatch):
    base = _resident(kind)

    class Extended(type(base)):
        __slots__ = ("slot_data",)

    source = object.__new__(Extended)
    source.__dict__.update(vars(base))
    source.slot_data = {"owner": source, "values": [1]}

    def forbidden(*args, **kwargs):
        pytest.fail(
            "A resident copy called a constructor, restoration or builder compilation"
        )

    with monkeypatch.context() as patch:
        patch.setattr(type(base), "__init__", forbidden)
        if hasattr(type(base), "__setstate__"):
            patch.setattr(type(base), "__setstate__", forbidden)
        if isinstance(base, MolSysBuilder):
            patch.setattr(MolSysBuilder, "build", forbidden)
        duplicate = source.copy()
    assert type(duplicate) is Extended
    assert duplicate.slot_data["owner"] is duplicate
    duplicate.slot_data["values"].append(2)
    assert source.slot_data["values"] == [1]


@pytest.mark.parametrize("kind", KINDS)
def test_deepcopy_preserves_a_containing_graph_memo(kind):
    source = _resident(kind)
    shared = {"values": [1]}
    source.extension = shared
    duplicate, alias, metadata = copy.deepcopy([source, source, shared])
    assert duplicate is alias
    assert duplicate.extension is metadata
    assert metadata is not shared


@pytest.mark.parametrize("invalid", [None, 1, "true", np.bool_(True)])
def test_native_copy_validates_skip_digestion_even_when_truthy(source, invalid):
    from molsysmt._private.smonitor import ArgumentError

    with pytest.raises(ArgumentError):
        source.copy(skip_digestion=invalid)


@pytest.mark.parametrize(
    "operation,deferred",
    [
        (copy.copy, True),
        (copy.deepcopy, False),
        (lambda item: item.copy(), False),
        (lambda item: item.copy(deep=False), True),
    ],
)
def test_builder_copy_preserves_incomplete_staging_and_geometry_mode(
    operation, deferred, monkeypatch
):
    import molsysmt.native._structure_array as storage

    source = MolSysBuilder()
    source.add_atom(atom_name="C", atom_type="C")
    source.set_coordinates(puw.quantity(np.zeros((3, 1, 3)), "nm"))

    def forbidden(*args, **kwargs):
        pytest.fail("Copy/count assembled geometry or compiled an incomplete builder")

    with monkeypatch.context() as patch:
        patch.setattr(MolSysBuilder, "build", forbidden)
        patch.setattr(storage._StructureArray, "_dense", forbidden)
        duplicate = operation(source)
        assert duplicate.n_structures == 3
        assert duplicate.n_groups == 0
        assert duplicate.n_atoms == 1
    assert (
        np.shares_memory(
            source.structures._coordinates._blocks[0],
            duplicate.structures._coordinates._blocks[0],
        )
        == deferred
    )
    duplicate.structures.set_coordinates(
        indices=[0],
        structure_indices=[1],
        value=puw.quantity([[[10.0, 20.0, 30.0]]], "angstrom"),
    )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.get_coordinates(), to_unit="nm"), 0.0
    )
    np.testing.assert_allclose(
        puw.get_value(
            duplicate.structures.get_coordinates(indices=[0], structure_indices=[1]),
            to_unit="nm",
        ),
        [[[1.0, 2.0, 3.0]]],
    )


def test_plain_dictionary_form_retains_python_shallow_copy_semantics():
    source = {"coordinates": [1]}
    assert copy.copy(source)["coordinates"] is source["coordinates"]


@pytest.mark.parametrize("operation", [copy.copy, lambda item: msm.copy(item)])
@pytest.mark.parametrize(
    "kind",
    [
        "MolSysDict",
        "TopologyDict",
        "ChemicalStatesDict",
        "InteractionsDict",
        "ViewerJSON",
    ],
)
def test_copied_admitted_payloads_preserve_registered_data_and_reconstruction(
    kind, operation
):
    source = build_minimal_molsys(n_structures=3)
    if kind == "ChemicalStatesDict":
        original, target = source.chemical_states, "molsysmt.ChemicalStates"
    elif kind == "TopologyDict":
        original, target = source.topology, "molsysmt.Topology"
    elif kind == "InteractionsDict":
        original = msm.Interactions.from_records(
            [
                {
                    "structure_index": 0,
                    "interaction_type": "synthetic",
                    "participants": [
                        {"role": "a", "atom_indices": [0]},
                        {"role": "b", "atom_indices": [1]},
                    ],
                }
            ],
            n_atoms=4,
            n_structures=3,
            evaluated_structure_indices=[0, 1],
            method="synthetic",
            software={"producer": "0.1"},
        )
        target = "molsysmt.Interactions"
    else:
        original, target = source, "molsysmt.MolSys"
    payload = msm.convert(original, to_form=f"molsysmt.{kind}")
    duplicate = operation(payload)
    assert duplicate.data is not payload.data
    if kind == "ViewerJSON":
        # Graphics copying/serialization is separate from native decoding.
        np.testing.assert_equal(duplicate.data, payload.data)
        assert duplicate.data["atoms"]["atom_id"] == ["0", "1", "2", "3"]
        return
    restored = msm.convert(duplicate, to_form=target)
    assert msm.get(restored, n_atoms=True) == 4
    if kind == "InteractionsDict":
        np.testing.assert_array_equal(restored.to_dict()["occurrence_indices"], [0])
        np.testing.assert_array_equal(restored.evaluated_structure_indices, [0, 1])
        assert restored.software == {"producer": "0.1"}
    elif kind == "ChemicalStatesDict":
        assert restored.n_chemical_states == 1
        assert restored.get_bonds().at[0, "bond_order"] == 1
    else:
        topology = restored if kind == "TopologyDict" else restored.topology
        assert topology.atoms["atom_id"].tolist() == ["0", "1", "2", "3"]
        assert topology.atoms["atom_name"].tolist() == ["N", "CA", "O", "H"]
        if kind != "TopologyDict":
            np.testing.assert_array_equal(
                puw.get_value(restored.structures.get_coordinates(), to_unit="nm"),
                np.arange(36.0).reshape(3, 4, 3),
            )


def test_copy_preserves_json_serialization_of_a_json_payload():
    payload = ViewerJSON(
        data={
            "version": "0.1",
            "atoms": {"atom_id": ["0"]},
            "bonds": {"atom_pairs": []},
            "structures": [{"coordinates": [[0.0, 1.0, 2.0]]}],
        }
    )
    duplicate = payload.copy()
    assert json.loads(duplicate.dumps()) == payload.data
    duplicate.data["atoms"]["atom_id"][0] = "different"
    assert payload.data["atoms"]["atom_id"] == ["0"]
