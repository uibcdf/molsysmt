import numpy as np

from molsysmt.native import MolSys, ViewerJSON
from molsysmt.form.molsysmt_Topology.to_molsysmt_ViewerJSON import to_molsysmt_ViewerJSON


def _minimal_topology():
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
    topo._set_component_indices([0, 0])
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
    topo.bonds.loc[0, "bond_order"] = 1

    return topo


def test_topology_to_ViewerJSON():
    topo = _minimal_topology()
    viewer = to_molsysmt_ViewerJSON(topo)

    assert isinstance(viewer, ViewerJSON)
    data = viewer.data
    assert data["atoms"]["group_id"] == ["10", "10"]
    assert data["atoms"]["chain_id"] == ["1", "1"]
    assert data["bonds"]["indexA"] == [0]
    assert data["bonds"]["indexB"] == [1]
    assert data["frames"] == []
