"""
Unit and regression test for the build peptide of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import shutil
import pytest

# Distance between atoms in space and time

@pytest.mark.skipif(shutil.which("tleap") is None, reason="tleap is not available in PATH")
def test_build_peptide_molsysmt_MolSys_1():
    seq = 'TyrGlyGlyPheMet'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys')
    seq_2 = msm.convert(molsys, to_form='string:amino_acids_3')
    assert seq.lower()==seq_2.lower()


def test_build_peptide_molsysmt_MolSys_2():
    seq = 'TyrGlyGlyPheMet'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    seq_2 = msm.convert(molsys, to_form='string:amino_acids_3')
    n_atoms = msm.get(molsys, n_atoms=True)
    n_bonds = msm.get(molsys, n_bonds=True)

    assert seq.lower() == seq_2.lower()
    assert n_atoms > 0
    assert n_bonds > 0


def test_build_peptide_molsysmt_MolSys_3():
    seq = 'ACEALAALANME'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')

    coordinates = msm.pyunitwizard.get_value(molsys.structures.coordinates[0], to_unit='nm')
    bonds = np.array(molsys.topology.bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=int))
    atom_types = np.array(molsys.topology.atoms['atom_type'].to_numpy(), dtype=object)

    heavy_indices = np.where(atom_types != 'H')[0]
    bonded_set = {tuple(sorted((int(ii), int(jj)))) for ii, jj in bonds.tolist()}
    bonded_distances = np.linalg.norm(coordinates[bonds[:, 0], :] - coordinates[bonds[:, 1], :], axis=1)

    min_nonbonded_heavy_distance = np.inf
    for ii, atom_index_1 in enumerate(heavy_indices):
        for atom_index_2 in heavy_indices[ii + 1:]:
            pair = tuple(sorted((int(atom_index_1), int(atom_index_2))))
            if pair in bonded_set:
                continue
            distance = np.linalg.norm(coordinates[atom_index_1, :] - coordinates[atom_index_2, :])
            if distance < min_nonbonded_heavy_distance:
                min_nonbonded_heavy_distance = distance

    assert 'atom_ff_type' in molsys.topology.atoms.columns
    assert min_nonbonded_heavy_distance >= 0.10
    assert np.max(bonded_distances) <= 0.185


def test_build_peptide_molsysmt_MolSys_4():
    seq = 'AG'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')

    atom_table = molsys.topology.atoms[['group_index', 'atom_name']]
    group_names = molsys.topology.groups['group_name']

    atom_names_by_group = {}
    for group_index, atom_name in atom_table.to_numpy():
        group_name = group_names.iloc[int(group_index)]
        atom_names_by_group.setdefault(group_name, []).append(atom_name)

    # Match LEaP behavior for uncapped peptides: standard residue termini.
    assert atom_names_by_group['ALA'].count('H') == 1
    assert 'H1' not in atom_names_by_group['ALA']
    assert 'H2' not in atom_names_by_group['ALA']
    assert 'H3' not in atom_names_by_group['ALA']
    assert 'OXT' not in atom_names_by_group['GLY']

    assert msm.get(molsys, n_atoms=True) == 17
    assert msm.get(molsys, n_bonds=True) == 16

#def test_build_peptide_molsysmt_MolSys_2():
#    seq = 'TyrGlyGlyPheMet'
#    molsys = msm.build.build_peptide(seq, to_form=['dialanine_amber14_tip3p.prmtop','dialanine_amber14_tip3p.inpcrd'])
#    molsys = msm.convert(['dialanine_amber14_tip3p.prmtop','dialanine_amber14_tip3p.inpcrd'],
#                         to_form='molsysmt.MolSys')
#    os.remove('dialanine_amber14_tip3p.prmtop')
#    os.remove('dialanine_amber14_tip3p.inpcrd')
#    seq_2 = msm.convert(molsys, to_form='string:aminoacids3', selection='molecule_type=="peptide"')
#    is_solvated = msm.build.is_solvated(molsys)
#    check_1 = (seq.lower()==seq_2.lower())
#    check_2 = is_solvated
#    assert check_1 and check_2
