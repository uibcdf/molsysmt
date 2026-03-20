"""
Extended tests for molsysmt.basic.extract covering uncovered branches:
- output_filename sets to_form implicitly (convert path)
"""
import molsysmt as msm
import pytest
import tempfile
import os


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
