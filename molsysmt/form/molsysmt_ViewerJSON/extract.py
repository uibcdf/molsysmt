from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from copy import deepcopy
import numpy as np


@digest(form='molsysmt.ViewerJSON')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """Extract a subset of atoms/structures from a ViewerJSON."""

    if is_all(atom_indices) and is_all(structure_indices):
        return deepcopy(item) if copy_if_all else item

    new_item = deepcopy(item)
    if 'estructures' not in new_item.data and 'frames' in new_item.data:
        new_item.data['estructures'] = new_item.data.pop('frames')

    atoms = new_item.data.get('atoms', {})

    if not is_all(atom_indices):
        idx = np.array(atom_indices, dtype=int)
        for key, values in list(atoms.items()):
            try:
                atoms[key] = list(np.array(values)[idx])
            except Exception:
                pass
        new_item.data['atoms'] = atoms

        if 'estructures' in new_item.data:
            estructures = []
            for frame in new_item.data.get('estructures', []):
                new_frame = deepcopy(frame)
                if 'positions' in new_frame:
                    arr = np.array(new_frame['positions'])
                    arr = arr[idx] if arr.ndim > 1 else arr
                    new_frame['positions'] = arr.tolist()
                estructures.append(new_frame)
            new_item.data['estructures'] = estructures

    if not is_all(structure_indices) and 'estructures' in new_item.data:
        idx = set(structure_indices)
        new_item.data['estructures'] = [
            ff for ii, ff in enumerate(new_item.data.get('estructures', [])) if ii in idx
        ]

    return new_item
