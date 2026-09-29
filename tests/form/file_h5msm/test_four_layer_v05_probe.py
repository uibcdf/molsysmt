"""Exercise four independent H5MSM 0.5 layer codecs in one probe file."""

import h5py
import numpy as np

import molsysmt as msm
from molsysmt.form._h5msm05_structures import (
    read_independent_structures,
    write_independent_structures,
)
from molsysmt.form._h5msm05_topology import (
    read_independent_topology,
    write_independent_topology,
)
from molsysmt.form._h5msm_chemical_states import (
    read_independent_chemical_states,
    write_independent_chemical_states,
)
from molsysmt.interactions._hdf5_collection import (
    read_named_analyses,
    write_named_analyses,
)
from molsysmt.native import Structures, Topology


def test_four_layer_file_keeps_chemistry_and_observations_separate(tmp_path):
    topology = Topology(n_atoms=3)
    topology.add_bonds([[0, 1]])
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm")
    )
    hbonds = msm.Interactions.from_records(
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
    filename = tmp_path / "four_layers.h5msm"

    with h5py.File(filename, "w") as file:
        file.attrs["type"] = "h5msm"
        file.attrs["version"] = "0.5"
        write_independent_topology(file, topology)
        write_independent_chemical_states(
            file, msm.convert(topology, to_form="molsysmt.ChemicalStates")
        )
        write_independent_structures(file, structures)
        write_named_analyses(file.create_group("interactions"), {"hbonds": hbonds})
        assert set(file) == {
            "topology", "chemical_states", "structures", "interactions"
        }
        assert "bonds" not in file["topology"]

    with h5py.File(filename, "r") as file:
        stable = read_independent_topology(file)
        states = read_independent_chemical_states(file)
        frames = read_independent_structures(file, structure_indices=[1, 0])
        interactions = read_named_analyses(file["interactions"])["hbonds"]

    assert stable._chemical_states == []
    assert len(states.get_bonds()) == 1
    assert frames.coordinates.shape == (2, 3, 3)
    assert interactions.query(structure_indices=[0]).n_interactions == 0
    assert interactions.query(structure_indices=[1]).n_interactions == 1
