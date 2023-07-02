from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib
import numpy as np
import gc

@digest()
def unwrap(molecular_system, selection='all', structure_indices='all',
        syntax='MolSysMT', engine='MolSysMT', in_place=False):
    """
    To be written soon...
    """

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract, copy

        coordinates= get(molecular_system, element='atom', selection=selection, coordinates=True)
        n_structures = coordinates.shape[0]
        n_atoms = coordinates.shape[1]
        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

        coordinates, length_units = puw.get_value_and_unit(coordinates)
        box = puw.get_value(box, to_unit=length_units)

        msmlib.pbc.unwrap(coordinates, box)

        coordinates=puw.quantity(coordinates, length_units)

    else:

        raise NotImplementedMethodError()

    if in_place:

        set(molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, box)

        gc.collect()

    else:

        tmp_molecular_system = copy(molecular_system)

        set(tmp_molecular_system, selection=selection, structure_indices=structure_indices,
            syntax='MolSysMT', coordinates=coordinates)

        del(coordinates, box)
        
        gc.collect()

        return tmp_molecular_system

