"""Check a state-only native owner rebuilt from modular H5MSM 0.5."""

import pickle

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form._h5msm05_modular import (
    read_state_only_molsys_file,
    write_modular_file,
)
from molsysmt.native import MolSys, Structures, Topology


@pytest.mark.parametrize("n_states", [0, 1, 2])
def test_state_only_molsys_preserves_absent_topology(tmp_path, n_states):
    states = msm.ChemicalStates(n_atoms=3)
    for _ in range(n_states):
        states.append_state()
    filename = tmp_path / "state_only.h5msm"
    write_modular_file(filename, chemical_states=states)

    result = read_state_only_molsys_file(filename)
    assert result.topology is None
    assert result.structures is None
    assert result.get_n_atoms() == 3
    assert result.chemical_states.n_chemical_states == n_states
    assert result.to_form("molsysmt.ChemicalStates").n_atoms == 3

    assert result.get(n_atoms=True) == 3
    with pytest.raises(ValueError, match="requires a topology"):
        result.info()
    subset = result.extract(atom_indices=[2, 0])
    assert subset.topology is None
    assert subset.structures is None
    assert subset.get_n_atoms() == 2
    assert subset.chemical_states.n_chemical_states == n_states
    assert result.get_n_atoms() == 3
    with pytest.raises(ValueError, match="declared structure-index domain"):
        result.extract(structure_indices=[0])

    for clone in (result.copy(), pickle.loads(pickle.dumps(result))):
        assert clone.topology is None
        assert clone.structures is None
        assert clone.chemical_states.n_chemical_states == n_states
        assert clone.chemical_states is not result.chemical_states


def test_state_only_reader_rejects_a_present_topology(tmp_path):
    filename = tmp_path / "complete.h5msm"
    write_modular_file(
        filename,
        topology=Topology(n_atoms=2),
        chemical_states=msm.ChemicalStates(n_atoms=2),
    )
    with pytest.raises(ValueError, match="cannot contain other"):
        read_state_only_molsys_file(filename)


def test_state_only_reader_preserves_covalent_records(tmp_path):
    topology = Topology(n_atoms=3)
    topology.add_bonds([[0, 1]])
    states = msm.convert(topology, to_form="molsysmt.ChemicalStates")
    filename = tmp_path / "state_bonds.h5msm"
    write_modular_file(filename, chemical_states=states)

    result = read_state_only_molsys_file(filename)
    assert result.topology is None
    bond_indices = result.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist()
    assert bond_indices == [[0, 1]]
    subset = result.extract(atom_indices=[1, 0])
    assert subset.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1]]
    assert result.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1]]


def test_partial_constructor_rejects_mismatched_atom_axes():
    states = msm.ChemicalStates(n_atoms=3)
    with pytest.raises(ValueError, match="share an atom domain"):
        MolSys._from_partial_domains(
            chemical_states=states, topology=Topology(n_atoms=2)
        )

    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
    )
    with pytest.raises(ValueError, match="share an atom domain"):
        MolSys._from_partial_domains(
            chemical_states=states, structures=structures
        )
