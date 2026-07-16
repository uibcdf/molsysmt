"""
Unit and regression test for the view module of the molsysmt package on molsysmt.MolSys with MolSysViewer.
"""

import molsysmt as msm
import numpy as np


def test_view_molsysmt_MolSys_with_MolSysViewer_form(alanine_molsys):

    view = msm.view(alanine_molsys)
    assert msm.get_form(view) == 'molsysviewer.MolSysView'


def test_view_molsysmt_MolSys_with_MolSysViewer_compare(alanine_molsys):

    view = msm.view(alanine_molsys)
    assert msm.compare(view, alanine_molsys, coordinates=True, box=True)


def test_molsysviewer_preserves_thermodynamic_structure_metadata(alanine_molsys):
    puw = msm.pyunitwizard
    alanine_molsys.structures.temperature = puw.quantity([300.0], 'K')
    alanine_molsys.structures.potential_energy = puw.quantity([-10.0], 'kJ/mol')
    alanine_molsys.structures.kinetic_energy = puw.quantity([3.0], 'kJ/mol')
    view = msm.view(alanine_molsys)

    temperature, potential, kinetic, total = msm.get(
        view,
        temperature=True,
        potential_energy=True,
        kinetic_energy=True,
        total_energy=True,
    )

    np.testing.assert_allclose(puw.get_value(temperature, to_unit='K'), [300.0])
    np.testing.assert_allclose(puw.get_value(potential, to_unit='kJ/mol'), [-10.0])
    np.testing.assert_allclose(puw.get_value(kinetic, to_unit='kJ/mol'), [3.0])
    np.testing.assert_allclose(puw.get_value(total, to_unit='kJ/mol'), [-7.0])
