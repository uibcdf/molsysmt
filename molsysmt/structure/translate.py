from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw
import gc

@digest()
def translate(molecular_system, translation=None, selection='all', structure_indices='all',
        syntax='MolSysMT', in_place=False):

    from molsysmt.basic import get, set, select, copy

    coordinates = get(molecular_system, element='atom', selection=selection, structure_indices=structure_indices,
                      syntax=syntax, coordinates=True)

    coordinates, length_unit = puw.get_value_and_unit(coordinates)
    translation = puw.get_value(translation, to_unit=length_unit)

    if translation.shape==(1,1,3):
        coordinates += translation[0,0,:]
    elif translation.shape==(coordinates.shape[0],1,3):
        for ii in range(coordinates.shape[0]):
            coordinates[ii,:,:] += translation[ii,0,:]
    elif np.all(translation.shape[:]==coordinates.shape[:]):
        coordinates += translation
    else:
        raise ValueError

    coordinates = puw.quantity(coordinates, length_unit)

    if in_place:
        set(molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)
        del(coordinates, translation)
        gc.collect()
    else:
        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)
        del(coordinates, translation)
        gc.collect()
        return tmp_molecular_system

