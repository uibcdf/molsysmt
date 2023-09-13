from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib
import gc

@digest()
def flip(molecular_system, vector=[0,0,1], point=[0,0,0], selection='all', structure_indices='all',
        syntax='MolSysMT', in_place=False):
    """
    To be written soon...
    """

    from molsysmt.basic import get, set, select, copy
    from molsysmt.structure import translate

    coordinates = get(molecular_system, element='atom', selection=selection, structure_indices=structure_indices,
                      syntax=syntax, coordinates=True)

    coordinates, length_unit =  puw.get_value_and_unit(coordinates)
    point = puw.get_value(point, to_unit=length_unit)

    coordinates = msmlib.structure.flip(coordinates, vector, point)

    coordinates = puw.quantity(coordinates, unit=length_unit)

    if in_place:

        set(molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)
        del(coordinates)
        gc.collect()

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)
        del(coordinates)
        gc.collect()

        return tmp_molecular_system

