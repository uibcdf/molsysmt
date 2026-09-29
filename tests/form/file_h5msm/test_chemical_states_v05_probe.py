"""Probe the independent chemical-state layer proposed for H5MSM 0.5."""

import h5py
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.form._h5msm_chemical_states import (
    read_independent_chemical_states,
    write_independent_chemical_states,
)
from molsysmt.interactions._hdf5_collection import (
    read_named_analyses,
    write_named_analyses,
)
from molsysmt.native import ChemicalStates, Topology


def test_chemical_state_only_layer_roundtrips_without_topology(tmp_path):
    topology = Topology(n_atoms=3)
    topology._reference_chemical_state.state_id = "reactant"
    topology._reference_chemical_state.atom_attributes["formal_charge"] = pd.Series(
        pd.array([0, pd.NA, -1], dtype="Int16")
    )
    topology._append_chemical_state_bonds(
        [[0, 1]], bond_order=[1], evidence=["explicit"]
    )
    second = topology._append_chemical_state(state_id="product")
    topology._set_chemical_state_atom_attribute(
        "formal_charge", [1, 0, -1], state_index=second
    )
    states = msm.convert(topology, to_form="molsysmt.ChemicalStates")
    states._set_reference_index(None)
    filename = tmp_path / "chemical_states_only.h5msm"

    with h5py.File(filename, "w") as file:
        file.attrs["type"] = "h5msm"
        file.attrs["version"] = "0.5"
        write_independent_chemical_states(file, states)
        assert set(file.keys()) == {"chemical_states"}

    with h5py.File(filename, "r") as file:
        observed = read_independent_chemical_states(file)

    assert observed.n_atoms == 3
    assert observed.n_chemical_states == 2
    assert observed.reference_chemical_state_index is None
    assert observed._states[0].state_id == "reactant"
    assert observed._states[1].state_id == "product"
    assert observed._states[0].atom_attributes.equals(
        states._states[0].atom_attributes
    )
    assert observed._states[0].bonds.equals(states._states[0].bonds)


def test_absent_and_present_empty_chemical_state_layers_are_distinct(tmp_path):
    filename = tmp_path / "empty_chemical_states.h5msm"
    with h5py.File(filename, "w") as file:
        assert read_independent_chemical_states(file) is None
        write_independent_chemical_states(file, ChemicalStates(n_atoms=4))
        with pytest.raises(ValueError, match="already exists"):
            write_independent_chemical_states(file, ChemicalStates(n_atoms=4))
        observed = read_independent_chemical_states(file)

    assert observed.n_atoms == 4
    assert observed.n_chemical_states == 0
    assert observed.reference_chemical_state_index is None


def test_unknown_chemical_state_layer_schema_is_rejected(tmp_path):
    filename = tmp_path / "unknown_chemical_states.h5msm"
    with h5py.File(filename, "w") as file:
        write_independent_chemical_states(file, ChemicalStates(n_atoms=2))
        file["chemical_states"].attrs["schema_version"] = 99
        with pytest.raises(ValueError, match="chemical-state layer schema"):
            read_independent_chemical_states(file)


def test_chemical_states_and_interactions_are_independent_siblings(tmp_path):
    filename = tmp_path / "chemical_states_and_interactions.h5msm"
    states = ChemicalStates(n_atoms=2)
    states.append_state()
    interactions = msm.Interactions.from_records(
        [], n_atoms=2, n_structures=1, evaluated_structure_indices=[0],
        method="candidate",
    )

    with h5py.File(filename, "w") as file:
        file.attrs["type"] = "h5msm"
        file.attrs["version"] = "0.5"
        write_independent_chemical_states(file, states)
        write_named_analyses(file.create_group("interactions"), {"hbonds": interactions})
        assert set(file) == {"chemical_states", "interactions"}

    with h5py.File(filename, "r") as file:
        assert read_independent_chemical_states(file).n_chemical_states == 1
        result = read_named_analyses(file["interactions"])["hbonds"]
        assert result.n_atoms == 2
        assert result.n_interactions == 0
        assert result.evaluated_structure_indices.tolist() == [0]
