from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw

@digest()
def translate(molecular_system, translation=None, selection='all', structure_indices='all',
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

