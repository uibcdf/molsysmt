from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np
from smonitor import signal

@signal(tags=['api', 'structure'])
@arg_digest()
def center(molecular_system, selection='all', center_of_selection='all', weights=None, center_coordinates=None,
           structure_indices='all', syntax='MolSysMT', engine='MolSysMT', in_place=False, skip_digestion=False):
    """
    To be written soon...
    """

    from . import get_center
    from . import translate

    if engine=='MolSysMT':

        coordinates_selection_center = get_center(molecular_system, selection=center_of_selection, weights=weights,
                                                  structure_indices=structure_indices, syntax=syntax, engine=engine)

        if center_coordinates is None:
            translation = -coordinates_selection_center
        else:
            translation = center_coordinates-coordinates_selection_center

        del(coordinates_selection_center)

        output = translate(molecular_system, translation=translation, selection=selection,
                           structure_indices=structure_indices, syntax='MolSysMT',
                           in_place=in_place)

        target = molecular_system if in_place else output
        residual_center = get_center(target, selection=center_of_selection, weights=weights,
                                     structure_indices=structure_indices, syntax=syntax, engine=engine)
        residual = puw.get_value(residual_center, to_unit='nm')

        if center_coordinates is None:
            needs_correction = not np.allclose(residual, 0.0, atol=1e-12)
            correction = -residual_center
        else:
            target_center = puw.get_value(center_coordinates, to_unit='nm')
            needs_correction = not np.allclose(residual, target_center, atol=1e-12)
            correction = center_coordinates - residual_center

        if needs_correction:
            output = translate(target, translation=correction, selection=selection,
                               structure_indices=structure_indices, syntax='MolSysMT',
                               in_place=in_place)
            if in_place:
                output = molecular_system

        return output

    else:

        raise NotImplementedMethodError(caller='molsysmt.structure.center')
