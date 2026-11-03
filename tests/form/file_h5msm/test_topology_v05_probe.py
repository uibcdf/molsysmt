"""Probe a stable topology independent of chemical states in H5MSM 0.5."""

import h5py
import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.form._h5msm05_topology import (
    read_independent_topology,
    write_independent_topology,
)
from molsysmt.form._h5msm_chemical_states import (
    read_independent_chemical_states,
    write_independent_chemical_states,
)
from molsysmt.native import Topology


def _topology():
    topology = Topology(n_atoms=3, n_groups=1, n_molecules=1, n_entities=1, n_chains=1)
    topology.atoms["atom_id"] = pd.array(["7", "8", "9"], dtype="string")
    topology.atoms["atom_name"] = ["C", "N", "O"]
    topology.atoms["isotope"] = pd.array([13, pd.NA, 18], dtype="UInt16")
    topology.atoms["group_index"] = pd.array([0, 0, 0], dtype="Int64")
    topology.atoms["chain_index"] = pd.array([0, 0, 0], dtype="Int64")
    topology.groups["group_id"] = pd.array(["g1"], dtype="string")
    topology.groups["molecule_index"] = pd.array([0], dtype="Int64")
    topology.molecules["molecule_id"] = pd.array(["m1"], dtype="string")
    topology.molecules["entity_index"] = pd.array([0], dtype="Int64")
    topology.entities["entity_id"] = pd.array(["e1"], dtype="string")
    topology.chains["chain_id"] = pd.array(["c1"], dtype="string")
    return topology


def test_topology_only_has_no_chemical_state_or_covalent_records(tmp_path):
    filename = tmp_path / "topology_only.h5msm"
    source = _topology()
    states = msm.ChemicalStates(n_atoms=3)
    states.append_state()
    states.add_bonds([[0, 1]])
    with h5py.File(filename, "w") as file:
        file.attrs["type"] = "h5msm"
        file.attrs["version"] = "0.5"
        assert read_independent_topology(file) is None
        write_independent_topology(file, source)
        assert set(file) == {"topology"}
        assert set(file["topology"]) == {
            "atoms",
            "groups",
            "molecules",
            "entities",
            "chains",
        }

    with h5py.File(filename, "r") as file:
        observed = read_independent_topology(file)
    assert observed.n_atoms == 3
    assert not hasattr(observed, "bonds")
    for name in ("atoms", "groups", "molecules", "entities", "chains"):
        pd.testing.assert_frame_equal(getattr(observed, name), getattr(source, name))
    assert not hasattr(observed.copy(), "bonds")
    subset = observed.extract(atom_indices=[0, 2], skip_digestion=True)
    assert subset.atoms["atom_id"].tolist() == ["7", "9"]
    assert not hasattr(subset, "bonds")


def test_topology_and_chemical_states_are_independent_siblings(tmp_path):
    filename = tmp_path / "topology_and_states.h5msm"
    source = _topology()
    states = msm.ChemicalStates(n_atoms=3)
    states.append_state()
    states.add_bonds([[0, 1]])
    with h5py.File(filename, "w") as file:
        write_independent_topology(file, source)
        write_independent_chemical_states(file, states)
        assert set(file) == {"topology", "chemical_states"}
        assert "bonds" not in file["topology"]
        assert len(read_independent_chemical_states(file).get_bonds()) == 1
        assert not hasattr(read_independent_topology(file), "bonds")


def test_invalid_topology_schema_is_rejected(tmp_path):
    filename = tmp_path / "invalid_topology.h5msm"
    with h5py.File(filename, "w") as file:
        write_independent_topology(file, _topology())
        file["topology"].attrs["schema_version"] = 99
        with pytest.raises(ValueError, match="topology layer schema"):
            read_independent_topology(file)


@pytest.mark.parametrize("chain_groups", [False, True])
def test_atom_molecules_are_stored_without_chemical_states(tmp_path, chain_groups):
    topology = Topology(n_atoms=3, n_groups=1, n_molecules=2, n_chains=1)
    topology.atoms["group_index"] = pd.array([0, None, None], dtype="Int64")
    topology.groups["molecule_index"] = pd.array([1], dtype="Int64")
    topology.set_atom_molecules([1, 0, None])
    if chain_groups:
        topology.set_chain_groups([[0]])
    filename = str(tmp_path / "stable_molecules.h5msm")
    msm.h5msm.write_layers(filename, topology=topology)
    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.5"
        assert set(file) == {"topology"}
        assert file["topology"].attrs["schema_version"] == 3
        dataset = file["topology/atom_molecules"]
        assert dataset.dtype == np.dtype("int64")
        assert dataset.shape == (3,)
        np.testing.assert_array_equal(dataset[:], [-1, 0, -1])
    restored = msm.h5msm.read_layers(filename, layers=["topology"])["topology"]
    assert restored.get(element="atom", molecule_index=True) == [1, 0, None]
    assert not hasattr(restored, "bonds")
    if chain_groups:
        assert restored.chain_groups == ((0,),)


