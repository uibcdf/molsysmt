from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib
import numpy as np
import gc

@digest()
def wrap_to_mic(molecular_system, selection='all', structure_indices='all',
                center_coordinates='[0,0,0] nanometers', center_of_selection=None, weights=None,
                center_at_origin=True, keep_covalent_bonds=False,
                syntax='MolSysMT', engine='MolSysMT', in_place=False):

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract, copy
        from molsysmt.structure import get_center

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        coordinates= get(molecular_system, element='atom', indices=atom_indices, coordinates=True)
        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

        if center_of_selection is not None:

            center_coordinates = get_center(molecular_system, selection=center_of_selection,
                                weights=weights, structure_indices=structure_indices,
                                syntax=syntax, engine='MolSysMT')

        coordinates, length_units = puw.get_value_and_unit(coordinates)
        box = puw.get_value(box, to_unit=length_units)
        center_coordinates = puw.get_value(center_coordinates, to_unit=length_units)

        msmlib.pbc.wrap_to_mic(coordinates, box, center_coordinates, center_at_origin)

        coordinates=puw.quantity(coordinates, length_units)

        del(box, center_coordinates)

    else:

        raise NotImplementedMethodError()

    if in_place:

        set(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        pass

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        return tmp_molecular_system

