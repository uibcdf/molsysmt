"""
`msm.extract` on a molsysviewer.MolSysView.

The form's `extract` was written with the public signature -- `selection`, `syntax` --
instead of the form-level one the dispatcher uses, so every call raised `TypeError`,
including the default one. See uibcdf/molsysmt#204.
"""

import pytest

import molsysmt as msm


@pytest.fixture()
def view(builder_pdb_molsys):
    return msm.convert(builder_pdb_molsys, to_form='molsysviewer.MolSysView')


def test_extract_without_a_selection_returns_an_equivalent_view(view):
    extracted = msm.extract(view)

    assert msm.get_form(extracted) == 'molsysviewer.MolSysView'
    assert extracted is not view
    assert msm.get(extracted, n_atoms=True) == msm.get(view, n_atoms=True)


def test_extract_with_a_selection_returns_the_selected_subset(view):
    n_atoms = msm.get(view, n_atoms=True)
    extracted = msm.extract(view, selection='atom_index<2')

    assert msm.get_form(extracted) == 'molsysviewer.MolSysView'
    assert msm.get(extracted, n_atoms=True) == 2
    assert msm.get(view, n_atoms=True) == n_atoms


def test_extract_without_copying_returns_the_same_view(view):
    from molsysmt.form.molsysviewer_MolSysView.extract import extract

    assert extract(view, copy_if_all=False, skip_digestion=True) is view
