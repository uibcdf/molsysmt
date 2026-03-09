"""
Regression tests for attribute extraction from string:pdb_text systems.
"""

import numpy as np
import molsysmt as msm


def test_get_string_pdb_system_counts(t4_pdb_text, t4_pdb_molsys):
    n_atoms, n_groups = msm.get(t4_pdb_text, element='system', n_atoms=True, n_groups=True)

    assert n_atoms == t4_pdb_molsys.topology.n_atoms
    assert n_groups == t4_pdb_molsys.topology.n_groups


def test_get_string_pdb_atom_names_from_written_text(t4_written_pdb_text, t4_pdb_molsys):
    atom_names = msm.get(t4_written_pdb_text, element='atom', selection=[0, 1, 2], name=True)
    expected = np.array(['N', 'CA', 'C'], dtype=object)

    assert np.all(atom_names == expected)


def test_get_string_pdb_group_names_from_written_text(t4_written_pdb_text):
    group_names = msm.get(t4_written_pdb_text, element='group', selection=[0, 1, 2], name=True)
    expected = np.array(['MET', 'ASN', 'ILE'], dtype=object)

    assert np.all(group_names == expected)


def test_get_string_pdb_multimodel_counts(md_1u19_pdb_text, md_1u19_pdb_molsys):
    n_atoms, n_structures = msm.get(md_1u19_pdb_text, element='system', n_atoms=True, n_structures=True)

    assert n_atoms == md_1u19_pdb_molsys.topology.n_atoms
    assert n_structures == md_1u19_pdb_molsys.structures.n_structures
