"""Probe complete MolSys persistence through the private H5MSM 0.5 codec."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form._h5msm05_modular import (
    read_complete_molsys_file,
    read_modular_file,
    write_complete_molsys_file,
    write_modular_file,
)
from molsysmt.native import MolSys, Structures


def _system():
    system = MolSys(n_atoms=3)
    system.topology.add_bonds([[0, 1]])
    system.chemical_states.append_state()
    system.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm")
    )
    system._set_structure_chemical_state_indices([0, 1])
    system.interactions = {
        "hbonds": msm.Interactions.from_records(
            [{
                "structure_index": 1,
                "interaction_type": "hbond",
                "participants": [
                    {"role": "donor", "atom_indices": [0]},
                    {"role": "hydrogen", "atom_indices": [1]},
                    {"role": "acceptor", "atom_indices": [2]},
                ],
            }],
            n_atoms=3, n_structures=2,
            evaluated_structure_indices=[0, 1], method="candidate",
        )
    }
    return system


def test_complete_molsys_roundtrip_preserves_one_chemical_authority(tmp_path):
    filename = tmp_path / "complete.h5msm"
    write_complete_molsys_file(filename, _system())
    restored = read_complete_molsys_file(filename)

    assert restored.chemical_states is restored.topology._chemical_states_domain
    assert restored.chemical_states.n_chemical_states == 2
    assert len(restored.chemical_states.get_bonds(0)) == 1
    assert restored.structures.coordinates.shape == (2, 3, 3)
    assert restored._get_structure_chemical_state_indices().tolist() == [0, 1]
    result = restored.interactions["hbonds"]
    assert result.query(structure_indices=[0]).n_interactions == 0
    assert result.query(structure_indices=[1]).n_interactions == 1
    assert restored.copy().interactions["hbonds"].n_interactions == 1


def test_writer_rejects_unrepresented_mechanics_before_creating_file(tmp_path):
    system = _system()
    system.molecular_mechanics.forcefield = "example"
    filename = tmp_path / "unsupported_mechanics.h5msm"
    with pytest.raises(ValueError, match="molecular mechanics"):
        write_complete_molsys_file(filename, system)
    assert not filename.exists()


def test_complete_molsys_reader_rejects_undeclared_shared_axes(tmp_path):
    system = _system()
    filename = tmp_path / "unlinked_complete.h5msm"
    write_modular_file(
        filename, topology=system.topology, chemical_states=system.chemical_states,
        structures=system.structures, interactions=dict(system.interactions),
    )
    with pytest.raises(ValueError, match="explicit atom-axis associations"):
        read_complete_molsys_file(filename)


def test_complete_molsys_reader_rejects_a_reordered_atom_axis(tmp_path):
    system = _system()
    filename = tmp_path / "reordered_axis.h5msm"
    write_modular_file(
        filename, topology=system.topology, chemical_states=system.chemical_states,
        structures=system.structures, interactions=dict(system.interactions),
        associations=[
            {
                "axis": "atom", "source": "chemical_states", "target": "topology",
                "source_name": None, "target_name": None, "indices": [2, 0, 1],
            },
            {
                "axis": "atom", "source": "structures", "target": "topology",
                "source_name": None, "target_name": None, "indices": "identity",
            },
            {
                "axis": "atom", "source": "interactions", "target": "topology",
                "source_name": "hbonds", "target_name": None, "indices": "identity",
            },
            {
                "axis": "structure", "source": "interactions", "target": "structures",
                "source_name": "hbonds", "target_name": None, "indices": "identity",
            },
        ],
    )
    with pytest.raises(ValueError, match="identity links"):
        read_complete_molsys_file(filename)


def test_selective_layer_read_does_not_load_omitted_topology(tmp_path):
    filename = tmp_path / "selective.h5msm"
    write_complete_molsys_file(filename, _system())
    with h5py.File(filename, "r+") as file:
        file["topology"].attrs["schema_version"] = 99

    selected = read_modular_file(filename, layers=("interactions", "associations"))
    assert set(selected) == {"interactions", "associations"}
    assert selected["interactions"]["hbonds"].n_interactions == 1
    assert selected["associations"] is not None
    assert list(read_modular_file(
        filename, layers="interactions", analysis_names="hbonds"
    )["interactions"]) == ["hbonds"]
    with pytest.raises(KeyError, match="missing"):
        read_modular_file(filename, layers="interactions", analysis_names="missing")
    with pytest.raises(ValueError, match="topology layer schema"):
        read_modular_file(filename)
