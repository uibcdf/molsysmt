"""
Unit and regression test for the get module of the molsysmt package on xtc file systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np


def test_get_file_xtc_1():
    molsys = systems['nglview']['md_1u19.xtc']
    n_atoms, n_structures = msm.get(molsys, element='system', n_atoms=True, n_structures=True)
    assert (n_atoms==5547) and (n_structures==51)


def test_get_file_xtc_mixed_atom_and_system_attributes_preserves_order():
    molsys = systems['nglview']['md_1u19.xtc']

    coordinates, time, structure_id = msm.get(
        molsys,
        element='atom',
        selection=[0, 2],
        structure_indices=[0, 1],
        coordinates=True,
        time=True,
        structure_id=True,
    )

    assert msm.pyunitwizard.get_value(coordinates).shape == (2, 2, 3)
    assert np.allclose(msm.pyunitwizard.get_value(time), [0.0, 20.0])
    assert structure_id == ['0', '10000']


def test_get_file_xtc_mixed_atom_and_system_attributes_preserves_dictionary_order():
    molsys = systems['nglview']['md_1u19.xtc']

    output = msm.get(
        molsys,
        element='atom',
        selection=[0, 2],
        structure_indices=[0, 1],
        structure_id=True,
        coordinates=True,
        time=True,
        output_type='dictionary',
    )

    assert list(output) == ['structure_id', 'coordinates', 'time']
    assert output['structure_id'] == ['0', '10000']
    assert msm.pyunitwizard.get_value(output['coordinates']).shape == (2, 2, 3)
    assert np.allclose(msm.pyunitwizard.get_value(output['time']), [0.0, 20.0])
