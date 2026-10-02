"""Probe a stable topology independent of chemical states in H5MSM 0.5."""

import h5py
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
    topology.atoms["atom_id"] = ["7", "8", "9"]
    topology.atoms["atom_name"] = ["C", "N", "O"]
    topology.atoms["isotope"] = pd.array([13, pd.NA, 18], dtype="UInt16")
    topology.atoms["group_index"] = pd.array([0, 0, 0], dtype="Int64")
    topology.atoms["chain_index"] = pd.array([0, 0, 0], dtype="Int64")
    topology.groups["group_id"] = ["g1"]
    topology.groups["molecule_index"] = pd.array([0], dtype="Int64")
    topology.molecules["molecule_id"] = ["m1"]
    topology.molecules["entity_index"] = pd.array([0], dtype="Int64")
    topology.entities["entity_id"] = ["e1"]
    topology.chains["chain_id"] = ["c1"]
    return topology


def test_topology_only_has_no_chemical_state_or_covalent_records(tmp_path):
    filename = tmp_path / "topology_only.h5msm"
    source = _topology()
    source.add_bonds([[0, 1]])
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
    assert observed._chemical_states == []
    for name in ("atoms", "groups", "molecules", "entities", "chains"):
        pd.testing.assert_frame_equal(getattr(observed, name), getattr(source, name))
    assert observed.copy()._chemical_states == []
    subset = observed.extract(atom_indices=[0, 2], skip_digestion=True)
    assert subset.atoms["atom_id"].tolist() == ["7", "9"]
    assert subset._chemical_states == []


def test_topology_and_chemical_states_are_independent_siblings(tmp_path):
    filename = tmp_path / "topology_and_states.h5msm"
    source = _topology()
    source.add_bonds([[0, 1]])
    with h5py.File(filename, "w") as file:
        write_independent_topology(file, source)
        write_independent_chemical_states(
            file, msm.convert(source, to_form="molsysmt.ChemicalStates")
        )
        assert set(file) == {"topology", "chemical_states"}
        assert "bonds" not in file["topology"]
        assert len(read_independent_chemical_states(file).get_bonds()) == 1
        assert read_independent_topology(file)._chemical_states == []


def test_invalid_topology_schema_is_rejected(tmp_path):
    filename = tmp_path / "invalid_topology.h5msm"
    with h5py.File(filename, "w") as file:
        write_independent_topology(file, _topology())
        file["topology"].attrs["schema_version"] = 99
        with pytest.raises(ValueError, match="topology layer schema"):
            read_independent_topology(file)
