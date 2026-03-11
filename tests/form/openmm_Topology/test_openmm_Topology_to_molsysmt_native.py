"""Deterministic tests for openmm.Topology conversions using MolSysBuilder fixtures."""

import molsysmt as msm


def test_openmm_topology_to_molsysmt_topology_preserves_builder_counts(builder_openmm_topology):
    topology = msm.convert(builder_openmm_topology, to_form='molsysmt.Topology')

    assert topology.n_atoms == 4
    assert topology.n_groups == 2
    assert topology.n_bonds == 2
    assert topology.n_chains == 1
    assert topology.n_molecules == 2
    assert topology.n_entities == 2


def test_openmm_topology_to_molsysmt_molsys_preserves_declared_atom_group_and_chain_names(builder_openmm_topology):
    molsys = msm.convert(builder_openmm_topology, to_form='molsysmt.MolSys')

    assert molsys.topology.atoms['atom_name'].to_list() == ['N', 'CA', 'C', 'O']
    assert molsys.topology.groups['group_name'].to_list() == ['ALA', 'HOH']
    assert molsys.topology.chains['chain_id'].to_list() == ['A']


def test_openmm_topology_to_molsysmt_molsys_rebuilds_lossy_molecule_and_entity_metadata(builder_openmm_topology):
    molsys = msm.convert(builder_openmm_topology, to_form='molsysmt.MolSys')

    assert molsys.topology.molecules['molecule_name'].to_list() == ['peptide 0', 'water']
    assert molsys.topology.molecules['molecule_type'].to_list() == ['peptide', 'water']
    assert molsys.topology.entities['entity_name'].to_list() == ['peptide 0', 'water']
    assert molsys.topology.entities['entity_type'].to_list() == ['peptide', 'water']
