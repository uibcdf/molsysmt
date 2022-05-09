from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt import puw
import numpy as np


def center(molecular_system, selection='all', center_of_selection='all', weights=None, new_coordinates_center=None, structure_indices='all',
           syntaxis='MolSysMT', engine='MolSysMT', in_place=False, check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection, syntaxis)
        center_of_selection = digest_selection(center_of_selection, syntaxis)
        structure_indices = digest_structure_indices(structure_indices)
        engine = digest_engine(engine)

    from . import get_center
    from . import translate

    if engine=='MolSysMT':

        coordinates_selection_center = get_center(molecular_system, selection=center_of_selection, groups_of_atoms=None, weights=weights,
                                                  structure_indices=structure_indices,
                                                  syntaxis=syntaxis, engine=engine, check=False)

        if new_coordinates_center is None:
            translation = -coordinates_selection_center
        else:
            translation = new_coordinates_center-coordinates_selection_center

        del(coordinates_selection_center)

        return translate(molecular_system, translation=translation, selection=selection,
                         structure_indices=structure_indices, syntaxis='MolSysMT',
                         in_place=in_place, check=False)

    else:

        raise NotImplementedError()

