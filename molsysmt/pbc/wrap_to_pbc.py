from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib
import numpy as np
import gc

@digest()
def wrap_to_pbc(molecular_system, selection='all', structure_indices='all',
                periodicity_from='[0,0,0] nanometers', center_of_selection=None, weights=None,
                center_coordinates='[0,0,0] nanometers', keep_covalent_bonds=False,
                syntax='MolSysMT', engine='MolSysMT', in_place=False):
    """
    To be written soon...
    """

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract, copy
        from molsysmt.structure import get_center

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        coordinates= get(molecular_system, element='atom', selection=atom_indices, coordinates=True)
        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

        if center_of_selection is not None:

            center_coordinates = get_center(molecular_system, selection=center_of_selection,
                                weights=weights, structure_indices=structure_indices,
                                syntax=syntax, engine='MolSysMT')

            coordinates, length_units = puw.get_value_and_unit(coordinates)
            box = puw.get_value(box, to_unit=length_units)
            center_coordinates = puw.get_value(center_coordinates, to_unit=length_units)

            msmlib.pbc.wrap_to_pbc_center(coordinates, box, center_coordinates)

            coordinates=puw.quantity(coordinates, length_units)

            del(box, center_coordinates)

        else:

            coordinates, length_units = puw.get_value_and_unit(coordinates)
            box = puw.get_value(box, to_unit=length_units)

            msmlib.pbc.wrap_to_pbc_no_center(coordinates, box)

            coordinates=puw.quantity(coordinates, length_units)

            del(box)

    else:

        raise NotImplementedMethodError()

    if in_place:

        set(molecular_system, selection='atom_index in @atom_indices', structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        pass

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, selection='atom_index in @atom_indices', structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        return tmp_molecular_system

