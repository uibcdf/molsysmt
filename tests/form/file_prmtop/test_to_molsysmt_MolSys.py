"""
Regression tests for the `file:prmtop` → `molsysmt.MolSys` conversion.

The converter imported a `to_molsysmt_Structures` sibling that never existed in the
form package. The name was never used — the body builds an empty `Structures()`,
because a prmtop carries topology only — but the import is executed at call time, so
every conversion to the library's central form raised `ModuleNotFoundError` and the
whole input format was unreachable from `molsysmt.MolSys`.

Oracle: the bundled pentalanine system (5207 atoms).
"""

import pytest

import molsysmt as msm
from molsysmt import systems


N_ATOMS = 5207


@pytest.fixture()
def prmtop():
    return systems['pentalanine']['pentalanine.prmtop']


def test_convert_to_molsysmt_MolSys(prmtop):
    molsys = msm.convert(prmtop, to_form='molsysmt.MolSys')

    assert msm.get_form(molsys) == 'molsysmt.MolSys'
    assert msm.get(molsys, n_atoms=True) == N_ATOMS
    # A prmtop holds no coordinates, so the MolSys carries a topology and an empty
    # structures container rather than a fabricated conformation.
    assert msm.get(molsys, n_structures=True) == 0


def test_the_conversion_is_advertised_and_callable(prmtop):
    from molsysmt.supported import conversions

    advertised = conversions(from_form='file:prmtop', to_form='molsysmt.MolSys').data
    assert advertised.loc['file:prmtop', 'molsysmt.MolSys']
    msm.convert(prmtop, to_form='molsysmt.MolSys')


def test_atom_selection_is_honoured(prmtop):
    molsys = msm.convert(prmtop, to_form='molsysmt.MolSys', selection=range(10))

    assert msm.get(molsys, n_atoms=True) == 10
