import numpy as np
from molsysmt import puw

def translate(molecular_system, translation=None, selection='all', frame_indices='all', syntaxis='MolSysMT', in_place=True):

    from molsysmt.multitool import get, set, select, copy

    coordinates, n_frames = get(molecular_system, target='atom', coordinates=True, n_frames=True)

    atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)
    n_atoms = atom_indices.shape[0]

    translation = puw.standardize(translation)
    unit = puw.get_unit(translation)
    translation_value = puw.get_value(translation)

    if type(translation_value) in [list, tuple]:
        translation_value = np.array(translation_value)

    if type(translation_value)==np.ndarray:
        if len(translation_value.shape)==1:
            if translation_value.shape[0]==3:
                translation_value = np.tile(translation_value,(n_atoms,1))
            else:
                raise ValueError('Wrong shape of translation vector')
        elif len(translation_value.shape)==2:
            if translation_value.shape[1]!=3:
                raise ValueError('Wrong shape of translation vector')

    translation = puw.quantity(translation_value, unit)

    if frame_indices is 'all':
        for ii in range(n_frames):
            coordinates[ii,atom_indices,:]+=translation
    else:
        for ii in frame_indices:
            coordinates[ii,atom_indices,:]+=translation

    if in_place:
        return set(molecular_system, coordinates=coordinates)
    else:
        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, coordinates=coordinates)
        return tmp_molecular_system

