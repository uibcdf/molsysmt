from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
from molsysmt import puw
import numpy as np


def center(molecular_system, selection='all', center_of_selection='all', weights=None, new_coordinates_center=None, frame_indices='all',
           syntaxis='MolSysMT', engine='MolSysMT', in_place=False):

    from molsysmt.structure.get_center import get_center
    from molsysmt.structure.translate import translate

    molecular_system = digest_molecular_system(molecular_system)
    frame_indices = digest_frame_indices(frame_indices)
    engine = digest_engine(engine)

    if engine=='MolSysMT':

        coordinates_selection_center = get_center(molecular_system, selection=center_of_selection, groups_of_atoms=None, weights=weights,
                                                  frame_indices=frame_indices, syntaxis=syntaxis, engine=engine)

        if new_coordinates_center is None:
            translation = -coordinates_selection_center
        else:
            translation = new_coordinates_center-coordinates_selection_center

        del(coordinates_selection_center)

        return translate(molecular_system, translation=translation, selection=selection,
                         frame_indices=frame_indices, syntaxis='MolSysMT', in_place=in_place)

    else:

        raise NotImplementedError()

