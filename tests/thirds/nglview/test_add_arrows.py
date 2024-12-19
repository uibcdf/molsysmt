"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np


def test_add_arrows_1():

    molsys = msm.systems['T4 lysozyme L99A']['181l.h5msm']
    molecular_system = msm.convert(molsys, selection='molecule_type=="protein"')
    view = msm.view(molecular_system, standard=False)
    msm.thirds.nglview.add_arrows(view, vectors='[2,2,2] angstroms', origin='atom_name=="CA"', color='#808080', radius='0.2 angstroms')
    n_arrows, coordinates = msm.get(molsys, element='atom', selection='atom_name=="CA"', n_atoms=True, coordinates=True)
    check_all_arrows = False
    for ii in range(n_arrows):
        aux = view._ngl_msg_archive[ii+1]
        check_1 = (aux['target']=='Widget')
        check_2 = (aux['args'][0]=='arrow')
        check_3 = (aux['kwargs']['radius'][0]==0.2)
        check_4 = np.allclose(aux['kwargs']['color'],(0.501960, 0.501960, 0.501960))
        check_5 = np.allclose(aux['kwargs']['position1'],puw.get_value(coordinates[0,ii], to_unit="angstroms"))
        check_6 = np.allclose(aux['kwargs']['position2'],puw.get_value(coordinates[0,ii], to_unit="angstroms")+np.array([2.0,2.0,2.0]))
        check_all_arrows = all([check_1, check_2, check_3, check_4, check_5, check_6])
        if not check_all_arrows:
            break

    assert check_all_arrows==True

def test_add_arrows_2():

    from molsysmt._private.colors import color_to_form

    molsys = msm.systems['T4 lysozyme L99A']['181l.h5msm']
    molecular_system = msm.convert(molsys, selection='molecule_type=="protein"')
    view = msm.view(molecular_system, standard=False)
    colors = ['#FF0000', '#00FF00', '#0000FF']
    arrows = puw.quantity([[10,0,0],[0,10,0],[0,0,10]], 'angstroms')
    msm.thirds.nglview.add_arrows(view, vectors=arrows,
                              origin=puw.quantity([[0,0,0],[0,0,0],[0,0,0]], 'angstroms'),
                              color=colors, radius='0.2 angstroms')
    n_arrows = 3
    check_all_arrows = False
    for ii in range(n_arrows):
        aux = view._ngl_msg_archive[ii+1]
        check_1 = (aux['target']=='Widget')
        check_2 = (aux['args'][0]=='arrow')
        check_3 = (aux['kwargs']['radius'][0]==0.2)
        check_4 = np.allclose(aux['kwargs']['color'],color_to_form(colors[ii], 'rgb'))
        check_5 = np.allclose(aux['kwargs']['position1'],[0,0,0])
        check_6 = np.allclose(aux['kwargs']['position2'],puw.get_value(arrows[ii], to_unit="angstroms"))
        check_all_arrows = all([check_1, check_2, check_3, check_4, check_5, check_6])
        if not check_all_arrows:
            break

    assert check_all_arrows==True


def test_add_arrows_3():

    from molsysmt._private.colors import color_to_form

    molsys = msm.systems['T4 lysozyme L99A']['181l.h5msm']
    molecular_system = msm.convert(molsys, selection='molecule_type=="protein"')
    view = msm.view(molecular_system, standard=False)

    arrows = puw.quantity([[9,0,0],[0,6,0],[0,0,-12], [0,5,5]], 'angstroms')
    coordinates = msm.get(view, element='atom',
                          selection='atom_name=="CA" and group_index in [10,30,60,90]', coordinates=True)
    msm.thirds.nglview.add_arrows(view, vectors=arrows, origin='atom_name=="CA" and group_index in [10,30,60,90]',
                                  color='#0B6E4F', radius='0.5 angstroms')
    n_arrows = 4
    check_all_arrows = False
    for ii in range(n_arrows):
        aux = view._ngl_msg_archive[ii+1]
        check_1 = (aux['target']=='Widget')
        check_2 = (aux['args'][0]=='arrow')
        check_3 = np.allclose(aux['kwargs']['radius'],[0.5])
        check_4 = np.allclose(aux['kwargs']['color'],color_to_form('#0B6E4F', 'rgb'))
        check_5 = np.allclose(aux['kwargs']['position1'],puw.get_value(coordinates[0,ii], to_unit="angstroms"))
        check_6 = np.allclose(aux['kwargs']['position2'],puw.get_value(coordinates[0,ii]+arrows[ii], to_unit="angstroms"))
        print(check_1, check_2, check_3, check_4, check_5, check_6)
        check_all_arrows = all([check_1, check_2, check_3, check_4, check_5, check_6])
        if not check_all_arrows:
            break

    assert check_all_arrows==True

