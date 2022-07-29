from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import puw

@digest()
def translate(molecular_system, translation=None, selection='all', structure_indices='all',
        syntax='MolSysMT', in_place=False):

    from molsysmt.basic import get, set, select, copy

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    coordinates = get(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    length_units = puw.get_unit(coordinates)
    coordinates = puw.get_value(coordinates)
    translation = puw.get_value(translation, to_unit=length_units)
    n_atoms = coordinates.shape[1]

    if type(translation) in [list, tuple]:
        translation = np.array(translation)

    if type(translation)==np.ndarray:
        if len(translation.shape)==1:
            if translation.shape[0]==3:
                translation = np.tile(translation,(n_atoms,1))
            else:
                raise ValueError('Wrong shape of translation vector')
        elif len(translation.shape)==2:
            if translation.shape[1]!=3:
                raise ValueError('Wrong shape of translation vector')
        elif len(translation.shape)==3:
            if translation.shape[2]!=3:
                raise ValueError('Wrong shape of translation vector')
            if translation.shape[1]==1:
                translation = np.tile(translation,(n_atoms,1))

    coordinates+=translation
    coordinates=coordinates*length_units

    if in_place:
        return set(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                   coordinates=coordinates)
    else:
        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
            coordinates=coordinates)
        return tmp_molecular_system

