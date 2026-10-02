"""Probe H5MSM 0.5 native topology and chemistry without structures."""

import pickle

import h5py
import pytest

import molsysmt as msm
from molsysmt.form._h5msm05_modular import (
    read_topology_chemistry_molsys_file,
    write_modular_file,
    write_topology_chemistry_molsys_file,
)
from molsysmt.native import MolSys, Topology


def _domains():
    topology = Topology(n_atoms=3)
    topology.add_bonds([[0, 1]])
    states = msm.convert(topology, to_form="molsysmt.ChemicalStates")
    return topology, states


def test_topology_and_chemistry_roundtrip_without_structures(tmp_path):
    topology, states = _domains()
    system = MolSys._from_partial_domains(topology=topology, chemical_states=states)
    filename = tmp_path / "topology_chemistry.h5msm"
    write_topology_chemistry_molsys_file(filename, system)
    with h5py.File(filename, "r") as file:
        assert set(file) == {"topology", "chemical_states", "associations"}
        assert "bonds" not in file["topology"]

    restored = read_topology_chemistry_molsys_file(filename)
    assert restored.structures is None
    assert restored.topology.n_atoms == 3
    assert restored.chemical_states is restored.topology._chemical_states_domain
    assert len(restored.chemical_states.get_bonds()) == 1
    assert msm.get(restored, n_atoms=True) == 3
    assert msm.get(restored, n_structures=True) is None

    for clone in (restored.copy(), pickle.loads(pickle.dumps(restored))):
        assert clone.structures is None
        assert clone.chemical_states is clone.topology._chemical_states_domain
        assert len(clone.chemical_states.get_bonds()) == 1


@pytest.mark.parametrize("indices", [None, [1, 0, 2]])
def test_reader_requires_one_identity_atom_link(tmp_path, indices):
    topology, states = _domains()
    filename = tmp_path / "unrepresentable.h5msm"
    associations = (
        None
        if indices is None
        else [
            {
                "axis": "atom",
                "source": "chemical_states",
                "target": "topology",
                "source_name": None,
                "target_name": None,
                "indices": indices,
            }
        ]
    )
    write_modular_file(
        filename,
        topology=topology,
        chemical_states=states,
        associations=associations,
    )
    with pytest.raises(ValueError, match="declared identity atom-axis link"):
        read_topology_chemistry_molsys_file(filename)
