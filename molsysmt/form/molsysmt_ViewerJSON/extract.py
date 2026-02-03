from molsysmt._private.digestion import arg_digest
from molsysmt._private.variables import is_all
from copy import deepcopy
import numpy as np


@arg_digest(form='molsysmt.ViewerJSON')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """Extract a subset of atoms/structures from a ViewerJSON."""

    if is_all(atom_indices) and is_all(structure_indices):
        return deepcopy(item) if copy_if_all else item

    new_item = deepcopy(item)
    if 'structures' not in new_item.data:
        if 'estructures' in new_item.data:
            new_item.data['structures'] = new_item.data.pop('estructures')
        elif 'frames' in new_item.data:
            new_item.data['structures'] = new_item.data.pop('frames')

    atoms = new_item.data.get('atoms', {})

    if not is_all(atom_indices):
        idx = np.array(atom_indices, dtype=int)
        for key, values in list(atoms.items()):
            try:
                atoms[key] = list(np.array(values)[idx])
            except Exception:
                pass
        new_item.data['atoms'] = atoms

        if 'structures' in new_item.data:
            structures = []
            for frame in new_item.data.get('structures', []):
                new_frame = deepcopy(frame)
                coords = new_frame.get('coordinates', None)
                if coords is not None:
                    arr = np.array(coords)
                    arr = arr[idx] if arr.ndim > 1 else arr
                    new_frame['coordinates'] = arr.tolist()
                structures.append(new_frame)
            new_item.data['structures'] = structures

    if not is_all(structure_indices) and 'structures' in new_item.data:
        idx = set(structure_indices)
        new_item.data['structures'] = [
            ff for ii, ff in enumerate(new_item.data.get('structures', [])) if ii in idx
        ]

    return new_item
