import numpy as np
import pytest

from molsysmt.native import MolSys, ViewerJSON
from molsysmt import pyunitwizard as puw
from molsysmt.form.molsysmt_MolSys import to_molsysmt_ViewerJSON


def _build_minimal_molsys():
    molsys = MolSys(
        n_atoms=2,
        n_groups=1,
        n_components=1,
        n_molecules=1,
        n_entities=1,
        n_chains=1,
        n_bonds=1,
    )

    topo = molsys.topology
    topo.atoms.loc[:, "atom_id"] = ["0", "1"]
    topo.atoms.loc[:, "atom_name"] = ["A", "B"]
    topo.atoms.loc[:, "group_index"] = [0, 0]
    topo.atoms.loc[:, "component_index"] = [0, 0]
    topo.atoms.loc[:, "chain_index"] = [0, 0]

    topo.groups.loc[:, "group_id"] = ["10"]
    topo.groups.loc[:, "group_name"] = ["GRP"]
    topo.groups.loc[:, "group_type"] = ["type"]
    topo.groups.loc[:, "molecule_index"] = [0]

    topo.chains.loc[:, "chain_id"] = ["1"]
    topo.chains.loc[:, "chain_name"] = ["A"]
    topo.chains.loc[:, "chain_type"] = ["polymer"]

    topo.molecules.loc[:, "molecule_id"] = ["100"]
    topo.molecules.loc[:, "molecule_name"] = ["Mol"]
    topo.molecules.loc[:, "molecule_type"] = ["protein"]
    topo.molecules.loc[:, "entity_index"] = [0]

    topo.entities.loc[:, "entity_id"] = ["1000"]
    topo.entities.loc[:, "entity_name"] = ["Ent"]
    topo.entities.loc[:, "entity_type"] = ["polymer"]

    topo.bonds.loc[0, "atom1_index"] = 0
    topo.bonds.loc[0, "atom2_index"] = 1
    topo.bonds.loc[0, "order"] = "1"

    coords = puw.quantity(np.array([[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]]), "nanometer")
    times = puw.quantity(np.array([0.0]), "picosecond")
    box = puw.quantity(np.array([np.eye(3)]), "nanometer")

    molsys.structures.coordinates = coords
    molsys.structures.time = times
    molsys.structures.box = box

    return molsys


def test_molsys_to_ViewerJSON():
    molsys = _build_minimal_molsys()
    viewer = to_molsysmt_ViewerJSON(molsys)

    assert isinstance(viewer, ViewerJSON)
    data = viewer.data
    assert data["atoms"]["atom_id"] == ["0", "1"]
    assert data["atoms"]["atom_name"] == ["A", "B"]
    assert data["atoms"]["group_id"] == ["10", "10"]
    assert len(data["structures"]) == 1
    assert np.allclose(np.array(data["structures"][0]["coordinates"]), [[0, 0, 0], [1, 0, 0]])
