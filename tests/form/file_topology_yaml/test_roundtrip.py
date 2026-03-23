import molsysmt as msm


def test_topology_yaml_roundtrip(builder_pdb_molsys, tmp_path):
    topology = builder_pdb_molsys.topology
    output = tmp_path / 'fixture.yaml'

    msm.convert(topology, to_form='file:topology_yaml', output_filename=str(output))

    assert msm.get_form(str(output)) == 'file:topology_yaml'

    topology_dict = msm.convert(str(output), to_form='molsysmt.TopologyDict')
    rebuilt = msm.convert(str(output), to_form='molsysmt.Topology')

    assert msm.get(topology_dict, element='atom', atom_name=True) == ['N', 'CA', 'C', 'O']
    assert rebuilt.n_atoms == topology.n_atoms
    assert rebuilt.n_bonds == topology.n_bonds
    assert rebuilt.groups['group_name'].tolist() == topology.groups['group_name'].tolist()
    assert rebuilt.chains['chain_id'].tolist() == topology.chains['chain_id'].tolist()


def test_topology_yaml_info(builder_pdb_molsys, tmp_path):
    output = tmp_path / 'fixture.yaml'
    msm.convert(builder_pdb_molsys.topology, to_form='file:topology_yaml', output_filename=str(output))
    assert msm.info(str(output)).data.loc[0, 'form'] == 'file:topology_yaml'
