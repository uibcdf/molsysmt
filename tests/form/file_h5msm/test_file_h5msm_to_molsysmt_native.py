"""Deterministic tests for file:h5msm conversions using MolSysBuilder fixtures."""

import molsysmt as msm


def test_file_h5msm_to_molsysmt_topology_preserves_builder_counts(builder_h5msm_file):
    topology = msm.convert(builder_h5msm_file, to_form='molsysmt.Topology')

    assert topology.n_atoms == 4
    assert topology.n_groups == 2
    assert topology.n_bonds == 2
    assert topology.n_chains == 1
    assert topology.n_molecules == 2
    assert topology.n_entities == 2


def test_file_h5msm_to_molsysmt_molsys_preserves_builder_names(builder_h5msm_file):
    molsys = msm.convert(builder_h5msm_file, to_form='molsysmt.MolSys')

    assert molsys.topology.atoms['atom_name'].to_list() == ['N', 'CA', 'C', 'O']
    assert molsys.topology.groups['group_name'].to_list() == ['ALA', 'HOH']
    assert molsys.topology.chains['chain_id'].to_list() == ['A']
    assert molsys.topology.molecules['molecule_name'].to_list() == ['protein 0', 'water']
    assert molsys.topology.entities['entity_name'].to_list() == ['protein 0', 'water']


def test_file_h5msm_to_molsysmt_molsys_preserves_builder_structure_metadata(builder_h5msm_file):
    molsys = msm.convert(builder_h5msm_file, to_form='molsysmt.MolSys')

    time = msm.get(molsys, time=True)
    structure_id = msm.get(molsys, structure_id=True)

    assert msm.pyunitwizard.get_value(time).tolist() == [0.0]
    assert structure_id == ['0']
