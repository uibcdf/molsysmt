from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw

@digest()
def move_away(molecular_system, selection='all', center_of_selection='all', weights=None, structure_indices=0,
              reference_molecular_system=None, reference_center_of_selection='all', reference_weights=None,
              reference_structure_indices=None, direction=None, distance='3 angstroms',
              in_place=False, syntax='MolSysMT', skip_digestion=False):
    """
    To be written soon..
    """

    from molsysmt.basic import get, set, select, copy
    from molsysmt.structure import get_center, center

    if reference_molecular_system is None:
        reference_molecular_system = molecular_system

    if reference_structure_indices is None:
        reference_structure_indices = structure_indices

    coordinates_reference_center = get_center(reference_molecular_system, selection=reference_center_of_selection,
                                              structure_indices=reference_structure_indices,
                                              weights=reference_weights, syntax=syntax, skip_digestion=True)

    if direction is None:

        coordinates_center = get_center(molecular_system, selection=center_of_selection, weights=weights,
                                        structure_indices=structure_indices, syntax=syntax, skip_digestion=True)

        direction = puw.get_value(coordinates_center-coordinates_reference_center)

        if direction.shape[0]!=1 or direction.shape[1]!=1:

            raise NotImplementedError

        direction = direction[:,0,:]
        for ii in range(direction.shape[0]):
            direction[ii] = direction[ii]/np.linalg.norm(direction[ii])

        atom_indices = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
        coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                          coordinates=True, skip_digestion=True)

        value, unit = puw.get_value_and_unit(distance)
        value = value * direction
        n_atoms = coordinates.shape[1]
        value = np.tile(value, (n_atoms,1))
        translation = puw.quantity(value, unit)
        coordinates+=translation

        if in_place:
            return set(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                       coordinates=coordinates, skip_digestion=True)
        else:
            tmp_molecular_system = copy(molecular_system)
            set(tmp_molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                coordinates=coordinates, skip_digestion=True)
            return tmp_molecular_system

    else:

        if in_place:

            center(molecular_system, selection=selection, center_of_selection=center_of_selection, weights=weights,
                  center_coordinates=coordinates_reference_center, in_place=True, skip_digestion=True)

            atom_indices = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
            coordinates = get(molecular_system, element='atom', selection=atom_indices,
                              structure_indices=structure_indices, coordinates=True, skip_digestion=True)

            if direction.shape[0]!=1 or coordinates.shape[0]!=1:
                raise NotImplementedError

            value, unit = puw.get_value_and_unit(distance)
            value = value * direction
            n_atoms = coordinates.shape[1]
            value = np.tile(value, (n_atoms,1))
            translation = puw.quantity(value, unit)
            coordinates+=translation

            return set(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                       coordinates=coordinates, skip_digestion=True)

        else:

            tmp_molecular_system = center(molecular_system, selection=selection,
                                          center_of_selection=center_of_selection, weights=weights,
                                          center_coordinates=coordinates_reference_center,
                                          in_place=False, skip_digestion=True)

            atom_indices = select(tmp_molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
            coordinates = get(tmp_molecular_system, element='atom', selection=atom_indices,
                              structure_indices=structure_indices, coordinates=True, skip_digestion=True)

            if direction.shape[0]!=1 or coordinates.shape[0]!=1:
                raise NotImplementedError

            value, unit = puw.get_value_and_unit(distance)
            value = value * direction
            n_atoms = coordinates.shape[1]
            value = np.tile(value, (n_atoms,1))
            translation = puw.quantity(value, unit)
            coordinates+=translation

            set(tmp_molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                coordinates=coordinates, skip_digestion=True)

            return tmp_molecular_system

