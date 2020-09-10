from .multitool import get as _get
from .multitool import set as _set
from .multitool import select, copy
import numpy as np

def translate(item, translation=None, selection='all', frame_indices='all', syntaxis='MolSysMT',
              in_place=True):

    coordinates, n_frames = _get(item, target='atom', coordinates=True, n_frames=True)

    atom_indices = select(item, selection=selection, syntaxis=syntaxis)
    n_atoms = atom_indices.shape[0]

    if type(translation._value) in [list, tuple]:
        translation._value = np.array(translation._value)

    if type(translation._value)==np.ndarray:
        if len(translation._value.shape)==1:
            if translation._value.shape[0]==3:
                translation._value = np.tile(translation._value,(n_atoms,1))
            else:
                raise ValueError('Wrong shape of translation vector')
        elif len(translation._value.shape)==2:
            if translation._value.shape[1]!=3:
                raise ValueError('Wrong shape of translation vector')

    if frame_indices is 'all':
        for ii in range(n_frames):
            coordinates[ii,atom_indices,:]+=translation
    else:
        for ii in frame_indices:
            coordinates[ii,atom_indices,:]+=translation

    if in_place:
        return _set(item, coordinates=coordinates)
    else:
        tmp_item = copy(item)
        _set(tmp_item, coordinates=coordinates)
        return tmp_item

