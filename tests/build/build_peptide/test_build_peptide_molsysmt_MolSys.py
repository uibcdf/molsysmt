"""
Unit and regression test for the build peptide of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import shutil
import pytest

# Distance between atoms in space and time

_AMINO_ACID_CODES_1 = np.array(list("ACDEFGHIKLMNPQRSTVWY"), dtype=object)


def _random_sequences(length, n_sequences, seed):
    rng = np.random.default_rng(seed)
    sequences = []
    while len(sequences) < n_sequences:
        symbols = rng.choice(_AMINO_ACID_CODES_1, size=length, replace=True)
        sequence = "".join(symbols.tolist())
        if sequence not in sequences:
            sequences.append(sequence)
    return sequences


_RANDOM_SEQUENCES_LEN10 = _random_sequences(length=10, n_sequences=10, seed=20260216)
_RANDOM_SEQUENCES_LEN10_EXTENDED = _random_sequences(length=10, n_sequences=40, seed=20260216)


def _get_min_nonbonded_heavy_distance(molsys):
    coordinates = msm.pyunitwizard.get_value(molsys.structures.coordinates[0], to_unit='nm')
    bonds = np.array(molsys.topology.bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=int))
    atom_types = np.array(molsys.topology.atoms['atom_type'].to_numpy(), dtype=object)
    heavy_indices = np.where(atom_types != 'H')[0]
    bonded_set = {tuple(sorted((int(ii), int(jj)))) for ii, jj in bonds.tolist()}

    min_nonbonded_heavy_distance = np.inf
    for ii, atom_index_1 in enumerate(heavy_indices):
        for atom_index_2 in heavy_indices[ii + 1:]:
            pair = tuple(sorted((int(atom_index_1), int(atom_index_2))))
            if pair in bonded_set:
                continue
            distance = np.linalg.norm(coordinates[atom_index_1, :] - coordinates[atom_index_2, :])
            if distance < min_nonbonded_heavy_distance:
                min_nonbonded_heavy_distance = distance

    return min_nonbonded_heavy_distance


def _get_build_metrics(molsys):
    coordinates = msm.pyunitwizard.get_value(molsys.structures.coordinates[0], to_unit='nm')
    bonds = np.array(molsys.topology.bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=int))
    atom_types = np.array(molsys.topology.atoms['atom_type'].to_numpy(), dtype=object)

    max_bond_nm = 0.0
    min_bond_nm = np.inf
    if bonds.shape[0] > 0:
        bonded_distances = np.linalg.norm(coordinates[bonds[:, 0], :] - coordinates[bonds[:, 1], :], axis=1)
        max_bond_nm = float(np.max(bonded_distances))
        min_bond_nm = float(np.min(bonded_distances))

    return {
        'n_atoms': int(molsys.topology.atoms.shape[0]),
        'n_bonds': int(molsys.topology.bonds.shape[0]),
        'max_bond_nm': max_bond_nm,
        'min_bond_nm': min_bond_nm,
        'min_nonbonded_heavy_nm': float(_get_min_nonbonded_heavy_distance(molsys)),
    }


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


@pytest.mark.parametrize('sequence', ['AP', 'GP', 'PP', 'ACEPROGLYNME'])
def test_build_peptide_molsysmt_MolSys_5(sequence):
    molsys = msm.build.build_peptide(sequence, to_form='molsysmt.MolSys', engine='MolSysMT')
    min_nonbonded_heavy_distance = _get_min_nonbonded_heavy_distance(molsys)
    assert np.isfinite(min_nonbonded_heavy_distance)
    assert min_nonbonded_heavy_distance >= 0.20


@pytest.mark.parametrize('sequence', ['AP', 'GP', 'PP', 'PA', 'PG', 'ACEPROGLYNME'])
@pytest.mark.skipif(shutil.which("tleap") is None, reason="tleap is not available in PATH")
def test_build_peptide_molsysmt_MolSys_6(sequence):
    molsys_tleap = msm.build.build_peptide(sequence, to_form='molsysmt.MolSys', engine='LEaP')
    molsys_molsysmt = msm.build.build_peptide(sequence, to_form='molsysmt.MolSys', engine='MolSysMT')

    metrics_tleap = _get_build_metrics(molsys_tleap)
    metrics_molsysmt = _get_build_metrics(molsys_molsysmt)

    assert metrics_molsysmt['n_atoms'] == metrics_tleap['n_atoms']
    assert metrics_molsysmt['n_bonds'] == metrics_tleap['n_bonds']
    assert abs(metrics_molsysmt['max_bond_nm'] - metrics_tleap['max_bond_nm']) <= 0.0045
    assert abs(metrics_molsysmt['min_nonbonded_heavy_nm'] - metrics_tleap['min_nonbonded_heavy_nm']) <= 0.01


@pytest.mark.parametrize('sequence', ['AP', 'GP', 'PP', 'PAP', 'GPPG', 'APPPG', 'ACEPPPNME'])
def test_build_peptide_molsysmt_MolSys_7(sequence):
    molsys = msm.build.build_peptide(sequence, to_form='molsysmt.MolSys', engine='MolSysMT')
    metrics = _get_build_metrics(molsys)

    assert metrics['n_atoms'] > 0
    assert metrics['n_bonds'] > 0
    assert metrics['min_bond_nm'] >= 0.095
    assert metrics['max_bond_nm'] <= 0.185
    assert metrics['min_nonbonded_heavy_nm'] >= 0.17


@pytest.mark.parametrize('sequence', ['AP', 'GP', 'PP', 'ACEPROGLYNME', 'PAP', 'GPPG'])
def test_build_peptide_molsysmt_MolSys_8(sequence):
    molsys_a = msm.build.build_peptide(sequence, to_form='molsysmt.MolSys', engine='MolSysMT')
    molsys_b = msm.build.build_peptide(sequence, to_form='molsysmt.MolSys', engine='MolSysMT')

    coords_a = msm.pyunitwizard.get_value(molsys_a.structures.coordinates[0], to_unit='nm')
    coords_b = msm.pyunitwizard.get_value(molsys_b.structures.coordinates[0], to_unit='nm')
    bonds_a = np.array(molsys_a.topology.bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=int))
    bonds_b = np.array(molsys_b.topology.bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=int))

    assert np.array_equal(bonds_a, bonds_b)
    assert np.allclose(coords_a, coords_b, atol=1.0e-12, rtol=0.0)


@pytest.mark.skipif(shutil.which("tleap") is None, reason="tleap is not available in PATH")
@pytest.mark.parametrize('sequence', _RANDOM_SEQUENCES_LEN10)
def test_build_peptide_molsysmt_MolSys_9(sequence):
    molsys_tleap = msm.build.build_peptide(sequence, to_form='molsysmt.MolSys', engine='LEaP')
    molsys_molsysmt = msm.build.build_peptide(sequence, to_form='molsysmt.MolSys', engine='MolSysMT')

    metrics_tleap = _get_build_metrics(molsys_tleap)
    metrics_molsysmt = _get_build_metrics(molsys_molsysmt)

    assert metrics_molsysmt['n_atoms'] == metrics_tleap['n_atoms']
    assert metrics_molsysmt['n_bonds'] == metrics_tleap['n_bonds']
    assert abs(metrics_molsysmt['max_bond_nm'] - metrics_tleap['max_bond_nm']) <= 0.0045
    assert metrics_molsysmt['min_nonbonded_heavy_nm'] >= 0.15
    assert metrics_molsysmt['min_nonbonded_heavy_nm'] >= metrics_tleap['min_nonbonded_heavy_nm'] - 0.025

def test_build_peptide_molsysmt_MolSys_10_random_sequences_catalog():
    assert len(_RANDOM_SEQUENCES_LEN10) == 10
    assert len(_RANDOM_SEQUENCES_LEN10_EXTENDED) == 40


def test_build_peptide_molsysmt_MolSys_11_empty_sequence_raises():
    from molsysmt._private.smonitor import ArgumentError
    with pytest.raises(ArgumentError):
        msm.build.build_peptide("", to_form="molsysmt.MolSys", engine="MolSysMT")


@pytest.mark.peptide_parity
@pytest.mark.skipif(shutil.which("tleap") is None, reason="tleap is not available in PATH")
@pytest.mark.parametrize('sequence', _RANDOM_SEQUENCES_LEN10_EXTENDED)
def test_build_peptide_molsysmt_MolSys_12_extended_random_parity(sequence):
    molsys_tleap = msm.build.build_peptide(sequence, to_form='molsysmt.MolSys', engine='LEaP')
    molsys_molsysmt = msm.build.build_peptide(sequence, to_form='molsysmt.MolSys', engine='MolSysMT')

    metrics_tleap = _get_build_metrics(molsys_tleap)
    metrics_molsysmt = _get_build_metrics(molsys_molsysmt)

    assert metrics_molsysmt['n_atoms'] == metrics_tleap['n_atoms']
    assert metrics_molsysmt['n_bonds'] == metrics_tleap['n_bonds']
    assert abs(metrics_molsysmt['max_bond_nm'] - metrics_tleap['max_bond_nm']) <= 0.0045
    assert metrics_molsysmt['min_nonbonded_heavy_nm'] >= 0.15
    assert metrics_molsysmt['min_nonbonded_heavy_nm'] >= metrics_tleap['min_nonbonded_heavy_nm'] - 0.025



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
