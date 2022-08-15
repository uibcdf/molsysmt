from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import puw
import numpy as np

@digest()
def center(molecular_system, selection='all', center_of_selection='all', weights=None, center_coordinates=None, structure_indices='all',
           syntax='MolSysMT', engine='MolSysMT', in_place=False):

    from . import get_center
    from . import translate

    if engine=='MolSysMT':

        coordinates_selection_center = get_center(molecular_system, selection=center_of_selection, groups_of_atoms=None, weights=weights,
                                                  structure_indices=structure_indices,
                                                  syntax=syntax, engine=engine)

        if center_coordinates is None:
            translation = -coordinates_selection_center
        else:
            translation = center_coordinates-coordinates_selection_center

        del(coordinates_selection_center)

        return translate(molecular_system, translation=translation, selection=selection,
                         structure_indices=structure_indices, syntax='MolSysMT',
                         in_place=in_place)

    else:

        raise NotImplementedMethodError()

