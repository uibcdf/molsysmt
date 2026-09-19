"""Extended tests for :func:`molsysmt.extract`."""

import os

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import systems


def test_extract_with_output_filename(t4_h5msm_molsys, tmp_path):
    """output_filename triggers the to_form=output_filename path (convert)."""
    out = str(tmp_path / 'out.pdb')
    msm.extract(t4_h5msm_molsys, selection='molecule_type=="protein"', output_filename=out)
    assert os.path.exists(out)


def test_extract_to_form_explicit(t4_h5msm_molsys):
    """to_form explicitly set returns converted form."""
    result = msm.extract(t4_h5msm_molsys, selection='molecule_type=="protein"',
                         to_form='molsysmt.Topology')
    assert msm.get_form(result) == 'molsysmt.Topology'


def test_extract_composite_materializes_native_system_and_preserves_single_state():
    topology = systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm']
    trajectory = systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd']

    result = msm.extract(
        [topology, trajectory],
        structure_indices=[0, 1, 19],
    )

    assert msm.get_form(result) == 'molsysmt.MolSys'
    assert msm.get(result, element='system', n_structures=True) == 3
    np.testing.assert_array_equal(
        result._get_structure_chemical_state_indices(),
        np.zeros(3, dtype=np.int64),
    )


def test_extract_molecular_mechanics_subsets_per_atom_parameters():
    from molsysmt.native import MolecularMechanics

    source = MolecularMechanics(
        forcefield='AMBER14',
        formal_charge=np.array([0, 1, -1]),
        partial_charge=np.array([0.1, 0.2, 0.3]),
        atom_ff_type=np.array(['CT', 'N', 'O']),
    )

    result = msm.extract(source, selection=[2, 0])

    assert msm.get_form(result) == 'molsysmt.MolecularMechanics'
    assert result.forcefield == 'AMBER14'
    np.testing.assert_array_equal(result.formal_charge, [-1, 0])
    np.testing.assert_allclose(np.asarray(result.partial_charge, dtype=float), [0.3, 0.1])
    np.testing.assert_array_equal(result.atom_ff_type, ['O', 'CT'])
    np.testing.assert_array_equal(source.formal_charge, [0, 1, -1])


def test_extract_molecular_mechanics_dict_subsets_per_atom_parameters():
    source = {
        'forcefield': 'AMBER14',
        'formal_charge': np.array([0, 1, -1]),
        'partial_charge': np.array([0.1, 0.2, 0.3]),
        'atom_ff_type': ['CT', 'N', 'O'],
    }

    result = msm.extract(source, selection=[1])

    assert msm.get_form(source) == 'molsysmt.MolecularMechanicsDict'
    assert result['forcefield'] == 'AMBER14'
    np.testing.assert_array_equal(result['formal_charge'], [1])
    np.testing.assert_allclose(result['partial_charge'], [0.2])
    assert result['atom_ff_type'] == ['N']
    np.testing.assert_array_equal(source['formal_charge'], [0, 1, -1])


def test_extract_molecular_mechanics_without_atom_data_reports_the_form():
    from molsysmt.native import MolecularMechanics

    with pytest.raises(msm.NotWithThisFormError, match='molsysmt.MolecularMechanics'):
        msm.extract(MolecularMechanics(forcefield='AMBER14'), selection=[0])


def test_extract_sequence_uses_residue_positions():
    assert msm.extract('AlaValPro', selection=[2, 0]) == 'ProAla'
    assert (
        msm.extract('amino_acids_3:AlaValPro', selection=[1])
        == 'amino_acids_3:Val'
    )


def test_extract_sequence_rejects_out_of_range_positions_with_a_catalog_error():
    with pytest.raises(msm.ArgumentError, match='string:amino_acids_3'):
        msm.extract('AlaValPro', selection=[3])


def test_convert_sequence_preserves_group_indexed_converter_contract():
    result = msm.convert(
        'amino_acids_3:AlaValPro',
        to_form='string:amino_acids_3',
        selection=[2, 0],
    )

    assert result == 'amino_acids_3:ProAla'
