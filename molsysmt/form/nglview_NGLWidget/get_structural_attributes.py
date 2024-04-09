#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='nglview.NGLWidget'

## From atom

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        n_structures = get_n_structures_from_system(item, skip_digestion=True)
        structure_indices = np.arange(n_structures)

    coordinates = []
    for ii in structure_indices:
        if is_all(atom_indices):
            coordinates.append(item[0].get_coordinates(ii))
        else:
            coordinates.append(item[0].get_coordinates(ii)[atom_indices,:])
    coordinates = np.array(coordinates)
    coordinates = puw.quantity(coordinates, unit='angstroms')
    coordinates = puw.standardize(coordinates)

    return coordinates



## From system


@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        n_structures = item.max_frame + 1
    else:
        n_structures = len(structure_indices)

    return n_structures

@digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_string_pdb_text
    from ..string_pdb_text import get_box_from_system as aux_get

    tmp_item = to_string_pdb_text(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_string_pdb_text
    from ..string_pdb_text import get_time_from_system as aux_get

    tmp_item = to_string_pdb_text(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_string_pdb_text
    from ..string_pdb_text import get_structure_id_from_system as aux_get

    tmp_item = to_string_pdb_text(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output



#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

