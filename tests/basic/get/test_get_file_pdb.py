"""
Regression tests for attribute extraction from file:pdb systems.
"""

import numpy as np
import molsysmt as msm


def test_get_file_pdb_system_counts(t4_pdb_file, t4_pdb_molsys):
    n_atoms, n_groups = msm.get(t4_pdb_file, element='system', n_atoms=True, n_groups=True)

    assert n_atoms == t4_pdb_molsys.topology.n_atoms
    assert n_groups == t4_pdb_molsys.topology.n_groups


def test_get_file_pdb_atom_names(t4_pdb_file, t4_pdb_molsys):
    atom_names = msm.get(t4_pdb_file, element='atom', selection=[0, 1, 2], name=True)
    expected = np.array(['N', 'CA', 'C'], dtype=object)

    assert np.all(atom_names == expected)


def test_get_file_pdb_group_names(t4_pdb_file):
    group_names = msm.get(t4_pdb_file, element='group', selection=[0, 1, 2], name=True)
    expected = np.array(['MET', 'ASN', 'ILE'], dtype=object)

    assert np.all(group_names == expected)


def test_get_file_pdb_multimodel_counts(md_1u19_pdb_file, md_1u19_pdb_molsys):
    n_atoms, n_structures = msm.get(md_1u19_pdb_file, element='system', n_atoms=True, n_structures=True)

    assert n_atoms == md_1u19_pdb_molsys.topology.n_atoms
    assert n_structures == md_1u19_pdb_molsys.structures.n_structures
