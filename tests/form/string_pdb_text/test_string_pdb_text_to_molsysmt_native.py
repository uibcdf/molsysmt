"""
Regression tests for string:pdb_text conversions to native MolSysMT forms.
"""

import numpy as np
import molsysmt as msm


def test_string_pdb_text_to_molsysmt_topology_preserves_counts(t4_pdb_text, t4_pdb_molsys):
    topology = msm.convert(t4_pdb_text, to_form='molsysmt.Topology')

    assert topology.n_atoms == t4_pdb_molsys.topology.n_atoms
    assert topology.n_groups == t4_pdb_molsys.topology.n_groups


def test_written_string_pdb_text_to_molsysmt_molsys_preserves_names(t4_written_pdb_text, t4_pdb_molsys):
    molsys = msm.convert(t4_written_pdb_text, to_form='molsysmt.MolSys')

    assert np.all(molsys.topology.atoms['atom_name'].to_numpy()[:5] == np.array(['N', 'CA', 'C', 'O', 'CB'], dtype=object))
    assert np.all(molsys.topology.groups['group_name'].to_numpy()[:3] == np.array(['MET', 'ASN', 'ILE'], dtype=object))


def test_string_pdb_text_to_molsysmt_structures_preserves_multimodel_shape(md_1u19_pdb_text, md_1u19_pdb_molsys):
    structures = msm.convert(md_1u19_pdb_text, to_form='molsysmt.Structures')

    assert structures.n_atoms == md_1u19_pdb_molsys.structures.n_atoms
    assert structures.n_structures == md_1u19_pdb_molsys.structures.n_structures
