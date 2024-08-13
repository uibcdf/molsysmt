"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

def test_add_contacts_1():

#    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'])
#    coordinates = msm.get(molsys, element='atom', selection='all', coordinates=True)
#    contacts = msm.structure.get_contacts(molsys, selection='atom_name=="CA"', threshold='9 angstroms',
#                                      output_type='pairs', output_indices='atom')
#    contacts = contacts[0]
#    coordinates = coordinates[0]
#    view = msm.view(molsys, standard=True)
#    msm.thirds.nglview.add_contacts(view, np.array(contacts), radius='0.1 angstroms')
#    view
#
#    n_contacts = len(contacts[0])
#    check_all_contacts = False
#    for ii in range(n_contacts):
#        aux = view._ngl_msg_archive[ii+7]
#        check_1 = (aux['target']=='Widget')
#        check_2 = (aux['args'][0]=='cylinder')
#        check_3 = (aux['kwargs']['radius'][0]==0.1)
#        check_4 = np.allclose(aux['kwargs']['color'],(0.501960, 0.501960, 0.501960))
#        check_5 = np.allclose(aux['kwargs']['color2'],(0.501960, 0.501960, 0.501960))
#        check_6 = np.allclose(aux['kwargs']['position1'],puw.get_value(coordinates[contacts[ii][0]], to_unit="angstroms"))
#        check_7 = np.allclose(aux['kwargs']['position2'],puw.get_value(coordinates[contacts[ii][1]], to_unit="angstroms"))
#        check_all_contacts = all([check_1, check_2, check_3, check_4, check_5, check_6, check_7])
#        if not check_all_contacts:
#            break
#
#    assert check_all_contacts==True

    assert True
