import molsysmt as msm


def test_topology_to_topology_dict_and_back(builder_pdb_molsys):
    topology = builder_pdb_molsys.topology

    topology_dict = msm.convert(topology, to_form='molsysmt.TopologyDict')

    assert msm.get(topology_dict, element='system', n_atoms=True) == 4
    assert msm.get(topology_dict, element='atom', atom_name=True) == ['N', 'CA', 'C', 'O']
    assert msm.get(topology_dict, element='group', group_name=True) == ['ALA', 'HOH']
    assert msm.get(topology_dict, element='chain', chain_id=True) == ['A']

    rebuilt = msm.convert(topology_dict, to_form='molsysmt.Topology')

    assert rebuilt.n_atoms == topology.n_atoms
    assert rebuilt.n_groups == topology.n_groups
    assert rebuilt.n_bonds == topology.n_bonds
    assert rebuilt.n_chains == topology.n_chains
    assert rebuilt.n_molecules == topology.n_molecules
    assert rebuilt.n_entities == topology.n_entities
    assert rebuilt.atoms['atom_name'].tolist() == topology.atoms['atom_name'].tolist()
    assert rebuilt.groups['group_name'].tolist() == topology.groups['group_name'].tolist()
    assert rebuilt.chains['chain_id'].tolist() == topology.chains['chain_id'].tolist()


def test_topology_dict_info(builder_pdb_molsys):
    topology_dict = msm.convert(builder_pdb_molsys.topology, to_form='molsysmt.TopologyDict')
    assert msm.info(topology_dict).data.loc[0, 'form'] == 'molsysmt.TopologyDict'
