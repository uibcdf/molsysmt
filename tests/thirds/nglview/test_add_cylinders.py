"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
import nglview as nv


def test_add_cylinders_1():

    view = nv.NGLWidget()

    bottom = puw.quantity([[0,0,0], [0,5,0]], 'angstroms')
    top = puw.quantity([[10,0,0], [0,10,0]], 'angstroms')

    msm.thirds.nglview.add_cylinders(view, bottom=bottom, top=top, color='#ff0000', color_2='#0000ff',
                                     radius='0.2 angstroms')

    assert view._ngl_msg_archive[0]['args'][0] == 'cylinder'
    assert np.allclose(view._ngl_msg_archive[0]['kwargs']['position1'], [0.0, 0.0, 0.0])
    assert np.allclose(view._ngl_msg_archive[0]['kwargs']['position2'], [10.0, 0.0, 0.0])
    assert view._ngl_msg_archive[0]['kwargs']['radius'][0] == 0.2
    assert np.allclose(view._ngl_msg_archive[0]['kwargs']['color'], (1.0, 0.0, 0.0))
    assert np.allclose(view._ngl_msg_archive[0]['kwargs']['color2'], (0.0, 0.0, 1.0))

    assert view._ngl_msg_archive[1]['args'][0] == 'cylinder'
    assert np.allclose(view._ngl_msg_archive[1]['kwargs']['position1'], [0.0, 5.0, 0.0])
    assert np.allclose(view._ngl_msg_archive[1]['kwargs']['position2'], [0.0, 10.0, 0.0])
    assert view._ngl_msg_archive[1]['kwargs']['radius'][0] == 0.2
    assert np.allclose(view._ngl_msg_archive[1]['kwargs']['color'], (1.0, 0.0, 0.0))
    assert np.allclose(view._ngl_msg_archive[1]['kwargs']['color2'], (0.0, 0.0, 1.0))


def test_add_cylinders_2():

    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'])

    contacts = msm.structure.get_contacts(molsys, selection='atom_name=="CA"', threshold='9 angstroms',
                                          output_type='pairs', output_indices='atom')

    start = msm.get(molsys, element='atom', selection=np.array(contacts[0])[:,0], coordinates=True)
    end = msm.get(molsys, element='atom', selection=np.array(contacts[0])[:,1], coordinates=True)

    view = msm.view(molsys, standard=True)
    msm.thirds.nglview.add_cylinders(view, bottom=start, top=end)

    n_contacts = len(contacts[0])

    offset = len(view._ngl_msg_archive) - n_contacts
    start = puw.get_value(start[0], to_unit='angstroms')
    end = puw.get_value(end[0], to_unit='angstroms')

    for ii in range(n_contacts):

        assert view._ngl_msg_archive[ii+offset]['args'][0] == 'cylinder'
        assert np.allclose(view._ngl_msg_archive[ii+offset]['kwargs']['position1'], start[ii])
        assert np.allclose(view._ngl_msg_archive[ii+offset]['kwargs']['position2'], end[ii])


def test_add_cylinders_3():

    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'])

    contacts = msm.structure.get_contacts(molsys, selection='atom_name=="CA"', threshold='9 angstroms',
                                          output_type='pairs', output_indices='atom')

    start, groups_start = msm.get(molsys, element='atom', selection=np.array(contacts[0])[:,0], coordinates=True,
                                  group_index=True)
    end, groups_end = msm.get(molsys, element='atom', selection=np.array(contacts[0])[:,1], coordinates=True,
                              group_index=True)

    view = msm.view(molsys, standard=True)
    msm.thirds.nglview.add_cylinders(view, start[0], end[0], color_values=groups_start, color_values_2=groups_end,
                                     colormap='viridis')

    n_contacts = len(contacts[0])

    offset = len(view._ngl_msg_archive) - n_contacts

    assert view._ngl_msg_archive[offset]['args'][0] == 'cylinder'
    assert np.allclose(view._ngl_msg_archive[offset]['kwargs']['color'], (0.267004, 0.004874, 0.329415))
    assert np.allclose(view._ngl_msg_archive[offset]['kwargs']['color2'], (0.276022, 0.044167, 0.370164))

    assert view._ngl_msg_archive[-1]['args'][0] == 'cylinder'
    assert np.allclose(view._ngl_msg_archive[-1]['kwargs']['color'], (0.926106, 0.89733, 0.104071))
    assert np.allclose(view._ngl_msg_archive[-1]['kwargs']['color2'], (0.993248, 0.906157, 0.143936))
