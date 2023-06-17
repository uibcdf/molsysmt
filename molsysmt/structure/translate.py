from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw
import gc

@digest()
def translate(molecular_system, translation=None, selection='all', structure_indices='all',
        syntax='MolSysMT', in_place=False):

    from molsysmt.basic import get, set, select, copy

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

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
        set(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
            coordinates=coordinates)
        del(coordinates, atom_indices, translation)
        gc.collect()
    else:
        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
            coordinates=coordinates)
        del(coordinates, atom_indices, translation)
        gc.collect()
        return tmp_molecular_system

