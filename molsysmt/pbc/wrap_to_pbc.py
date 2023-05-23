from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib
import numpy as np

@digest()
def wrap_to_pbc(molecular_system, selection='all', structure_indices='all',
                center_coordinates='[0,0,0] nanometers', center_of_selection=None, weights=None,
                center_at_origin=True, keep_covalent_bonds=False,
                syntax='MolSysMT', engine='MolSysMT', in_place=False):

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract, copy

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        coordinates= get(molecular_system, element='atom', indices=atom_indices, coordinates=True)
        n_structures = coordinates.shape[0]
        n_atoms = coordinates.shape[1]
        box, box_shape = get(molecular_system, element='system', structure_indices=structure_indices, box=True,
                             box_shape=True)

        orthogonal = 0
        if box_shape is None:
            raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
        elif box_shape == 'cubic':
            orthogonal =1

        if center_of_selection is not None:

            from molsysmt.structure import get_center
            center_coordinates = get_center(molecular_system, selection=center_of_selection,
                                weights=weights, structure_indices=structure_indices,
                                syntax=syntax, engine='MolSysMT')

        else:

            center_shape = np.shape(center_coordinates)
            if center_shape==(1,1,3):
                value = puw.get_value(center_coordinates)
                unit = puw.get_unit(center_coordinates)
                value = np.tile(value,[n_structures,1,1])
                center_coordinates = puw.quantity(value, unit)
            elif center_shape[0]!=n_structures:
                raise ValueError('center_coordinates needs the right shape')

        length_units = puw.get_unit(coordinates)

        box = np.asfortranarray(puw.get_value(box), dtype='float64')
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        center_coordinates = np.asfortranarray(puw.get_value(center_coordinates), dtype='float64')

        msmlib.pbc.wrap_to_pbc(coordinates, center_coordinates, box, orthogonal, n_atoms, n_structures)

        if recenter:
            translation = np.tile(-center_coordinates,(n_atoms,1))
            coordinates+=translation

        coordinates=puw.quantity(np.ascontiguousarray(coordinates), length_units)

    else:

        raise NotImplementedMethodError()

    if in_place:

        set(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        pass

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        return tmp_molecular_system

