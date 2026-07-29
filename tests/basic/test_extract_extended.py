"""
Extended tests for molsysmt.basic.extract covering uncovered branches:
- output_filename sets to_form implicitly (convert path)
"""
import molsysmt as msm
import pytest
import tempfile
import os
import numpy as np

from molsysmt import systems


def test_extract_with_output_filename(t4_h5msm_molsys, tmp_path):
    """output_filename triggers the to_form=output_filename path (convert)."""
    out = str(tmp_path / 'out.pdb')
    result = msm.extract(t4_h5msm_molsys, selection='molecule_type=="protein"',
                         output_filename=out)
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
