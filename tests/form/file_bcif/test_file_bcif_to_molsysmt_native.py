"""Regression tests for file:bcif conversions to native MolSysMT forms."""

import numpy as np
import molsysmt as msm


def test_file_bcif_to_molsysmt_topology_preserves_counts(hp35_bcif_file):
    topology = msm.convert(hp35_bcif_file, to_form='molsysmt.Topology')

    assert topology.n_atoms == 596
    assert topology.n_groups == 36
    assert topology.n_entities == 1


def test_file_bcif_to_molsysmt_molsys_preserves_first_names(hp35_bcif_file):
    molsys = msm.convert(hp35_bcif_file, to_form='molsysmt.MolSys')

    assert np.all(molsys.topology.atoms['atom_name'].to_numpy()[:5] == np.array(['N', 'CA', 'C', 'O', 'CB'], dtype=object))
    assert np.all(molsys.topology.groups['group_name'].to_numpy()[:3] == np.array(['MET', 'LEU', 'SER'], dtype=object))


def test_file_bcif_to_molsysmt_molsys_preserves_explicit_entity_ids(hp35_bcif_file):
    molsys = msm.convert(hp35_bcif_file, to_form='molsysmt.MolSys')

    assert molsys.topology.entities['entity_id'].to_list() == ['1']