@pytest.mark.parametrize(
    "values,dtype",
    [
        ([0, 0], "i8"),
        ([0, 0, 0], "i4"),
        ([0, 0, 0], "u8"),
        ([0.0, 0.0, 0.0], "f8"),
        ([-2, 0, 0], "i8"),
        ([0, 2, 0], "i8"),
        ([0, 0, 0], "i8"),
    ],
)
def test_invalid_atom_molecule_payload_is_rejected(tmp_path, values, dtype):
    topology = _topology()
    filename = tmp_path / "invalid_atom_molecules.h5msm"
    with h5py.File(filename, "w") as file:
        write_independent_topology(file, topology)
        file["topology"].attrs["schema_version"] = 3
        file["topology"].create_dataset("atom_molecules", data=values, dtype=dtype)
        with pytest.raises(ValueError, match="atom/molecule membership"):
            read_independent_topology(file)


def test_topology_projection_never_reads_chemical_states(tmp_path, monkeypatch):
    from molsysmt.form import _h5msm05_modular
    from molsysmt.native import MolSys

    source = MolSys(n_atoms=3, n_molecules=2)
    source.topology.set_atom_molecules([1, None, 0])
    filename = str(tmp_path / "projected.h5msm")
    msm.h5msm.write(source, filename)

    def forbidden(*args, **kwargs):
        raise AssertionError("Topology projection must not read chemical states")

    monkeypatch.setattr(_h5msm05_modular, "read_independent_chemical_states", forbidden)
    restored = msm.h5msm.read_layers(filename, layers=["topology"])["topology"]
    assert restored.get(element="atom", molecule_index=True) == [1, None, 0]


def test_legacy_group_free_membership_is_migrated_only_on_joint_load(tmp_path):
    from molsysmt.native import MolSys

    source = MolSys(n_atoms=3, n_molecules=2)
    source.chemical_states.add_bonds([[0, 1]])
    source.topology.set_atom_molecules([0, 0, 1])
    filename = str(tmp_path / "legacy_topology_layer.h5msm")
    msm.h5msm.write(source, filename)
    # Reproduce the old layer, which encoded group-free ownership only through
    # the associated reference state's component partition.
    with h5py.File(filename, "r+") as file:
        del file["topology/atom_molecules"]
        file["topology"].attrs["schema_version"] = 1
    projected = msm.h5msm.read_layers(filename, layers=["topology"])["topology"]
    assert projected.get(element="atom", molecule_index=True) == [None] * 3
    complete = msm.h5msm.read(filename)
    assert complete.topology.get(element="atom", molecule_index=True) == [0, 0, 1]
    complete.chemical_states.remove_bonds([0])
    assert complete.topology.get(element="atom", molecule_index=True) == [0, 0, 1]


@pytest.mark.parametrize("clear_declaration", [False, True])
def test_unknown_molecules_are_not_reconstructed_as_legacy_components(
    tmp_path, clear_declaration
):
    from molsysmt.native import MolSys

    source = MolSys(n_atoms=3, n_molecules=2)
    source.chemical_states.add_bonds([[0, 1]])
    if clear_declaration:
        source.topology.set_atom_molecules([0, 0, 1])
        source.topology.set_atom_molecules(None)
    assert source.topology._atom_molecule_membership is None
    filename = str(tmp_path / "unknown_ownership.h5msm")
    msm.h5msm.write(source, filename)
    restored = msm.h5msm.read(filename)
    assert restored.topology.get(element="atom", molecule_index=True) == [None] * 3


def test_legacy_equal_axis_lengths_do_not_establish_molecule_correspondence(tmp_path):
    from molsysmt.native import MolSys

    source = MolSys(n_atoms=3, n_molecules=2)
    source.chemical_states.add_bonds([[0, 1]])
    source.topology.set_atom_molecules([0, 0, 1])
    filename = str(tmp_path / "independent_axes.h5msm")
    msm.h5msm.write_layers(
        filename, topology=source.topology, chemical_states=source.chemical_states
    )
    with h5py.File(filename, "r+") as file:
        del file["topology/atom_molecules"]
        file["topology"].attrs["schema_version"] = 1
    payload = msm.h5msm.read_layers(filename, layers=["topology", "chemical_states"])
    assert payload["topology"].get(element="atom", molecule_index=True) == [None] * 3
    assert payload["chemical_states"].n_atoms == 3
