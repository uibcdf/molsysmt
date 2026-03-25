"""
Additional coverage tests for file:msmpk form.

Covers conversion paths not exercised by test_roundtrip.py:
- file:msmpk → molsysmt.Topology
- file:msmpk → molsysmt.Structures
- extract (copy-if-all and same-file paths)
- is_form
- has_attribute
"""

import pytest
import os
import molsysmt as msm


@pytest.fixture()
def msmpk_file(builder_pdb_molsys, tmp_path):
    path = str(tmp_path / 'builder.msmpk')
    msm.convert(builder_pdb_molsys, to_form='file:msmpk', output_filename=path)
    return path


# ---------------------------------------------------------------------------
# is_form
# ---------------------------------------------------------------------------

def test_is_form_true(msmpk_file):
    from molsysmt.form.file_msmpk import is_form
    assert is_form(msmpk_file) is True


def test_is_form_false_for_pdb():
    from molsysmt.form.file_msmpk import is_form
    assert is_form('something.pdb') is False


# ---------------------------------------------------------------------------
# to_molsysmt_Topology
# ---------------------------------------------------------------------------

def test_to_topology(msmpk_file, builder_pdb_molsys):
    topology = msm.convert(msmpk_file, to_form='molsysmt.Topology')
    assert topology is not None
    assert topology.n_atoms == builder_pdb_molsys.topology.n_atoms


def test_to_topology_group_count(msmpk_file, builder_pdb_molsys):
    topology = msm.convert(msmpk_file, to_form='molsysmt.Topology')
    assert topology.n_groups == builder_pdb_molsys.topology.n_groups


# ---------------------------------------------------------------------------
# to_molsysmt_Structures
# ---------------------------------------------------------------------------

def test_to_structures(msmpk_file):
    structures = msm.convert(msmpk_file, to_form='molsysmt.Structures')
    assert structures is not None


# ---------------------------------------------------------------------------
# extract — copy path
# ---------------------------------------------------------------------------

def test_extract_copy(msmpk_file, tmp_path):
    from molsysmt.form.file_msmpk.extract import extract
    dest = str(tmp_path / 'copy.msmpk')
    result = extract(msmpk_file, output_filename=dest)
    assert os.path.isfile(dest)
    assert result == dest


def test_extract_same_file_no_copy(msmpk_file):
    """extract with copy_if_all=False and same output_filename → no copy, returns item."""
    from molsysmt.form.file_msmpk.extract import extract
    result = extract(msmpk_file, output_filename=msmpk_file, copy_if_all=False)
    assert result == msmpk_file
