"""Probe native 0.5 persistence with chemistry and frames but no topology."""

import pickle

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form._h5msm05_modular import (
    read_topology_free_molsys_file,
    write_modular_file,
    write_topology_free_molsys_file,
)
from molsysmt.native import MolSys, Structures, Topology


def _link(indices):
    return {
        "axis": "atom", "source": "structures", "target": "chemical_states",
        "source_name": None, "target_name": None, "indices": indices,
    }


def _system():
    topology = Topology(n_atoms=3)
    topology.add_bonds([[0, 1]])
    states = msm.convert(topology, to_form="molsysmt.ChemicalStates")
    states.append_state()
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm")
    )
    analysis = msm.Interactions.from_records(
        [{
            "structure_index": 1,
            "interaction_type": "hbond",
            "participants": [
                {"role": "donor", "atom_indices": [0]},
                {"role": "hydrogen", "atom_indices": [1]},
                {"role": "acceptor", "atom_indices": [2]},
            ],
        }],
        n_atoms=3, n_structures=2, evaluated_structure_indices=[0, 1],
        method="candidate",
    )
    result = MolSys._from_partial_domains(
        chemical_states=states, structures=structures,
        interactions={"hbonds": analysis},
    )
    result._set_structure_chemical_state_indices([0, 1])
    return result


def test_topology_free_roundtrip_keeps_axes_and_state_assignments(tmp_path):
    filename = tmp_path / "topology_free.h5msm"
    write_topology_free_molsys_file(filename, _system())
    with h5py.File(filename, "r") as file:
        assert "topology" not in file
        assert set(file) == {
            "chemical_states", "structures", "interactions", "associations"
        }

    restored = read_topology_free_molsys_file(filename)
    assert restored.topology is None
    assert restored.structures.coordinates.shape == (2, 3, 3)
    assert restored.chemical_states.n_chemical_states == 2
    assert len(restored.chemical_states.get_bonds(0)) == 1
    assert restored._get_structure_chemical_state_indices().tolist() == [0, 1]
    assert restored.interactions["hbonds"].query(
        structure_indices=[0]
    ).n_interactions == 0
    assert restored.interactions["hbonds"].query(
        structure_indices=[1]
    ).n_interactions == 1

    selected = restored.extract(
        atom_indices=[2, 0, 1], structure_indices=[1, 0]
    )
    assert selected.topology is None
    assert selected.structures.coordinates.shape == (2, 3, 3)
    assert selected._get_structure_chemical_state_indices().tolist() == [1, 0]
    assert selected.chemical_states.get_bonds(0)[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[1, 2]]
    np.testing.assert_array_equal(
        selected.interactions["hbonds"].atom_source_indices, [2, 0, 1]
    )
    np.testing.assert_array_equal(
        selected.interactions["hbonds"].structure_source_indices, [1, 0]
    )
    assert selected.interactions["hbonds"].query(
        structure_indices=[0]
    ).n_interactions == 1

    for clone in (restored.copy(), pickle.loads(pickle.dumps(restored))):
        assert clone.topology is None
        assert clone.structures.coordinates.shape == (2, 3, 3)
        assert clone._get_structure_chemical_state_indices().tolist() == [0, 1]
        assert clone.interactions["hbonds"].n_interactions == 1


def test_chemical_states_and_interactions_define_axes_without_structures(tmp_path):
    source = _system()
    partial = MolSys._from_partial_domains(
        chemical_states=source.chemical_states.copy(),
        interactions={"hbonds": source.interactions["hbonds"].remap()},
    )
    filename = str(tmp_path / "states_and_interactions.h5msm")
    msm.h5msm.write(partial, filename)
    restored = msm.h5msm.read(filename)
    assert restored.topology is None
    assert restored.structures is None
    assert restored.get_n_atoms() == 3
    assert msm.get(restored, n_structures=True) == 2
    selected = restored.extract(atom_indices=[2, 0, 1], structure_indices=[1, 0])
    assert selected.chemical_states.n_atoms == 3
    assert selected.interactions["hbonds"].n_structures == 2
    assert selected.interactions["hbonds"].query(structure_indices=[0]).n_interactions == 1


@pytest.mark.parametrize("indices", [None, [1, 0, 2]])
def test_topology_free_reader_rejects_missing_or_reordered_atom_link(
    tmp_path, indices
):
    system = _system()
    filename = tmp_path / "unrepresentable.h5msm"
    write_modular_file(
        filename, chemical_states=system.chemical_states,
        structures=system.structures,
        associations=None if indices is None else [_link(indices)],
    )
    with pytest.raises(ValueError, match="declared identity links"):
        read_topology_free_molsys_file(filename)


def test_frame_only_structures_do_not_invent_an_atom_axis(tmp_path):
    states = msm.ChemicalStates(n_atoms=3)
    frames = Structures(time=msm.pyunitwizard.quantity([0.0, 1.0], "ps"))
    system = MolSys._from_partial_domains(
        chemical_states=states, structures=frames
    )
    filename = tmp_path / "time_only.h5msm"
    write_topology_free_molsys_file(filename, system)

    with h5py.File(filename, "r") as file:
        assert "associations" not in file
    restored = read_topology_free_molsys_file(filename)
    assert restored.topology is None
    assert restored.get_n_atoms() == 3
    assert restored.structures.n_structures == 2
    assert restored.structures.n_atoms == 0


def test_present_empty_interactions_cannot_be_hidden_in_native_mapping(tmp_path):
    system = _system()
    filename = tmp_path / "empty_analysis_layer.h5msm"
    write_modular_file(
        filename, chemical_states=system.chemical_states,
        structures=system.structures, interactions={},
        associations=[_link("identity")],
    )
    with pytest.raises(ValueError, match="present-empty interaction layer"):
        read_topology_free_molsys_file(filename)


def test_replacing_chemistry_cannot_break_structural_atom_alignment():
    system = _system()
    original = system.chemical_states
    with pytest.raises(msm.StructuralInconsistencyError, match="share an atom-index domain"):
        system.chemical_states = msm.ChemicalStates(n_atoms=2)
    assert system.chemical_states is original


def test_writer_rejects_unrepresented_mechanics_before_file_creation(tmp_path):
    system = _system()
    system.molecular_mechanics.forcefield = "example"
    filename = tmp_path / "unsupported_mechanics.h5msm"
    with pytest.raises(ValueError, match="molecular mechanics"):
        write_topology_free_molsys_file(filename, system)
    assert not filename.exists()
