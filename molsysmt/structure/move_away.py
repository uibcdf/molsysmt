from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw

@digest()
def move_away(molecular_system, selection=None, structure_indices=0, center='geometric center', center_selection=None,
              reference_molecular_system=None, reference_selection=None, reference_structure_indices=None,
              reference_center=None, reference_center_selection=None, direction=None, distance='3 angstroms',
              syntax='MolSysMT', engine='MolSysMT'):

    from molsysmt import select

    if reference_molecular_system is None:
        reference_molecular_system = molecular_system

    if reference_structure_index is None:
        reference_structure_index = structure_indices

    if reference_center is None:
        reference_center = center

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    reference_atom_indices = select(reference_molecular_system, selection=reference_selection, syntax=syntax)

    if direction is None:

        if center=='geometric center':
            from . import get_geometric_center as get_center
        elif center=='center_of_mass':
            from . import get_center_of_mass as get_center

        coordinates_center = get_center(molecular_system, selection=center_selection, syntax=syntax)
        coordinates_reference_center = get_center(reference_molecular_system, selection=reference_center_selection, syntax=syntax)

        direction = puw.get_value(coordinates_reference_center-coordinates_center)

        molecular_system, translation=None, selection='all', structure_indices='all',
        syntax='MolSysMT', in_place=False):

    from molsysmt.basic import get, set, select, copy

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    coordinates = get(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    if len(translation.shape)==1:
        n_atoms = coordinates.shape[1]
        value = puw.get_value(translation)
        unit = puw.get_unit(translation)
        value = np.tile(value, (n_atoms,1))
        translation = puw.quantity(value, unit)

    coordinates+=translation

    if in_place:
        return set(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                   coordinates=coordinates)
    else:
        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
            coordinates=coordinates)
        return tmp_molecular_system

