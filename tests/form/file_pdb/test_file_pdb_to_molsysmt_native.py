"""
Regression tests for file:pdb conversions to native MolSysMT forms.
"""

import numpy as np
import molsysmt as msm


def test_file_pdb_to_molsysmt_topology_preserves_counts(t4_pdb_file, t4_pdb_molsys):
    topology = msm.convert(t4_pdb_file, to_form='molsysmt.Topology')

    assert topology.n_atoms == t4_pdb_molsys.topology.n_atoms
    assert topology.n_groups == t4_pdb_molsys.topology.n_groups


def test_file_pdb_to_molsysmt_structures_preserves_shape(md_1u19_pdb_file, md_1u19_pdb_molsys):
    structures = msm.convert(md_1u19_pdb_file, to_form='molsysmt.Structures')

    assert structures.n_atoms == md_1u19_pdb_molsys.structures.n_atoms
    assert structures.n_structures == md_1u19_pdb_molsys.structures.n_structures


def test_file_pdb_to_molsysmt_molsys_preserves_first_atom_names(t4_pdb_file, t4_pdb_molsys):
    molsys = msm.convert(t4_pdb_file, to_form='molsysmt.MolSys')

    assert np.all(molsys.topology.atoms['atom_name'].to_numpy()[:5] == np.array(['N', 'CA', 'C', 'O', 'CB'], dtype=object))
    assert np.all(molsys.topology.groups['group_name'].to_numpy()[:3] == np.array(['MET', 'ASN', 'ILE'], dtype=object))


def test_file_pdb_from_builder_fixture_preserves_declared_truth(builder_pdb_molsys, builder_pdb_text, tmp_path):
    pdb_file = tmp_path / "builder_fixture.pdb"
    pdb_file.write_text(builder_pdb_text)

    molsys = msm.convert(str(pdb_file), to_form='molsysmt.MolSys')

    assert molsys.topology.n_atoms == builder_pdb_molsys.topology.n_atoms
    assert molsys.topology.n_groups == builder_pdb_molsys.topology.n_groups
    assert molsys.topology.n_bonds == builder_pdb_molsys.topology.n_bonds
    assert molsys.topology.atoms['atom_name'].tolist() == builder_pdb_molsys.topology.atoms['atom_name'].tolist()
    assert molsys.topology.groups['group_name'].tolist() == builder_pdb_molsys.topology.groups['group_name'].tolist()
    assert molsys.topology.chains['chain_id'].tolist() == builder_pdb_molsys.topology.chains['chain_id'].tolist()
