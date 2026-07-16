"""Public selection and index-validation contracts."""

import numpy as np
import pytest

import molsysmt as msm


def test_malformed_molsysmt_selection_raises_catalog_argument_error(t4_h5msm_molsys):
    with pytest.raises(msm.ArgumentError) as exc_info:
        msm.select(t4_h5msm_molsys, selection="atom_name ==")

    assert isinstance(exc_info.value.__cause__, SyntaxError)


def test_malformed_mdtraj_selection_raises_catalog_argument_error(t4_h5msm_molsys):
    pytest.importorskip("mdtraj")

    with pytest.raises(msm.ArgumentError) as exc_info:
        msm.select(t4_h5msm_molsys, selection="name ==== CA", syntax="MDTraj")

    assert isinstance(exc_info.value.__cause__, ValueError)


def test_mdanalysis_selection_uses_zero_based_atom_indices(t4_pdb_file):
    pytest.importorskip("MDAnalysis")

    observed = msm.select(t4_pdb_file, selection="name CA", syntax="MDAnalysis")
    expected = msm.select(t4_pdb_file, selection='atom_name == "CA"')

    assert observed == expected


def test_malformed_mdanalysis_selection_raises_catalog_argument_error(t4_pdb_file):
    pytest.importorskip("MDAnalysis")

    with pytest.raises(msm.ArgumentError) as exc_info:
        msm.select(t4_pdb_file, selection="this_is_not_a_selection", syntax="MDAnalysis")

    assert exc_info.value.__cause__ is not None


@pytest.mark.parametrize("selection", [[999_999], [-1]])
def test_select_rejects_out_of_range_element_indices(t4_h5msm_molsys, selection):
    with pytest.raises(msm.ArgumentError, match="out-of-range atom indices"):
        msm.select(t4_h5msm_molsys, selection=selection)


@pytest.mark.parametrize("structure_indices", [[1], [-1]])
def test_get_rejects_out_of_range_structure_indices(t4_h5msm_molsys, structure_indices):
    with pytest.raises(msm.ArgumentError, match="out-of-range structure indices"):
        msm.get(t4_h5msm_molsys, structure_indices=structure_indices, coordinates=True)


def test_select_accepts_a_boolean_mask(t4_h5msm_molsys):
    n_atoms = msm.get(t4_h5msm_molsys, n_atoms=True)
    mask = np.zeros(n_atoms, dtype=bool)
    mask[[1, 3]] = True

    assert msm.select(t4_h5msm_molsys, mask=mask) == [1, 3]


def test_select_rejects_a_boolean_mask_with_the_wrong_length(t4_h5msm_molsys):
    with pytest.raises(msm.ArgumentError, match="must contain 1441 entries"):
        msm.select(t4_h5msm_molsys, mask=np.ones(2, dtype=bool))


def test_get_rejects_an_out_of_range_index_mask(t4_h5msm_molsys):
    with pytest.raises(msm.ArgumentError, match="out-of-range atom indices"):
        msm.get(t4_h5msm_molsys, element="atom", mask=[999_999], atom_name=True)
