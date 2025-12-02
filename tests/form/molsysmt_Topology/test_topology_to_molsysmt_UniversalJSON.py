import numpy as np

from molsysmt.native import MolSys, UniversalJSON
from molsysmt.form.molsysmt_Topology import to_molsysmt_UniversalJSON


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

    return topo


def test_topology_to_UniversalJSON():
    topo = _minimal_topology()
    ujson = to_molsysmt_UniversalJSON(topo)

    assert isinstance(ujson, UniversalJSON)
    atoms = ujson.data["topology"]["atoms"]
    assert atoms["atom_id"] == ["0", "1"]
    assert atoms["group_id"] == ["10", "10"]
    assert ujson.data["coordinates"]["collections"][0]["structures"] == []
