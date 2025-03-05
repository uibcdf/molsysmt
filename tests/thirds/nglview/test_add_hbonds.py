"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

def test_add_hbonds_1():

    molsys = msm.convert(msm.systems['Barnase-Barstar']['barnase_barstar.h5msm'])

    hbonds, distance, angles = msm.hbonds.get_luzard_chandler_hbonds(molsys,
                                                                     selection='molecule_name=="BARNASE"',
                                                                     selection_2='molecule_name=="BARSTAR"')
    hbonds = hbonds[0]

    coordinates = msm.get(molsys, element='atom', selection='all', coordinates=True)
    coordinates = puw.get_value(coordinates[0], to_unit='angstroms')

    view = msm.view(molsys, standard=True)
    msm.thirds.nglview.add_hbonds(view, hbonds)

    n_hbonds = len(hbonds)
    check_all_hbonds = False
    for ii in range(n_hbonds):
        aux = view._ngl_msg_archive[ii+7]
        check_1 = (aux['target']=='Widget')
        check_2 = (aux['args'][0]=='cylinder')
        check_3 = (aux['kwargs']['radius'][0]==0.1)
        check_4 = np.allclose(aux['kwargs']['color'],(1.0, 0.76470588, 0.0))
        check_5 = np.allclose(aux['kwargs']['color2'],(1.0, 0.76470588, 0.0))
        check_6 = np.allclose(aux['kwargs']['position1'],coordinates[hbonds[ii,1]])
        check_7 = np.allclose(aux['kwargs']['position2'],coordinates[hbonds[ii,2]])
        check_all_hbonds = all([check_1, check_2, check_3, check_4, check_5, check_6, check_7])
        if not check_all_hbonds:
            break

    assert check_all_hbonds==True

def test_add_hbonds_2():

    molsys = msm.convert(msm.systems['Barnase-Barstar']['barnase_barstar.h5msm'])

    hbonds, distance, angles = msm.hbonds.get_luzard_chandler_hbonds(molsys,
                                                                     selection='molecule_name=="BARNASE"',
                                                                     selection_2='molecule_name=="BARSTAR"')
    hbonds = hbonds[0]

    coordinates = msm.get(molsys, element='atom', selection='all', coordinates=True)
    coordinates = puw.get_value(coordinates[0], to_unit='angstroms')

    group_indices = msm.get(molsys, element='atom', selection='all', group_indices=True)
    CA_atoms = msm.select(molsys, selection='atom_name=="CA"')

    view = msm.view(molsys, standard=True)
    msm.thirds.nglview.add_hbonds(view, hbonds, hbond_level='group')

    n_hbonds = len(hbonds)
    check_all_hbonds = False
    for ii in range(n_hbonds):
        CA1 = CA_atoms[group_indices[hbonds[ii,1]]]
        CA2 = CA_atoms[group_indices[hbonds[ii,2]]]
        aux = view._ngl_msg_archive[ii+7]
        check_1 = (aux['target']=='Widget')
        check_2 = (aux['args'][0]=='cylinder')
        check_3 = (aux['kwargs']['radius'][0]==0.1)
        check_4 = np.allclose(aux['kwargs']['color'],(1.0, 0.76470588, 0.0))
        check_5 = np.allclose(aux['kwargs']['color2'],(1.0, 0.76470588, 0.0))
        check_6 = np.allclose(aux['kwargs']['position1'],coordinates[CA1, :])
        check_7 = np.allclose(aux['kwargs']['position2'],coordinates[CA2, :])
        check_all_hbonds = all([check_1, check_2, check_3, check_4, check_5, check_6, check_7])
        if not check_all_hbonds:
            break

    assert check_all_hbonds==True


