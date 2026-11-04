"""Transporting naming metadata with explicit schema identities and rejection."""

import copy
import json

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, TopologyDict
from tests.native.test_group_naming_schemes import topology_with_schemes


@pytest.mark.parametrize("atoms", [False, True])
@pytest.mark.parametrize("enclosing", [False, True])
def test_dictionary_json_round_trip_preserves_mixed_declarations(atoms, enclosing):
    topology = topology_with_schemes(atoms=atoms)
    source = MolSys._from_partial_domains(topology=topology) if enclosing else topology
    target = "molsysmt.MolSysDict" if enclosing else "molsysmt.TopologyDict"
    wire = msm.convert(source, to_form=target)
    data = json.loads(json.dumps(wire.data, allow_nan=False))
    record = data["topology"] if enclosing else data
    assert record["version"] == "0.3"
    assert record["group_naming_schemes"]["codes"] == [1, 0, 2]
    assert record["group_naming_schemes"]["profiles"] == [
        {"name": "amber", "version": 1},
        {"name": "ccd", "version": 1},
        {"name": "legacy", "version": 1},
    ]
    result = msm.convert(
        type(wire)(data),
        to_form="molsysmt.MolSys" if enclosing else "molsysmt.Topology",
    )
    restored = result.topology if enclosing else result
    assert restored.group_naming_schemes == ("amber", None, "ccd")
    assert restored.groups.group_name.tolist() == ["HIP", "CYX", "GLH"]
    if enclosing:
        assert result.chemical_states is result.structures is None


@pytest.mark.parametrize("atoms", [False, True])
@pytest.mark.parametrize("enclosing", [False, True])
def test_public_h5msm_round_trip_uses_layer_four_without_root_bump(
    tmp_path, atoms, enclosing
):
    topology = topology_with_schemes(atoms=atoms)
    source = MolSys._from_partial_domains(topology=topology) if enclosing else topology
    filename = str(tmp_path / "naming.h5msm")
    msm.convert(source, to_form="file:h5msm", output_filename=filename)
    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.5"
        assert file["topology"].attrs["schema_version"] == 4
        assert file["topology/group_naming_schemes/codes"].dtype == np.dtype("uint8")
        assert file["topology/group_naming_schemes/codes"].shape == (3,)
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    assert restored.topology.group_naming_schemes == ("amber", None, "ccd")
    assert restored.topology.groups.group_name.tolist() == ["HIP", "CYX", "GLH"]
    assert restored.chemical_states is None
    if enclosing:
        assert restored.structures is None
    else:
        # Topology-to-file uses the existing MolSys projection with empty Structures.
        assert restored.structures.coordinates is None
        assert restored.structures.n_structures == 0


@pytest.mark.parametrize(
    "damage",
    [
        "registry",
        "version",
        "boolean_version",
        "code",
        "boolean_code",
        "count",
        "matrix",
        "extra",
        "old_schema",
    ],
)
def test_dictionary_invalid_metadata_fails_instead_of_becoming_unknown(damage):
    wire = msm.convert(topology_with_schemes(), to_form="molsysmt.TopologyDict")
    data = copy.deepcopy(wire.data)
    naming = data["group_naming_schemes"]
    if damage == "registry":
        naming["profiles"][0]["name"] = "different"
    elif damage == "version":
        naming["profiles"][0]["version"] = 2
    elif damage == "boolean_version":
        naming["profiles"][0]["version"] = True
    elif damage == "code":
        naming["codes"][0] = 4
    elif damage == "boolean_code":
        naming["codes"][0] = True
    elif damage == "count":
        naming["codes"].pop()
    elif damage == "matrix":
        naming["codes"] = [[1, 0, 2]]
    elif damage == "extra":
        naming["unused"] = "must not disappear"
    else:
        data["version"] = "0.2"
    with pytest.raises(ValueError, match="naming|TopologyDict"):
        msm.convert(TopologyDict(data), to_form="molsysmt.Topology")


@pytest.mark.parametrize(
    "damage", ["version", "profiles", "length", "dtype", "codes", "extra", "old_schema"]
)
def test_h5msm_rejects_invalid_naming_payload(tmp_path, damage):
    filename = str(tmp_path / "bad_naming.h5msm")
    msm.h5msm.write(
        MolSys._from_partial_domains(topology=topology_with_schemes()), filename
    )
    with h5py.File(filename, "r+") as file:
        declared = file["topology/group_naming_schemes"]
        if damage == "version":
            declared.attrs["schema_version"] = 2
        elif damage == "profiles":
            declared.attrs["profiles"] = "[]"
        elif damage in {"length", "dtype", "codes"}:
            del declared["codes"]
            values = (
                [1, 0]
                if damage == "length"
                else [1, 0, 4]
                if damage == "codes"
                else [1, 0, 2]
            )
            declared.create_dataset(
                "codes", data=values, dtype="i8" if damage == "dtype" else "u1"
            )
        elif damage == "extra":
            declared.attrs["ignored"] = "must not disappear"
        else:
            file["topology"].attrs["schema_version"] = 1
    with pytest.raises(ValueError, match="naming|topology layer"):
        msm.h5msm.read_layers(filename, layers=["topology"])


@pytest.mark.parametrize("chain_groups", [False, True])
@pytest.mark.parametrize("atom_molecules", [False, True])
def test_layer_four_preserves_independent_membership_relations(
    tmp_path, chain_groups, atom_molecules
):
    topology = topology_with_schemes()
    if atom_molecules:
        topology.atoms.loc[3, "group_index"] = None
        topology.set_atom_molecules([0], atom_indices=[3])
    if chain_groups:
        topology.set_chain_groups([[2, 0, 1]])
    filename = str(tmp_path / "relations.h5msm")
    msm.h5msm.write_layers(filename, topology=topology)
    restored = msm.h5msm.read_layers(filename, layers=["topology"])["topology"]
    assert restored.group_naming_schemes == ("amber", None, "ccd")
    assert restored.get(element="atom", molecule_index=True) == [0, 0, 0, 0]
    if chain_groups:
        assert restored.chain_groups == ((2, 0, 1),)


def test_old_schema_retains_unknown_and_new_dictionary_can_be_extracted(tmp_path):
    source = topology_with_schemes()
    wire = msm.convert(source, to_form="molsysmt.TopologyDict")
    extracted = msm.extract(wire, selection=[0, 3])
    assert msm.convert(extracted, to_form="molsysmt.Topology").group_naming_schemes == (
        "ccd",
        None,
    )
    source.set_group_naming_schemes(None)
    old = msm.convert(source, to_form="molsysmt.TopologyDict")
    assert old.data["version"] == "0.2"
    assert "group_naming_schemes" not in old.data
    assert (
        msm.convert(old, to_form="molsysmt.Topology").group_naming_schemes
        == (None,) * 3
    )
    filename = str(tmp_path / "unknown.h5msm")
    msm.h5msm.write(MolSys._from_partial_domains(topology=source), filename)
    with h5py.File(filename, "r") as file:
        assert file["topology"].attrs["schema_version"] == 1
    assert (
        msm.h5msm.read_layers(filename, layers=["topology"])[
            "topology"
        ].group_naming_schemes
        == (None,) * 3
    )
